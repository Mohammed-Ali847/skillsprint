# src/services/progress_service.py
import datetime, json
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from src.database import models

class ProgressService:
    """Tracks employee learning progress, task submissions, quiz grading, and overall status."""

    @classmethod
    def get_employee_progress(cls, db: Session, employee_id: int) -> Dict[str, Any]:
        employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
        if not employee:
            raise ValueError(f"Employee {employee_id} not found.")

        # Get latest active or approved plan
        plan = db.query(models.OnboardingPlan).filter(
            models.OnboardingPlan.employee_id == employee_id
        ).order_by(models.OnboardingPlan.created_at.desc()).first()

        if not plan:
            return {
                "employee_id": employee.id,
                "full_name": employee.full_name,
                "has_plan": False,
                "status": "No Plan Assigned",
                "progress_percentage": 0.0
            }

        total_modules = len(plan.learning_modules)
        completed_modules = len([m for m in plan.learning_modules if m.status == "COMPLETED"])

        total_tasks = len(plan.tasks)
        completed_tasks = len([t for t in plan.tasks if t.status in ["COMPLETED", "APPROVED"]])

        total_checklists = len(plan.checklists)
        completed_checklists = len([c for c in plan.checklists if c.status == "COMPLETED"])

        # Quizzes
        quiz_attempts = db.query(models.QuizAttempt).filter(models.QuizAttempt.employee_id == employee_id).all()
        avg_quiz_score = round(sum(qa.score for qa in quiz_attempts) / len(quiz_attempts), 1) if quiz_attempts else 0.0

        # Overall progress formula
        total_items = max(total_modules + total_tasks + total_checklists, 1)
        completed_items = completed_modules + completed_tasks + completed_checklists
        overall_progress = round((completed_items / total_items) * 100.0, 1)

        # Evaluate status (liv)
        eval_status = "On Track"
        if overall_progress >= 100.0:
            eval_status = "Completed"
        elif quiz_attempts and avg_quiz_score < 70.0:
            eval_status = "Requires Attention"
        elif completed_modules == total_modules and total_modules > 0:
            eval_status = "Assessment Required"
        elif overall_progress < 25.0:
            eval_status = "Behind Schedule"

        employee.training_status = eval_status
        db.commit()

        return {
            "employee_id": employee.id,
            "full_name": employee.full_name,
            "role": employee.role.name if employee.role else "N/A",
            "department": employee.department.name if employee.department else "N/A",
            "plan_id": plan.id,
            "plan_title": plan.title,
            "plan_status": plan.status,
            "training_status": eval_status,
            "overall_progress_percentage": overall_progress,
            "modules": {
                "total": total_modules,
                "completed": completed_modules,
                "percentage": round((completed_modules / max(total_modules, 1)) * 100.0, 1)
            },
            "tasks": {
                "total": total_tasks,
                "completed": completed_tasks,
                "percentage": round((completed_tasks / max(total_tasks, 1)) * 100.0, 1)
            },
            "checklists": {
                "total": total_checklists,
                "completed": completed_checklists,
                "percentage": round((completed_checklists / max(total_checklists, 1)) * 100.0, 1)
            },
            "quiz_stats": {
                "attempts_count": len(quiz_attempts),
                "average_score": avg_quiz_score
            }
        }

    @classmethod
    def complete_module(cls, db: Session, module_id: int) -> models.LearningModule:
        mod = db.query(models.LearningModule).filter(models.LearningModule.id == module_id).first()
        if mod:
            mod.status = "COMPLETED"
            db.commit()
            db.refresh(mod)
        return mod

    @classmethod
    def toggle_checklist(cls, db: Session, checklist_id: int, completed: bool) -> models.Checklist:
        chk = db.query(models.Checklist).filter(models.Checklist.id == checklist_id).first()
        if chk:
            chk.status = "COMPLETED" if completed else "PENDING"
            chk.completed_at = datetime.datetime.utcnow() if completed else None
            db.commit()
            db.refresh(chk)
        return chk

    @classmethod
    def submit_task_evidence(cls, db: Session, task_id: int, evidence_text: str) -> models.Task:
        task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if task:
            task.submitted_evidence = evidence_text
            task.status = "APPROVED"
            task.completed_at = datetime.datetime.utcnow()
            db.commit()
            db.refresh(task)
        return task

    @classmethod
    def submit_quiz_attempt(cls, db: Session, employee_id: int, quiz_id: int, user_answers: Dict[str, Any]) -> Dict[str, Any]:
        """Grades quiz attempt, validates answers against source text, records score."""
        quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
        if not quiz:
            raise ValueError(f"Quiz {quiz_id} not found.")

        questions = quiz.questions
        total_q = len(questions)
        if total_q == 0:
            return {"score": 100.0, "passed": True, "results": []}

        correct_count = 0
        detailed_results = []

        for q in questions:
            user_ans = str(user_answers.get(str(q.id), "")).strip().lower()
            try:
                real_ans = json.loads(q.correct_answer_json)
            except Exception:
                real_ans = q.correct_answer_json

            is_correct = False
            if isinstance(real_ans, list):
                is_correct = any(user_ans == str(a).strip().lower() for a in real_ans)
            else:
                is_correct = (user_ans == str(real_ans).strip().lower())

            if is_correct:
                correct_count += 1

            detailed_results.append({
                "question_id": q.id,
                "question_text": q.question_text,
                "submitted_answer": user_answers.get(str(q.id)),
                "correct_answer": real_ans,
                "is_correct": is_correct,
                "explanation": q.explanation,
                "source": f"{q.source_doc_id} §{q.source_section_id}"
            })

        score = round((correct_count / total_q) * 100.0, 1)
        passed = (score >= quiz.passing_score)

        attempt = models.QuizAttempt(
            employee_id=employee_id,
            quiz_id=quiz.id,
            score=score,
            passed=passed,
            answers_json=json.dumps(user_answers),
            completed_at=datetime.datetime.utcnow()
        )
        db.add(attempt)
        db.commit()

        # If score is low (< 75%), trigger Adaptive Recommendation engine automatically
        if not passed or score < 75.0:
            from src.services.adaptive_service import AdaptiveService
            AdaptiveService.generate_remediation(
                db=db,
                employee_id=employee_id,
                module=quiz.module,
                score=score
            )

        return {
            "attempt_id": attempt.id,
            "score": score,
            "passing_score": quiz.passing_score,
            "passed": passed,
            "total_questions": total_q,
            "correct_count": correct_count,
            "results": detailed_results
        }

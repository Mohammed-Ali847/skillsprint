# src/services/onboarding_service.py
import json, datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from src.database import models
from src.genai_pipeline.client import genai_client
from src.python_validation.engine import PythonValidationEngine

class OnboardingService:
    """Orchestrates end-to-end curriculum generation, persistence, and independent validation."""

    @classmethod
    def generate_plan_for_employee(cls, db: Session, employee_id: int) -> Dict[str, Any]:
        employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
        if not employee:
            raise ValueError(f"Employee {employee_id} not found.")

        role = employee.role
        department = employee.department

        # 1. Fetch mandatory requirements for this role from the Role Requirement Matrix
        role_reqs = db.query(models.RoleRequirement).filter(
            models.RoleRequirement.role_id == role.id,
            models.RoleRequirement.is_mandatory == True
        ).all()

        mandatory_items = []
        for rr in role_reqs:
            req = rr.requirement
            if req and req.document:
                mandatory_items.append({
                    "code": req.req_code,
                    "text": req.requirement_text,
                    "doc": req.document.doc_code,
                    "sec": req.section_id,
                    "competency": req.competency,
                    "stage": rr.due_stage,
                    "priority": rr.priority
                })

        # 2. Gather authoritative source chunks
        active_chunks = db.query(models.DocumentChunk).join(models.DocumentVersion).filter(
            models.DocumentVersion.is_active == True
        ).limit(35).all()

        evidence_list = []
        for c in active_chunks:
            doc = c.version.document
            if doc:
                evidence_list.append({
                    "doc_code": doc.doc_code,
                    "section_id": c.section_id,
                    "heading": c.section_heading,
                    "content": c.content
                })

        # 3. Invoke GenAI Generation Pipeline (Pipeline 1)
        plan_dict = genai_client.synthesize_onboarding_plan(
            employee_code=employee.employee_code,
            role_code=role.code,
            role_name=role.name,
            department=department.name if department else "Corporate",
            experience_level=employee.experience_level,
            mandatory_reqs=mandatory_items,
            evidence_chunks=evidence_list
        )

        # 4. Create Parent OnboardingPlan record
        plan_record = models.OnboardingPlan(
            employee_id=employee.id,
            role_id=role.id,
            title=plan_dict.get("plan_title", f"Onboarding Journey: {role.name}"),
            status="DRAFT",
            version=1,
            prompt_version=plan_dict.get("prompt_version", "v1.0"),
            model_used=genai_client.model_name
        )
        db.add(plan_record)
        db.flush()

        # Build requirement lookup dict
        req_lookup = {r.req_code: r for r in db.query(models.Requirement).all()}

        # 5. Persist Modules, Tasks, Scenarios, Quizzes
        for m_data in plan_dict.get("modules", []):
            r_code = m_data.get("requirement_code")
            req_obj = req_lookup.get(r_code)

            module_record = models.LearningModule(
                plan_id=plan_record.id,
                requirement_id=req_obj.id if req_obj else None,
                module_code=m_data.get("module_code", "MOD-01"),
                title=m_data.get("title", "Untitled Module"),
                category=m_data.get("category", "KNOWLEDGE"),
                purpose=m_data.get("purpose", ""),
                learning_objectives=json.dumps(m_data.get("learning_objectives", [])),
                key_concepts=json.dumps(m_data.get("key_concepts", [])),
                estimated_duration_mins=m_data.get("estimated_duration_mins", 45),
                stage=m_data.get("stage", "Week 1"),
                difficulty=m_data.get("difficulty", "Beginner"),
                source_doc_id=m_data.get("source_doc_id", ""),
                source_section_id=m_data.get("source_section_id", ""),
                verification_status="VERIFIED",
                status="ASSIGNED"
            )
            db.add(module_record)
            db.flush()

            # Tasks
            for t in m_data.get("tasks", []):
                t_record = models.Task(
                    plan_id=plan_record.id,
                    requirement_id=req_obj.id if req_obj else None,
                    description=t.get("description", ""),
                    expected_outcome=t.get("expected_outcome", ""),
                    completion_criteria=t.get("completion_criteria", ""),
                    difficulty=t.get("difficulty", "Beginner"),
                    due_stage=t.get("due_stage", "Week 1"),
                    source_doc_id=t.get("source_doc_id", ""),
                    source_section_id=t.get("source_section_id", ""),
                    status="PENDING"
                )
                db.add(t_record)

            # Scenarios
            for s in m_data.get("scenarios", []):
                s_record = models.Scenario(
                    plan_id=plan_record.id,
                    module_id=module_record.id,
                    situation=s.get("situation", ""),
                    employee_role=s.get("employee_role", role.name),
                    decision_prompt=s.get("decision_prompt", ""),
                    expected_behavior=s.get("expected_behavior", ""),
                    evaluation_rubric=s.get("evaluation_rubric", ""),
                    source_doc_id=s.get("source_doc_id", ""),
                    source_section_id=s.get("source_section_id", "")
                )
                db.add(s_record)

            # Quizzes
            q_questions = m_data.get("quiz_questions", [])
            if q_questions:
                quiz_record = models.Quiz(
                    module_id=module_record.id,
                    title=f"Knowledge Check: {module_record.title}",
                    passing_score=75.0
                )
                db.add(quiz_record)
                db.flush()

                for q in q_questions:
                    q_record = models.QuizQuestion(
                        quiz_id=quiz_record.id,
                        requirement_id=req_obj.id if req_obj else None,
                        question_text=q.get("question_text", ""),
                        question_type=q.get("question_type", "MCQ"),
                        options_json=json.dumps(q.get("options", [])),
                        correct_answer_json=json.dumps(q.get("correct_answer", "")),
                        explanation=q.get("explanation", ""),
                        difficulty=q.get("difficulty", "Beginner"),
                        source_doc_id=q.get("source_doc_id", ""),
                        source_section_id=q.get("source_section_id", "")
                    )
                    db.add(q_record)

        # 6. Checklists
        for c_data in plan_dict.get("checklists", []):
            c_record = models.Checklist(
                plan_id=plan_record.id,
                activity=c_data.get("activity", ""),
                is_mandatory=c_data.get("is_mandatory", True),
                due_stage=c_data.get("due_stage", "Day 1"),
                responsible_person=c_data.get("responsible_person", "Employee"),
                source_doc_id=c_data.get("source_doc_id", ""),
                source_section_id=c_data.get("source_section_id", ""),
                status="PENDING"
            )
            db.add(c_record)

        # 7. Assessments
        for a_data in plan_dict.get("assessments", []):
            a_record = models.Assessment(
                plan_id=plan_record.id,
                title=a_data.get("title", f"{role.name} Competency Assessment"),
                assessment_type=a_data.get("assessment_type", "PRACTICAL"),
                rubric_json=json.dumps(a_data.get("rubric", [])),
                status="ASSIGNED"
            )
            db.add(a_record)

        db.commit()

        # 8. Trigger Pipeline 2: Independent Python Ground-Truth Validator
        val_result = PythonValidationEngine.validate_plan(
            db=db,
            plan_id=plan_record.id,
            plan_dict=plan_dict,
            role_id=role.id
        )

        return {
            "plan_id": plan_record.id,
            "employee_id": employee.id,
            "employee_name": employee.full_name,
            "role_name": role.name,
            "title": plan_record.title,
            "status": val_result["overall_status"],
            "coverage_score": val_result["coverage_score"],
            "traceability_score": val_result["traceability_score"],
            "consistency_score": val_result["consistency_score"],
            "modules_count": len(plan_dict.get("modules", [])),
            "checklists_count": len(plan_dict.get("checklists", [])),
            "assessments_count": len(plan_dict.get("assessments", [])),
            "validation": val_result
        }

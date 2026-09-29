import pytest
from src.database import models
from src.services.onboarding_service import OnboardingService
from src.python_validation.engine import PythonValidationEngine
from src.services.progress_service import ProgressService
from src.services.adaptive_service import AdaptiveService
from src.services.impact_service import ImpactService
from src.reports.report_generator import ReportGenerator

def test_full_onboarding_lifecycle_e2e(db_session):
    # 1. Select an employee (e.g. Employee 2: Marcus Vance - Customer Support)
    emp = db_session.query(models.Employee).filter(models.Employee.id == 2).first()
    if not emp:
        emp = db_session.query(models.Employee).first()
    assert emp is not None

    # 2. Pipeline 1: Generate Onboarding Plan
    plan_result = OnboardingService.generate_plan_for_employee(db_session, emp.id)
    assert plan_result["employee_id"] == emp.id
    plan_id = plan_result["plan_id"]
    assert plan_id is not None
    assert plan_result["modules_count"] > 0
    assert plan_result["checklists_count"] > 0
    assert plan_result["assessments_count"] > 0

    # 3. Pipeline 2: Independent Python Ground-Truth Validation
    val_record = db_session.query(models.ValidationResult).filter(
        models.ValidationResult.plan_id == plan_id
    ).first()
    assert val_record is not None
    assert val_record.coverage_score > 0
    assert val_record.traceability_score > 0
    assert val_record.overall_status in [
        "VERIFIED", "VERIFIED_WITH_WARNING", "UNSUPPORTED", "CONTRADICTION_DETECTED", "INCOMPLETE", "MANUAL_REVIEW_REQUIRED"
    ]

    # Verify Comparison Matrix (LLM != Ground Truth contract)
    assert val_record.comparison_json is not None

    # 4. Learner Interaction & Progress Tracking
    # Toggle first checklist item
    plan = db_session.query(models.OnboardingPlan).filter(models.OnboardingPlan.id == plan_id).first()
    assert len(plan.checklists) > 0
    chk = plan.checklists[0]
    res_chk = ProgressService.toggle_checklist(db_session, chk.id, completed=True)
    assert res_chk.status == "COMPLETED"

    # Submit task evidence
    assert len(plan.tasks) > 0
    task = plan.tasks[0]
    res_task = ProgressService.submit_task_evidence(
        db_session,
        task_id=task.id,
        evidence_text="https://github.com/apexnova/ticket-verification-demo-submission"
    )
    assert res_task.status == "APPROVED"

    # Submit Quiz Attempt
    quiz = db_session.query(models.Quiz).join(models.LearningModule).filter(models.LearningModule.plan_id == plan_id).first()
    if quiz and quiz.questions:
        q1 = quiz.questions[0]
        # Purposefully submit incorrect answer to test adaptive remediation
        answers = {str(q1.id): "INCORRECT_DISTRACTOR_OPTION"}
        score_res = ProgressService.submit_quiz_attempt(db_session, emp.id, quiz.id, answers)
        assert "score" in score_res
        assert score_res["score"] < 75.0

        # Verify adaptive remediation was generated for failing score
        recs = AdaptiveService.get_employee_recommendations(db_session, emp.id)
        assert len(recs) > 0
        assert recs[0]["weak_topic"] or recs[0]["reason"]

    # 5. Cascading Policy Update & Selective Regeneration
    impact = ImpactService.analyze_policy_update(
        db=db_session,
        doc_code="DOC-POL-01",
        old_version_str="1.0",
        new_version_str="2.0"
    )
    assert impact["affected_requirements_count"] > 0
    assert impact["impact_id"] > 0

    # 6. Executive Compliance Reporting
    report = ReportGenerator.generate_compliance_report(db_session)
    assert report["summary"]["total_employees"] >= 10
    assert report["summary"]["total_onboarding_plans"] >= 1
    assert len(report["role_breakdown"]) >= 10

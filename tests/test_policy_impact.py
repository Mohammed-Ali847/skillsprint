import pytest
from src.database import models
from src.services.impact_service import ImpactService

def test_analyze_policy_update(db_session):
    # Verify DOC-POL-01 exists and has versions
    doc = db_session.query(models.Document).filter(models.Document.doc_code == "DOC-POL-01").first()
    assert doc is not None

    versions = [v.version_str for v in doc.versions]
    assert "1.0" in versions
    assert "2.0" in versions

    result = ImpactService.analyze_policy_update(
        db=db_session,
        doc_code="DOC-POL-01",
        old_version_str="1.0",
        new_version_str="2.0"
    )

    assert result["document_code"] == "DOC-POL-01"
    assert result["old_version"] == "1.0"
    assert result["new_version"] == "2.0"
    assert result["affected_requirements_count"] > 0
    assert result["affected_roles_count"] > 0
    assert "impact_id" in result
    assert isinstance(result["diff_sample"], list)

    # Check that a PolicyImpactRecord was committed
    record = db_session.query(models.PolicyImpactRecord).filter(
        models.PolicyImpactRecord.id == result["impact_id"]
    ).first()
    assert record is not None

def test_selective_module_regeneration(db_session):
    # Get any module in the system
    module = db_session.query(models.LearningModule).first()
    if not module:
        # If no plan generated yet, create a dummy module
        plan = db_session.query(models.OnboardingPlan).first()
        if not plan:
            emp = db_session.query(models.Employee).first()
            plan = models.OnboardingPlan(employee_id=emp.id, role_id=emp.role_id, status="DRAFT")
            db_session.add(plan)
            db_session.commit()

        module = models.LearningModule(
            plan_id=plan.id,
            module_code="MOD-TEST-OUTDATED",
            title="Legacy Security Module",
            stage="Week 1",
            source_doc_id="DOC-POL-01",
            source_section_id="1.1",
            verification_status="OUTDATED_SOURCE"
        )
        db_session.add(module)
        db_session.commit()
        db_session.refresh(module)
    else:
        module.verification_status = "OUTDATED_SOURCE"
        db_session.commit()

    result = ImpactService.selective_regenerate_module(db_session, module.id)
    assert result["module_id"] == module.id
    assert result["status"] == "VERIFIED"

    # Verify directly from DB
    refreshed = db_session.query(models.LearningModule).filter(models.LearningModule.id == module.id).first()
    assert refreshed.verification_status == "VERIFIED"

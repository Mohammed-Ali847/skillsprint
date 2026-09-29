# src/api/routes.py
import os, json, datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from src.database.session import get_db
from src.database import models
from src.security.auth import hash_password, verify_password, create_access_token
from src.document_validation.validator import DocumentValidator
from src.document_processing.parser import DocumentParser
from src.document_processing.chunker import DocumentChunker
from src.services.extraction_service import RequirementExtractionService
from src.role_matrix.matrix_generator import RoleMatrixService
from src.services.onboarding_service import OnboardingService
from src.python_validation.engine import PythonValidationEngine
from src.services.review_service import ReviewService
from src.services.progress_service import ProgressService
from src.services.adaptive_service import AdaptiveService
from src.services.impact_service import ImpactService
from src.reports.report_generator import ReportGenerator
from src.reports.exporter import ReportExporter
from src.config.settings import settings

router = APIRouter()

@router.get("/health")
def api_health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "dual_pipeline": {
            "genai_generation_pipeline": "active",
            "python_ground_truth_validator": "active"
        }
    }

# --- 1. Authentication ---
@router.post("/auth/login")
def login(payload: Dict[str, str], db: Session = Depends(get_db)):
    username = payload.get("username", "").strip()
    password = payload.get("password", "").strip()
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    
    token = create_access_token({"sub": user.username, "role": user.role, "user_id": user.id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "email": user.email
        }
    }

@router.get("/auth/me")
def get_me(username: str = "admin", db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return {"id": user.id, "username": user.username, "role": user.role, "email": user.email}

# --- 2. Departments & Roles ---
@router.get("/departments")
def list_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()

@router.get("/roles")
def list_roles(db: Session = Depends(get_db)):
    roles = db.query(models.Role).all()
    results = []
    for r in roles:
        req_count = len(r.role_requirements)
        results.append({
            "id": r.id,
            "code": r.code,
            "name": r.name,
            "department": r.department.name if r.department else "General",
            "experience_level": r.experience_level,
            "description": r.description,
            "requirements_count": req_count
        })
    return results

@router.post("/roles")
def create_role(payload: Dict[str, Any], db: Session = Depends(get_db)):
    """Dynamic role creation supporting the Hidden Role Challenge."""
    code = payload.get("code", "").upper().strip()
    name = payload.get("name", "").strip()
    dept_id = payload.get("department_id")
    level = payload.get("experience_level", "Mid")
    desc = payload.get("description", "")

    existing = db.query(models.Role).filter(models.Role.code == code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Role with code {code} already exists.")

    new_role = models.Role(
        code=code,
        name=name,
        department_id=dept_id,
        experience_level=level,
        description=desc
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return {"message": "Role created successfully", "role": {"id": new_role.id, "code": new_role.code, "name": new_role.name}}

# --- 3. Employees ---
@router.get("/employees")
def list_employees(db: Session = Depends(get_db)):
    employees = db.query(models.Employee).all()
    results = []
    for e in employees:
        active_plan = db.query(models.OnboardingPlan).filter(
            models.OnboardingPlan.employee_id == e.id
        ).order_by(models.OnboardingPlan.created_at.desc()).first()

        results.append({
            "id": e.id,
            "employee_code": e.employee_code,
            "full_name": e.full_name,
            "role": e.role.name if e.role else "N/A",
            "role_code": e.role.code if e.role else "N/A",
            "department": e.department.name if e.department else "N/A",
            "experience_level": e.experience_level,
            "manager": e.reporting_manager,
            "training_status": e.training_status,
            "active_plan_id": active_plan.id if active_plan else None,
            "active_plan_status": active_plan.status if active_plan else "NO_PLAN"
        })
    return results

@router.get("/employees/{id}")
def get_employee(id: int, db: Session = Depends(get_db)):
    e = db.query(models.Employee).filter(models.Employee.id == id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Employee not found.")
    return {
        "id": e.id,
        "employee_code": e.employee_code,
        "full_name": e.full_name,
        "role_id": e.role_id,
        "role": e.role.name if e.role else "N/A",
        "role_code": e.role.code if e.role else "N/A",
        "department": e.department.name if e.department else "N/A",
        "experience_level": e.experience_level,
        "manager": e.reporting_manager,
        "training_status": e.training_status
    }

# --- 4. Documents & Ingestion ---
@router.get("/documents")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(models.Document).all()
    results = []
    for d in docs:
        active_v = db.query(models.DocumentVersion).filter(
            models.DocumentVersion.document_id == d.id,
            models.DocumentVersion.is_active == True
        ).first()

        chunks_count = len(active_v.chunks) if active_v else 0
        results.append({
            "id": d.id,
            "doc_code": d.doc_code,
            "title": d.title,
            "doc_type": d.doc_type,
            "department": d.department.name if d.department else "General",
            "current_version": d.current_version,
            "file_format": d.file_format,
            "is_active": d.is_active,
            "is_flagged_adversarial": d.is_flagged_adversarial,
            "chunks_count": chunks_count,
            "precedence_level": active_v.precedence_level if active_v else 3
        })
    return results

@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    doc_code: str = Form(...),
    title: str = Form(...),
    doc_type: str = Form("POLICY"),
    department_id: Optional[int] = Form(None),
    version_str: str = Form("1.0"),
    precedence_level: int = Form(1),
    db: Session = Depends(get_db)
):
    """Full-pipeline document ingestion: Validation, Duplicate check, Adversarial Scan, Parsing, Chunking, Extraction."""
    file_bytes = await file.read()
    
    # 1. Document Pre-validation
    valid, msg, meta = DocumentValidator.validate_upload(file.filename, file_bytes, db=db)
    if not valid:
        raise HTTPException(status_code=400, detail=msg)

    # 2. Adversarial Scanning
    from src.security.adversarial_scanner import AdversarialScanner
    is_suspicious, findings = AdversarialScanner.scan_text(file_bytes.decode('utf-8', errors='ignore'))

    # 3. Save physical file
    ext = meta["file_format"]
    save_dir = os.path.join(settings.BASE_DIR, "sample_documents", ext)
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, f"{doc_code}.{ext}")
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # 4. Save Document & Version record
    doc_record = models.Document(
        doc_code=doc_code,
        title=title,
        doc_type=doc_type,
        department_id=department_id,
        current_version=version_str,
        file_path=file_path,
        file_format=ext,
        checksum=meta["checksum"],
        is_active=True,
        is_flagged_adversarial=is_suspicious
    )
    db.add(doc_record)
    db.flush()

    ver_record = models.DocumentVersion(
        document_id=doc_record.id,
        version_str=version_str,
        effective_date=datetime.datetime.utcnow(),
        change_summary="Uploaded via ingestion pipeline.",
        is_active=True,
        precedence_level=precedence_level
    )
    db.add(ver_record)
    db.flush()

    # 5. Parse Document into Sections
    sections = DocumentParser.parse_file(file_path)

    # 6. Chunk content
    chunks = DocumentChunker.chunk_sections(sections)
    for c in chunks:
        chunk_obj = models.DocumentChunk(
            version_id=ver_record.id,
            chunk_index=c["chunk_index"],
            section_id=c["section_id"],
            section_heading=c["section_heading"],
            page_number=c["page_number"],
            paragraph_ref=c["paragraph_ref"],
            content=c["content"],
            token_count=c["token_count"]
        )
        db.add(chunk_obj)
        db.flush()

        # 7. Extract candidate requirements
        RequirementExtractionService.extract_from_chunk(db, chunk_obj, doc_record, ver_record)

    db.commit()

    return {
        "message": "Document successfully ingested, chunked, and requirements extracted.",
        "document_id": doc_record.id,
        "doc_code": doc_record.doc_code,
        "version": version_str,
        "sections_parsed": len(sections),
        "chunks_created": len(chunks),
        "is_flagged_adversarial": is_suspicious,
        "adversarial_findings": findings
    }

@router.get("/documents/{id}/chunks")
def get_document_chunks(id: int, db: Session = Depends(get_db)):
    doc = db.query(models.Document).filter(models.Document.id == id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    active_v = db.query(models.DocumentVersion).filter(
        models.DocumentVersion.document_id == doc.id,
        models.DocumentVersion.is_active == True
    ).first()

    if not active_v:
        return []

    return [
        {
            "chunk_id": c.id,
            "chunk_index": c.chunk_index,
            "section_id": c.section_id,
            "section_heading": c.section_heading,
            "page_number": c.page_number,
            "paragraph_ref": c.paragraph_ref,
            "content": c.content,
            "token_count": c.token_count
        } for c in active_v.chunks
    ]

# --- 5. Role Requirement Matrix ---
@router.get("/role-matrix")
def get_role_matrix_overview(db: Session = Depends(get_db)):
    return RoleMatrixService.get_complete_matrix_overview(db)

@router.get("/role-matrix/{role_id}")
def get_role_matrix_details(role_id: int, db: Session = Depends(get_db)):
    return RoleMatrixService.get_matrix_for_role(db, role_id)

# --- 6. Onboarding Generation & Plans ---
@router.post("/onboarding/generate")
def generate_onboarding_plan(payload: Dict[str, int], db: Session = Depends(get_db)):
    emp_id = payload.get("employee_id")
    if not emp_id:
        raise HTTPException(status_code=400, detail="employee_id is required.")
    
    plan_result = OnboardingService.generate_plan_for_employee(db, emp_id)
    return plan_result

@router.get("/onboarding/{plan_id}")
def get_onboarding_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(models.OnboardingPlan).filter(models.OnboardingPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found.")

    modules_data = []
    for m in plan.learning_modules:
        modules_data.append({
            "id": m.id,
            "module_code": m.module_code,
            "title": m.title,
            "category": m.category,
            "purpose": m.purpose,
            "learning_objectives": json.loads(m.learning_objectives) if m.learning_objectives else [],
            "key_concepts": json.loads(m.key_concepts) if m.key_concepts else [],
            "estimated_duration_mins": m.estimated_duration_mins,
            "stage": m.stage,
            "difficulty": m.difficulty,
            "source_doc_id": m.source_doc_id,
            "source_section_id": m.source_section_id,
            "verification_status": m.verification_status,
            "status": m.status,
            "has_quiz": len(m.quizzes) > 0,
            "quiz_id": m.quizzes[0].id if m.quizzes else None
        })

    tasks_data = [
        {
            "id": t.id,
            "description": t.description,
            "expected_outcome": t.expected_outcome,
            "completion_criteria": t.completion_criteria,
            "difficulty": t.difficulty,
            "due_stage": t.due_stage,
            "status": t.status,
            "source_doc_id": t.source_doc_id,
            "source_section_id": t.source_section_id,
            "submitted_evidence": t.submitted_evidence
        } for t in plan.tasks
    ]

    checklists_data = [
        {
            "id": c.id,
            "activity": c.activity,
            "is_mandatory": c.is_mandatory,
            "due_stage": c.due_stage,
            "status": c.status,
            "responsible_person": c.responsible_person,
            "source_doc_id": c.source_doc_id,
            "source_section_id": c.source_section_id
        } for c in plan.checklists
    ]

    assessments_data = [
        {
            "id": a.id,
            "title": a.title,
            "assessment_type": a.assessment_type,
            "rubric": json.loads(a.rubric_json) if a.rubric_json else [],
            "status": a.status,
            "score": a.score
        } for a in plan.assessments
    ]

    last_val = db.query(models.ValidationResult).filter(
        models.ValidationResult.plan_id == plan.id
    ).order_by(models.ValidationResult.run_at.desc()).first()

    return {
        "id": plan.id,
        "title": plan.title,
        "status": plan.status,
        "employee_id": plan.employee_id,
        "employee_name": plan.employee.full_name if plan.employee else "N/A",
        "role_name": plan.role.name if plan.role else "N/A",
        "coverage_score": plan.coverage_score,
        "traceability_score": plan.traceability_score,
        "consistency_score": plan.consistency_score,
        "prompt_version": plan.prompt_version,
        "model_used": plan.model_used,
        "modules": modules_data,
        "tasks": tasks_data,
        "checklists": checklists_data,
        "assessments": assessments_data,
        "validation_summary": {
            "validation_id": last_val.id if last_val else None,
            "missing_req_count": last_val.missing_req_count if last_val else 0,
            "unsupported_count": last_val.unsupported_count if last_val else 0,
            "contradiction_count": last_val.contradiction_count if last_val else 0,
            "duplicate_count": last_val.duplicate_count if last_val else 0
        } if last_val else None
    }

@router.get("/onboarding/employee/{employee_id}")
def get_employee_plan(employee_id: int, db: Session = Depends(get_db)):
    plan = db.query(models.OnboardingPlan).filter(
        models.OnboardingPlan.employee_id == employee_id
    ).order_by(models.OnboardingPlan.created_at.desc()).first()

    if not plan:
        raise HTTPException(status_code=404, detail="No onboarding plan found for this employee.")
    return get_onboarding_plan(plan.id, db)

# --- 7. Execution Actions: Modules, Tasks, Checklists, Quizzes ---
@router.post("/modules/{module_id}/complete")
def complete_module(module_id: int, db: Session = Depends(get_db)):
    mod = ProgressService.complete_module(db, module_id)
    if not mod:
        raise HTTPException(status_code=404, detail="Module not found.")
    return {"message": "Module completed successfully", "module_id": mod.id, "status": mod.status}

@router.post("/checklists/{checklist_id}/toggle")
def toggle_checklist(checklist_id: int, payload: Dict[str, bool], db: Session = Depends(get_db)):
    completed = payload.get("completed", True)
    chk = ProgressService.toggle_checklist(db, checklist_id, completed)
    if not chk:
        raise HTTPException(status_code=404, detail="Checklist not found.")
    return {"message": "Checklist toggled", "checklist_id": chk.id, "status": chk.status}

@router.post("/tasks/{task_id}/submit")
def submit_task(task_id: int, payload: Dict[str, str], db: Session = Depends(get_db)):
    evidence = payload.get("evidence", "Evidence verified by supervisor.")
    task = ProgressService.submit_task_evidence(db, task_id, evidence)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    return {"message": "Task submitted and approved", "task_id": task.id, "status": task.status}

@router.get("/quizzes/{quiz_id}")
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found.")

    questions = []
    for q in quiz.questions:
        questions.append({
            "id": q.id,
            "question_text": q.question_text,
            "question_type": q.question_type,
            "options": json.loads(q.options_json) if q.options_json else [],
            "difficulty": q.difficulty,
            "source_doc_id": q.source_doc_id,
            "source_section_id": q.source_section_id
        })

    return {
        "id": quiz.id,
        "title": quiz.title,
        "passing_score": quiz.passing_score,
        "questions": questions
    }

@router.post("/quizzes/{quiz_id}/submit")
def submit_quiz(quiz_id: int, payload: Dict[str, Any], db: Session = Depends(get_db)):
    emp_id = payload.get("employee_id")
    answers = payload.get("answers", {})
    if not emp_id:
        raise HTTPException(status_code=400, detail="employee_id is required.")

    result = ProgressService.submit_quiz_attempt(db, emp_id, quiz_id, answers)
    return result

# --- 8. Independent Python Ground Truth Validation & Comparison ---
@router.post("/validation/run/{plan_id}")
def run_plan_validation(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(models.OnboardingPlan).filter(models.OnboardingPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found.")

    # Reconstruct plan dictionary for validator
    plan_dict = {
        "modules": [
            {
                "module_code": m.module_code,
                "title": m.title,
                "requirement_code": m.requirement.req_code if m.requirement else None,
                "source_doc_id": m.source_doc_id,
                "source_section_id": m.source_section_id,
                "stage": m.stage,
                "difficulty": m.difficulty,
                "learning_objectives": json.loads(m.learning_objectives) if m.learning_objectives else [],
                "key_concepts": json.loads(m.key_concepts) if m.key_concepts else [],
                "quiz_questions": [
                    {
                        "question_text": q.question_text,
                        "correct_answer": json.loads(q.correct_answer_json) if q.correct_answer_json else "",
                        "source_doc_id": q.source_doc_id,
                        "source_section_id": q.source_section_id
                    } for q in m.quizzes[0].questions
                ] if m.quizzes else []
            } for m in plan.learning_modules
        ],
        "checklists": [
            {"activity": c.activity, "source_doc_id": c.source_doc_id, "source_section_id": c.source_section_id}
            for c in plan.checklists
        ]
    }

    val_res = PythonValidationEngine.validate_plan(db, plan.id, plan_dict, plan.role_id)
    return val_res

@router.get("/validation/{plan_id}")
def get_validation_details(plan_id: int, db: Session = Depends(get_db)):
    val = db.query(models.ValidationResult).filter(
        models.ValidationResult.plan_id == plan_id
    ).order_by(models.ValidationResult.run_at.desc()).first()

    if not val:
        raise HTTPException(status_code=404, detail="No validation result found for this plan.")

    return {
        "validation_id": val.id,
        "run_at": val.run_at.isoformat() if val.run_at else None,
        "overall_status": val.overall_status,
        "coverage_score": val.coverage_score,
        "traceability_score": val.traceability_score,
        "consistency_score": val.consistency_score,
        "missing_count": val.missing_req_count,
        "unsupported_count": val.unsupported_count,
        "contradiction_count": val.contradiction_count,
        "duplicate_count": val.duplicate_count,
        "details": json.loads(val.details_json) if val.details_json else {}
    }

@router.get("/comparison/{plan_id}")
def get_comparison_matrix(plan_id: int, db: Session = Depends(get_db)):
    """Returns the 100+ row GenAI vs Python Ground Truth comparison table."""
    val = db.query(models.ValidationResult).filter(
        models.ValidationResult.plan_id == plan_id
    ).order_by(models.ValidationResult.run_at.desc()).first()

    if not val or not val.comparison_json:
        # Generate on the fly if needed
        plan = db.query(models.OnboardingPlan).filter(models.OnboardingPlan.id == plan_id).first()
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found.")
        from src.comparison_engine.comparator import ComparisonEngine
        comparison = ComparisonEngine.generate_comparison_matrix(db, plan.role_id, {})
        return {"total_rows": len(comparison), "rows": comparison}

    comparison_data = json.loads(val.comparison_json)
    return {
        "plan_id": plan_id,
        "total_rows": len(comparison_data),
        "rows": comparison_data
    }

# --- 9. Reviewer Workflow & Audit Trail ---
@router.get("/reviews/queue")
def get_review_queue(db: Session = Depends(get_db)):
    return ReviewService.get_review_queue(db)

@router.post("/reviews/{plan_id}/decision")
def post_review_decision(plan_id: int, payload: Dict[str, Any], db: Session = Depends(get_db)):
    action = payload.get("action", "APPROVE")
    notes = payload.get("notes", "Reviewed by authorized reviewer.")
    reviewer_id = payload.get("reviewer_id", 2)
    override_status = payload.get("override_status")

    res = ReviewService.process_decision(
        db=db,
        plan_id=plan_id,
        reviewer_id=reviewer_id,
        action=action,
        notes=notes,
        override_status=override_status
    )
    return res

@router.get("/audit-logs")
def list_audit_logs(db: Session = Depends(get_db)):
    logs = db.query(models.AuditLog).order_by(models.AuditLog.timestamp.desc()).limit(50).all()
    return [
        {
            "id": l.id,
            "user_id": l.user_id,
            "user_name": l.user.username if l.user else "System",
            "action": l.action,
            "entity_type": l.entity_type,
            "entity_id": l.entity_id,
            "payload_before": l.payload_before,
            "payload_after": l.payload_after,
            "timestamp": l.timestamp.isoformat() if l.timestamp else None
        } for l in logs
    ]

# --- 10. Progress & Adaptive Recommendations ---
@router.get("/progress/{employee_id}")
def get_employee_progress(employee_id: int, db: Session = Depends(get_db)):
    return ProgressService.get_employee_progress(db, employee_id)

@router.get("/recommendations/{employee_id}")
def get_employee_recommendations(employee_id: int, db: Session = Depends(get_db)):
    return AdaptiveService.get_employee_recommendations(db, employee_id)

# --- 11. Policy Update Impact Analysis ---
@router.post("/policy-impact/analyze")
def analyze_policy_impact(payload: Dict[str, str], db: Session = Depends(get_db)):
    doc_code = payload.get("doc_code", "DOC-POL-01")
    old_ver = payload.get("old_version", "1.0")
    new_ver = payload.get("new_version", "2.0")

    impact = ImpactService.analyze_policy_update(db, doc_code, old_ver, new_ver)
    return impact

@router.post("/policy-impact/regenerate-module/{module_id}")
def regenerate_module(module_id: int, db: Session = Depends(get_db)):
    return ImpactService.selective_regenerate_module(db, module_id)

# --- 12. Reports & Exports ---
@router.get("/reports/compliance")
def get_compliance_report(db: Session = Depends(get_db)):
    return ReportGenerator.generate_compliance_report(db)

@router.get("/export/csv")
def export_csv_report(db: Session = Depends(get_db)):
    report = ReportGenerator.generate_compliance_report(db)
    csv_str = ReportExporter.export_csv(report)
    return Response(content=csv_str, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=compliance_report.csv"})

@router.get("/export/pdf")
def export_pdf_report(db: Session = Depends(get_db)):
    report = ReportGenerator.generate_compliance_report(db)
    target_path = os.path.join(settings.BASE_DIR, "reports", "executive_compliance_report.pdf")
    ReportExporter.export_pdf(report, target_path)
    return FileResponse(path=target_path, filename="executive_compliance_report.pdf", media_type="application/pdf")

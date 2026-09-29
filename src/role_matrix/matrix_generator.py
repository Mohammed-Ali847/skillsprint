# src/role_matrix/matrix_generator.py
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from src.database import models

class RoleMatrixService:
    """Manages the Role Requirement Matrix, returning role-specific policies, processes, tasks, and competencies."""

    @staticmethod
    def get_matrix_for_role(db: Session, role_id: int) -> Dict[str, Any]:
        role = db.query(models.Role).filter(models.Role.id == role_id).first()
        if not role:
            return {"error": "Role not found"}

        role_reqs = db.query(models.RoleRequirement).filter(models.RoleRequirement.role_id == role_id).all()
        
        mandatory_list = []
        optional_list = []
        competencies = set()
        policies_involved = set()
        
        for rr in role_reqs:
            req = rr.requirement
            if not req:
                continue
            doc = req.document
            ver = req.version
            
            item = {
                "role_req_id": rr.id,
                "requirement_id": req.id,
                "requirement_code": req.req_code,
                "text": req.requirement_text,
                "category": req.category,
                "is_mandatory": rr.is_mandatory,
                "priority": rr.priority,
                "due_stage": rr.due_stage,
                "competency": req.competency,
                "document_code": doc.doc_code if doc else "N/A",
                "document_title": doc.title if doc else "N/A",
                "document_type": doc.doc_type if doc else "N/A",
                "section_id": req.section_id,
                "version": ver.version_str if ver else "1.0",
                "specific_instructions": rr.specific_instructions
            }
            
            competencies.add(req.competency)
            if doc:
                policies_involved.add(f"{doc.doc_code}: {doc.title}")
                
            if rr.is_mandatory:
                mandatory_list.append(item)
            else:
                optional_list.append(item)
                
        return {
            "role_id": role.id,
            "role_code": role.code,
            "role_name": role.name,
            "department": role.department.name if role.department else "General",
            "experience_level": role.experience_level,
            "description": role.description,
            "total_requirements": len(role_reqs),
            "mandatory_count": len(mandatory_list),
            "optional_count": len(optional_list),
            "competencies": sorted(list(competencies)),
            "source_documents_count": len(policies_involved),
            "mandatory_requirements": mandatory_list,
            "optional_requirements": optional_list
        }

    @staticmethod
    def get_complete_matrix_overview(db: Session) -> List[Dict[str, Any]]:
        roles = db.query(models.Role).all()
        overview = []
        for r in roles:
            matrix_data = RoleMatrixService.get_matrix_for_role(db, r.id)
            overview.append({
                "role_id": r.id,
                "role_code": r.code,
                "role_name": r.name,
                "department": matrix_data.get("department"),
                "experience_level": r.experience_level,
                "total_requirements": matrix_data.get("total_requirements", 0),
                "mandatory_count": matrix_data.get("mandatory_count", 0),
                "optional_count": matrix_data.get("optional_count", 0),
                "competency_count": len(matrix_data.get("competencies", []))
            })
        return overview

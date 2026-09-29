# src/python_validation/coverage_validator.py
from typing import Dict, Any, List, Set
from sqlalchemy.orm import Session
from src.database import models

class CoverageValidator:
    """Calculates deterministic Mandatory Requirement Coverage from actual database records."""

    @classmethod
    def validate_plan_coverage(cls, db: Session, role_id: int, plan_dict: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Fetch all mandatory requirements for this role from the Role Requirement Matrix
        role_reqs = db.query(models.RoleRequirement).filter(
            models.RoleRequirement.role_id == role_id,
            models.RoleRequirement.is_mandatory == True
        ).all()

        total_mandatory = len(role_reqs)
        if total_mandatory == 0:
            return {
                "coverage_score": 100.0,
                "total_mandatory": 0,
                "covered_count": 0,
                "missing_count": 0,
                "covered_requirements": [],
                "missing_requirements": []
            }

        expected_req_codes = {rr.requirement.req_code: rr.requirement for rr in role_reqs if rr.requirement}
        
        # 2. Extract requirement codes covered in generated plan (from modules, checklists, tasks)
        covered_codes = set()
        for m in plan_dict.get("modules", []):
            code = m.get("requirement_code")
            if code and code in expected_req_codes:
                covered_codes.add(code)
                
        for c in plan_dict.get("checklists", []):
            code = c.get("requirement_code")
            if code and code in expected_req_codes:
                covered_codes.add(code)
                
        # 3. Partition into covered vs missing
        covered_list = []
        missing_list = []
        
        for code, req in expected_req_codes.items():
            item_info = {
                "requirement_code": code,
                "text": req.requirement_text,
                "category": req.category,
                "competency": req.competency,
                "source_doc": req.document.doc_code if req.document else "N/A",
                "source_sec": req.section_id
            }
            if code in covered_codes:
                covered_list.append(item_info)
            else:
                missing_list.append(item_info)

        coverage_score = round((len(covered_codes) / total_mandatory) * 100.0, 2)

        return {
            "coverage_score": coverage_score,
            "total_mandatory": total_mandatory,
            "covered_count": len(covered_codes),
            "missing_count": len(missing_list),
            "covered_requirements": covered_list,
            "missing_requirements": missing_list
        }

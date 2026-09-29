# src/python_validation/role_relevance_validator.py
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from src.database import models

class RoleRelevanceValidator:
    """Verifies that generated learning modules match the selected employee's role and department."""

    @classmethod
    def validate_role_relevance(cls, db: Session, role_id: int, plan_dict: Dict[str, Any]) -> Dict[str, Any]:
        role = db.query(models.Role).filter(models.Role.id == role_id).first()
        if not role:
            return {"error": "Role not found", "irrelevant_count": 0, "irrelevant_items": []}

        # Valid requirements for this role
        valid_role_reqs = db.query(models.RoleRequirement).filter(models.RoleRequirement.role_id == role_id).all()
        valid_req_codes = {rr.requirement.req_code for rr in valid_role_reqs if rr.requirement}
        
        irrelevant_items = []
        for m in plan_dict.get("modules", []):
            code = m.get("requirement_code")
            if code and code not in valid_req_codes:
                irrelevant_items.append({
                    "module_code": m.get("module_code"),
                    "title": m.get("title"),
                    "requirement_code": code,
                    "target_role": role.name,
                    "reason": f"Requirement {code} is not part of {role.name}'s approved Role Requirement Matrix."
                })

        return {
            "target_role": role.name,
            "irrelevant_count": len(irrelevant_items),
            "irrelevant_items": irrelevant_items,
            "is_all_relevant": len(irrelevant_items) == 0
        }

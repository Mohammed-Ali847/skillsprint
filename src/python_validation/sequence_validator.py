# src/python_validation/sequence_validator.py
from typing import Dict, Any, List

class SequenceValidator:
    """Verifies logical learning order, prerequisite integrity, and stage pacing."""

    STAGE_ORDER = {
        "Day 1": 1,
        "Week 1": 2,
        "Week 2": 3,
        "First 30 Days": 4,
        "First 60 Days": 5,
        "First 90 Days": 6
    }

    DIFFICULTY_RANK = {
        "Beginner": 1,
        "Intermediate": 2,
        "Advanced": 3
    }

    @classmethod
    def validate_learning_sequence(cls, plan_dict: Dict[str, Any]) -> Dict[str, Any]:
        sequence_issues = []
        modules = plan_dict.get("modules", [])
        
        # 1. Check Day 1 Overload
        day1_modules = [m for m in modules if m.get("stage") == "Day 1"]
        if len(day1_modules) > 8:
            sequence_issues.append({
                "type": "DAY_ONE_OVERLOAD",
                "count": len(day1_modules),
                "reason": f"Day 1 contains {len(day1_modules)} modules, exceeding the recommended maximum of 8."
            })

        # 2. Check Prerequisite Ordering (Advanced before Basics or Prerequisite scheduled later)
        module_stages = {m.get("module_code"): m.get("stage", "Day 1") for m in modules}

        for m in modules:
            m_code = m.get("module_code")
            prereq = m.get("prerequisite_module_code")
            current_stage_rank = cls.STAGE_ORDER.get(m.get("stage", "Day 1"), 1)

            if prereq and prereq in module_stages:
                prereq_stage_rank = cls.STAGE_ORDER.get(module_stages[prereq], 1)
                if prereq_stage_rank > current_stage_rank:
                    sequence_issues.append({
                        "type": "INVALID_PREREQUISITE_SEQUENCE",
                        "module": m_code,
                        "prerequisite": prereq,
                        "module_stage": m.get("stage"),
                        "prerequisite_stage": module_stages[prereq],
                        "reason": f"Module {m_code} in {m.get('stage')} scheduled BEFORE prerequisite {prereq} in {module_stages[prereq]}."
                    })

            # Check difficulty progression
            diff_rank = cls.DIFFICULTY_RANK.get(m.get("difficulty", "Beginner"), 1)
            if diff_rank == 3 and current_stage_rank == 1:
                sequence_issues.append({
                    "type": "ADVANCED_TASK_ON_DAY_ONE",
                    "module": m_code,
                    "reason": f"Advanced difficulty module '{m.get('title')}' scheduled on Day 1 before foundational orientation."
                })

        return {
            "sequence_issue_count": len(sequence_issues),
            "sequence_issues": sequence_issues,
            "is_valid_sequence": len(sequence_issues) == 0
        }

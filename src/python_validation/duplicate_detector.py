# src/python_validation/duplicate_detector.py
from typing import Dict, Any, List

class DuplicateDetector:
    """Detects duplicate or near-duplicate learning modules, tasks, and quiz questions."""

    @staticmethod
    def _jaccard_similarity(str1: str, str2: str) -> float:
        set1 = set(str1.lower().split())
        set2 = set(str2.lower().split())
        if not set1 or not set2:
            return 0.0
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union

    @classmethod
    def check_duplicates(cls, plan_dict: Dict[str, Any]) -> Dict[str, Any]:
        duplicate_flags = []
        modules = plan_dict.get("modules", [])

        # Check module duplicate titles & requirement collisions
        seen_reqs = {}
        for i, m in enumerate(modules):
            req_code = m.get("requirement_code")
            if req_code:
                if req_code in seen_reqs:
                    duplicate_flags.append({
                        "type": "DUPLICATE_REQUIREMENT_MODULE",
                        "module_code": m.get("module_code"),
                        "conflicting_module": seen_reqs[req_code],
                        "requirement_code": req_code,
                        "reason": f"Multiple modules ({m.get('module_code')} and {seen_reqs[req_code]}) target the same requirement."
                    })
                else:
                    seen_reqs[req_code] = m.get("module_code")

            # Check pairwise text similarity with subsequent modules
            for j in range(i + 1, len(modules)):
                other_m = modules[j]
                sim = cls._jaccard_similarity(m.get("title", ""), other_m.get("title", ""))
                if sim > 0.85:
                    duplicate_flags.append({
                        "type": "NEAR_DUPLICATE_TITLE",
                        "module_a": m.get("module_code"),
                        "module_b": other_m.get("module_code"),
                        "similarity": round(sim, 2),
                        "reason": f"High lexical overlap ({round(sim*100)}%) between module titles."
                    })

        return {
            "duplicate_count": len(duplicate_flags),
            "duplicates": duplicate_flags,
            "has_duplicates": len(duplicate_flags) > 0
        }

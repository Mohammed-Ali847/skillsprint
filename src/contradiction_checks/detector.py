# src/contradiction_checks/detector.py
import re
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from src.database import models
from src.services.precedence_service import PrecedenceService

class ContradictionDetector:
    """Identifies contradictory policy statements, outdated rules, and precedence violations."""

    # Documented corporate contradiction benchmarks
    CONTRADICTION_BENCHMARKS = [
        {
            "id": "CONT-001",
            "topic": "Password Rotation Frequency",
            "conflicting_pattern": r'\b180\s*days?\b',
            "authoritative_rule": "DOC-POL-01 v2.0 mandates 90-day password rotation. FAQ-01 citing 180 days is superseded.",
            "rule_code": "REQ-SEC-001"
        },
        {
            "id": "CONT-002",
            "topic": "Frontline Support Refund Limit",
            "conflicting_pattern": r'\$500\b',
            "authoritative_rule": "DOC-SOP-02 v2.0 caps Support Executive refunds at $150. FAQ-02 citing $500 is superseded by SOP.",
            "rule_code": "REQ-SUP-004"
        },
        {
            "id": "CONT-003",
            "topic": "Priority 1 Outage Escalation SLA",
            "conflicting_pattern": r'30\s*minutes?.*escalat',
            "authoritative_rule": "DOC-SOP-02 v2.0 mandates 15-minute P1 escalation SLA. FAQ-02 citing 30 minutes is incorrect.",
            "rule_code": "REQ-SUP-002"
        },
        {
            "id": "CONT-004",
            "topic": "Local Unencrypted CSV Data Storage",
            "conflicting_pattern": r'save.*(?:desktop|laptop).*csv',
            "authoritative_rule": "DOC-POL-02 and DOC-SOP-05 prohibit local unencrypted customer data. FAQ-03 is superseded.",
            "rule_code": "REQ-DAT-002"
        },
        {
            "id": "CONT-005",
            "topic": "Vacation Leave Carryover Limit",
            "conflicting_pattern": r'10\s*days?.*carry\s*over',
            "authoritative_rule": "DOC-POL-07 v2.0 caps annual carryover at 5 days expiring March 31. v1.0 (10 days) is obsolete.",
            "rule_code": "REQ-LEV-002"
        },
        {
            "id": "CONT-006",
            "topic": "Travel Flight Pre-Approval Threshold",
            "conflicting_pattern": r'\$1500.*flight',
            "authoritative_rule": "DOC-POL-08 v2.0 requires VP approval for flights over $800. v1.0 ($1500) is obsolete.",
            "rule_code": "REQ-EXP-002"
        },
        {
            "id": "CONT-007",
            "topic": "Severity 1 Critical Breach Notification SLA",
            "conflicting_pattern": r'24\s*hours?.*breach',
            "authoritative_rule": "DOC-SOP-01 v2.0 mandates 4-hour breach notification SLA to CISO/DPO. v1.0 (24h) is obsolete.",
            "rule_code": "REQ-INC-002"
        }
    ]

    @classmethod
    def scan_plan_contradictions(cls, db: Session, plan_dict: Dict[str, Any]) -> Dict[str, Any]:
        detected_contradictions = []

        for m in plan_dict.get("modules", []):
            text_corpus = m.get("title", "") + " " + m.get("purpose", "") + " " + " ".join(m.get("learning_objectives", []))
            for q in m.get("quiz_questions", []):
                text_corpus += " " + q.get("question_text", "") + " " + str(q.get("correct_answer", ""))

            for bench in cls.CONTRADICTION_BENCHMARKS:
                if re.search(bench["conflicting_pattern"], text_corpus, re.IGNORECASE):
                    detected_contradictions.append({
                        "contradiction_id": bench["id"],
                        "topic": bench["topic"],
                        "module_code": m.get("module_code"),
                        "violating_text_snippet": re.search(bench["conflicting_pattern"], text_corpus, re.IGNORECASE).group(0),
                        "authoritative_rule": bench["authoritative_rule"],
                        "status": "CONTRADICTION_DETECTED"
                    })

        return {
            "contradiction_count": len(detected_contradictions),
            "contradictions": detected_contradictions,
            "has_contradictions": len(detected_contradictions) > 0
        }

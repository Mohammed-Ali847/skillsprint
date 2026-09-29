# src/security/adversarial_scanner.py
import re
import base64
from typing import Tuple, List, Dict, Any

class AdversarialScanner:
    """Scans uploaded documents and queries for malicious prompt injection and evasion patterns."""

    INJECTION_PATTERNS = [
        (r'ignore\s+(?:all\s+)?(?:previous\s+)?instructions', "INSTRUCTION_OVERRIDE"),
        (r'system\s+instruction\s+override', "SYSTEM_OVERRIDE"),
        (r'jailbreak', "JAILBREAK_ATTEMPT"),
        (r'disregard\s+(?:all\s+)?(?:company\s+)?(?:policies|the\s+role)', "POLICY_BYPASS"),
        (r'you\s+are\s+now\s+in\s+.*mode', "MODE_SWITCH"),
        (r'dan\s+mode', "MODE_SWITCH"),
        (r'output\s+.*(?:system\s+prompt|system\s+instructions|model\s+parameters|api\s+.*keys)', "PROMPT_EXFILTRATION"),
        (r'print\s+(?:out\s+)?all\s+(?:employee\s+)?salaries', "DATA_EXFILTRATION"),
        (r'automatically\s+award\s+.*100%', "GRADE_MANIPULATION"),
        (r'waive\s+all\s+(?:mandatory\s+)?requirements', "COMPLIANCE_BYPASS"),
        (r'mark\s+all\s+mandatory\s+requirements\s+as\s+verified', "COMPLIANCE_BYPASS"),
        (r'exempt\s+from\s+.*policy', "POLICY_BYPASS"),
        (r'cancelled\s+all\s+(?:soc2|iso27001|gdpr)', "REGULATORY_BYPASS_SPOOF"),
        (r'</context>', "CONTEXT_ESCAPE"),
        (r'</instruction>', "INSTRUCTION_ESCAPE"),
        (r'</system>', "SYSTEM_TAG_ESCAPE")
    ]

    @classmethod
    def scan_text(cls, text: str) -> Tuple[bool, List[Dict[str, str]]]:
        """Scans text for adversarial directives and decoded Base64 payloads."""
        findings = []
        text_lower = text.lower()

        # 1. Regex Pattern Matching
        for pattern, threat_type in cls.INJECTION_PATTERNS:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                findings.append({
                    "threat_type": threat_type,
                    "pattern": pattern,
                    "snippet": matches[0][:80]
                })

        # 2. Base64 Hidden Payload Detection
        b64_matches = re.findall(r'[A-Za-z0-9+/]{20,}={0,2}', text)
        for b64 in b64_matches:
            try:
                decoded = base64.b64decode(b64).decode('utf-8', errors='ignore').lower()
                for pattern, threat_type in cls.INJECTION_PATTERNS:
                    if re.search(pattern, decoded, re.IGNORECASE):
                        findings.append({
                            "threat_type": f"BASE64_{threat_type}",
                            "pattern": "Base64 hidden payload",
                            "snippet": decoded[:80]
                        })
            except Exception:
                pass

        is_suspicious = len(findings) > 0
        return is_suspicious, findings

# scripts/seed_data_builder.py
import json

ALL_DOCUMENTS = []

def add_doc(code, title, doc_type, dept, fmt, ver, prec, v1_info, v2_info=None, reqs=None):
    versions = []
    if v1_info:
        versions.append({
            "version_str": "1.0",
            "effective_date": "2025-01-01T00:00:00",
            "expiry_date": "2026-01-01T00:00:00" if v2_info else None,
            "is_active": False if v2_info else True,
            "superseded_by": "2.0" if v2_info else None,
            "change_summary": v1_info.get("summary", "Initial release"),
            "sections": v1_info.get("sections", [])
        })
    if v2_info:
        versions.append({
            "version_str": "2.0",
            "effective_date": "2026-01-01T00:00:00",
            "expiry_date": None,
            "is_active": True,
            "superseded_by": None,
            "change_summary": v2_info.get("summary", "Updated version"),
            "sections": v2_info.get("sections", []),
            "requirements": reqs or []
        })
    elif v1_info and reqs:
        versions[0]["requirements"] = reqs
        
    ALL_DOCUMENTS.append({
        "doc_code": code,
        "title": title,
        "doc_type": doc_type,
        "dept_code": dept,
        "format": fmt,
        "current_version": ver,
        "precedence_level": prec,
        "versions": versions
    })

print("Initialized seed_data_builder.py base framework.")

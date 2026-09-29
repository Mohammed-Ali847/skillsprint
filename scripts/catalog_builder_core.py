import json, os

catalog = []

def make_doc(code, title, doc_type, dept, fmt, ver, prec, v1_sections, v1_summary, v2_sections=None, v2_summary=None, reqs=None):
    versions = []
    if v1_sections:
        versions.append({
            "version_str": "1.0",
            "effective_date": "2025-01-15T00:00:00",
            "expiry_date": "2026-01-14T23:59:59" if v2_sections else None,
            "is_active": False if v2_sections else True,
            "superseded_by": "2.0" if v2_sections else None,
            "change_summary": v1_summary or "Initial approved corporate release.",
            "sections": v1_sections
        })
    if v2_sections:
        versions.append({
            "version_str": "2.0",
            "effective_date": "2026-01-15T00:00:00",
            "expiry_date": None,
            "is_active": True,
            "superseded_by": None,
            "change_summary": v2_summary or "Comprehensive revision and updated compliance controls.",
            "sections": v2_sections,
            "requirements": reqs or []
        })
    elif v1_sections and reqs:
        versions[0]["requirements"] = reqs
        
    return {
        "doc_code": code,
        "title": title,
        "doc_type": doc_type,
        "dept_code": dept,
        "file_format": fmt,
        "current_version": ver,
        "precedence_level": prec,
        "versions": versions
    }

print("Base builder helper loaded.")

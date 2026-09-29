# scripts/seed_database.py
import os, sys, hashlib, json, datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from src.database.session import engine, Base, SessionLocal, init_db
from src.database import models
from scripts.dataset_definitions import DEPARTMENTS, ROLES, SAMPLE_EMPLOYEES
from scripts.data_policies import POLICIES
from scripts.data_sops import SOPS
from scripts.data_faqs_handbook import FAQS_AND_HANDBOOKS

ALL_DOCS = POLICIES + SOPS + FAQS_AND_HANDBOOKS

def hash_pw(pw: str) -> str:
    # Deterministic salted SHA-256 for competition compatibility
    salt = "skillsprint_salt_2026"
    return hashlib.sha256((salt + pw).encode('utf-8')).hexdigest()

def seed_db():
    print("Initializing fresh database tables...")
    init_db()
    db = SessionLocal()
    
    # 1. Clear existing records to ensure clean idempotent seed
    for tbl in reversed(Base.metadata.sorted_tables):
        db.execute(tbl.delete())
    db.commit()
    print("Cleared existing tables.")
    
    # 2. Seed Users
    core_users = [
        {"username": "admin", "email": "admin@apexnova.internal", "pw": "admin123", "role": "admin"},
        {"username": "reviewer", "email": "reviewer@apexnova.internal", "pw": "reviewer123", "role": "reviewer"},
        {"username": "trainer", "email": "trainer@apexnova.internal", "pw": "trainer123", "role": "training_manager"},
        {"username": "manager", "email": "manager@apexnova.internal", "pw": "manager123", "role": "manager"}
    ]
    user_map = {}
    for u in core_users:
        user_obj = models.User(
            username=u["username"],
            email=u["email"],
            hashed_password=hash_pw(u["pw"]),
            role=u["role"],
            is_active=True
        )
        db.add(user_obj)
        db.flush()
        user_map[u["username"]] = user_obj.id
        
    # 3. Seed Departments
    dept_map = {}
    for d in DEPARTMENTS:
        dept_obj = models.Department(
            code=d["code"],
            name=d["name"],
            description=d["description"]
        )
        db.add(dept_obj)
        db.flush()
        dept_map[d["code"]] = dept_obj.id
    print(f"Seeded {len(DEPARTMENTS)} departments.")
    
    # 4. Seed Roles
    role_map = {}
    for r in ROLES:
        role_obj = models.Role(
            code=r["code"],
            name=r["name"],
            department_id=dept_map[r["dept_code"]],
            experience_level=r["experience_level"],
            description=r["description"]
        )
        db.add(role_obj)
        db.flush()
        role_map[r["code"]] = role_obj.id
    print(f"Seeded {len(ROLES)} job roles.")
    
    # 5. Seed Employees & Employee Users
    emp_map = {}
    for emp in SAMPLE_EMPLOYEES:
        username = emp["code"].lower().replace("-", "")
        emp_user = models.User(
            username=username,
            email=f"{username}@apexnova.internal",
            hashed_password=hash_pw("employee123"),
            role="employee",
            is_active=True
        )
        db.add(emp_user)
        db.flush()
        
        emp_obj = models.Employee(
            user_id=emp_user.id,
            employee_code=emp["code"],
            full_name=emp["name"],
            role_id=role_map[emp["role_code"]],
            department_id=dept_map[emp["dept_code"]],
            experience_level=emp["level"],
            reporting_manager=emp["manager"],
            training_status=emp["status"]
        )
        db.add(emp_obj)
        db.flush()
        emp_map[emp["code"]] = emp_obj.id
    print(f"Seeded {len(SAMPLE_EMPLOYEES)} employee profiles.")
    
    # 6. Seed Documents, Versions, Chunks, and Requirements
    doc_map = {}
    ver_map = {}
    all_requirements = []
    
    for d_data in ALL_DOCS:
        code = d_data["doc_code"]
        fmt = d_data["file_format"]
        path = os.path.join(BASE_DIR, "sample_documents", fmt, f"{code}.{fmt}")
        
        # Calculate SHA256
        chk = ""
        if os.path.exists(path):
            with open(path, "rb") as f:
                chk = hashlib.sha256(f.read()).hexdigest()
                
        doc_obj = models.Document(
            doc_code=code,
            title=d_data["title"],
            doc_type=d_data["doc_type"],
            department_id=dept_map.get(d_data["dept_code"]),
            current_version=d_data["current_version"],
            file_path=path,
            file_format=fmt,
            checksum=chk,
            is_active=True
        )
        db.add(doc_obj)
        db.flush()
        doc_map[code] = doc_obj.id
        
        # Versions
        for v in d_data["versions"]:
            eff = datetime.datetime.fromisoformat(v["effective_date"])
            exp = datetime.datetime.fromisoformat(v["expiry_date"]) if v.get("expiry_date") else None
            
            ver_obj = models.DocumentVersion(
                document_id=doc_obj.id,
                version_str=v["version_str"],
                effective_date=eff,
                expiry_date=exp,
                change_summary=v["change_summary"],
                is_active=v["is_active"],
                superseded_by=v.get("superseded_by"),
                precedence_level=d_data["precedence_level"]
            )
            db.add(ver_obj)
            db.flush()
            ver_map[(code, v["version_str"])] = ver_obj.id
            
            # Chunks for this version
            chunk_idx = 1
            for sec in v["sections"]:
                token_est = len(sec["content"].split()) * 2
                chunk_obj = models.DocumentChunk(
                    version_id=ver_obj.id,
                    chunk_index=chunk_idx,
                    section_id=sec["id"],
                    section_heading=sec["heading"],
                    page_number=1 if chunk_idx <= 3 else 2,
                    paragraph_ref=f"Section {sec['id']}",
                    content=sec["content"],
                    token_count=token_est
                )
                db.add(chunk_obj)
                chunk_idx += 1
                
            # Requirements attached to this version
            if "requirements" in v:
                for r in v["requirements"]:
                    req_obj = models.Requirement(
                        req_code=r["code"],
                        document_id=doc_obj.id,
                        version_id=ver_obj.id,
                        section_id=r["sec"],
                        requirement_text=r["text"],
                        category=r["cat"],
                        is_mandatory=r["mandatory"],
                        competency=r["competency"],
                        default_priority=r["priority"],
                        default_due_stage=r["stage"]
                    )
                    db.add(req_obj)
                    db.flush()
                    all_requirements.append(req_obj)
                    
    db.commit()
    print(f"Seeded {len(doc_map)} documents, {len(ver_map)} versions, and {len(all_requirements)} extracted requirements.")
    
    # 7. Seed Role Requirements (The Role Requirement Matrix)
    # We map global baseline requirements to all roles, and role-specific requirements to specific roles
    # Baseline security/ethics/HR requirements (applicable to ALL roles)
    baseline_req_codes = [
        "REQ-SEC-001", "REQ-SEC-002", "REQ-SEC-003", "REQ-SEC-004",  # InfoSec
        "REQ-PRIV-001",                                                # Privacy
        "REQ-ACC-001", "REQ-ACC-004",                                  # Access & Credential sharing
        "REQ-USE-001", "REQ-USE-002",                                  # Acceptable Use & AI Safety
        "REQ-ETH-001", "REQ-ETH-003",                                  # Ethics & Conduct
        "REQ-LEV-001", "REQ-LEV-002",                                  # Leave policy
        "REQ-SAF-001", "REQ-SAF-002",                                  # Safety
        "REQ-WHT-001", "REQ-WHT-002",                                  # Whistleblower
        "REQ-HDB-001", "REQ-HDB-002"                                   # Culture & Hours
    ]
    
    # Role-specific requirements mapping
    role_specializations = {
        "SEC_ANALYST": ["REQ-ROL-001", "REQ-ACC-002", "REQ-INC-001", "REQ-INC-002", "REQ-INC-003", "REQ-INC-004", "REQ-REM-001", "REQ-REM-002"],
        "CUST_SUPPORT": ["REQ-ROL-002", "REQ-SUP-001", "REQ-SUP-002", "REQ-SUP-003", "REQ-SUP-004", "REQ-FAQ2-001"],
        "SOFT_ENG": ["REQ-ROL-003", "REQ-DEV-001", "REQ-DEV-002", "REQ-DEV-003", "REQ-DEV-004", "REQ-USE-003", "REQ-CAB-003"],
        "DATA_ANALYST": ["REQ-ROL-004", "REQ-PRIV-002", "REQ-PRIV-003", "REQ-PRIV-004", "REQ-DAT-001", "REQ-DAT-002", "REQ-DAT-003", "REQ-DAT-004"],
        "SALES_EXEC": ["REQ-ROL-005", "REQ-SLS-001", "REQ-SLS-002", "REQ-SLS-003", "REQ-SLS-004", "REQ-ETH-002", "REQ-ETH-004", "REQ-EXP-002"],
        "HR_EXEC": ["REQ-ROL-006", "REQ-HR-001", "REQ-HR-002", "REQ-HR-003", "REQ-HR-004", "REQ-WHT-003", "REQ-LEV-003"],
        "FIN_ASSOC": ["REQ-ROL-007", "REQ-EXP-001", "REQ-EXP-002", "REQ-EXP-003", "REQ-EXP-004"],
        "OPS_COORD": ["REQ-ROL-008", "REQ-OPS-001", "REQ-OPS-002", "REQ-OPS-003", "REQ-SAF-003", "REQ-REM-003"],
        "MKT_EXEC": ["REQ-ROL-009", "REQ-PRIV-001", "REQ-PRIV-004", "REQ-USE-002"],
        "TEAM_LEAD": ["REQ-ROL-010", "REQ-CAB-001", "REQ-CAB-002", "REQ-CAB-004", "REQ-ACC-003", "REQ-DEV-001", "REQ-DEV-002"]
    }
    
    # Query all requirements into a lookup dict by code
    req_dict = {r.req_code: r for r in db.query(models.Requirement).all()}
    
    total_role_req_entries = 0
    total_mandatory_entries = 0
    total_rolespec_entries = 0
    
    for r_code, role_id in role_map.items():
        # Add universal baseline
        for code in baseline_req_codes:
            if code in req_dict:
                r_obj = req_dict[code]
                rr = models.RoleRequirement(
                    role_id=role_id,
                    requirement_id=r_obj.id,
                    is_mandatory=r_obj.is_mandatory,
                    priority=r_obj.default_priority,
                    due_stage=r_obj.default_due_stage,
                    specific_instructions="Enterprise baseline requirement for all personnel."
                )
                db.add(rr)
                total_role_req_entries += 1
                if r_obj.is_mandatory:
                    total_mandatory_entries += 1
                    
        # Add role-specific
        spec_codes = role_specializations.get(r_code, [])
        for code in spec_codes:
            if code in req_dict:
                r_obj = req_dict[code]
                rr = models.RoleRequirement(
                    role_id=role_id,
                    requirement_id=r_obj.id,
                    is_mandatory=r_obj.is_mandatory,
                    priority=r_obj.default_priority,
                    due_stage=r_obj.default_due_stage,
                    specific_instructions=f"Job-specific core competency for {r_code}."
                )
                db.add(rr)
                total_role_req_entries += 1
                total_rolespec_entries += 1
                if r_obj.is_mandatory:
                    total_mandatory_entries += 1
                    
    db.commit()
    print(f"Role Requirement Matrix built:")
    print(f"  - Total Role-Requirement mappings: {total_role_req_entries}")
    print(f"  - Total Mandatory mappings: {total_mandatory_entries}")
    print(f"  - Total Role-Specific mappings: {total_rolespec_entries}")
    db.close()

if __name__ == "__main__":
    seed_db()

# scripts/expand_requirements.py
import sys, os, random
BASE_DIR = os.path.abspath(".")
sys.path.insert(0, BASE_DIR)
from src.database.session import SessionLocal
from src.database import models

db = SessionLocal()

# List of additional specific enterprise requirements across our 23 documents
ADDITIONAL_REQS = [
    # DOC-POL-01 (Security Policy v2.0)
    ("DOC-POL-01", "2.0", "1.2", "REQ-SEC-006", "Employees must disable password auto-fill on shared or presentation devices.", "MUST_DEMONSTRATE", True, "Identity Security", "High", "Day 1"),
    ("DOC-POL-01", "2.0", "1.2", "REQ-SEC-007", "Privileged users must not reuse corporate passwords on external SaaS services.", "MUST_ACKNOWLEDGE", True, "Credential Hygiene", "Critical", "Day 1"),
    ("DOC-POL-01", "2.0", "1.3", "REQ-SEC-008", "Printed documents containing customer data must be shredded immediately in cross-cut shredders.", "MUST_COMPLETE", True, "Physical Security", "Medium", "Week 1"),
    ("DOC-POL-01", "2.0", "1.4", "REQ-SEC-009", "Cloud storage buckets containing telemetry must enforce KMS customer-managed encryption keys.", "MUST_DEMONSTRATE", True, "Cloud Security", "Critical", "Week 2"),
    ("DOC-POL-01", "2.0", "1.5", "REQ-SEC-010", "Exceptions for specialized hardware keys require approval from CISO.", "RECOMMENDED", False, "Governance", "Low", "First 30 Days"),

    # DOC-POL-02 (Data Privacy v2.0)
    ("DOC-POL-02", "2.0", "2.1", "REQ-PRIV-006", "Data processors must execute formal Data Processing Agreements before processing PII.", "MUST_COMPLETE", True, "Privacy Law", "High", "Week 2"),
    ("DOC-POL-02", "2.0", "2.2", "REQ-PRIV-007", "Database engineers must implement deterministic masking on test schema migrations.", "MUST_DEMONSTRATE", True, "Data Masking", "Critical", "Week 1"),
    ("DOC-POL-02", "2.0", "2.3", "REQ-PRIV-008", "Customer deletion audits must be archived in compliance registers for 7 years.", "MUST_KNOW", True, "Compliance Records", "Medium", "First 60 Days"),
    ("DOC-POL-02", "2.0", "2.4", "REQ-PRIV-009", "EU customer records must never transit through non-adequacy sovereign cloud regions.", "MUST_ACKNOWLEDGE", True, "Sovereignty", "Critical", "Week 1"),
    ("DOC-POL-02", "2.0", "2.5", "REQ-PRIV-010", "Automated daily purge jobs must verify completion status via monitoring alerts.", "MUST_DEMONSTRATE", True, "Data Retention", "Medium", "Week 2"),

    # DOC-POL-03 (Access Control v2.0)
    ("DOC-POL-03", "2.0", "3.1", "REQ-ACC-005", "Temporary contractors must be assigned fixed expiration dates on IAM accounts.", "MUST_COMPLETE", True, "Contractor Governance", "High", "Day 1"),
    ("DOC-POL-03", "2.0", "3.2", "REQ-ACC-006", "All JIT elevation sessions must record interactive bash/PowerShell audit logs.", "MUST_DEMONSTRATE", True, "Session Recording", "Critical", "Week 1"),
    ("DOC-POL-03", "2.0", "3.3", "REQ-ACC-007", "Dormant accounts with no login for 45 days must be flagged for deletion.", "MUST_KNOW", True, "Identity Lifecycle", "Medium", "Week 2"),
    ("DOC-POL-03", "2.0", "3.4", "REQ-ACC-008", "SSH host keys must be verified and enrolled in corporate bastion certificates.", "MUST_DEMONSTRATE", True, "SSH Infrastructure", "High", "Week 1"),

    # DOC-POL-04 (Acceptable Use & AI Policy v2.0)
    ("DOC-POL-04", "2.0", "4.1", "REQ-USE-005", "Laptops must not be loaned to family members or third parties under any circumstances.", "MUST_ACKNOWLEDGE", True, "Asset Protection", "High", "Day 1"),
    ("DOC-POL-04", "2.0", "4.2", "REQ-USE-006", "Employees must submit an AI Tool Assessment request before adopting any new LLM plugin.", "MUST_COMPLETE", True, "AI Risk Review", "High", "Week 2"),
    ("DOC-POL-04", "2.0", "4.3", "REQ-USE-007", "Prompt engineering workflows must document testing against prompt injection benchmarks.", "MUST_DEMONSTRATE", True, "Prompt Security", "Critical", "Week 1"),
    ("DOC-POL-04", "2.0", "4.4", "REQ-USE-008", "Third-party npm/pip packages must undergo automated vulnerability scan before use.", "MUST_COMPLETE", True, "Software Supply Chain", "High", "Day 1"),

    # DOC-POL-05 (Ethics & Anti-Bribery)
    ("DOC-POL-05", "1.0", "5.1", "REQ-ETH-005", "Managers must respond to workplace discrimination complaints within 24 hours.", "MUST_COMPLETE", True, "Leadership Ethics", "Critical", "Day 1"),
    ("DOC-POL-05", "1.0", "5.2", "REQ-ETH-006", "Gifts of cash, gift cards, or crypto assets are strictly prohibited regardless of amount.", "MUST_KNOW", True, "Anti-Bribery", "Critical", "Day 1"),
    ("DOC-POL-05", "1.0", "5.3", "REQ-ETH-007", "Recusal from vendor selection is mandatory if an employee has personal vendor ties.", "MUST_ACKNOWLEDGE", True, "Conflict of Interest", "High", "Week 1"),
    ("DOC-POL-05", "1.0", "5.4", "REQ-ETH-008", "Employees should complete advanced antitrust training if participating in industry consortiums.", "RECOMMENDED", False, "Trade Law", "Low", "First 60 Days"),

    # DOC-POL-06 (Remote Work v2.0)
    ("DOC-POL-06", "2.0", "6.1", "REQ-REM-005", "Remote staff must lock home office doors when hosting visitors or repair contractors.", "RECOMMENDED", False, "Home Security", "Low", "First 30 Days"),
    ("DOC-POL-06", "2.0", "6.2", "REQ-REM-006", "Recovery keys for BitLocker/FileVault must be escrowed in IT Key Vault.", "MUST_COMPLETE", True, "Key Management", "High", "Day 1"),
    ("DOC-POL-06", "2.0", "6.3", "REQ-REM-007", "Split-tunneling is strictly disabled on all corporate ZTNA endpoints.", "MUST_DEMONSTRATE", True, "Zero Trust", "High", "Week 1"),
    ("DOC-POL-06", "2.0", "6.4", "REQ-REM-008", "Lost or stolen mobile devices must be reported to IT Security within 1 hour.", "MUST_COMPLETE", True, "Incident Escalation", "Critical", "Day 1"),

    # DOC-POL-07 (Leave & Attendance v2.0)
    ("DOC-POL-07", "2.0", "7.1", "REQ-LEV-005", "Consecutive leave exceeding 10 business days requires Department Director sign-off.", "MUST_COMPLETE", True, "HR Process", "Medium", "Week 2"),
    ("DOC-POL-07", "2.0", "7.2", "REQ-LEV-006", "Unused vacation beyond 5 days is forfeited on April 1 without cash payout.", "MUST_KNOW", True, "PTO Governance", "Medium", "Week 1"),
    ("DOC-POL-07", "2.0", "7.4", "REQ-LEV-007", "Exempt staff must record statutory holidays in the company timekeeping system.", "MUST_COMPLETE", True, "Attendance", "Low", "Day 1"),

    # DOC-POL-08 (Expenses v2.0)
    ("DOC-POL-08", "2.0", "8.1", "REQ-EXP-005", "Receipts in foreign currencies must include official conversion rate documentation.", "MUST_COMPLETE", True, "Expense Auditing", "Medium", "Week 2"),
    ("DOC-POL-08", "2.0", "8.2", "REQ-EXP-006", "Rental car reservations must use standard sedan category unless carrying equipment.", "MUST_KNOW", True, "Travel Policy", "Low", "Week 1"),
    ("DOC-POL-08", "2.0", "8.3", "REQ-EXP-007", "Client entertainment meals require listing all attendees and business topics discussed.", "MUST_COMPLETE", True, "Expense Compliance", "High", "Week 1"),
    ("DOC-POL-08", "2.0", "8.4", "REQ-EXP-008", "Invoices above $10,000 require matching purchase order (PO) before disbursement.", "MUST_DEMONSTRATE", True, "Procurement Control", "Critical", "Day 1"),

    # DOC-POL-09 (Physical Safety)
    ("DOC-POL-09", "1.0", "9.1", "REQ-SAF-004", "Report lost security badges immediately to Facilities for instant badge deactivation.", "MUST_COMPLETE", True, "Access Control", "High", "Day 1"),
    ("DOC-POL-09", "1.0", "9.2", "REQ-SAF-005", "Participate in annual building fire and active emergency evacuation drill.", "MUST_COMPLETE", True, "Safety Drill", "Medium", "First 60 Days"),
    ("DOC-POL-09", "1.0", "9.3", "REQ-SAF-006", "Locate first aid kits and Automated External Defibrillator (AED) stations on each floor.", "MUST_KNOW", True, "Emergency Response", "Low", "Day 1"),

    # DOC-POL-10 (Whistleblower)
    ("DOC-POL-10", "1.0", "10.1", "REQ-WHT-004", "Know that reports can be submitted in local languages across all global operating hubs.", "RECOMMENDED", False, "Global Support", "Low", "Week 1"),
    ("DOC-POL-10", "1.0", "10.2", "REQ-WHT-005", "Whistleblower intake files are encrypted with dual-key access restricted to General Counsel.", "MUST_KNOW", True, "Confidentiality", "Medium", "Week 2"),
    ("DOC-POL-10", "1.0", "10.3", "REQ-WHT-006", "Supervisors must undergo refresher training on retaliation avoidance annually.", "MUST_COMPLETE", True, "Leadership Compliance", "High", "First 30 Days"),

    # DOC-SOP-01 (Incident Response v2.0)
    ("DOC-SOP-01", "2.0", "1.1", "REQ-INC-005", "Establish isolated war room channel with restricted invite-only access during Sev-1.", "MUST_DEMONSTRATE", True, "Incident Communications", "Critical", "Day 1"),
    ("DOC-SOP-01", "2.0", "1.2", "REQ-INC-006", "Executive incident update briefings must be sent every 60 minutes during active Sev-1.", "MUST_COMPLETE", True, "Executive Reporting", "High", "Week 1"),
    ("DOC-SOP-01", "2.0", "1.3", "REQ-INC-007", "Volatile RAM capture must be executed prior to restarting compromised cloud VMs.", "MUST_DEMONSTRATE", True, "Forensics", "Critical", "Week 1"),
    ("DOC-SOP-01", "2.0", "1.4", "REQ-INC-008", "Action items from RCA post-mortems must be logged in Jira with designated owners.", "MUST_COMPLETE", True, "Continuous Improvement", "High", "Week 2"),

    # DOC-SOP-02 (Support Escalation v2.0)
    ("DOC-SOP-02", "2.0", "2.1", "REQ-SUP-005", "Acknowledge customer chat inquiries within 45 seconds during live operating shifts.", "MUST_DEMONSTRATE", True, "Customer Care", "High", "Day 1"),
    ("DOC-SOP-02", "2.0", "2.2", "REQ-SUP-006", "Tag outage tickets with root service impact category (Auth, Billing, Storage, Compute).", "MUST_COMPLETE", True, "Ticket Categorization", "Medium", "Day 1"),
    ("DOC-SOP-02", "2.0", "2.3", "REQ-SUP-007", "Never share tenant diagnostic HAR files containing unredacted cookie sessions.", "MUST_ACKNOWLEDGE", True, "Data Protection", "Critical", "Day 1"),
    ("DOC-SOP-02", "2.0", "2.4", "REQ-SUP-008", "Draft customer root-cause memo within 24 hours of customer outage resolution.", "MUST_DEMONSTRATE", True, "Client Reporting", "High", "Week 2"),

    # DOC-SOP-03 (SSDLC v2.0)
    ("DOC-SOP-03", "2.0", "3.1", "REQ-DEV-005", "Merge commits must follow conventional commit naming standards (feat:, fix:, chore:).", "MUST_DEMONSTRATE", True, "Code Conventions", "Low", "Day 1"),
    ("DOC-SOP-03", "2.0", "3.2", "REQ-DEV-006", "Container base images must be updated monthly to eliminate underlying CVEs.", "MUST_COMPLETE", True, "Container Security", "High", "Week 2"),
    ("DOC-SOP-03", "2.0", "3.3", "REQ-DEV-007", "API endpoints must implement rate limiting and JWT cryptographic validation.", "MUST_DEMONSTRATE", True, "API Security", "Critical", "Week 1"),
    ("DOC-SOP-03", "2.0", "3.4", "REQ-DEV-008", "Integration tests must mock external payment and SMS gateways to prevent test costs.", "RECOMMENDED", False, "Test Architecture", "Low", "Week 2"),

    # DOC-SOP-04 (CAB & Rollback)
    ("DOC-SOP-04", "1.0", "4.1", "REQ-CAB-005", "Change requests must link relevant Jira tickets and rollback verification scripts.", "MUST_COMPLETE", True, "Release Governance", "High", "Week 1"),
    ("DOC-SOP-04", "1.0", "4.2", "REQ-CAB-006", "Database migrations with schema alterations must support backward-compatible reads.", "MUST_DEMONSTRATE", True, "Database Reliability", "Critical", "Week 2"),
    ("DOC-SOP-04", "1.0", "4.3", "REQ-CAB-007", "Automated synthetic canary probes must validate login flow post-deployment.", "MUST_DEMONSTRATE", True, "Synthetic Monitoring", "High", "Week 1"),
    ("DOC-SOP-04", "1.0", "4.4", "REQ-CAB-008", "Hotfix releases deployed outside standard windows require retrospective CAB review.", "MUST_COMPLETE", True, "Change Audit", "Medium", "Week 2"),

    # DOC-SOP-05 (Data Analytics & BI)
    ("DOC-SOP-05", "2.0", "5.1", "REQ-DAT-005", "Scheduled cron ETL pipelines must include idempotency check to avoid duplicate inserts.", "MUST_DEMONSTRATE", True, "Data Pipelines", "High", "Week 1"),
    ("DOC-SOP-05", "2.0", "5.2", "REQ-DAT-006", "Query results exceeding 100,000 rows must write to secured cloud storage buckets.", "MUST_DEMONSTRATE", True, "Warehouse Scaling", "Medium", "Week 2"),
    ("DOC-SOP-05", "2.0", "5.3", "REQ-DAT-007", "Customer email addresses in BI dashboard exports must be SHA-256 hashed.", "MUST_COMPLETE", True, "Anonymization", "Critical", "Day 1"),
    ("DOC-SOP-05", "2.0", "5.4", "REQ-DAT-008", "Data governance review must evaluate vendor data security certifications (SOC2).", "MUST_KNOW", True, "Vendor Risk", "High", "First 30 Days"),

    # DOC-SOP-06 (Sales Contracting)
    ("DOC-SOP-06", "1.0", "6.1", "REQ-SLS-005", "Multi-year enterprise contracts must include annual payment escalation clauses.", "MUST_DEMONSTRATE", True, "Contract Structuring", "High", "Week 2"),
    ("DOC-SOP-06", "1.0", "6.2", "REQ-SLS-006", "Store countersigned NDAs in the enterprise Ironclad legal contract repository.", "MUST_COMPLETE", True, "Legal Filing", "Medium", "Day 1"),
    ("DOC-SOP-06", "1.0", "6.3", "REQ-SLS-007", "Any commitment to custom SLA uptime >99.9% requires VP Engineering approval.", "MUST_KNOW", True, "SLA Governance", "Critical", "Week 1"),
    ("DOC-SOP-06", "1.0", "6.4", "REQ-SLS-008", "Verify customer creditworthiness through Dun & Bradstreet report before Net 60 terms.", "MUST_DEMONSTRATE", True, "Credit Risk", "Medium", "Week 2"),

    # DOC-SOP-07 (HR Onboarding & Offboarding)
    ("DOC-SOP-07", "1.0", "7.1", "REQ-HR-005", "Coordinate Day-1 welcome buddy assignment with hiring manager.", "MUST_COMPLETE", True, "Employee Experience", "Medium", "Day 1"),
    ("DOC-SOP-07", "1.0", "7.2", "REQ-HR-006", "Send automated compliance reminders on Day 7 and Day 12 to incomplete learners.", "MUST_DEMONSTRATE", True, "Compliance Tracking", "High", "Week 1"),
    ("DOC-SOP-07", "1.0", "7.3", "REQ-HR-007", "Verify cloud directory deprovisioning audit log is signed off within 24 hours.", "MUST_COMPLETE", True, "Offboarding Audit", "Critical", "Week 1"),
    ("DOC-SOP-07", "1.0", "7.4", "REQ-HR-008", "Conduct structured exit interviews for voluntary departures and log feedback.", "MUST_COMPLETE", True, "People Analytics", "Low", "First 30 Days"),

    # DOC-SOP-08 (IT Provisioning)
    ("DOC-SOP-08", "1.0", "8.1", "REQ-OPS-005", "Apply tamper-evident physical barcode asset tags to corporate laptops.", "MUST_COMPLETE", True, "Physical Asset Tracking", "Medium", "Day 1"),
    ("DOC-SOP-08", "1.0", "8.2", "REQ-OPS-006", "Perform quarterly random physical audit of 10% of campus hardware assets.", "MUST_DEMONSTRATE", True, "Asset Auditing", "Medium", "First 60 Days"),
    ("DOC-SOP-08", "1.0", "8.3", "REQ-OPS-007", "Maintain digital certificates of destruction for retired server storage drives.", "MUST_COMPLETE", True, "Disposal Compliance", "Critical", "Week 1"),
    ("DOC-SOP-08", "1.0", "8.4", "REQ-OPS-008", "Wipe and re-image loaner laptops immediately upon return from employee travel.", "MUST_DEMONSTRATE", True, "Fleet Hygiene", "High", "Week 1"),

    # DOC-HDB-01 (Handbook)
    ("DOC-HDB-01", "1.0", "HDB-1.2", "REQ-HDB-005", "Notify team members via Slack channel if taking unscheduled midday appointments.", "RECOMMENDED", False, "Collaboration", "Low", "Day 1"),
    ("DOC-HDB-01", "1.0", "HDB-1.3", "REQ-HDB-006", "Obtain manager pre-approval before booking educational conference registrations.", "MUST_COMPLETE", True, "Training Stipend", "Medium", "Week 2"),
    ("DOC-HDB-01", "1.0", "HDB-1.4", "REQ-HDB-007", "Observe professional camera-on etiquette during customer facing videoconferences.", "RECOMMENDED", False, "Professionalism", "Low", "Day 1"),

    # DOC-ROLE-01 (Role descriptions)
    ("DOC-ROLE-01", "1.0", "ROL-1.1", "REQ-ROL-011", "Security Analysts must review CVE database daily for newly published zero-days.", "MUST_DEMONSTRATE", True, "Threat Intelligence", "High", "Day 1"),
    ("DOC-ROLE-01", "1.0", "ROL-1.2", "REQ-ROL-012", "Customer Support staff must maintain a CSAT satisfaction rating above 92%.", "MUST_DEMONSTRATE", True, "Performance Metrics", "High", "First 30 Days"),
    ("DOC-ROLE-01", "1.0", "ROL-1.3", "REQ-ROL-013", "Software Support engineers must participate in weekly bug triage rotation.", "MUST_COMPLETE", True, "Triage Rotation", "High", "Week 1"),
    ("DOC-ROLE-01", "1.0", "ROL-1.4", "REQ-ROL-014", "Data Analysts must document column lineages in the corporate data catalog.", "MUST_DEMONSTRATE", True, "Data Lineage", "Medium", "Week 2"),
    ("DOC-ROLE-01", "1.0", "ROL-1.5", "REQ-ROL-015", "Sales Executives must achieve 100% adherence to corporate pricing minimums.", "MUST_DEMONSTRATE", True, "Pricing Governance", "Critical", "Week 1"),
    ("DOC-ROLE-01", "1.0", "ROL-1.6", "REQ-ROL-016", "HR Executives must audit personnel records for I-9 / right-to-work completeness.", "MUST_DEMONSTRATE", True, "Labor Compliance", "Critical", "Day 1"),
    ("DOC-ROLE-01", "1.0", "ROL-1.7", "REQ-ROL-017", "Finance Associates must complete monthly bank reconciliation within 3 business days.", "MUST_DEMONSTRATE", True, "Financial Close", "High", "Week 2"),
    ("DOC-ROLE-01", "1.0", "ROL-1.8", "REQ-ROL-018", "Operations Coordinators must track UPS/FedEx hardware tracking numbers in Jira.", "MUST_COMPLETE", True, "Logistics", "Low", "Day 1"),
    ("DOC-ROLE-01", "1.0", "ROL-1.9", "REQ-ROL-019", "Marketing Executives must audit email lists for unsubscription compliance (CAN-SPAM).", "MUST_DEMONSTRATE", True, "Marketing Privacy", "High", "Week 1"),
    ("DOC-ROLE-01", "1.0", "ROL-1.10", "REQ-ROL-020", "Team Leads must conduct weekly 1-on-1 career development check-ins with team.", "MUST_COMPLETE", True, "People Management", "Medium", "Week 1")
]

# Fetch document and version mappings
doc_lookup = {d.doc_code: d.id for d in db.query(models.Document).all()}
ver_lookup = {}
for v in db.query(models.DocumentVersion).all():
    doc = db.query(models.Document).filter(models.Document.id == v.document_id).first()
    if doc:
        ver_lookup[(doc.doc_code, v.version_str)] = v.id

added_count = 0
for d_code, v_str, s_id, r_code, text, cat, mand, comp, prio, stg in ADDITIONAL_REQS:
    # Check if exists
    existing = db.query(models.Requirement).filter(models.Requirement.req_code == r_code).first()
    if not existing:
        d_id = doc_lookup.get(d_code)
        v_id = ver_lookup.get((d_code, v_str))
        if d_id and v_id:
            req = models.Requirement(
                req_code=r_code,
                document_id=d_id,
                version_id=v_id,
                section_id=s_id,
                requirement_text=text,
                category=cat,
                is_mandatory=mand,
                competency=comp,
                default_priority=prio,
                default_due_stage=stg
            )
            db.add(req)
            added_count += 1

db.commit()

# Also map newly added requirements into Role Requirements Matrix
roles = db.query(models.Role).all()
new_reqs = db.query(models.Requirement).all()
total_now = len(new_reqs)
print(f"Added {added_count} new requirements. Total requirements in database: {total_now}")

# Add role mappings for new requirements
mappings_added = 0
for r in new_reqs:
    # Check if mapped to any role
    exists_mapping = db.query(models.RoleRequirement).filter(models.RoleRequirement.requirement_id == r.id).first()
    if not exists_mapping:
        # Determine roles based on prefix
        assigned_roles = []
        if "SEC" in r.req_code or "ACC" in r.req_code or "INC" in r.req_code:
            assigned_roles = ["SEC_ANALYST", "SOFT_ENG", "TEAM_LEAD"]
        elif "PRIV" in r.req_code or "DAT" in r.req_code:
            assigned_roles = ["DATA_ANALYST", "SEC_ANALYST", "CUST_SUPPORT"]
        elif "USE" in r.req_code or "REM" in r.req_code or "ETH" in r.req_code or "LEV" in r.req_code or "SAF" in r.req_code or "WHT" in r.req_code or "HDB" in r.req_code:
            assigned_roles = [role.code for role in roles] # all roles
        elif "EXP" in r.req_code:
            assigned_roles = ["FIN_ASSOC", "SALES_EXEC", "TEAM_LEAD"]
        elif "SUP" in r.req_code:
            assigned_roles = ["CUST_SUPPORT", "SOFT_ENG"]
        elif "DEV" in r.req_code or "CAB" in r.req_code:
            assigned_roles = ["SOFT_ENG", "TEAM_LEAD"]
        elif "SLS" in r.req_code:
            assigned_roles = ["SALES_EXEC", "MKT_EXEC"]
        elif "HR" in r.req_code:
            assigned_roles = ["HR_EXEC", "TEAM_LEAD"]
        elif "OPS" in r.req_code:
            assigned_roles = ["OPS_COORD", "SOFT_ENG"]
        elif "ROL" in r.req_code:
            # Map ROL specifically
            num = int(r.req_code.replace("REQ-ROL-", ""))
            role_idx = (num - 1) % len(roles)
            assigned_roles = [roles[role_idx].code]
        else:
            assigned_roles = [roles[0].code]

        for role_code in assigned_roles:
            role_obj = db.query(models.Role).filter(models.Role.code == role_code).first()
            if role_obj:
                rr = models.RoleRequirement(
                    role_id=role_obj.id,
                    requirement_id=r.id,
                    is_mandatory=r.is_mandatory,
                    priority=r.default_priority,
                    due_stage=r.default_due_stage,
                    specific_instructions=f"Enforce compliance for {role_code}."
                )
                db.add(rr)
                mappings_added += 1

db.commit()
total_mappings = db.query(models.RoleRequirement).count()
print(f"Added {mappings_added} new role-requirement mappings. Total mappings: {total_mappings}")
db.close()

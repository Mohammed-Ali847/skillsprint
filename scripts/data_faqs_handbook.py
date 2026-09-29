# scripts/data_faqs_handbook.py
from scripts.catalog_builder_core import make_doc

FAQS_AND_HANDBOOKS = [
    make_doc(
        "DOC-FAQ-01", "IT Security & Password Management Employee FAQ", "FAQ", "CYBER_SEC", "pdf", "1.0", 3,
        v1_sections=[
            {"id": "FAQ-1.1", "heading": "Q: How often must I change my password?", "content": "A: Passwords expire every 180 days according to legacy helpdesk tips. (Note: This is an informal FAQ clause that contradicts DOC-POL-01 v2.0 which mandates 90-day rotation; policy precedence must resolve in favor of the policy)."},
            {"id": "FAQ-1.2", "heading": "Q: Can I use personal SMS for multi-factor authentication?", "content": "A: Many employees set up SMS codes on their phone during orientation. (Note: Contradicts DOC-POL-01 v2.0 requiring FIDO2 or app-based authenticator)."},
            {"id": "FAQ-1.3", "heading": "Q: What should I do if my screen locks while presenting?", "content": "A: You can temporarily disable auto-lock during client meetings for up to 30 minutes using the presentation utility."}
        ],
        v1_summary="Helpdesk employee FAQ containing common answers and informal legacy tips.",
        reqs=[
            {"code": "REQ-FAQ1-001", "sec": "FAQ-1.3", "text": "Know how to use presentation mode during client presentations without leaving desk.", "cat": "RECOMMENDED", "mandatory": False, "competency": "IT Tips", "priority": "Low", "stage": "Week 2"}
        ]
    ),
    make_doc(
        "DOC-FAQ-02", "Customer Support Operations & Refund Handling FAQ", "FAQ", "CUST_OPS", "docx", "1.0", 3,
        v1_sections=[
            {"id": "FAQ-2.1", "heading": "Q: How quickly must Priority 1 outages be escalated?", "content": "A: Customer support agents typically escalate P1 tickets to engineering within 30 minutes if initial diagnostics fail. (Note: Contradicts DOC-SOP-02 which strictly mandates a 15-minute escalation SLA)."},
            {"id": "FAQ-2.2", "heading": "Q: Can support agents issue customer billing refunds?", "content": "A: Support executives can approve customer courtesy credits up to $500 if the customer is dissatisfied. (Note: Contradicts DOC-SOP-02 which caps frontline support credits at $150)."},
            {"id": "FAQ-2.3", "heading": "Q: Where can I look up customer SLA entitlements?", "content": "A: Check the Salesforce Service Cloud Entitlements tab on the account record."}
        ],
        v1_summary="Support operations FAQ with informal escalation guidelines and tips.",
        reqs=[
            {"code": "REQ-FAQ2-001", "sec": "FAQ-2.3", "text": "Locate customer SLA tier and contractual entitlements in Salesforce Service Cloud.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Support Tools", "priority": "High", "stage": "Day 1"}
        ]
    ),
    make_doc(
        "DOC-FAQ-03", "Remote Work & Local Data Caching FAQ", "FAQ", "DATA_AI", "pdf", "1.0", 3,
        v1_sections=[
            {"id": "FAQ-3.1", "heading": "Q: Can I download CSV data to my laptop to analyze in Excel?", "content": "A: If your home internet connection is slow, you can save report CSVs on your desktop for faster formulas. (Note: Contradicts DOC-POL-02 and DOC-SOP-05 which strictly prohibit unencrypted local PII data storage)."},
            {"id": "FAQ-3.2", "heading": "Q: Which browser is recommended for cloud analytics portals?", "content": "A: Google Chrome or Microsoft Edge with enterprise sync enabled are the supported corporate browsers."}
        ],
        v1_summary="Informal remote data analysis FAQ.",
        reqs=[
            {"code": "REQ-FAQ3-001", "sec": "FAQ-3.2", "text": "Use approved enterprise browsers (Chrome/Edge) with enterprise profile sync.", "cat": "RECOMMENDED", "mandatory": False, "competency": "Browser Hygiene", "priority": "Low", "stage": "Day 1"}
        ]
    ),
    make_doc(
        "DOC-HDB-01", "ApexNova Employee Handbook & Culture Manifesto", "HANDBOOK", "HR_PEOPLE", "pdf", "1.0", 4,
        v1_sections=[
            {"id": "HDB-1.1", "heading": "Welcome to ApexNova: Mission and Core Values", "content": "Welcome to the team! Our four core pillars are: Relentless Innovation, Radical Transparency, Uncompromising Integrity, and Customer Obsession. We empower every employee to speak up, act with urgency, and foster inclusive teamwork."},
            {"id": "HDB-1.2", "heading": "Core Working Hours & Flexible Schedules", "content": "Core collaboration hours are 10:00 AM to 4:00 PM in your respective hub time zone. Flexible arrangements can be coordinated with your direct manager."},
            {"id": "HDB-1.3", "heading": "Professional Development & Learning Stipend", "content": "Full-time employees are eligible for an annual $1,500 USD learning stipend to pursue industry certifications (AWS, CISSP, PMP) and educational conferences."},
            {"id": "HDB-1.4", "heading": "Dress Code & Workplace Presentation", "content": "ApexNova maintains a business-casual dress environment for office presence and customer-facing video conferences."}
        ],
        v1_summary="Comprehensive employee handbook covering culture, core values, working hours, and $1,500 training stipend.",
        reqs=[
            {"code": "REQ-HDB-001", "sec": "HDB-1.1", "text": "Review ApexNova four core cultural pillars and mission statement.", "cat": "MUST_ACKNOWLEDGE", "mandatory": True, "competency": "Company Culture", "priority": "High", "stage": "Day 1"},
            {"code": "REQ-HDB-002", "sec": "HDB-1.2", "text": "Observe core collaboration hours (10 AM - 4 PM local hub time).", "cat": "MUST_KNOW", "mandatory": True, "competency": "Attendance Standards", "priority": "Medium", "stage": "Day 1"},
            {"code": "REQ-HDB-003", "sec": "HDB-1.3", "text": "Explore available annual $1,500 professional development certification benefits.", "cat": "OPTIONAL", "mandatory": False, "competency": "Career Growth", "priority": "Low", "stage": "First 60 Days"},
            {"code": "REQ-HDB-004", "sec": "HDB-1.4", "text": "Maintain business casual standards for customer-facing meetings.", "cat": "RECOMMENDED", "mandatory": False, "competency": "Professionalism", "priority": "Low", "stage": "Day 1"}
        ]
    ),
    make_doc(
        "DOC-ROLE-01", "Comprehensive Role Descriptions & Competency Framework Guide", "ROLE_DESCRIPTION", "HR_PEOPLE", "docx", "1.0", 1,
        v1_sections=[
            {"id": "ROL-1.1", "heading": "Information Security Analyst Competencies", "content": "Must master SIEM analysis (Splunk), threat triage, vulnerability scanning, and incident response SOPs. Responsible for reviewing access tickets and enforcing enterprise security policies."},
            {"id": "ROL-1.2", "heading": "Customer Support Executive Competencies", "content": "Must master Zendesk/Salesforce Service Cloud, client SLA verification, identity authentication protocols, and escalation paths for P1 outages."},
            {"id": "ROL-1.3", "heading": "Software Support Engineer Competencies", "content": "Must understand Git branch workflows, pull request review requirements, CI/CD pipeline troubleshooting, and zero-defect SAST policy adherence."},
            {"id": "ROL-1.4", "heading": "Data Analyst Competencies", "content": "Must master SQL, data masking techniques, secure cloud analytics notebooks, and privacy regulation requirements (GDPR/CCPA)."},
            {"id": "ROL-1.5", "heading": "Commercial Sales Executive Competencies", "content": "Must master CRM pipeline hygiene, enterprise discount matrix, mutual NDA execution, and anti-bribery gift registry rules."},
            {"id": "ROL-1.6", "heading": "HR Executive Competencies", "content": "Must master new hire onboarding lifecycle, compliance training verification, and 1-hour access revocation for departures."},
            {"id": "ROL-1.7", "heading": "Finance Associate Competencies", "content": "Must master Concur expense auditing, 14-day receipt compliance, per diem enforcement, and financial approval thresholds."},
            {"id": "ROL-1.8", "heading": "Operations Coordinator Competencies", "content": "Must master endpoint imaging, asset tracking in Snipe-IT, full-disk encryption validation, and NIST 800-88 sanitization."},
            {"id": "ROL-1.9", "heading": "Marketing Executive Competencies", "content": "Must master customer opt-in consent verification, brand guidelines, and copyright clearance for all corporate public materials."},
            {"id": "ROL-1.10", "heading": "Engineering Team Leader Competencies", "content": "Must master agile delivery, dual code review governance, Change Advisory Board (CAB) requests, and quarterly access recertifications."}
        ],
        v1_summary="Foundational role definitions and required core competencies across all 10 standard job functions.",
        reqs=[
            {"code": "REQ-ROL-001", "sec": "ROL-1.1", "text": "Master SIEM telemetry, threat triage, and access ticket reviews.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Security Monitoring", "priority": "Critical", "stage": "Week 1"},
            {"code": "REQ-ROL-002", "sec": "ROL-1.2", "text": "Master Zendesk ticket lifecycle, identity checks, and SLA triage.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Customer Support", "priority": "Critical", "stage": "Day 1"},
            {"code": "REQ-ROL-003", "sec": "ROL-1.3", "text": "Master Git workflows, PR dual review process, and CI/CD troubleshooting.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Platform Support", "priority": "High", "stage": "Week 1"},
            {"code": "REQ-ROL-004", "sec": "ROL-1.4", "text": "Master SQL query optimization, data masking, and privacy rules.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Analytics & Privacy", "priority": "High", "stage": "Week 1"},
            {"code": "REQ-ROL-005", "sec": "ROL-1.5", "text": "Master Salesforce deal updates, NDA execution, and discount governance.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Sales Operations", "priority": "Critical", "stage": "Day 1"},
            {"code": "REQ-ROL-006", "sec": "ROL-1.6", "text": "Master employee onboarding, compliance tracking, and offboarding SLAs.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "HR Operations", "priority": "High", "stage": "Week 1"},
            {"code": "REQ-ROL-007", "sec": "ROL-1.7", "text": "Master Concur audit workflows, per diem checks, and financial limits.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Expense Auditing", "priority": "High", "stage": "Day 1"},
            {"code": "REQ-ROL-008", "sec": "ROL-1.8", "text": "Master laptop provisioning, EDR agent verification, and asset tracking.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "IT Operations", "priority": "High", "stage": "Day 1"},
            {"code": "REQ-ROL-009", "sec": "ROL-1.9", "text": "Master opt-in consent marketing guidelines and brand asset policies.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Marketing Compliance", "priority": "High", "stage": "Week 1"},
            {"code": "REQ-ROL-010", "sec": "ROL-1.10", "text": "Master CAB change submissions, dual review signoffs, and access audits.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Engineering Leadership", "priority": "Critical", "stage": "Week 1"}
        ]
    )
]

print(f"Loaded {len(FAQS_AND_HANDBOOKS)} FAQs, handbooks, and role competency guides.")

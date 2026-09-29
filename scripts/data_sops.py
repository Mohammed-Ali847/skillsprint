# scripts/data_sops.py
from scripts.catalog_builder_core import make_doc

SOPS = [
    make_doc(
        "DOC-SOP-01", "Incident Response, Triage & Breach Notification SOP", "SOP", "CYBER_SEC", "pdf", "2.0", 2,
        v1_sections=[
            {"id": "1.1", "heading": "Legacy Severity 1 Reporting", "content": "Critical incidents were reported to leadership within 24 hours of confirmation."}
        ],
        v1_summary="24-hour breach notification SLA for Sev-1 incidents.",
        v2_sections=[
            {"id": "1.1", "heading": "Incident Severity Classification", "content": "Incidents are classified from Severity 1 (Critical data breach or total platform outage) to Severity 4 (Minor cosmetic bug). Sev-1 requires immediate incident commander assignment."},
            {"id": "1.2", "heading": "4-Hour Critical Breach Notification SLA", "content": "Upon confirmation of a Severity 1 cybersecurity breach involving customer records, the Incident Commander must notify the CISO and Data Protection Officer within 4 hours."},
            {"id": "1.3", "heading": "Evidence Preservation & Chain of Custody", "content": "Memory dumps, system audit logs, and network capture packets must be cryptographically hashed and copied to isolated forensic storage with documented chain of custody."},
            {"id": "1.4", "heading": "Post-Incident Root Cause Analysis (RCA)", "content": "A blameless Post-Mortem and formal RCA report must be published within 5 business days of incident resolution."}
        ],
        v2_summary="Shortened Sev-1 breach reporting from 24h to 4h, strict forensic chain of custody, and 5-day RCA report SLA.",
        reqs=[
            {"code": "REQ-INC-001", "sec": "1.1", "text": "Classify incident severity levels correctly and escalate Sev-1/Sev-2 to Incident Commander.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Incident Triage", "priority": "Critical", "stage": "Day 1"},
            {"code": "REQ-INC-002", "sec": "1.2", "text": "Report confirmed Sev-1 critical data breaches to CISO/DPO within 4 hours.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Breach Response", "priority": "Critical", "stage": "Day 1"},
            {"code": "REQ-INC-003", "sec": "1.3", "text": "Preserve forensic evidence with cryptographic hashes and maintain chain of custody.", "cat": "MUST_KNOW", "mandatory": True, "competency": "Forensics", "priority": "High", "stage": "Week 1"},
            {"code": "REQ-INC-004", "sec": "1.4", "text": "Publish blameless RCA document within 5 business days following incident closure.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Post-Mortem", "priority": "Medium", "stage": "Week 2"}
        ]
    ),
    make_doc(
        "DOC-SOP-02", "Customer Ticket Escalation & SLA Management SOP", "SOP", "CUST_OPS", "docx", "2.0", 2,
        v1_sections=[
            {"id": "2.1", "heading": "Legacy P1 Response SLA", "content": "Priority 1 tickets required response within 30 minutes and allowed frontline refund approvals up to $500."}
        ],
        v1_summary="30-min P1 response SLA and high frontline refund limit.",
        v2_sections=[
            {"id": "2.1", "heading": "Ticket Priority Triage & Response SLAs", "content": "Customer tickets are triaged into P1 (Urgent/System Down: 15-minute response SLA), P2 (High/Degraded: 1-hour SLA), P3 (Normal: 4-hour SLA), and P4 (Low: 24-hour SLA)."},
            {"id": "2.2", "heading": "15-Minute Escalation Threshold for P1", "content": "If a P1 customer outage ticket is unresolved after 15 minutes, it must be automatically escalated to Engineering Duty Lead and Customer Success Director."},
            {"id": "2.3", "heading": "Customer Identity Verification Protocol", "content": "Before modifying tenant configurations, releasing diagnostic logs, or resetting MFA, Support Executives must authenticate customer caller identity via cryptographic one-time security PIN."},
            {"id": "2.4", "heading": "Customer Concession & Refund Authority Limits", "content": "Support Executives may authorize billing credits or refunds up to $150 USD. Credits between $150 and $1,000 require Finance Associate review; amounts above $1,000 require VP approval."}
        ],
        v2_summary="P1 response tightened to 15 min, mandatory security PIN caller verification, and $150 frontline refund limit.",
        reqs=[
            {"code": "REQ-SUP-001", "sec": "2.1", "text": "Triage tickets and meet the 15-minute response SLA for Priority 1 urgent tickets.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "SLA Management", "priority": "Critical", "stage": "Day 1"},
            {"code": "REQ-SUP-002", "sec": "2.2", "text": "Escalate unresolved P1 outages to Engineering Duty Lead within 15 minutes.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Escalation", "priority": "Critical", "stage": "Day 1"},
            {"code": "REQ-SUP-003", "sec": "2.3", "text": "Verify customer identity via cryptographic security PIN before account modifications.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Customer Verification", "priority": "Critical", "stage": "Day 1"},
            {"code": "REQ-SUP-004", "sec": "2.4", "text": "Enforce $150 maximum frontline refund limit; escalate higher amounts to Finance.", "cat": "MUST_KNOW", "mandatory": True, "competency": "Billing Governance", "priority": "High", "stage": "Week 1"}
        ]
    ),
    make_doc(
        "DOC-SOP-03", "Secure Software Development Lifecycle (SSDLC) & Code Review SOP", "SOP", "ENG_DEV", "pdf", "2.0", 2,
        v1_sections=[
            {"id": "3.1", "heading": "Legacy Single Approver Merge", "content": "Pull requests could be merged with a single peer approval."}
        ],
        v1_summary="Single peer review approval without automated SAST blocking.",
        v2_sections=[
            {"id": "3.1", "heading": "Branch Protection & Dual Peer Review", "content": "Direct pushes to main/master branches are disabled. Every pull request requires at least two approved reviews from senior engineers before merge eligibility."},
            {"id": "3.2", "heading": "Automated Static Security Testing (SAST) Gates", "content": "CI/CD pipelines enforce automated SAST and dependency vulnerability scans (Snyk/SonarQube). Merges are blocked if any Critical or High security flaws are detected."},
            {"id": "3.3", "heading": "Secret Scanning & Credential Exposure", "content": "Pre-commit git hooks block commits containing API keys, private certificates, or database credentials. Exposed tokens trigger immediate credential invalidation."},
            {"id": "3.4", "heading": "Unit & Integration Test Coverage Threshold", "content": "All new code additions must maintain a minimum 80% automated unit and integration test coverage."}
        ],
        v2_summary="Dual peer reviews required, zero Critical/High SAST flaws allowed, pre-commit secret scanning, and 80% test coverage minimum.",
        reqs=[
            {"code": "REQ-DEV-001", "sec": "3.1", "text": "Ensure pull requests obtain two independent senior code reviews before merging.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Code Quality", "priority": "High", "stage": "Day 1"},
            {"code": "REQ-DEV-002", "sec": "3.2", "text": "Resolve all Critical and High SAST vulnerability warnings prior to code merge.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Secure Coding", "priority": "Critical", "stage": "Week 1"},
            {"code": "REQ-DEV-003", "sec": "3.3", "text": "Install and maintain pre-commit secret detection hooks to prevent credential leaks.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Secret Hygiene", "priority": "High", "stage": "Day 1"},
            {"code": "REQ-DEV-004", "sec": "3.4", "text": "Author automated tests achieving at least 80% coverage on new feature code.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Testing Standards", "priority": "Medium", "stage": "Week 2"}
        ]
    ),
    make_doc(
        "DOC-SOP-04", "Production Deployment, Change Advisory Board (CAB) & Rollback SOP", "SOP", "ENG_DEV", "docx", "1.0", 2,
        v1_sections=[
            {"id": "4.1", "heading": "Standard & Emergency CAB Approval", "content": "All production software deployments require a submitted Change Request (CR) approved by the Change Advisory Board (CAB) at least 24 hours prior to release window. Emergency hotfixes require dual sign-off from VP Engineering and Director of SecOps."},
            {"id": "4.2", "heading": "Automated Canary Deployment Strategy", "content": "Deployments must proceed via canary rollout: 5% traffic for 30 minutes, 25% for 1 hour, and 100% only if error budget degradation remains below 0.05%."},
            {"id": "4.3", "heading": "Automated Rollback Criteria", "content": "If p99 latency spikes by >25% or 5xx server error rate exceeds 0.1%, automated deployment orchestrators trigger an immediate rollback to the previous stable release artifact."},
            {"id": "4.4", "heading": "Deployment Blackout Windows", "content": "No standard production deployments are permitted on Fridays after 14:00 UTC or during major global peak retail holidays without explicit CTO exemption."}
        ],
        v1_summary="Formal CAB change control, 3-stage canary releases, automated rollback thresholds, and Friday afternoon deployment blackouts.",
        reqs=[
            {"code": "REQ-CAB-001", "sec": "4.1", "text": "Submit CAB Change Request 24h prior to deployment; obtain dual approval for hotfixes.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Change Management", "priority": "High", "stage": "Week 1"},
            {"code": "REQ-CAB-002", "sec": "4.2", "text": "Execute production deployments using canary stages (5%, 25%, 100%) with health checks.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Release Engineering", "priority": "High", "stage": "Week 2"},
            {"code": "REQ-CAB-003", "sec": "4.3", "text": "Trigger immediate automated rollback if 5xx errors exceed 0.1% or latency surges >25%.", "cat": "MUST_KNOW", "mandatory": True, "competency": "Site Reliability", "priority": "Critical", "stage": "Day 1"},
            {"code": "REQ-CAB-004", "sec": "4.4", "text": "Respect Friday deployment blackouts unless written CTO emergency waiver is granted.", "cat": "MUST_ACKNOWLEDGE", "mandatory": True, "competency": "Operational Discipline", "priority": "Medium", "stage": "Day 1"}
        ]
    ),
    make_doc(
        "DOC-SOP-05", "Data Analytics, BI Reporting & Data Export SOP", "SOP", "DATA_AI", "pdf", "2.0", 2,
        v1_sections=[
            {"id": "5.1", "heading": "Legacy Data Exports", "content": "Analysts were permitted to download CSV extracts to local desktop computers for rapid analysis."}
        ],
        v1_summary="Allowed CSV downloads to local employee workstations.",
        v2_sections=[
            {"id": "5.1", "heading": "BI Query Optimization & Resource Caps", "content": "All analytical queries against BigQuery and PostgreSQL warehouses must include partition filters. Ad-hoc queries scanning over 500GB of telemetry require Data Engineering approval."},
            {"id": "5.2", "heading": "Strict Ban on Local Unencrypted Data Dumps", "content": "Downloading unencrypted raw customer datasets or CSV files to local desktop or laptop drives is strictly prohibited. Analysis must occur within secure cloud analytics notebooks."},
            {"id": "5.3", "heading": "Mandatory Data Masking in BI Dashboards", "content": "Credit card numbers, bank routing codes, tax identifiers, and passwords must be irreversibly hashed or masked (e.g. ****-****-1234) before rendering on executive BI dashboards."},
            {"id": "5.4", "heading": "Third-Party Data Sharing Sign-off", "content": "Sharing any analytical data extracts with third-party vendors requires formal sign-off from the Data Governance Board and Legal."}
        ],
        v2_summary="Prohibited local unencrypted CSV exports, enforced partition filters, mandatory PII masking, and vendor sharing sign-off.",
        reqs=[
            {"code": "REQ-DAT-001", "sec": "5.1", "text": "Apply partition filters on warehouse queries to prevent excessive compute scans.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Query Optimization", "priority": "Medium", "stage": "Week 1"},
            {"code": "REQ-DAT-002", "sec": "5.2", "text": "Conduct analytical workflows inside secure cloud notebooks without local file exports.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Data Security", "priority": "Critical", "stage": "Day 1"},
            {"code": "REQ-DAT-003", "sec": "5.3", "text": "Ensure all sensitive fields (tax IDs, card numbers) are masked on BI dashboards.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Data Masking", "priority": "High", "stage": "Week 1"},
            {"code": "REQ-DAT-004", "sec": "5.4", "text": "Secure Data Governance Board approval before providing data extracts to vendors.", "cat": "MUST_ACKNOWLEDGE", "mandatory": True, "competency": "Governance", "priority": "High", "stage": "Week 2"}
        ]
    ),
    make_doc(
        "DOC-SOP-06", "Sales Contracting, Enterprise Discounting & Deal Approval SOP", "SOP", "COMM_SALES", "docx", "1.0", 2,
        v1_sections=[
            {"id": "6.1", "heading": "Enterprise Discounting Matrix", "content": "Sales Executives may grant discounts up to 10% on list price. Discounts from 11% to 20% require Sales Director approval. Discounts exceeding 20% require VP Sales and CFO authorization."},
            {"id": "6.2", "heading": "Mandatory Non-Disclosure Agreements (NDA)", "content": "Before discussing product roadmaps or architectural internals with prospective customers, an executed mutual ApexNova NDA must be on file."},
            {"id": "6.3", "heading": "Standard Terms of Service and Master Services Agreement (MSA)", "content": "Modifications to standard indemnification, liability caps, or warranty clauses in customer MSAs must be formally reviewed and approved by Corporate Legal."},
            {"id": "6.4", "heading": "CRM Opportunity Record Completeness", "content": "Sales Executives must record deal stages, close dates, key stakeholders, and procurement timelines in Salesforce within 2 business days of customer meetings."}
        ],
        v1_summary="Tiered discounting approval (10% self, 20% Director, >20% VP/CFO), mandatory NDAs, and Legal contract review.",
        reqs=[
            {"code": "REQ-SLS-001", "sec": "6.1", "text": "Adhere to the Discounting Authority Matrix when drafting customer proposals.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Deal Structuring", "priority": "Critical", "stage": "Day 1"},
            {"code": "REQ-SLS-002", "sec": "6.2", "text": "Verify an executed mutual NDA is logged before sharing technical roadmaps.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Commercial Legal", "priority": "High", "stage": "Day 1"},
            {"code": "REQ-SLS-003", "sec": "6.3", "text": "Route customer redlines on liability or SLA clauses to Legal for review.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Contract Governance", "priority": "High", "stage": "Week 1"},
            {"code": "REQ-SLS-004", "sec": "6.4", "text": "Maintain updated CRM opportunity records within 2 business days of meetings.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "CRM Discipline", "priority": "Medium", "stage": "Week 1"}
        ]
    ),
    make_doc(
        "DOC-SOP-07", "Employee Onboarding, Offboarding & Identity Lifecycle SOP", "SOP", "HR_PEOPLE", "pdf", "1.0", 2,
        v1_sections=[
            {"id": "7.1", "heading": "New Hire Pre-Boarding & Day-1 Setup", "content": "HR must verify background check clearance, sign offer letter, and dispatch IT hardware request at least 5 business days prior to employee start date. On Day 1, HR provides orientation and policy review."},
            {"id": "7.2", "heading": "Mandatory Compliance Training Window", "content": "New hires must complete Information Security Basics, Workplace Harassment, and Code of Conduct training within their first 14 calendar days of employment."},
            {"id": "7.3", "heading": "Voluntary & Involuntary Offboarding SLA", "content": "Upon notice of employee termination, IT and Security must revoke all single sign-on, VPN, and physical badge access immediately (within 1 hour for involuntary, within 24 hours for voluntary)."},
            {"id": "7.4", "heading": "Hardware Recovery & Asset Reconciliation", "content": "Corporate equipment (laptops, badges, monitors) must be returned to IT Operations within 7 business days of departure."}
        ],
        v1_summary="5-day pre-boarding hardware SLA, 14-day mandatory training completion, 1-hour access revocation for involuntary offboarding.",
        reqs=[
            {"code": "REQ-HR-001", "sec": "7.1", "text": "Execute pre-boarding checklist and dispatch IT equipment request 5 days prior to start.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "HR Operations", "priority": "High", "stage": "Day 1"},
            {"code": "REQ-HR-002", "sec": "7.2", "text": "Verify new hires finish mandatory compliance modules within their first 14 days.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Compliance Tracking", "priority": "Critical", "stage": "Week 2"},
            {"code": "REQ-HR-003", "sec": "7.3", "text": "Trigger identity access revocation within 1 hour of involuntary employee departure.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Security Offboarding", "priority": "Critical", "stage": "Day 1"},
            {"code": "REQ-HR-004", "sec": "7.4", "text": "Reconcile returning hardware assets within 7 business days of offboarding.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Asset Recovery", "priority": "Medium", "stage": "Week 1"}
        ]
    ),
    make_doc(
        "DOC-SOP-08", "IT Helpdesk Hardware Provisioning & Asset Decommissioning SOP", "SOP", "INFRA_IT", "docx", "1.0", 2,
        v1_sections=[
            {"id": "8.1", "heading": "Standard Laptop Provisioning Checklist", "content": "IT Operations must image laptops with approved enterprise base OS image, install endpoint EDR agents (CrowdStrike), configure BitLocker/FileVault disk encryption, and register asset tag in Snipe-IT."},
            {"id": "8.2", "heading": "Hardware Warranty & Refresh Cycles", "content": "Laptops and developer workstations are refreshed every 36 months. Battery replacements or hardware repairs must be logged via internal IT Helpdesk ticketing."},
            {"id": "8.3", "heading": "NIST 800-88 Cryptographic Sanitization", "content": "Decommissioned or reassigned hard drives must undergo certified cryptographic erasure following NIST Special Publication 800-88 guidelines before disposal or donation."},
            {"id": "8.4", "heading": "Peripheral Inventory & Loaner Fleet", "content": "IT Operations maintains a loaner laptop fleet for travel emergencies. Loaners must be returned within 14 days of travel conclusion."}
        ],
        v1_summary="Standard laptop imaging with EDR and disk encryption, 36-month refresh cycle, and NIST 800-88 drive wipe.",
        reqs=[
            {"code": "REQ-OPS-001", "sec": "8.1", "text": "Image endpoints with approved corporate OS, EDR agent, and verified disk encryption.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Endpoint Imaging", "priority": "High", "stage": "Day 1"},
            {"code": "REQ-OPS-002", "sec": "8.2", "text": "Log all hardware maintenance, repairs, and serial updates in Snipe-IT asset database.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Asset Tracking", "priority": "Medium", "stage": "Week 1"},
            {"code": "REQ-OPS-003", "sec": "8.3", "text": "Execute NIST 800-88 compliant cryptographic wipes on decommissioned storage media.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Media Sanitization", "priority": "Critical", "stage": "Week 1"},
            {"code": "REQ-OPS-004", "sec": "8.4", "text": "Manage loaner equipment returns and maintain ready emergency device pool.", "cat": "RECOMMENDED", "mandatory": False, "competency": "Inventory Management", "priority": "Low", "stage": "Week 2"}
        ]
    )
]

print(f"Loaded {len(SOPS)} operational SOP documents.")

# scripts/data_policies.py
from scripts.catalog_builder_core import make_doc

POLICIES = [
    make_doc(
        "DOC-POL-01", "ApexNova Enterprise Information Security Policy", "POLICY", "CYBER_SEC", "pdf", "2.0", 1,
        v1_sections=[
            {"id": "1.1", "heading": "Password Standard (Legacy)", "content": "Passwords must have at least 12 characters. Password rotation occurs every 180 days. SMS MFA is allowed for all staff."},
            {"id": "1.2", "heading": "Workstation Timeout", "content": "Workstations must lock after 15 minutes of inactivity."}
        ],
        v1_summary="Legacy security baseline allowing 12-char passwords and SMS MFA.",
        v2_sections=[
            {"id": "1.1", "heading": "Purpose & Organizational Scope", "content": "This policy establishes corporate information security controls across ApexNova Global Technologies, governing all cloud assets, infrastructure, and employee equipment."},
            {"id": "1.2", "heading": "Identity Authentication & MFA Standard", "content": "All corporate accounts must enforce passphrases of at least 16 characters with symbols, uppercase, lowercase, and digits. Passphrases must be rotated every 90 days. SMS MFA is strictly deprecated; FIDO2 hardware keys or authenticator apps are mandatory for all production and customer-facing staff."},
            {"id": "1.3", "heading": "Workstation Auto-Lock & Clean Desk Standard", "content": "Unattended workstations must automatically lock screen after 5 minutes of inactivity. Workstations must maintain a clean desk posture free of written credentials or customer identifiers."},
            {"id": "1.4", "heading": "Data Encryption Standards", "content": "All data at rest must use AES-256 encryption. All data in transit must enforce TLS 1.3 encryption. Unencrypted storage of client records on local hard drives is strictly prohibited."},
            {"id": "1.5", "heading": "Removable Storage Media Ban", "content": "Use of unencrypted USB flash drives, personal external storage devices, or unauthorized mass media is strictly prohibited on corporate laptops."}
        ],
        v2_summary="Enforced 16-char passwords, 90-day rotation, FIDO2/app MFA, 5-min auto-lock, AES-256/TLS 1.3, and USB ban.",
        reqs=[
            {"code": "REQ-SEC-001", "sec": "1.2", "text": "Configure 16+ char passphrase rotated every 90 days with FIDO2 or app-based MFA.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Identity Security", "priority": "Critical", "stage": "Day 1"},
            {"code": "REQ-SEC-002", "sec": "1.3", "text": "Configure 5-minute screen auto-lock and maintain clean desk standard.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Physical Hygiene", "priority": "High", "stage": "Day 1"},
            {"code": "REQ-SEC-003", "sec": "1.4", "text": "Enforce AES-256 at rest and TLS 1.3 in transit; prohibit unencrypted local data storage.", "cat": "MUST_KNOW", "mandatory": True, "competency": "Data Protection", "priority": "Critical", "stage": "Week 1"},
            {"code": "REQ-SEC-004", "sec": "1.5", "text": "Acknowledge strict ban on unauthorized USB flash drives and external mass storage.", "cat": "MUST_ACKNOWLEDGE", "mandatory": True, "competency": "Endpoint Security", "priority": "High", "stage": "Day 1"},
            {"code": "REQ-SEC-005", "sec": "1.1", "text": "Review enterprise security scope and governance responsibilities.", "cat": "RECOMMENDED", "mandatory": False, "competency": "Security Awareness", "priority": "Low", "stage": "First 30 Days"}
        ]
    ),
    make_doc(
        "DOC-POL-02", "Global Data Privacy & Customer Data Handling Policy", "POLICY", "DATA_AI", "docx", "2.0", 1,
        v1_sections=[
            {"id": "2.1", "heading": "Legacy PII Sandbox Rules", "content": "Staging environments could use anonymized or partial production snapshots if approved by team lead."}
        ],
        v1_summary="Legacy privacy rules allowing partial production data in test environments.",
        v2_sections=[
            {"id": "2.1", "heading": "Privacy Framework & GDPR/CCPA Compliance", "content": "ApexNova complies with GDPR, CCPA, and global privacy standards. Personal Identifiable Information (PII) must only be collected for explicitly consented business purposes."},
            {"id": "2.2", "heading": "Strict Ban on Real PII in Non-Production", "content": "Under no circumstances may live production customer data or unmasked PII be imported or stored in development, staging, sandbox, or test environments. Fully synthetic or tokenized data must be utilized."},
            {"id": "2.3", "heading": "Right to Be Forgotten & Erasure SLA", "content": "Customer requests for data erasure must be processed and fully wiped from all operational clusters and cold backups within 30 calendar days."},
            {"id": "2.4", "heading": "Data Residency and Regional Isolation", "content": "Customer telemetry and database records must remain within the sovereign region (EU, US, APAC) designated in the customer agreement. Cross-border transfers require legal DPA approval."},
            {"id": "2.5", "heading": "Data Retention & Archival Schedules", "content": "Transactional logs must be archived after 90 days and permanently expunged after 365 days unless legal holds apply."}
        ],
        v2_summary="Zero PII in non-production, 30-day erasure SLA, strict geographic data residency, and 365-day retention cap.",
        reqs=[
            {"code": "REQ-PRIV-001", "sec": "2.1", "text": "Understand GDPR, CCPA, and data minimization principles for customer data.", "cat": "MUST_KNOW", "mandatory": True, "competency": "Privacy Compliance", "priority": "High", "stage": "Week 1"},
            {"code": "REQ-PRIV-002", "sec": "2.2", "text": "Never copy or export unmasked production PII into dev or staging environments.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Synthetic Data", "priority": "Critical", "stage": "Day 1"},
            {"code": "REQ-PRIV-003", "sec": "2.3", "text": "Execute customer Right to be Forgotten requests within the mandatory 30-day SLA.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Privacy Operations", "priority": "High", "stage": "Week 2"},
            {"code": "REQ-PRIV-004", "sec": "2.4", "text": "Verify regional sovereignty restrictions before moving cloud storage buckets.", "cat": "MUST_ACKNOWLEDGE", "mandatory": True, "competency": "Data Sovereignty", "priority": "Medium", "stage": "First 30 Days"},
            {"code": "REQ-PRIV-005", "sec": "2.5", "text": "Ensure transactional logs adhere to 365-day automated purge lifecycle policies.", "cat": "RECOMMENDED", "mandatory": False, "competency": "Data Retention", "priority": "Low", "stage": "First 60 Days"}
        ]
    ),
    make_doc(
        "DOC-POL-03", "Access Control, Identity & Credential Management Policy", "POLICY", "CYBER_SEC", "pdf", "2.0", 1,
        v1_sections=[
            {"id": "3.1", "heading": "Annual Privilege Reviews", "content": "System administrators reviewed server access once per calendar year."}
        ],
        v1_summary="Annual privilege review cycle with persistent production admin rights.",
        v2_sections=[
            {"id": "3.1", "heading": "Principle of Least Privilege & RBAC", "content": "Access to corporate and production infrastructure is governed strictly by Role-Based Access Control (RBAC). Employees receive only minimum permissions necessary for their role."},
            {"id": "3.2", "heading": "Just-In-Time (JIT) Privileged Access", "content": "Permanent root or cluster admin credentials are prohibited. Privileged access to production environments requires dual-authorization ticketing and expires automatically after 8 hours."},
            {"id": "3.3", "heading": "Quarterly Access Recertification", "content": "Managers must recertify employee access permissions every 90 days. Accounts inactive for over 45 days are automatically suspended."},
            {"id": "3.4", "heading": "Credential Sharing Prohibition", "content": "Sharing user accounts, passwords, or personal SSH keys is strictly prohibited and results in immediate termination of employment."}
        ],
        v2_summary="Least privilege RBAC, 8-hour JIT access expiration, quarterly recertification, and strict credential sharing prohibition.",
        reqs=[
            {"code": "REQ-ACC-001", "sec": "3.1", "text": "Operate strictly under least privilege and request only required role scopes.", "cat": "MUST_KNOW", "mandatory": True, "competency": "Identity Governance", "priority": "High", "stage": "Day 1"},
            {"code": "REQ-ACC-002", "sec": "3.2", "text": "Request dual-approved Just-In-Time access with 8-hour auto-expiration for production tasks.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Privilege Hygiene", "priority": "Critical", "stage": "Week 1"},
            {"code": "REQ-ACC-003", "sec": "3.3", "text": "Managers must complete quarterly recertification for all team member permissions.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Access Auditing", "priority": "High", "stage": "First 30 Days"},
            {"code": "REQ-ACC-004", "sec": "3.4", "text": "Acknowledge that credential sharing is strictly forbidden and grounds for termination.", "cat": "MUST_ACKNOWLEDGE", "mandatory": True, "competency": "Security Conduct", "priority": "Critical", "stage": "Day 1"}
        ]
    ),
    make_doc(
        "DOC-POL-04", "Acceptable Use of Corporate IT Assets & AI Tools Policy", "POLICY", "INFRA_IT", "docx", "2.0", 1,
        v1_sections=[
            {"id": "4.1", "heading": "General Software Usage", "content": "Employees were permitted to install software tools with manager email permission."}
        ],
        v1_summary="Legacy acceptable use policy with no AI governance rules.",
        v2_sections=[
            {"id": "4.1", "heading": "Corporate Equipment Usage Standards", "content": "ApexNova computing hardware, networks, and cloud instances are reserved for authorized business functions. Installation of unauthorized software is blocked by endpoint protection."},
            {"id": "4.2", "heading": "Enterprise AI & LLM Governance", "content": "Employees may only use company-approved GenAI platforms with enterprise data privacy agreements. Inputting proprietary code, customer telemetry, financial statements, or PII into unauthorized public consumer AI platforms (e.g. public consumer ChatGPT/Claude) is strictly prohibited and treated as a data leak violation."},
            {"id": "4.3", "heading": "Verification of AI-Generated Content", "content": "Engineers and content creators utilizing approved AI tools must independently inspect, review, and validate all generated code and text for security flaws, factual hallucinations, and copyright compliance before production merge."},
            {"id": "4.4", "heading": "Open Source License Hygiene", "content": "Developers must not incorporate viral GPL-v3 or AGPL copyleft libraries into proprietary distributed products without Architecture Review Board signoff."}
        ],
        v2_summary="Strict ban on customer data in public consumer LLMs, mandatory verification of AI output, and open-source license governance.",
        reqs=[
            {"code": "REQ-USE-001", "sec": "4.1", "text": "Use corporate computing assets exclusively for approved business operations.", "cat": "MUST_ACKNOWLEDGE", "mandatory": True, "competency": "Asset Governance", "priority": "Medium", "stage": "Day 1"},
            {"code": "REQ-USE-002", "sec": "4.2", "text": "Never paste proprietary IP, source code, or customer PII into public consumer AI tools.", "cat": "MUST_KNOW", "mandatory": True, "competency": "AI Safety & Governance", "priority": "Critical", "stage": "Day 1"},
            {"code": "REQ-USE-003", "sec": "4.3", "text": "Independently validate AI-generated code and content for factual accuracy and security.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Quality Assurance", "priority": "High", "stage": "Week 1"},
            {"code": "REQ-USE-004", "sec": "4.4", "text": "Verify third-party open-source components against the corporate approved license list.", "cat": "RECOMMENDED", "mandatory": False, "competency": "Open Source Hygiene", "priority": "Medium", "stage": "Week 2"}
        ]
    ),
    make_doc(
        "DOC-POL-05", "Code of Business Conduct, Ethics & Anti-Bribery Policy", "POLICY", "HR_PEOPLE", "pdf", "1.0", 1,
        v1_sections=[
            {"id": "5.1", "heading": "Workplace Respect & Harassment Prevention", "content": "ApexNova is committed to a harassment-free environment. Discrimination or harassment on the basis of race, religion, gender, sexual orientation, disability, or age is prohibited."},
            {"id": "5.2", "heading": "Anti-Bribery & FCPA Compliance", "content": "Employees must not offer, pay, solicit, or accept bribes, kickbacks, or facilitation payments. Gifts or hospitality to or from clients exceeding $50 USD in value must be formally declared in the Compliance Gift Registry."},
            {"id": "5.3", "heading": "Conflict of Interest Disclosures", "content": "Employees must disclose outside commercial interests, advisory roles, or family relationships with active vendors using the annual Ethics Declaration portal within 14 days of employment."},
            {"id": "5.4", "heading": "Fair Competition & Antitrust Rules", "content": "Personnel must never participate in price-fixing, market division, or unlawful competitor discussions."}
        ],
        v1_summary="Comprehensive ethics, anti-harassment, anti-bribery ($50 gift cap), and conflict of interest standards.",
        reqs=[
            {"code": "REQ-ETH-001", "sec": "5.1", "text": "Complete mandatory anti-harassment and respectful workplace orientation.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Workplace Conduct", "priority": "High", "stage": "Week 1"},
            {"code": "REQ-ETH-002", "sec": "5.2", "text": "Declare any client/vendor gift or hospitality over $50 in the Compliance Gift Registry.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Anti-Bribery", "priority": "Critical", "stage": "Day 1"},
            {"code": "REQ-ETH-003", "sec": "5.3", "text": "Submit initial Conflict of Interest Disclosure in Ethics Portal within 14 days.", "cat": "MUST_ACKNOWLEDGE", "mandatory": True, "competency": "Ethics Governance", "priority": "High", "stage": "Week 2"},
            {"code": "REQ-ETH-004", "sec": "5.4", "text": "Acknowledge adherence to fair competition and antitrust regulations.", "cat": "MUST_ACKNOWLEDGE", "mandatory": True, "competency": "Legal Compliance", "priority": "Medium", "stage": "Week 1"}
        ]
    ),
    make_doc(
        "DOC-POL-06", "Remote Work, Hybrid Operations & Mobile Device Security Policy", "POLICY", "INFRA_IT", "docx", "2.0", 1,
        v1_sections=[
            {"id": "6.1", "heading": "Legacy Mobile Email", "content": "Corporate email could be synchronized to personal mobile phones without MDM."}
        ],
        v1_summary="Legacy BYOD allowance without mobile management enforcement.",
        v2_sections=[
            {"id": "6.1", "heading": "Remote Work Eligibility & Environment", "content": "Eligible remote employees must maintain a private workspace with secure high-speed internet and ergonomic seating."},
            {"id": "6.2", "heading": "Endpoint Disk Encryption Standards", "content": "All company-provided laptops must have BitLocker (Windows) or FileVault (macOS) full-disk encryption enabled and active prior to network authorization."},
            {"id": "6.3", "heading": "Public Network Connection Standards", "content": "When connecting through public Wi-Fi (airports, cafes, hotels), employees must route all network traffic through the company Zero Trust Network Access (ZTNA) tunnel."},
            {"id": "6.4", "heading": "Mobile Device Management (MDM) Mandate", "content": "Access to corporate email, Slack, or ticketing platforms on smartphones requires enrolling the device in Microsoft Intune MDM, permitting containerized corporate remote wipe upon separation or loss."}
        ],
        v2_summary="Enforced whole-disk encryption, mandatory ZTNA on public Wi-Fi, and Intune MDM for mobile email.",
        reqs=[
            {"code": "REQ-REM-001", "sec": "6.2", "text": "Confirm BitLocker or FileVault full-disk encryption is active on all company laptops.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Endpoint Security", "priority": "High", "stage": "Day 1"},
            {"code": "REQ-REM-002", "sec": "6.3", "text": "Always engage corporate ZTNA tunnel when working on public Wi-Fi connections.", "cat": "MUST_KNOW", "mandatory": True, "competency": "Network Hygiene", "priority": "High", "stage": "Day 1"},
            {"code": "REQ-REM-003", "sec": "6.4", "text": "Enroll personal or corporate mobile device in Intune MDM before accessing company mail.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Mobile Security", "priority": "Medium", "stage": "Week 1"},
            {"code": "REQ-REM-004", "sec": "6.1", "text": "Complete the self-paced Home Ergonomics and Workspace safety survey.", "cat": "RECOMMENDED", "mandatory": False, "competency": "Ergonomics", "priority": "Low", "stage": "First 30 Days"}
        ]
    ),
    make_doc(
        "DOC-POL-07", "Employee Leave, Attendance & Overtime Policy", "POLICY", "HR_PEOPLE", "pdf", "2.0", 1,
        v1_sections=[
            {"id": "7.1", "heading": "Legacy Vacation Carryover", "content": "Employees could automatically carry forward up to 10 unused vacation days each year."}
        ],
        v1_summary="10 days automatic leave carryover with no forfeiture timeline.",
        v2_sections=[
            {"id": "7.1", "heading": "Paid Time Off (PTO) Accrual", "content": "Full-time employees receive 20 days of paid annual vacation leave accrued monthly. Leave must be scheduled through the HR portal with manager sign-off."},
            {"id": "7.2", "heading": "Vacation Carryover Cap & March 31 Deadline", "content": "A maximum of 5 unused vacation days may be carried over into the next calendar year with written manager approval. Carried days must be used by March 31 or they are forfeited."},
            {"id": "7.3", "heading": "Quarterly Mental Health Wellness Days", "content": "All employees receive 1 designated paid Wellness Day per quarter (4 per year) that does not reduce accrued vacation balance."},
            {"id": "7.4", "heading": "Overtime Authorization Standard", "content": "Overtime for non-exempt staff must be pre-authorized in writing by Department Managers before being logged in the payroll system."}
        ],
        v2_summary="Vacation carryover capped at 5 days expiring March 31, 1 wellness day per quarter, and overtime pre-authorization.",
        reqs=[
            {"code": "REQ-LEV-001", "sec": "7.1", "text": "Submit vacation leave requests via HR portal at least 5 business days in advance.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "HR Operations", "priority": "Medium", "stage": "Week 2"},
            {"code": "REQ-LEV-002", "sec": "7.2", "text": "Acknowledge the 5-day vacation carryover limit and March 31 forfeiture rule.", "cat": "MUST_ACKNOWLEDGE", "mandatory": True, "competency": "Leave Governance", "priority": "Medium", "stage": "Week 1"},
            {"code": "REQ-LEV-003", "sec": "7.4", "text": "Obtain written manager pre-approval before performing overtime hours.", "cat": "MUST_KNOW", "mandatory": True, "competency": "Payroll Compliance", "priority": "High", "stage": "Day 1"},
            {"code": "REQ-LEV-004", "sec": "7.3", "text": "Schedule and take quarterly mental health wellness days.", "cat": "RECOMMENDED", "mandatory": False, "competency": "Wellbeing", "priority": "Low", "stage": "First 30 Days"}
        ]
    ),
    make_doc(
        "DOC-POL-08", "Financial Authorization, Travel & Expense Reimbursement Policy", "POLICY", "FIN_OPS", "docx", "2.0", 1,
        v1_sections=[
            {"id": "8.1", "heading": "Legacy Expense Window", "content": "Expense reports could be submitted within 30 days of incurring expense."}
        ],
        v1_summary="30-day expense submission window with flexible hotel booking.",
        v2_sections=[
            {"id": "8.1", "heading": "14-Day Expense Submission Window", "content": "All corporate travel and business expense reports must be submitted into Concur with itemized receipts attached within 14 calendar days of expense occurrence. Claims past 14 days require VP Finance exception approval."},
            {"id": "8.2", "heading": "Commercial Air Travel Guidelines", "content": "Flights must be booked in economy class via corporate travel platform. Any flight booking exceeding $800 USD requires pre-approval by Department VP."},
            {"id": "8.3", "heading": "Daily Meal Per Diem Caps", "content": "Meals are reimbursed up to $75 USD per day ($15 Breakfast, $25 Lunch, $35 Dinner). Alcohol is non-reimbursable unless tied to an approved executive client dinner."},
            {"id": "8.4", "heading": "Financial Delegation of Authority", "content": "Managers may approve operational spend up to $2,500; Directors up to $10,000; VPs up to $50,000; CFO signoff required for amounts exceeding $50,000."}
        ],
        v2_summary="14-day receipt submission deadline, $800 flight pre-approval cap, $75 daily meal limit, and tiered financial delegation.",
        reqs=[
            {"code": "REQ-EXP-001", "sec": "8.1", "text": "Submit expense reports with itemized receipts within 14 calendar days of purchase.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Expense Administration", "priority": "High", "stage": "Week 2"},
            {"code": "REQ-EXP-002", "sec": "8.2", "text": "Secure Department VP approval before booking any flight exceeding $800.", "cat": "MUST_KNOW", "mandatory": True, "competency": "Travel Policy", "priority": "High", "stage": "Week 1"},
            {"code": "REQ-EXP-003", "sec": "8.3", "text": "Adhere to the $75/day meal per diem and exclude personal alcohol from claims.", "cat": "MUST_KNOW", "mandatory": True, "competency": "Expense Discipline", "priority": "Medium", "stage": "Week 1"},
            {"code": "REQ-EXP-004", "sec": "8.4", "text": "Enforce financial authority authorization thresholds when approving invoices.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Financial Control", "priority": "Critical", "stage": "Day 1"}
        ]
    ),
    make_doc(
        "DOC-POL-09", "Workplace Health, Physical Safety & Emergency Response Policy", "POLICY", "INFRA_IT", "pdf", "1.0", 1,
        v1_sections=[
            {"id": "9.1", "heading": "Physical Access & Visitor Protocol", "content": "Employees must wear security badges at all times on company premises. Tailgating into secured data rooms is strictly forbidden. Visitors must register and remain escorted."},
            {"id": "9.2", "heading": "Emergency Evacuation & Fire Alarms", "content": "Upon hearing the fire alarm, all occupants must evacuate via emergency stairs to designated muster points. Do not attempt to use elevators."},
            {"id": "9.3", "heading": "Accident & Injury Reporting SLA", "content": "Any injury, near miss, or hazard on company property must be reported to Facilities and HR within 2 hours of the incident."}
        ],
        v1_summary="Physical security badge rules, emergency evacuation procedures, and 2-hour injury reporting SLA.",
        reqs=[
            {"code": "REQ-SAF-001", "sec": "9.1", "text": "Wear security badge visibly and prevent tailgating into corporate facilities.", "cat": "MUST_DEMONSTRATE", "mandatory": True, "competency": "Facility Security", "priority": "High", "stage": "Day 1"},
            {"code": "REQ-SAF-002", "sec": "9.2", "text": "Locate designated emergency exits, muster points, and fire evacuation routes.", "cat": "MUST_KNOW", "mandatory": True, "competency": "Emergency Response", "priority": "High", "stage": "Day 1"},
            {"code": "REQ-SAF-003", "sec": "9.3", "text": "Report workplace injuries, hazards, or near misses to HR/Facilities within 2 hours.", "cat": "MUST_COMPLETE", "mandatory": True, "competency": "Safety Reporting", "priority": "Medium", "stage": "Week 1"}
        ]
    ),
    make_doc(
        "DOC-POL-10", "Whistleblower Protection & Non-Retaliation Policy", "POLICY", "HR_PEOPLE", "docx", "1.0", 1,
        v1_sections=[
            {"id": "10.1", "heading": "Scope of Whistleblower Disclosures", "content": "Employees are protected when reporting good-faith suspicions of financial fraud, bribery, major safety violations, or regulatory non-compliance."},
            {"id": "10.2", "heading": "Confidential Ethics Hotline", "content": "Anonymous reports can be lodged 24/7 via the independent EthicsPoint hotline (ethics.apexnova.internal) or phone hotlines."},
            {"id": "10.3", "heading": "Strict Non-Retaliation Guarantee", "content": "Retaliation of any kind against an employee making a report in good faith is strictly prohibited and results in immediate dismissal of the retaliator."}
        ],
        v1_summary="Whistleblower reporting protections, 24/7 anonymous EthicsPoint hotline, and strict non-retaliation rules.",
        reqs=[
            {"code": "REQ-WHT-001", "sec": "10.1", "text": "Understand the scope of protected whistleblower reporting disclosures.", "cat": "MUST_KNOW", "mandatory": True, "competency": "Ethical Reporting", "priority": "Medium", "stage": "Week 1"},
            {"code": "REQ-WHT-002", "sec": "10.2", "text": "Identify the confidential 24/7 EthicsPoint reporting channels.", "cat": "MUST_KNOW", "mandatory": True, "competency": "Whistleblower Access", "priority": "Medium", "stage": "Week 1"},
            {"code": "REQ-WHT-003", "sec": "10.3", "text": "Acknowledge that retaliation against reporters leads to immediate termination.", "cat": "MUST_ACKNOWLEDGE", "mandatory": True, "competency": "Non-Retaliation", "priority": "Critical", "stage": "Day 1"}
        ]
    )
]

print(f"Loaded {len(POLICIES)} core corporate policies.")

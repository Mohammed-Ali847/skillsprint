# ApexNova Global Technologies - Fictional Company Knowledge Base Definitions
# Enterprise Cloud, Cybersecurity & AI Automation Provider

COMPANY_INFO = {
    "name": "ApexNova Global Technologies",
    "domain": "Enterprise Cloud Infrastructure, AI Platforms & Cybersecurity Operations",
    "headquarters": "San Francisco, CA (with global hubs in London, Singapore, and Tokyo)",
    "employees_count": 2800,
    "founded": 2019,
    "mission": "Delivering secure, autonomous, and resilient cloud architecture for critical global enterprises."
}

DEPARTMENTS = [
    {"code": "CYBER_SEC", "name": "Cybersecurity & Information Assurance", "description": "Responsible for threat intelligence, zero-trust infrastructure, access control, and incident triage."},
    {"code": "CUST_OPS", "name": "Customer Operations & Technical Support", "description": "Front-line customer engagement, enterprise SLA resolution, and tier-2 escalation management."},
    {"code": "ENG_DEV", "name": "Engineering & Platform Development", "description": "Core platform engineering, secure software lifecycle, and distributed systems architecture."},
    {"code": "DATA_AI", "name": "Data Intelligence & Artificial Intelligence", "description": "Data governance, analytics engineering, LLM pipeline orchestration, and BI reporting."},
    {"code": "COMM_SALES", "name": "Commercial & Enterprise Sales", "description": "Enterprise customer acquisition, contract negotiation, and customer relationship expansion."},
    {"code": "HR_PEOPLE", "name": "People Operations & Human Resources", "description": "Talent onboarding, workplace conduct, compensation, and regulatory compliance."},
    {"code": "FIN_OPS", "name": "Finance, Accounting & Procurement", "description": "Financial planning, expense governance, audit readiness, and vendor procurement."},
    {"code": "INFRA_IT", "name": "Infrastructure & Global IT Operations", "description": "Internal IT helpdesk, endpoint device provisioning, and corporate network topology."}
]

ROLES = [
    {
        "code": "SEC_ANALYST",
        "name": "Information Security Analyst",
        "dept_code": "CYBER_SEC",
        "experience_level": "Mid",
        "description": "Monitors security telemetry, assesses vulnerabilities, enforces access policies, investigates incident alerts, and ensures SOC2/ISO27001 posture."
    },
    {
        "code": "CUST_SUPPORT",
        "name": "Customer Support Executive",
        "dept_code": "CUST_OPS",
        "experience_level": "Junior",
        "description": "Handles tier-1 and tier-2 enterprise client tickets, verifies customer identity, enforces SLAs, executes escalation SOPs, and manages client satisfaction."
    },
    {
        "code": "SOFT_ENG",
        "name": "Software Support Engineer",
        "dept_code": "ENG_DEV",
        "experience_level": "Mid",
        "description": "Triages platform production bugs, reviews code patches, validates CI/CD pipelines, follows SSDLC guidelines, and coordinates with platform engineers."
    },
    {
        "code": "DATA_ANALYST",
        "name": "Data Analyst",
        "dept_code": "DATA_AI",
        "experience_level": "Mid",
        "description": "Builds executive BI dashboards, analyzes telemetry datasets, enforces data handling policies, ensures GDPR anonymization, and generates reports."
    },
    {
        "code": "SALES_EXEC",
        "name": "Sales Executive",
        "dept_code": "COMM_SALES",
        "experience_level": "Senior",
        "description": "Leads high-value enterprise sales pursuits, follows sales discounting authority rules, executes non-disclosure agreements, and completes anti-bribery training."
    },
    {
        "code": "HR_EXEC",
        "name": "HR Executive",
        "dept_code": "HR_PEOPLE",
        "experience_level": "Mid",
        "description": "Manages end-to-end employee onboarding lifecycle, oversees workplace conduct adherence, tracks leave management compliance, and handles employee grievances."
    },
    {
        "code": "FIN_ASSOC",
        "name": "Finance Associate",
        "dept_code": "FIN_OPS",
        "experience_level": "Junior",
        "description": "Processes corporate expense reports, audits financial authorizations, verifies vendor invoices, and ensures compliance with travel and disbursement limits."
    },
    {
        "code": "OPS_COORD",
        "name": "Operations Coordinator",
        "dept_code": "INFRA_IT",
        "experience_level": "Junior",
        "description": "Coordinates internal hardware provisioning, monitors facility safety protocols, maintains IT asset registries, and organizes cross-departmental equipment returns."
    },
    {
        "code": "MKT_EXEC",
        "name": "Marketing Executive",
        "dept_code": "COMM_SALES",
        "experience_level": "Mid",
        "description": "Coordinates brand campaigns, manages corporate public communications, enforces customer privacy in marketing lists, and adheres to copyright guidelines."
    },
    {
        "code": "TEAM_LEAD",
        "name": "Engineering Team Leader",
        "dept_code": "ENG_DEV",
        "experience_level": "Senior",
        "description": "Oversees engineering sprint delivery, conducts mandatory code reviews, approves change advisory board (CAB) releases, and mentors engineering talent."
    }
]

SAMPLE_EMPLOYEES = [
    {"code": "EMP-1001", "name": "Elena Rostova", "role_code": "SEC_ANALYST", "dept_code": "CYBER_SEC", "level": "Mid", "manager": "Marcus Vance (CISO)", "status": "On Track"},
    {"code": "EMP-1002", "name": "David Kim", "role_code": "CUST_SUPPORT", "dept_code": "CUST_OPS", "level": "Junior", "manager": "Sarah Jenkins (Head of Support)", "status": "Requires Attention"},
    {"code": "EMP-1003", "name": "Amira Al-Mansoor", "role_code": "SOFT_ENG", "dept_code": "ENG_DEV", "level": "Mid", "manager": "Tariq Bradley (VP Engineering)", "status": "On Track"},
    {"code": "EMP-1004", "name": "Liam O'Connor", "role_code": "DATA_ANALYST", "dept_code": "DATA_AI", "level": "Mid", "manager": "Dr. Aris Thorne (Chief Data Scientist)", "status": "Behind Schedule"},
    {"code": "EMP-1005", "name": "Samantha Wu", "role_code": "SALES_EXEC", "dept_code": "COMM_SALES", "level": "Senior", "manager": "Robert Sterling (CRO)", "status": "On Track"},
    {"code": "EMP-1006", "name": "Kwame Mensah", "role_code": "HR_EXEC", "dept_code": "HR_PEOPLE", "level": "Mid", "manager": "Rachel Adams (Chief People Officer)", "status": "On Track"},
    {"code": "EMP-1007", "name": "Isabella Rossi", "role_code": "FIN_ASSOC", "dept_code": "FIN_OPS", "level": "Junior", "manager": "Gerald Huang (VP Finance)", "status": "On Track"},
    {"code": "EMP-1008", "name": "Carlos Gomez", "role_code": "OPS_COORD", "dept_code": "INFRA_IT", "level": "Junior", "manager": "Hannah Croft (Director of IT)", "status": "Assessment Required"},
    {"code": "EMP-1009", "name": "Priya Sharma", "role_code": "MKT_EXEC", "dept_code": "COMM_SALES", "level": "Mid", "manager": "Victoria Chase (CMO)", "status": "On Track"},
    {"code": "EMP-1010", "name": "Lucas Meyer", "role_code": "TEAM_LEAD", "dept_code": "ENG_DEV", "level": "Senior", "manager": "Tariq Bradley (VP Engineering)", "status": "On Track"}
]

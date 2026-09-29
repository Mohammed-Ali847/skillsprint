# SkillSprint AI: Evaluator & Demo Guide (TechWiz 7 Competition)

This document provides a step-by-step live demonstration script for competition judges and evaluators assessing **SkillSprint AI** against the TechWiz 7 SRS v1.0.

---

## Prerequisites
1. Open terminal and navigate to the project directory:
   ```bash
   cd C:\Users\Mohammed\.gemini\antigravity\scratch\skillsprint_ai
   ```
2. Start the FastAPI server:
   ```bash
   python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```
3. Open your browser to: [http://localhost:8000/](http://localhost:8000/)

---

## 11-Step Interactive Evaluation Script

### Step 1: System Health & Dual-Pipeline Verification
- **Action:** Visit `http://localhost:8000/api/health` in your browser.
- **Verification:** Observe that both pipelines report active status:
  ```json
  {
    "status": "healthy",
    "project": "SkillSprint AI",
    "dual_pipeline": {
      "genai_generation_pipeline": "active",
      "python_ground_truth_validator": "active"
    }
  }
  ```

### Step 2: Executive Dashboard & Role Switching
- **Action:** Open `http://localhost:8000/` to view the dark-mode dashboard.
- **Observe:**
  - Live metric cards showing **10 Employees**, **23 Documents**, **173 Requirements**, and **10 Roles**.
  - Top-right **Perspective Switcher** allowing instantaneous switching between:
    - *System Administrator*
    - *HR Specialist*
    - *Line Manager*
    - *New Employee*

### Step 3: Document Hub & Ingestion Engine
- **Action:** Click **Document Hub** in the sidebar.
- **Observe:**
  - Complete list of 23 seeded enterprise documents from ApexNova Global Technologies.
  - Notice the **Precedence Level** tags:
    - `POLICY` $\implies$ Level 1 (Corporate Policy)
    - `SOP` $\implies$ Level 2 (Standard Operating Procedure)
    - `FAQ` $\implies$ Level 3 (Frequently Asked Questions)
    - `HANDBOOK` $\implies$ Level 4 (Employee Handbook)
  - Click **View Chunks** on `DOC-POL-01` to inspect section-aware chunking and token counts.

### Step 4: Role Requirement Matrix
- **Action:** Click **Role Matrix** in the sidebar.
- **Observe:**
  - Grid showing all 10 corporate roles.
  - Click **View Requirements** for *Information Security Analyst* (`SEC_ANALYST`).
  - View the list of mandatory and optional requirements, complete with document citations, section IDs, priority levels, and due stages.

### Step 5: Onboarding Plan Synthesis (Pipeline 1)
- **Action:** Click **Onboarding Plans** in the sidebar.
- **Observe:**
  - Select employee **Marcus Vance** (Customer Support Executive).
  - Click **Generate Onboarding Plan**.
  - Pipeline 1 generates a personalized 90-day onboarding journey (modules, practical tasks, scenarios, and quizzes).
  - Pipeline 2 automatically executes in the background.

### Step 6: Independent Python Validation & Comparison Matrix (Pipeline 2)
- **Action:** Click **Validation Engine** in the sidebar.
- **Observe:**
  - View the validation scorecards: **Mandatory Coverage %**, **Active Traceability %**, and **Consistency Score**.
  - Scroll down to the **GenAI vs. Python Ground Truth Comparison Matrix**.
  - Observe over **100 requirement rows** comparing the Python expected standard against the GenAI synthesized result.
  - Notice that Python genuinely flags discrepancies without blindly rubber-stamping the AI's claims, fulfilling the `LLM ≠ Ground Truth` contract.

### Step 7: Human-in-the-Loop Review Triage Queue
- **Action:** Switch perspective to **HR Specialist** and click **Review Queue** in the sidebar.
- **Observe:**
  - Plans flagged with warnings or incomplete coverage appear in the triage queue.
  - Evaluators can inspect the exact missing requirements or cited sources.
  - Click **Review Action** to submit an authorized action: `APPROVE`, `REJECT`, `EDIT`, or `OVERRIDE`, writing an immutable entry into the audit trail.

### Step 8: Learner Experience & Adaptive Remediation
- **Action:** Switch perspective to **New Employee** (Marcus Vance) and click **Employee Portal**.
- **Observe:**
  - Visual 90-day onboarding roadmap with progress tracker.
  - Checklists: Click any checklist item to toggle completion status.
  - Tasks: Click **Submit Evidence** and provide a GitHub URL or ticket ID.
  - Quizzes: Click **Take Knowledge Check** on any module.
  - **Failing Quiz Simulation:** Intentionally select wrong answers and submit.
  - **Verification:** Observe that an **Adaptive Remediation Card** is immediately generated, recommending targeted revision modules for the failed competencies.

### Step 9: Policy Evolution & Selective Regeneration
- **Action:** Click **Policy Impact** in the sidebar.
- **Observe:**
  - Select document `DOC-POL-01`, old version `1.0`, and new version `2.0`.
  - Click **Analyze Policy Impact**.
  - Inspect the **Unified Diff**, showing password rotation updating from legacy guidance to 90 days with MFA.
  - Inspect the list of affected roles, employees, and modules automatically flagged as `OUTDATED_SOURCE`.
  - Click **Selectively Regenerate Module** to re-ground only the impacted learning module without disturbing unrelated training progress.

### Step 10: Adversarial Prompt Injection Defense
- **Action:** Click **Adversarial Logs** in the sidebar or run the test suite:
  ```bash
  pytest tests/test_prompt_injection.py -v
  ```
- **Observe:**
  - All 10 adversarial documents (`ADV-001` through `ADV-010`) are scanned and blocked.
  - Review the intercepted payloads (system instruction overrides, Base64 evasion, salary exfiltration, and grade manipulation).

### Step 11: Executive Compliance Reporting & Export
- **Action:** Click **Reports & Audit** in the sidebar.
- **Observe:**
  - View real-time compliance metrics across all 10 corporate roles.
  - Click **Download CSV Report** to obtain a structured CSV audit file.
  - Click **Download PDF Report** to view a branded, multi-page executive compliance document generated dynamically via **ReportLab**.

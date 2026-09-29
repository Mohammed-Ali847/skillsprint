# SkillSprint AI: Independent Python Ground-Truth Validator (Pipeline 2)

## 1. Architectural Mandate: Pipeline 2 Independence

In **SkillSprint AI**, the validation pipeline is completely decoupled from the generative AI pipeline. Pipeline 2:
- Does **not** query any Large Language Model.
- Does **not** compute fuzzy vector cosine similarity to judge compliance.
- Does **not** accept self-attested status flags from GenAI.
- Operates purely as a deterministic Python rule and graph verification engine over the SQLite relational truth table.

---

## 2. Mathematical Formulations & Validation Subsystems

### 2.1 Mandatory Requirement Coverage (`CoverageValidator`)
Let $\mathcal{R}_{\text{mandatory}}(r)$ be the set of mandatory requirements mapped to role $r$ in the Role Requirement Matrix, and let $\mathcal{R}_{\text{covered}}(P)$ be the set of requirement codes explicitly addressed by the modules and checklists in plan $P$:

$$\text{Coverage Score} = \begin{cases} 
100.0\% & \text{if } |\mathcal{R}_{\text{mandatory}}(r)| = 0 \\
\left( \frac{|\mathcal{R}_{\text{mandatory}}(r) \cap \mathcal{R}_{\text{covered}}(P)|}{|\mathcal{R}_{\text{mandatory}}(r)|} \right) \times 100\% & \text{otherwise}
\end{cases}$$

- **Omission Penalty:** If any requirement in $\mathcal{R}_{\text{mandatory}}(r)$ is absent from the plan, it is appended to `missing_requirements`, and the plan verification status is degraded to `INCOMPLETE`.

---

### 2.2 Active Source Traceability (`TraceabilityValidator`)
Let $\mathcal{I}$ be the set of all generated curriculum items (learning modules, tasks, scenarios, quiz questions), and let $\mathcal{A}$ be the set of active document versions approved in the corporate repository:

$$\text{Valid Citation}(i) = \begin{cases}
\text{True} & \text{if } \text{doc\_id}(i) \in \mathcal{A} \land \text{section\_id}(i) \in \text{Sections}(\text{doc\_id}(i)) \\
\text{False} & \text{otherwise}
\end{cases}$$

$$\text{Traceability Score} = \left( \frac{\sum_{i \in \mathcal{I}} \mathbb{I}(\text{Valid Citation}(i))}{|\mathcal{I}|} \right) \times 100\%$$

- **Obsolete Version Citation:** If an item cites an inactive version superseded by a newer policy, it is flagged as `OUTDATED_SOURCE`.
- **Ghost Citation:** If an item cites a non-existent document or section, it is flagged as `UNSUPPORTED`.

---

### 2.3 Factual Grounding & Hallucination Elimination (`HallucinationDetector`)
Rather than asking an LLM "Does this module match the document?", Pipeline 2 uses algorithmic token grounding:
1. **Stopword Elimination:** Strips syntactic stopwords (e.g. *the, and, must, shall, policy, corporate*).
2. **Salient Token Extraction:** Extracts alphanumeric tokens of length $\ge 3$ from the generated module title and objectives:
   $$\mathcal{T}_{\text{module}} = \text{SalientTokens}(\text{Module Title} \cup \text{Objectives})$$
3. **Chunk Token Extraction:** Extracts salient tokens from the cited active source chunk:
   $$\mathcal{T}_{\text{source}} = \text{SalientTokens}(\text{Chunk Content})$$
4. **Factual Grounding Condition:**
   $$\text{Grounding Score} = |\mathcal{T}_{\text{module}} \cap \mathcal{T}_{\text{source}}|$$
   If $\text{Grounding Score} == 0$, the module is flagged as an unsupported hallucination.

---

### 2.4 Contradiction Benchmark Suite (`ContradictionDetector`)
Pipeline 2 scans all generated titles, purposes, objectives, and quiz answers against regex signatures of documented corporate friction points:

| ID | Subject | Conflicting Pattern | Authoritative Ground-Truth Rule | Status Assigned |
| :---: | :--- | :--- | :--- | :---: |
| `CONT-001` | Password Rotation | `\b180\s*days?\b` | `DOC-POL-01 v2.0` mandates 90 days. FAQ-01 is superseded. | `CONTRADICTION_DETECTED` |
| `CONT-002` | Frontline Support Refund | `\$500\b` | `DOC-SOP-02 v2.0` caps refunds at $150. FAQ-02 is superseded. | `CONTRADICTION_DETECTED` |
| `CONT-003` | P1 Outage Escalation | `30\s*minutes?.*escalat` | `DOC-SOP-02 v2.0` mandates 15 minutes. FAQ-02 is incorrect. | `CONTRADICTION_DETECTED` |
| `CONT-004` | Local CSV Customer Data | `save.*(?:desktop\|laptop).*csv` | `DOC-POL-02` strictly prohibits unencrypted local exports. | `CONTRADICTION_DETECTED` |
| `CONT-005` | Vacation Carryover | `10\s*days?.*carry\s*over` | `DOC-POL-07 v2.0` caps carryover at 5 days. v1.0 (10d) is obsolete. | `CONTRADICTION_DETECTED` |
| `CONT-006` | Flight Pre-Approval | `\$1500.*flight` | `DOC-POL-08 v2.0` requires VP approval for flights >$800. | `CONTRADICTION_DETECTED` |
| `CONT-007` | Critical Breach SLA | `24\s*hours?.*breach` | `DOC-SOP-01 v2.0` mandates 4-hour notification to CISO/DPO. | `CONTRADICTION_DETECTED` |

---

### 2.5 Sequence & Prerequisite DAG (`SequenceValidator`)
Evaluates the learning journey as a directed acyclic graph (DAG):
1. **Day 1 Overload:** Flags plans containing $>8$ modules on Day 1.
2. **Topological Order:**
   $$\text{StageRank}(\text{module}) \ge \text{StageRank}(\text{prerequisite})$$
   If a dependent module is scheduled earlier than its prerequisite, an `INVALID_PREREQUISITE_SEQUENCE` error is logged.
3. **Difficulty Progression:** Beginner $\implies$ Intermediate $\implies$ Advanced. Flags Advanced modules scheduled on Day 1.

---

## 3. Verification State Machine

```text
                                  +-------------------+
                                  | Pipeline 1 Output |
                                  +-------------------+
                                            |
                                            v
                                  +-------------------+
                                  | Contradictions?   |--- YES ---> [ CONTRADICTION_DETECTED ]
                                  +-------------------+
                                            | NO
                                            v
                                  +-------------------+
                                  | Hallucinations?   |--- YES ---> [ UNSUPPORTED ]
                                  +-------------------+
                                            | NO
                                            v
                                  +-------------------+
                                  | Missing Req /     |--- YES ---> [ INCOMPLETE ]
                                  | Coverage < 100%?  |
                                  +-------------------+
                                            | NO
                                            v
                                  +-------------------+
                                  | Traceability <100%|--- YES ---> [ VERIFIED_WITH_WARNING ]
                                  | or Sequence Error?|
                                  +-------------------+
                                            | NO
                                            v
                                  +-------------------+
                                  | VERIFIED (CLEAN)  |
                                  +-------------------+
```

---

## 4. 100+ Row Comparison Matrix Specification

To fulfill SRS Section 1.10 Item 6, `ComparisonEngine` evaluates at least 100 requirement rows against the generated plan:

| Column | Type | Example |
| :--- | :--- | :--- |
| `requirement_id` | String | `REQ-SEC-001` |
| `role` | String | `Information Security Analyst` |
| `source` | String | `DOC-POL-01 §1.2` |
| `python_expected` | String | `[MANDATORY] Password Rotation and MFA (DOC-POL-01 Sec 1.2)` |
| `genai_result` | String | `Covered in 'Identity Security Fundamentals...' (DOC-POL-01 Sec 1.2)` |
| `match_status` | String | `Match` or `Mismatch` |
| `coverage_status` | String | `Covered` or `Missing` |
| `traceability_status` | String | `Verified` or `Unverified` |
| `validation_status` | String | `Verified`, `Verified with Warning`, or `Requirement Missing` |
| `explanation` | String | Detailed audit trail explaining the exact reason for the status. |

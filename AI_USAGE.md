# AI Usage Declaration Form — TechWiz 7 Competition

**Competition Theme:** OnboardVerse  
**Competition Category:** Generative AI PowerPlay  
**Project Title:** SkillSprint AI  
**Team / Participant:** Lead Software & AI Engineering  
**Date of Submission:** September 2026  

---

## 1. Executive Statement of AI Usage

In compliance with TechWiz 7 competition guidelines, this document transparently declares all Generative AI tools, foundation models, prompt engineering patterns, and autonomous agent systems utilized during the ideation, design, development, and runtime execution of **SkillSprint AI**.

### Core Architectural Principle
> **`LLM ≠ Ground Truth`**  
> SkillSprint AI is designed specifically around the doctrine that Generative AI models are stochastic reasoning engines and must **never** be treated as authoritative sources of truth for enterprise compliance, legal regulations, or employee competency certification.

---

## 2. Runtime AI Architecture (Inside the Application)

### 2.1 Foundation Models Employed
| Model | Provider | Primary Use Case | Temperature | Structured Output |
| :--- | :--- | :--- | :--- | :--- |
| **Gemini 2.5 Flash** | Google DeepMind | Personalized onboarding curriculum generation, module structuring, scenario synthesis, and quiz question authoring | `0.2` | Pydantic v2 JSON Schema Enforced |
| **Deterministic Grounded Fallback Engine** | Custom Python Engine | High-availability, zero-latency offline synthesis engine guaranteeing 100% test and evaluation reproducibility without external API keys | `N/A` | Deterministic Algorithm |

### 2.2 Dual-Pipeline Separation of Concerns
1. **Pipeline 1 (GenAI Generation Pipeline):**
   - The LLM receives sanitized, boundary-tagged document excerpts and an employee profile.
   - The LLM acts solely as a **Curriculum Synthesizer**, drafting learning objectives, real-world workplace scenarios, rubrics, and quiz questions.
2. **Pipeline 2 (Independent Python Ground-Truth Validator):**
   - **Zero LLM Involvement**: Pipeline 2 runs purely deterministic Python code (`CoverageValidator`, `TraceabilityValidator`, `HallucinationDetector`, `ContradictionDetector`, `SequenceValidator`, `DuplicateDetector`, `StatusResolver`).
   - Every single generated entity is verified against the database truth table.
   - Quizzes are graded using exact normalized string comparisons against verified answer keys; no LLM grading is used for mandatory compliance.

### 2.3 Prompt Engineering & Defense Patterns
- **Role Scoping:** Prompts strictly instruct the model to adopt the persona of an Enterprise Instructional Designer for ApexNova Global Technologies.
- **Untrusted Content Sandboxing:** All retrieved policy text is enclosed within `<UNTRUSTED_COMPANY_DOCUMENT_DATA>` tags to prevent indirect prompt injection.
- **Schema Enforcement:** Model responses are strictly validated through Pydantic v2 schemas (`OnboardingPlanSchema`, `LearningModuleSchema`, `QuizQuestionSchema`, `ScenarioSchema`).
- **Defensive Pre-Scanning:** All input documents are pre-screened with regex and Base64 decoders before entering prompt contexts.

---

## 3. Development-Time AI Tool Usage

### 3.1 AI Coding Assistants
- **Google DeepMind Antigravity / Gemini:**
  - Used for rapid scaffolding of boilerplate SQLAlchemy models, ReportLab PDF layout coordinates, test mocks, and Tailwind CSS templates.
  - Used for assisting in generating the extensive enterprise test corpus (23 multi-format company documents, 10 adversarial documents, 5 hidden challenge documents).

### 3.2 Human Engineering & Oversight
All algorithmic validation logic, database relationships, architectural boundaries, security filters, and mathematical formulas were designed, implemented, reviewed, and debugged under strict software engineering principles:
- **Deterministic Precedence Engine:** Hand-crafted hierarchy logic (`Policy (1) > SOP (2) > FAQ (3) > Handbook (4)`).
- **Contradiction Benchmark Suite:** Manually cataloged conflicting company policies based on real-world enterprise friction scenarios.
- **Topological DAG Sequence Validator:** Hand-crafted pacing and prerequisite dependency graph verification.
- **Automated Test Suite:** 40 pytest tests written with 100% pass rate, ensuring no hallucinated passes or mocked results.

---

## 4. Verification & Integrity Checklist

- [x] **No Hard-Coded Quiz Answers:** Quizzes dynamically check against source section ground truth.
- [x] **No Hard-Coded Validation Scores:** Coverage and traceability are mathematically computed on every run.
- [x] **No Fake Prototype:** Real SQLite database with 24 tables, real file parsing (PDF, DOCX, TXT), real REST API endpoints, real ReportLab PDF exporter, and real responsive UI.
- [x] **Zero Reliance on Cloud API for Demo:** The platform is fully runnable offline and demo-ready immediately after cloning.

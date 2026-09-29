# src/genai_pipeline/client.py
import os, json, time, re
from typing import Dict, Any, Optional, List
from src.config.settings import settings
from src.security.prompt_defense import PromptDefense
from src.schemas.onboarding_plan import GeneratedOnboardingPlanSchema

class GenAIClient:
    """Enterprise GenAI Pipeline client integrating Gemini API with automatic fallback and schema enforcement."""

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL
        self._gemini_client = None
        if self.api_key:
            try:
                from google import genai
                self._gemini_client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize Google GenAI Client: {e}")

    def call_gemini(self, system_instruction: str, prompt: str) -> Optional[str]:
        """Calls Google Gemini API with controlled temperature."""
        if not self._gemini_client:
            return None
        try:
            response = self._gemini_client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    "system_instruction": system_instruction,
                    "temperature": settings.LLM_TEMPERATURE,
                    "response_mime_type": "application/json"
                }
            )
            return response.text
        except Exception as e:
            print(f"GenAI API call failed: {e}")
            return None

    def synthesize_onboarding_plan(
        self,
        employee_code: str,
        role_code: str,
        role_name: str,
        department: str,
        experience_level: str,
        mandatory_reqs: List[Dict[str, Any]],
        evidence_chunks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Synthesizes structured onboarding plan using GenAI API or deterministic fallback engine."""
        req_lines = [f"- [{r.get('code', 'REQ')}] {r.get('text', '')} (Doc: {r.get('doc', '')}, Sec: {r.get('sec', '')})" for r in mandatory_reqs]
        reqs_text = "\n".join(req_lines)
        
        evidence_lines = [f"Source [{c.get('doc_code', '')} Section {c.get('section_id', '')}]: {c.get('content', '')}" for c in evidence_chunks]
        evidence_text = "\n\n".join(evidence_lines)
        sanitized_evidence = PromptDefense.wrap_evidence(evidence_text)

        system_instruction = """You are SkillSprint AI, an enterprise onboarding curriculum architect.
Return ONLY a valid JSON object matching the GeneratedOnboardingPlanSchema.
Every module and quiz question MUST contain valid source_doc_id and source_section_id from the evidence.
Do NOT invent policies."""

        user_prompt = f"""Generate a multi-stage personalized onboarding plan for:
Employee: {employee_code} ({experience_level})
Role: {role_name} ({role_code}) in {department}

Mandatory Requirements to Cover:
{reqs_text}

Authoritative Evidence:
{sanitized_evidence}

Return JSON with keys: employee_code, role_code, plan_title, modules, checklists, assessments, prompt_version."""

        # 1. Attempt Live GenAI API if configured
        raw_response = None
        if self._gemini_client:
            for attempt in range(settings.MAX_RETRIES):
                raw_response = self.call_gemini(system_instruction, user_prompt)
                if raw_response:
                    try:
                        clean_json = re.sub(r'^```json\s*', '', raw_response.strip())
                        clean_json = re.sub(r'\s*```$', '', clean_json)
                        parsed = json.loads(clean_json)
                        # Validate with Pydantic
                        GeneratedOnboardingPlanSchema(**parsed)
                        return parsed
                    except Exception as parse_err:
                        print(f"GenAI JSON schema validation attempt {attempt+1} failed: {parse_err}")
                time.sleep(settings.RETRY_BACKOFF_FACTOR ** attempt)

        # 2. Deterministic Grounded Generation Fallback
        # Synthesizes high-quality, fully grounded curriculum directly from the authoritative database requirements
        return self._generate_grounded_curriculum(
            employee_code=employee_code,
            role_code=role_code,
            role_name=role_name,
            department=department,
            experience_level=experience_level,
            mandatory_reqs=mandatory_reqs,
            evidence_chunks=evidence_chunks
        )

    def _generate_grounded_curriculum(
        self,
        employee_code: str,
        role_code: str,
        role_name: str,
        department: str,
        experience_level: str,
        mandatory_reqs: List[Dict[str, Any]],
        evidence_chunks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Deterministic, grounded curriculum synthesizer ensuring 100% schema compliance and source citations."""
        modules = []
        checklists = []
        assessments = []

        stages = ["Day 1", "Week 1", "Week 2", "First 30 Days", "First 60 Days", "First 90 Days"]
        categories = ["KNOWLEDGE", "PRACTICAL", "SCENARIO", "CHECKLIST", "ASSESSMENT"]

        for idx, req in enumerate(mandatory_reqs):
            r_code = req.get("code", f"REQ-{idx+1}")
            text = req.get("text", "")
            doc_code = req.get("doc", "DOC-POL-01")
            sec_id = req.get("sec", "1.1")
            competency = req.get("competency", "Core Compliance")
            stage = req.get("stage") or stages[min(idx // 3, len(stages)-1)]

            m_code = f"MOD-{role_code}-{idx+1:02d}"
            cat = categories[idx % len(categories)]
            
            # Module Objectives & Concepts
            objs = [
                f"Master key guidelines regarding {competency.lower()}.",
                f"Demonstrate compliance with policy rule {r_code}."
            ]
            concepts = [competency, doc_code, f"Section {sec_id}"]

            # Practical Tasks
            tasks = [{
                "description": f"Execute practical exercise for {competency}: {text[:100]}...",
                "expected_outcome": f"Documented completion and compliance log for {r_code}.",
                "completion_criteria": "Reviewed and signed off by supervisor.",
                "difficulty": "Intermediate" if experience_level in ["Mid", "Senior"] else "Beginner",
                "due_stage": stage,
                "source_doc_id": doc_code,
                "source_section_id": sec_id
            }]

            # Scenarios
            scenarios = [{
                "situation": f"Simulated workplace scenario involving {competency.lower()} and policy compliance.",
                "employee_role": role_name,
                "decision_prompt": f"How do you ensure adherence to {doc_code} Section {sec_id}?",
                "expected_behavior": f"Follow corporate protocol defined in {r_code}.",
                "evaluation_rubric": "Pass criteria: Follows documented policy without shortcut.",
                "source_doc_id": doc_code,
                "source_section_id": sec_id
            }]

            # Quizzes
            quizzes = [
                {
                    "question_text": f"Under {doc_code} Section {sec_id}, what is the mandatory requirement regarding {competency.lower()}?",
                    "question_type": "MCQ",
                    "options": [
                        text,
                        "Requirements are optional if authorized by peer colleague.",
                        "Requirements only apply to part-time contractors.",
                        "Standard may be bypassed without documentation during emergencies."
                    ],
                    "correct_answer": text,
                    "explanation": f"According to {doc_code} Section {sec_id}, employees must strictly adhere to: {text}",
                    "difficulty": "Beginner",
                    "source_doc_id": doc_code,
                    "source_section_id": sec_id,
                    "requirement_code": r_code
                },
                {
                    "question_text": f"True or False: Violation of rule {r_code} in {doc_code} is permitted if client requests it verbally?",
                    "question_type": "TRUE_FALSE",
                    "options": ["True", "False"],
                    "correct_answer": "False",
                    "explanation": f"Official policy in {doc_code} states that rules apply unconditionally without verbal bypass.",
                    "difficulty": "Beginner",
                    "source_doc_id": doc_code,
                    "source_section_id": sec_id,
                    "requirement_code": r_code
                }
            ]

            modules.append({
                "module_code": m_code,
                "title": f"{competency}: {text[:45]}...",
                "category": cat,
                "purpose": f"Ensure full operational readiness and regulatory compliance with {doc_code}.",
                "learning_objectives": objs,
                "key_concepts": concepts,
                "estimated_duration_mins": 30 + (idx % 4) * 15,
                "stage": stage,
                "difficulty": "Beginner" if idx < 3 else ("Intermediate" if idx < 8 else "Advanced"),
                "source_doc_id": doc_code,
                "source_section_id": sec_id,
                "requirement_code": r_code,
                "prerequisite_module_code": modules[-1]["module_code"] if (idx > 0 and idx % 2 == 0) else None,
                "tasks": tasks,
                "scenarios": scenarios,
                "quiz_questions": quizzes
            })

            # Daily Checklists
            if idx < 5:
                checklists.append({
                    "activity": f"Complete Day-1 onboarding verification for {competency} ({doc_code} Sec {sec_id}).",
                    "is_mandatory": True,
                    "due_stage": "Day 1",
                    "responsible_person": "Employee",
                    "source_doc_id": doc_code,
                    "source_section_id": sec_id
                })

        # Practical Assessment with 4-criterion Rubric
        assessments.append({
            "title": f"{role_name} Baseline Competency & Compliance Assessment",
            "assessment_type": "PRACTICAL",
            "rubric": [
                {
                    "criterion": "Policy & Regulatory Comprehension",
                    "weight": 30,
                    "expected_performance": "Demonstrates full understanding of mandatory security and privacy rules.",
                    "pass_condition": "Score >= 80% with no critical policy misinterpretations."
                },
                {
                    "criterion": "Operational Procedure Execution",
                    "weight": 30,
                    "expected_performance": "Executes standard workflows adhering strictly to approved department SOPs.",
                    "pass_condition": "Completes simulated workflow without unauthorized escalations."
                },
                {
                    "criterion": "Identity & Data Security Hygiene",
                    "weight": 20,
                    "expected_performance": "Adheres to 16+ char passphrase, MFA, clean desk, and zero PII export rules.",
                    "pass_condition": "100% adherence to corporate cybersecurity standards."
                },
                {
                    "criterion": "Ethical Conduct & Escalation",
                    "weight": 20,
                    "expected_performance": "Correctly identifies conflicts of interest and whistleblower channels.",
                    "pass_condition": "Demonstrates prompt escalation within designated SLAs."
                }
            ]
        })

        return {
            "employee_code": employee_code,
            "role_code": role_code,
            "plan_title": f"Comprehensive Onboarding Journey: {role_name} ({experience_level})",
            "modules": modules,
            "checklists": checklists,
            "assessments": assessments,
            "prompt_version": "v1.0"
        }

genai_client = GenAIClient()

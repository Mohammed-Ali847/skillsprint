# src/schemas/onboarding_plan.py
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class LearningObjectiveSchema(BaseModel):
    objective_id: str
    description: str

class ChecklistItemSchema(BaseModel):
    activity: str
    is_mandatory: bool = True
    due_stage: str = "Day 1"  # Day 1, Week 1, Week 2, First 30 Days, First 60 Days, First 90 Days
    responsible_person: str = "Employee"
    source_doc_id: str
    source_section_id: str

class PracticalTaskSchema(BaseModel):
    description: str
    expected_outcome: str
    completion_criteria: str
    difficulty: str = "Beginner"  # Beginner, Intermediate, Advanced
    due_stage: str = "Week 1"
    source_doc_id: str
    source_section_id: str

class ScenarioSchema(BaseModel):
    situation: str
    employee_role: str
    decision_prompt: str
    expected_behavior: str
    evaluation_rubric: str
    source_doc_id: str
    source_section_id: str

class QuizQuestionSchema(BaseModel):
    question_text: str
    question_type: str = "MCQ"  # MCQ, MULTIPLE_RESPONSE, TRUE_FALSE, SCENARIO
    options: List[str]
    correct_answer: Any  # string or list of strings
    explanation: str
    difficulty: str = "Beginner"
    source_doc_id: str
    source_section_id: str
    requirement_code: Optional[str] = None

class RubricCriterionSchema(BaseModel):
    criterion: str
    weight: int = 25
    expected_performance: str
    pass_condition: str

class PracticalAssessmentSchema(BaseModel):
    title: str
    assessment_type: str = "PRACTICAL"
    rubric: List[RubricCriterionSchema]

class GeneratedModuleSchema(BaseModel):
    module_code: str
    title: str
    category: str = "KNOWLEDGE"  # KNOWLEDGE, PRACTICAL, SCENARIO, CHECKLIST, ASSESSMENT
    purpose: str
    learning_objectives: List[str]
    key_concepts: List[str]
    estimated_duration_mins: int = 45
    stage: str = "Week 1"
    difficulty: str = "Beginner"
    source_doc_id: str
    source_section_id: str
    requirement_code: str
    prerequisite_module_code: Optional[str] = None
    tasks: List[PracticalTaskSchema] = []
    scenarios: List[ScenarioSchema] = []
    quiz_questions: List[QuizQuestionSchema] = []

class GeneratedOnboardingPlanSchema(BaseModel):
    employee_code: str
    role_code: str
    plan_title: str
    modules: List[GeneratedModuleSchema]
    checklists: List[ChecklistItemSchema]
    assessments: List[PracticalAssessmentSchema]
    prompt_version: str = "v1.0"

import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from src.database.session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="employee")  # admin, training_manager, reviewer, manager, employee
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    employee = relationship("Employee", back_populates="user", uselist=False)
    review_actions = relationship("ReviewAction", back_populates="reviewer")
    audit_logs = relationship("AuditLog", back_populates="user")


class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    
    roles = relationship("Role", back_populates="department")
    employees = relationship("Employee", back_populates="department")
    documents = relationship("Document", back_populates="department")


class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    description = Column(Text, default="")
    experience_level = Column(String(50), default="Junior")  # Junior, Mid, Senior
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    department = relationship("Department", back_populates="roles")
    employees = relationship("Employee", back_populates="role")
    role_requirements = relationship("RoleRequirement", back_populates="role")
    onboarding_plans = relationship("OnboardingPlan", back_populates="role")


class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    employee_code = Column(String(50), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    experience_level = Column(String(50), default="Junior")
    location = Column(String(100), default="Headquarters")
    joining_date = Column(DateTime, default=datetime.datetime.utcnow)
    reporting_manager = Column(String(255), default="Department Head")
    training_status = Column(String(50), default="On Track")  # On Track, Requires Attention, Behind Schedule, Assessment Required, Completed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="employee")
    role = relationship("Role", back_populates="employees")
    department = relationship("Department", back_populates="employees")
    onboarding_plans = relationship("OnboardingPlan", back_populates="employee")
    quiz_attempts = relationship("QuizAttempt", back_populates="employee")
    adaptive_recommendations = relationship("AdaptiveRecommendation", back_populates="employee")


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    doc_code = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    doc_type = Column(String(50), default="POLICY")  # POLICY, SOP, FAQ, HANDBOOK, ROLE_DESCRIPTION, COMPLIANCE
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    current_version = Column(String(20), default="1.0")
    file_path = Column(String(500), default="")
    file_format = Column(String(20), default="pdf")  # pdf, docx, txt, md
    checksum = Column(String(64), index=True, default="")
    is_active = Column(Boolean, default=True)
    is_flagged_adversarial = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    department = relationship("Department", back_populates="documents")
    versions = relationship("DocumentVersion", back_populates="document", cascade="all, delete-orphan")
    requirements = relationship("Requirement", back_populates="document")


class DocumentVersion(Base):
    __tablename__ = "document_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    version_str = Column(String(20), nullable=False)  # e.g., 1.0, 2.0
    effective_date = Column(DateTime, default=datetime.datetime.utcnow)
    expiry_date = Column(DateTime, nullable=True)
    change_summary = Column(Text, default="")
    is_active = Column(Boolean, default=True)
    superseded_by = Column(String(20), nullable=True)
    precedence_level = Column(Integer, default=1)  # 1: Policy, 2: SOP, 3: FAQ, 4: Informal Guidance
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    document = relationship("Document", back_populates="versions")
    chunks = relationship("DocumentChunk", back_populates="version", cascade="all, delete-orphan")
    requirements = relationship("Requirement", back_populates="version")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    version_id = Column(Integer, ForeignKey("document_versions.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    section_id = Column(String(100), default="")
    section_heading = Column(String(255), default="")
    page_number = Column(Integer, default=1)
    paragraph_ref = Column(String(100), default="")
    content = Column(Text, nullable=False)
    embedding_json = Column(Text, default="[]")  # Float array as JSON
    token_count = Column(Integer, default=0)
    
    version = relationship("DocumentVersion", back_populates="chunks")


class Requirement(Base):
    __tablename__ = "requirements"
    
    id = Column(Integer, primary_key=True, index=True)
    req_code = Column(String(50), unique=True, index=True, nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    version_id = Column(Integer, ForeignKey("document_versions.id"), nullable=False)
    section_id = Column(String(100), default="")
    requirement_text = Column(Text, nullable=False)
    category = Column(String(50), default="MUST_KNOW")  # MUST_KNOW, MUST_COMPLETE, MUST_DEMONSTRATE, MUST_ACKNOWLEDGE, RECOMMENDED, OPTIONAL, NOT_APPLICABLE
    is_mandatory = Column(Boolean, default=True)
    competency = Column(String(255), default="General Compliance")
    default_priority = Column(String(50), default="High")  # Critical, High, Medium, Low
    default_due_stage = Column(String(50), default="Week 1")  # Day 1, Week 1, Week 2, First 30 Days, First 60 Days, First 90 Days
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    document = relationship("Document", back_populates="requirements")
    version = relationship("DocumentVersion", back_populates="requirements")
    role_requirements = relationship("RoleRequirement", back_populates="requirement")
    learning_modules = relationship("LearningModule", back_populates="requirement")


class RoleRequirement(Base):
    __tablename__ = "role_requirements"
    
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    is_mandatory = Column(Boolean, default=True)
    priority = Column(String(50), default="High")
    due_stage = Column(String(50), default="Week 1")
    specific_instructions = Column(Text, default="")
    
    role = relationship("Role", back_populates="role_requirements")
    requirement = relationship("Requirement", back_populates="role_requirements")


class OnboardingPlan(Base):
    __tablename__ = "onboarding_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    title = Column(String(255), nullable=False)
    status = Column(String(50), default="DRAFT")  # DRAFT, VERIFIED, VERIFIED_WITH_WARNING, INCOMPLETE, UNSUPPORTED, CONTRADICTORY, MANUAL_REVIEW_REQUIRED, APPROVED, ACTIVE, COMPLETED
    version = Column(Integer, default=1)
    prompt_version = Column(String(50), default="v1.0")
    model_used = Column(String(100), default="gemini-2.5-flash")
    coverage_score = Column(Float, default=0.0)
    traceability_score = Column(Float, default=0.0)
    consistency_score = Column(Float, default=100.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    employee = relationship("Employee", back_populates="onboarding_plans")
    role = relationship("Role", back_populates="onboarding_plans")
    learning_modules = relationship("LearningModule", back_populates="plan", cascade="all, delete-orphan")
    checklists = relationship("Checklist", back_populates="plan", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="plan", cascade="all, delete-orphan")
    scenarios = relationship("Scenario", back_populates="plan", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="plan", cascade="all, delete-orphan")
    validation_results = relationship("ValidationResult", back_populates="plan", cascade="all, delete-orphan")
    review_actions = relationship("ReviewAction", back_populates="plan", cascade="all, delete-orphan")


class LearningModule(Base):
    __tablename__ = "learning_modules"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("onboarding_plans.id"), nullable=False)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=True)
    module_code = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(String(50), default="KNOWLEDGE")  # KNOWLEDGE, PRACTICAL, SCENARIO, CHECKLIST, ASSESSMENT
    purpose = Column(Text, default="")
    learning_objectives = Column(Text, default="[]")  # JSON list
    key_concepts = Column(Text, default="[]")  # JSON list
    estimated_duration_mins = Column(Integer, default=45)
    stage = Column(String(50), default="Week 1")  # Day 1, Week 1, Week 2, First 30 Days, First 60 Days, First 90 Days
    difficulty = Column(String(50), default="Beginner")  # Beginner, Intermediate, Advanced
    source_doc_id = Column(String(50), default="")
    source_section_id = Column(String(100), default="")
    verification_status = Column(String(50), default="VERIFIED")
    status = Column(String(50), default="ASSIGNED")  # ASSIGNED, IN_PROGRESS, COMPLETED, SKIPPED
    
    plan = relationship("OnboardingPlan", back_populates="learning_modules")
    requirement = relationship("Requirement", back_populates="learning_modules")
    quizzes = relationship("Quiz", back_populates="module", cascade="all, delete-orphan")


class Checklist(Base):
    __tablename__ = "checklists"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("onboarding_plans.id"), nullable=False)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=True)
    activity = Column(Text, nullable=False)
    is_mandatory = Column(Boolean, default=True)
    due_stage = Column(String(50), default="Day 1")
    status = Column(String(50), default="PENDING")  # PENDING, COMPLETED, SKIPPED
    source_doc_id = Column(String(50), default="")
    source_section_id = Column(String(100), default="")
    responsible_person = Column(String(255), default="Employee")
    completed_at = Column(DateTime, nullable=True)
    
    plan = relationship("OnboardingPlan", back_populates="checklists")


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("onboarding_plans.id"), nullable=False)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=True)
    description = Column(Text, nullable=False)
    expected_outcome = Column(Text, default="")
    completion_criteria = Column(Text, default="")
    difficulty = Column(String(50), default="Beginner")
    due_stage = Column(String(50), default="Week 1")
    status = Column(String(50), default="PENDING")  # PENDING, IN_PROGRESS, SUBMITTED, APPROVED
    source_doc_id = Column(String(50), default="")
    source_section_id = Column(String(100), default="")
    submitted_evidence = Column(Text, default="")
    completed_at = Column(DateTime, nullable=True)
    
    plan = relationship("OnboardingPlan", back_populates="tasks")


class Scenario(Base):
    __tablename__ = "scenarios"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("onboarding_plans.id"), nullable=False)
    module_id = Column(Integer, ForeignKey("learning_modules.id"), nullable=True)
    situation = Column(Text, nullable=False)
    employee_role = Column(String(100), default="")
    decision_prompt = Column(Text, default="")
    expected_behavior = Column(Text, default="")
    evaluation_rubric = Column(Text, default="")
    source_doc_id = Column(String(50), default="")
    source_section_id = Column(String(100), default="")
    
    plan = relationship("OnboardingPlan", back_populates="scenarios")


class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("learning_modules.id"), nullable=False)
    title = Column(String(255), nullable=False)
    passing_score = Column(Float, default=70.0)
    
    module = relationship("LearningModule", back_populates="quizzes")
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("QuizAttempt", back_populates="quiz")


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), default="MCQ")  # MCQ, MULTIPLE_RESPONSE, TRUE_FALSE, SCENARIO
    options_json = Column(Text, nullable=False)  # JSON list of options
    correct_answer_json = Column(Text, nullable=False)  # JSON list/string of correct option(s)
    explanation = Column(Text, default="")
    difficulty = Column(String(50), default="Beginner")
    source_doc_id = Column(String(50), default="")
    source_section_id = Column(String(100), default="")
    
    quiz = relationship("Quiz", back_populates="questions")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    score = Column(Float, default=0.0)
    passed = Column(Boolean, default=False)
    answers_json = Column(Text, default="{}")
    completed_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    employee = relationship("Employee", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")


class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("onboarding_plans.id"), nullable=False)
    title = Column(String(255), nullable=False)
    assessment_type = Column(String(50), default="PRACTICAL")  # KNOWLEDGE, PRACTICAL, SCENARIO, ROLE_SPECIFIC
    rubric_json = Column(Text, default="[]")  # List of {criterion, weight, expected_performance, pass_condition}
    score = Column(Float, nullable=True)
    status = Column(String(50), default="ASSIGNED")  # ASSIGNED, SUBMITTED, PASSED, FAILED
    feedback = Column(Text, default="")
    
    plan = relationship("OnboardingPlan", back_populates="assessments")


class Prerequisite(Base):
    __tablename__ = "prerequisites"
    
    id = Column(Integer, primary_key=True, index=True)
    dependent_module_id = Column(Integer, ForeignKey("learning_modules.id"), nullable=False)
    prerequisite_module_id = Column(Integer, ForeignKey("learning_modules.id"), nullable=False)
    dependency_type = Column(String(50), default="MANDATORY")  # MANDATORY, RECOMMENDED


class ValidationResult(Base):
    __tablename__ = "validation_results"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("onboarding_plans.id"), nullable=False)
    run_at = Column(DateTime, default=datetime.datetime.utcnow)
    coverage_score = Column(Float, default=0.0)
    traceability_score = Column(Float, default=0.0)
    consistency_score = Column(Float, default=100.0)
    missing_req_count = Column(Integer, default=0)
    unsupported_count = Column(Integer, default=0)
    contradiction_count = Column(Integer, default=0)
    duplicate_count = Column(Integer, default=0)
    details_json = Column(Text, default="{}")
    comparison_json = Column(Text, default="[]")
    overall_status = Column(String(50), default="VERIFIED")
    
    plan = relationship("OnboardingPlan", back_populates="validation_results")


class ReviewAction(Base):
    __tablename__ = "review_actions"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("onboarding_plans.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(50), nullable=False)  # APPROVE, REJECT, EDIT, REGENERATE, OVERRIDE
    notes = Column(Text, default="")
    original_status = Column(String(50), default="")
    override_status = Column(String(50), default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    plan = relationship("OnboardingPlan", back_populates="review_actions")
    reviewer = relationship("User", back_populates="review_actions")


class PolicyImpactRecord(Base):
    __tablename__ = "policy_impact_records"
    
    id = Column(Integer, primary_key=True, index=True)
    old_version_id = Column(Integer, ForeignKey("document_versions.id"), nullable=True)
    new_version_id = Column(Integer, ForeignKey("document_versions.id"), nullable=False)
    detected_changes_json = Column(Text, default="[]")
    affected_reqs_json = Column(Text, default="[]")
    affected_roles_json = Column(Text, default="[]")
    affected_modules_json = Column(Text, default="[]")
    affected_quizzes_json = Column(Text, default="[]")
    affected_employees_json = Column(Text, default="[]")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class AdaptiveRecommendation(Base):
    __tablename__ = "adaptive_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    reason = Column(Text, nullable=False)
    weak_topic = Column(String(255), default="")
    recommended_module_id = Column(Integer, ForeignKey("learning_modules.id"), nullable=True)
    recommendation_type = Column(String(50), default="REVISION_MODULE")  # REVISION_MODULE, ADDITIONAL_QUIZ, ADDITIONAL_TASK, ADVANCED_MODULE, MANAGER_REVIEW
    status = Column(String(50), default="ACTIVE")  # ACTIVE, DISMISSED, COMPLETED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    employee = relationship("Employee", back_populates="adaptive_recommendations")
    recommended_module = relationship("LearningModule")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(String(100), nullable=False)
    payload_before = Column(Text, default="")
    payload_after = Column(Text, default="")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="audit_logs")

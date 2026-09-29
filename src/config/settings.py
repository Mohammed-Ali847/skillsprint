import os

# Automatically load .env file if present
_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_env_file = os.path.join(_base_dir, ".env")
if os.path.exists(_env_file):
    with open(_env_file, "r", encoding="utf-8") as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                _k = _k.strip()
                _v = _v.strip()
                if _k and _k not in os.environ:
                    os.environ[_k] = _v

class Settings:
    PROJECT_NAME: str = "SkillSprint AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')), 'skillsprint.db')}")
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "skillsprint-ai-competition-super-secret-key-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY", ""))
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-004")
    LLM_TEMPERATURE: float = 0.2
    MAX_RETRIES: int = 3
    RETRY_BACKOFF_FACTOR: float = 1.5
    
    UPLOAD_DIR: str = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")), "sample_documents")
    REPORTS_DIR: str = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")), "reports")
    PROMPTS_DIR: str = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")), "src", "prompt_templates")
    MAX_FILE_SIZE_MB: int = 25
    ALLOWED_EXTENSIONS: set = {".pdf", ".docx", ".txt", ".md", ".csv"}

settings = Settings()

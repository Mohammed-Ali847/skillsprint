# src/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.config.settings import settings
from src.database.session import init_db
from src.api.routes import router as api_router

# Initialize FastAPI App
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="SkillSprint AI: Enterprise Generative AI-Powered Training & Onboarding Intelligence Platform with Independent Python Ground-Truth Validation (TechWiz 7 Competition SRS v1.0).",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router, prefix="/api")

# Mount Static Assets
static_dir = os.path.join(settings.BASE_DIR, "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def serve_index():
    index_path = os.path.join(settings.BASE_DIR, "templates", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "api_docs": "/docs",
        "message": "Templates directory initialized."
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "dual_pipeline": {
            "genai_generation_pipeline": "active",
            "python_ground_truth_validator": "active"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

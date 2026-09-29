# src/services/version_service.py
import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from src.database import models

class VersionService:
    """Manages document versions, activation states, and obsolescence tracking."""

    @staticmethod
    def get_active_version(db: Session, document_id: int) -> Optional[models.DocumentVersion]:
        now = datetime.datetime.utcnow()
        return db.query(models.DocumentVersion).filter(
            models.DocumentVersion.document_id == document_id,
            models.DocumentVersion.is_active == True,
            models.DocumentVersion.effective_date <= now
        ).order_by(models.DocumentVersion.effective_date.desc()).first()

    @staticmethod
    def register_new_version(
        db: Session,
        document_id: int,
        version_str: str,
        effective_date: datetime.datetime,
        change_summary: str,
        precedence_level: int = 1
    ) -> models.DocumentVersion:
        """Registers a new document version and supersedes older active versions."""
        # Find existing active versions
        existing_active = db.query(models.DocumentVersion).filter(
            models.DocumentVersion.document_id == document_id,
            models.DocumentVersion.is_active == True
        ).all()

        for old_v in existing_active:
            old_v.is_active = False
            old_v.superseded_by = version_str
            old_v.expiry_date = effective_date

        new_v = models.DocumentVersion(
            document_id=document_id,
            version_str=version_str,
            effective_date=effective_date,
            change_summary=change_summary,
            is_active=True,
            superseded_by=None,
            precedence_level=precedence_level
        )
        db.add(new_v)
        
        # Update current version string on parent document
        doc = db.query(models.Document).filter(models.Document.id == document_id).first()
        if doc:
            doc.current_version = version_str
            
        db.commit()
        db.refresh(new_v)
        return new_v

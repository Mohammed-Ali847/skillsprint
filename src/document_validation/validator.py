# src/document_validation/validator.py
import os, hashlib
from typing import Tuple, Dict, Any, Optional
from sqlalchemy.orm import Session
from src.database import models
from src.config.settings import settings

class DocumentValidator:
    """Validates uploaded company documents before ingestion."""

    @staticmethod
    def calculate_checksum(file_bytes: bytes) -> str:
        return hashlib.sha256(file_bytes).hexdigest()

    @classmethod
    def validate_upload(cls, filename: str, file_bytes: bytes, db: Optional[Session] = None) -> Tuple[bool, str, Dict[str, Any]]:
        # 1. Check file size
        size_bytes = len(file_bytes)
        if size_bytes == 0:
            return False, "File is empty (0 bytes).", {}
            
        max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        if size_bytes > max_bytes:
            return False, f"File size exceeds maximum limit of {settings.MAX_FILE_SIZE_MB}MB.", {}

        # 2. Check extension
        ext = os.path.splitext(filename)[1].lower()
        if ext not in settings.ALLOWED_EXTENSIONS:
            return False, f"Unsupported file extension '{ext}'. Allowed formats: {list(settings.ALLOWED_EXTENSIONS)}", {}

        # 3. Calculate checksum
        checksum = cls.calculate_checksum(file_bytes)

        # 4. Check for duplicate if DB session is provided
        if db:
            existing = db.query(models.Document).filter(models.Document.checksum == checksum).first()
            if existing:
                return False, f"Duplicate document detected: Identical file already uploaded under code '{existing.doc_code}'.", {"existing_id": existing.id}

        metadata = {
            "filename": filename,
            "file_format": ext.replace(".", ""),
            "size_bytes": size_bytes,
            "checksum": checksum
        }
        return True, "File passed pre-ingestion validation.", metadata

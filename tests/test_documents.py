import os
from pathlib import Path
import pytest
from datetime import datetime, timedelta

from src.document_validation.validator import DocumentValidator
from src.document_processing.parser import DocumentParser
from src.document_processing.chunker import DocumentChunker
from src.services.precedence_service import PrecedenceService
from src.database import models

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def test_document_validator_checksum():
    content = b"Sample policy content for ApexNova Global"
    checksum = DocumentValidator.calculate_checksum(content)
    assert len(checksum) == 64
    assert checksum == DocumentValidator.calculate_checksum(content)

def test_document_validator_empty_file():
    valid, msg, meta = DocumentValidator.validate_upload("test.pdf", b"")
    assert not valid
    assert "empty" in msg.lower()

def test_document_validator_oversized_file():
    oversized = b"0" * (26 * 1024 * 1024)  # 26MB exceeds 25MB
    valid, msg, meta = DocumentValidator.validate_upload("huge.pdf", oversized)
    assert not valid
    assert "exceeds" in msg.lower()

def test_document_validator_unsupported_ext():
    valid, msg, meta = DocumentValidator.validate_upload("payload.exe", b"executable bytes")
    assert not valid
    assert "unsupported" in msg.lower()

def test_document_validator_valid_upload():
    content = b"ApexNova Information Security Policy v2.0"
    valid, msg, meta = DocumentValidator.validate_upload("policy.pdf", content)
    assert valid
    assert meta["file_format"] == "pdf"
    assert meta["size_bytes"] == len(content)

def test_document_parser_pdf():
    pdf_path = PROJECT_ROOT / "sample_documents" / "pdf" / "DOC-POL-01.pdf"
    if pdf_path.exists():
        sections = DocumentParser.parse_pdf(str(pdf_path))
        assert len(sections) > 0
        assert any("Section" in s["heading"] or "1." in s["id"] or len(s["content"]) > 10 for s in sections)

def test_document_parser_docx():
    docx_path = PROJECT_ROOT / "sample_documents" / "docx" / "DOC-POL-01.docx"
    if docx_path.exists():
        sections = DocumentParser.parse_docx(str(docx_path))
        assert len(sections) > 0
        assert any(len(s["content"]) > 10 for s in sections)

def test_document_parser_text():
    text_path = PROJECT_ROOT / "sample_documents" / "text" / "DOC-POL-01.md"
    if text_path.exists():
        sections = DocumentParser.parse_file(str(text_path))
        assert len(sections) > 0
        assert sections[0]["content"]

def test_document_chunker():
    sections = [
        {
            "id": "1.1",
            "heading": "Password Rotation and Complexity",
            "content": "All employees must rotate corporate passwords every 90 days. Passwords must be at least 14 characters with uppercase, lowercase, numbers, and symbols. MFA is mandatory across all cloud environments.",
            "page": 1
        },
        {
            "id": "1.2",
            "heading": "Remote Device Encryption",
            "content": "All corporate laptops must enable AES-256 BitLocker or FileVault disk encryption. Local admin access is revoked by default.",
            "page": 1
        }
    ]
    chunks = DocumentChunker.chunk_sections(sections, max_chunk_words=100)
    assert len(chunks) >= 2
    assert chunks[0]["token_count"] > 0
    assert "chunk_index" in chunks[0]

def test_precedence_hierarchy_policy_over_sop():
    doc_pol = models.Document(doc_code="DOC-POL-01", title="Security Policy", doc_type="POLICY")
    ver_pol = models.DocumentVersion(version_str="1.0", precedence_level=1, effective_date=datetime(2025, 1, 1))

    doc_sop = models.Document(doc_code="DOC-SOP-01", title="Onboarding SOP", doc_type="SOP")
    ver_sop = models.DocumentVersion(version_str="1.0", precedence_level=2, effective_date=datetime(2025, 1, 1))

    winner_doc, winner_ver, rationale = PrecedenceService.resolve_conflict(doc_pol, ver_pol, doc_sop, ver_sop)
    assert winner_doc.doc_type == "POLICY"
    assert "higher authority" in rationale.lower()

def test_precedence_hierarchy_sop_over_faq():
    doc_sop = models.Document(doc_code="DOC-SOP-01", title="Onboarding SOP", doc_type="SOP")
    ver_sop = models.DocumentVersion(version_str="1.0", precedence_level=2, effective_date=datetime(2025, 1, 1))

    doc_faq = models.Document(doc_code="DOC-FAQ-01", title="Onboarding FAQ", doc_type="FAQ")
    ver_faq = models.DocumentVersion(version_str="1.0", precedence_level=3, effective_date=datetime(2025, 1, 1))

    winner_doc, winner_ver, rationale = PrecedenceService.resolve_conflict(doc_sop, ver_sop, doc_faq, ver_faq)
    assert winner_doc.doc_type == "SOP"

def test_precedence_date_newer_wins_same_type():
    doc_a = models.Document(doc_code="DOC-POL-01", title="Security Policy v1", doc_type="POLICY")
    ver_a = models.DocumentVersion(version_str="1.0", precedence_level=1, effective_date=datetime(2024, 1, 1))

    doc_b = models.Document(doc_code="DOC-POL-01-REV", title="Security Policy v2", doc_type="POLICY")
    ver_b = models.DocumentVersion(version_str="2.0", precedence_level=1, effective_date=datetime(2025, 6, 1))

    winner_doc, winner_ver, rationale = PrecedenceService.resolve_conflict(doc_a, ver_a, doc_b, ver_b)
    assert winner_ver.version_str == "2.0"
    assert "newer" in rationale.lower()

# src/document_processing/parser.py
import os, re
from typing import List, Dict, Any, Optional
from pypdf import PdfReader
from docx import Document as DocxDocument

class DocumentParser:
    """Extracts structured text, headings, sections, and metadata from PDF, DOCX, TXT, and Markdown files."""

    @staticmethod
    def parse_pdf(file_path: str) -> List[Dict[str, Any]]:
        """Parses a PDF file page by page, detecting sections and paragraph structures."""
        reader = PdfReader(file_path)
        sections = []
        full_text = ""
        current_section = {"id": "1.0", "heading": "General", "content": "", "page": 1}
        
        for page_idx, page in enumerate(reader.pages):
            page_num = page_idx + 1
            text = page.extract_text() or ""
            full_text += f"\n--- Page {page_num} ---\n" + text
            
            lines = text.split("\n")
            for line in lines:
                line_str = line.strip()
                if not line_str:
                    continue
                # Heading / Section regex pattern (e.g., Section 1.2: Title or 1.2 Heading)
                match = re.match(r'^(?:Section\s+)?(\d+\.[\d\.]*)\s*:?\s*(.+)$', line_str, re.IGNORECASE)
                if match:
                    if current_section["content"].strip():
                        sections.append(current_section)
                    current_section = {
                        "id": match.group(1).rstrip("."),
                        "heading": match.group(2).strip(),
                        "content": "",
                        "page": page_num
                    }
                else:
                    current_section["content"] += (" " + line_str if current_section["content"] else line_str)
                    
        if current_section["content"].strip():
            sections.append(current_section)
            
        if not sections:
            # Fallback if no specific section headings were regex matched
            sections.append({
                "id": "1.0",
                "heading": os.path.basename(file_path),
                "content": full_text.strip(),
                "page": 1
            })
            
        return sections

    @staticmethod
    def parse_docx(file_path: str) -> List[Dict[str, Any]]:
        """Parses DOCX document retaining paragraph headings, bullet points, and sections."""
        doc = DocxDocument(file_path)
        sections = []
        current_section = {"id": "1.0", "heading": "Introduction", "content": "", "page": 1}
        
        para_idx = 1
        for p in doc.paragraphs:
            text = p.text.strip()
            if not text:
                continue
                
            is_heading = p.style.name.startswith("Heading") or text.startswith("Section ") or text.startswith("## ")
            sec_match = re.match(r'^(?:##\s*|Section\s+)?(\d+\.[\d\.]*)\s*:?\s*(.+)$', text, re.IGNORECASE)
            
            if is_heading and sec_match:
                if current_section["content"].strip():
                    sections.append(current_section)
                current_section = {
                    "id": sec_match.group(1).rstrip("."),
                    "heading": sec_match.group(2).strip(),
                    "content": "",
                    "page": (para_idx // 15) + 1
                }
            elif is_heading and not sec_match:
                if current_section["content"].strip():
                    sections.append(current_section)
                current_section = {
                    "id": f"sec-{len(sections)+1}",
                    "heading": text.replace("##", "").strip(),
                    "content": "",
                    "page": (para_idx // 15) + 1
                }
            else:
                current_section["content"] += (" " + text if current_section["content"] else text)
                
            para_idx += 1
            
        if current_section["content"].strip():
            sections.append(current_section)
            
        return sections

    @staticmethod
    def parse_text_or_md(file_path: str) -> List[Dict[str, Any]]:
        """Parses Markdown or plain text into sections based on markdown headings."""
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            
        sections = []
        current_section = {"id": "1.0", "heading": "General Content", "content": "", "page": 1}
        
        line_idx = 1
        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue
                
            md_match = re.match(r'^(?:#+|\d+\.)\s*(?:Section\s+)?(\d+\.[\d\.]*)?\s*:?\s*(.+)$', line_str)
            if md_match and (line_str.startswith("#") or line_str.startswith("Section")):
                if current_section["content"].strip():
                    sections.append(current_section)
                sec_id = md_match.group(1) or f"sec-{len(sections)+1}"
                current_section = {
                    "id": sec_id.rstrip("."),
                    "heading": md_match.group(2).strip(),
                    "content": "",
                    "page": (line_idx // 40) + 1
                }
            else:
                current_section["content"] += (" " + line_str if current_section["content"] else line_str)
                
            line_idx += 1
            
        if current_section["content"].strip():
            sections.append(current_section)
            
        return sections

    @classmethod
    def parse_file(cls, file_path: str) -> List[Dict[str, Any]]:
        """Auto-detects format and parses into standardized section dictionaries."""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return cls.parse_pdf(file_path)
        elif ext == ".docx":
            return cls.parse_docx(file_path)
        elif ext in [".txt", ".md", ".csv"]:
            return cls.parse_text_or_md(file_path)
        else:
            raise ValueError(f"Unsupported document format: {ext}")

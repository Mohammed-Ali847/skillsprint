# src/document_processing/chunker.py
from typing import List, Dict, Any

class DocumentChunker:
    """Splits parsed sections into manageable, traceable chunks with preserved metadata."""

    @staticmethod
    def chunk_sections(sections: List[Dict[str, Any]], max_chunk_words: int = 250, overlap_words: int = 30) -> List[Dict[str, Any]]:
        chunks = []
        global_chunk_idx = 1
        
        for sec in sections:
            sec_id = sec.get("id", "1.0")
            sec_heading = sec.get("heading", "General")
            page_num = sec.get("page", 1)
            content = sec.get("content", "").strip()
            
            words = content.split()
            if not words:
                continue
                
            if len(words) <= max_chunk_words:
                chunks.append({
                    "chunk_index": global_chunk_idx,
                    "section_id": sec_id,
                    "section_heading": sec_heading,
                    "page_number": page_num,
                    "paragraph_ref": f"Section {sec_id}",
                    "content": content,
                    "token_count": len(words) * 2
                })
                global_chunk_idx += 1
            else:
                # Sliding window chunking
                start = 0
                part_idx = 1
                while start < len(words):
                    end = min(start + max_chunk_words, len(words))
                    chunk_text = " ".join(words[start:end])
                    chunks.append({
                        "chunk_index": global_chunk_idx,
                        "section_id": f"{sec_id}.{part_idx}" if part_idx > 1 else sec_id,
                        "section_heading": f"{sec_heading} (Part {part_idx})" if part_idx > 1 else sec_heading,
                        "page_number": page_num,
                        "paragraph_ref": f"Section {sec_id} Para {part_idx}",
                        "content": chunk_text,
                        "token_count": len(words[start:end]) * 2
                    })
                    global_chunk_idx += 1
                    part_idx += 1
                    if end == len(words):
                        break
                    start += (max_chunk_words - overlap_words)
                    
        return chunks

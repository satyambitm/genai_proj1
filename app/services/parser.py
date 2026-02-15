"""
Parser Service — Extracts text from uploaded medical report files.

Supports:
- PDF files (via PyMuPDF)
- Images (PNG, JPG, JPEG) — encoded to base64 for GPT-4 Vision
- Plain text files
"""

import base64
import fitz  # PyMuPDF
from pathlib import Path
from typing import Optional


def parse_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file using PyMuPDF.
    
    Args:
        file_path: Path to the PDF file.
    
    Returns:
        Extracted text content from all pages.
    """
    doc = fitz.open(file_path)
    text_parts = []

    for page_num, page in enumerate(doc, start=1):
        page_text = page.get_text("text")
        if page_text.strip():
            text_parts.append(f"--- Page {page_num} ---\n{page_text.strip()}")

    doc.close()
    return "\n\n".join(text_parts)


def parse_image(file_path: str) -> str:
    """
    Encode an image file to base64 string for GPT-4 Vision API.
    
    Args:
        file_path: Path to the image file (PNG, JPG, JPEG).
    
    Returns:
        Base64-encoded image string.
    """
    with open(file_path, "rb") as f:
        image_bytes = f.read()
    return base64.b64encode(image_bytes).decode("utf-8")


def parse_text(file_path: str) -> str:
    """
    Read content from a plain text file.
    
    Args:
        file_path: Path to the text file.
    
    Returns:
        Text content of the file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def detect_file_type(filename: str) -> str:
    """
    Detect the file type from the filename extension.
    
    Returns:
        'pdf', 'image', or 'text'
    """
    ext = Path(filename).suffix.lower().lstrip(".")
    if ext == "pdf":
        return "pdf"
    elif ext in ("png", "jpg", "jpeg"):
        return "image"
    elif ext == "txt":
        return "text"
    else:
        raise ValueError(f"Unsupported file type: .{ext}")


def extract_text(file_path: str, filename: str) -> Optional[str]:
    """
    Extract text from a file based on its type.
    For images, returns None (they need GPT-4 Vision processing).
    
    Args:
        file_path: Path to the saved file.
        filename: Original filename (used to detect type).
    
    Returns:
        Extracted text, or None for image files.
    """
    file_type = detect_file_type(filename)

    if file_type == "pdf":
        text = parse_pdf(file_path)
        if not text.strip():
            # PDF has no selectable text — likely a scanned document
            return None
        return text
    elif file_type == "text":
        return parse_text(file_path)
    elif file_type == "image":
        # Images need GPT-4 Vision — return None to signal that
        return None

    return None

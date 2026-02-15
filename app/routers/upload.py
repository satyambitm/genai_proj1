"""
Upload Router — Handles medical report file uploads.

- POST /api/upload — Upload a medical report file (PDF, PNG, JPG, TXT)
- Validates file type and size
- Extracts text where possible
"""

import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.config import get_settings
from app.models.schemas import UploadResponse
from app.services.parser import detect_file_type, extract_text

router = APIRouter(prefix="/api", tags=["Upload"])
settings = get_settings()


@router.post("/upload", response_model=UploadResponse)
async def upload_report(file: UploadFile = File(..., description="Medical report file")):
    """
    Upload a medical report file for analysis.

    Accepted formats: PDF, PNG, JPG, JPEG, TXT
    Max file size: 10MB (configurable)
    """
    # ── Validate file extension ────────────────────────────────────────
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")

    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: .{ext}. Allowed: {settings.ALLOWED_EXTENSIONS}",
        )

    # ── Read file contents ─────────────────────────────────────────────
    contents = await file.read()
    file_size = len(contents)

    # ── Validate file size ─────────────────────────────────────────────
    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if file_size > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum allowed: {settings.MAX_FILE_SIZE_MB}MB",
        )

    # ── Save file to disk ──────────────────────────────────────────────
    file_id = str(uuid.uuid4())
    safe_filename = f"{file_id}_{file.filename}"
    upload_dir = settings.UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, safe_filename)

    with open(file_path, "wb") as f:
        f.write(contents)

    # ── Detect type & extract text ─────────────────────────────────────
    file_type = detect_file_type(file.filename)
    extracted_text = extract_text(file_path, file.filename)

    return UploadResponse(
        file_id=file_id,
        filename=file.filename,
        file_type=file_type,
        file_size_bytes=file_size,
        extracted_text=extracted_text,
        message=(
            "File uploaded successfully. Text extracted."
            if extracted_text
            else "File uploaded successfully. Image/scanned PDF detected — will use GPT-4 Vision for analysis."
        ),
    )

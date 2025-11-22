import time
import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings

# Configure media root outside web root
MEDIA_ROOT = Path("uploads").absolute()
MEDIA_ROOT.mkdir(exist_ok=True)

# Configuration
# Use configured limit from settings if available
MAX_FILE_SIZE = getattr(settings, "MAX_FILE_SIZE", 10 * 1024 * 1024)
ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/gif",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def validate_file(file: UploadFile) -> None:
    """Validate file content type and size."""
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file.content_type} not allowed. Allowed: {ALLOWED_CONTENT_TYPES}",
        )


async def save_upload(file: UploadFile, prefix: str = "") -> tuple[str, int]:
    """
    Save uploaded file to MEDIA_ROOT and return (file_path, file_size).
    Validates file as it streams.
    """
    validate_file(file)
    
    # Generate filename
    ext = Path(file.filename).suffix
    filename = f"{prefix}_{int(time.time())}{ext}"
    target = MEDIA_ROOT / filename
    
    # Write file and track size
    file_size = 0
    try:
        with target.open("wb") as buffer:
            while True:
                chunk = await file.read(1024 * 1024)  # Read 1MB at a time
                if not chunk:
                    break
                file_size += len(chunk)
                if file_size > MAX_FILE_SIZE:
                    target.unlink()  # Delete incomplete file
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"File size exceeds {MAX_FILE_SIZE / 1024 / 1024}MB limit",
                    )
                buffer.write(chunk)
    except HTTPException:
        raise
    except Exception as e:
        if target.exists():
            target.unlink()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}",
        )
    
    return str(target), file_size


def get_file_path(file_id: int, filename: str) -> Path:
    """Retrieve path for a stored file (used for serving)."""
    # In production, this would query the DB; here we construct from params
    # This is a security stub; real implementation fetches from DB
    return MEDIA_ROOT / filename


def delete_file(file_path: str) -> None:
    """Delete a file from storage."""
    path = Path(file_path)
    if path.exists() and str(path).startswith(str(MEDIA_ROOT)):
        path.unlink()

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.api.dependencies import get_current_user
from app.core.storage import save_upload, delete_file, MEDIA_ROOT
from pathlib import Path

router = APIRouter(prefix="/api/v1/files", tags=["files"])


class FileUploadResponse(BaseModel):
    id: int
    filename: str
    file_size: int
    content_type: str
    created_at: str


class FileDownloadResponse(FileResponse):
    pass


# In-memory file store for demo; replace with DB queries
_files = {}
_next_id = 1


@router.post("/upload", status_code=201, response_model=dict)
async def upload_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """
    Upload a file. Only authenticated users can upload.
    Validates file type and size before saving.
    """
    global _next_id
    
    # Save file to disk
    file_path, file_size = await save_upload(file, prefix=f"user_{current_user['sub']}")
    
    # Store metadata
    file_id = _next_id
    _files[file_id] = {
        "id": file_id,
        "filename": file.filename,
        "file_path": file_path,
        "content_type": file.content_type,
        "file_size": file_size,
        "user_id": int(current_user["sub"]),
    }
    _next_id += 1
    
    return {
        "id": file_id,
        "filename": file.filename,
        "file_size": file_size,
        "content_type": file.content_type,
    }


@router.get("/{file_id}", response_class=FileResponse)
async def download_file(
    file_id: int,
    current_user: dict = Depends(get_current_user),
):
    """
    Download a file. Only the user who uploaded it can download (or admin).
    """
    file_meta = _files.get(file_id)
    if not file_meta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    # Check authorization
    if file_meta["user_id"] != int(current_user["sub"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to download this file",
        )
    
    file_path = Path(file_meta["file_path"])
    if not file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found on disk")
    
    return FileResponse(
        path=file_path,
        filename=file_meta["filename"],
        media_type=file_meta["content_type"],
    )


@router.delete("/{file_id}", status_code=204)
async def delete_file_endpoint(
    file_id: int,
    current_user: dict = Depends(get_current_user),
):
    """
    Delete a file. Only the user who uploaded it can delete it (or admin).
    """
    file_meta = _files.get(file_id)
    if not file_meta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    # Check authorization
    if file_meta["user_id"] != int(current_user["sub"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this file",
        )
    
    # Delete from disk
    delete_file(file_meta["file_path"])
    
    # Remove from store
    del _files[file_id]
    
    return None

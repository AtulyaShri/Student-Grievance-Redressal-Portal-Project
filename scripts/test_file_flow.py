"""
Manual test for file upload/download flow.
Run with: python scripts/test_file_flow.py
"""
import sys
sys.path.insert(0, r"f:\\student portal\\grievance_portal")

import asyncio
from io import BytesIO
from unittest.mock import Mock
from fastapi import UploadFile
from app.core.storage import save_upload, validate_file, MEDIA_ROOT
from pathlib import Path

async def test_file_flow():
    print(f"MEDIA_ROOT: {MEDIA_ROOT}")
    print(f"MEDIA_ROOT exists: {MEDIA_ROOT.exists()}\n")
    
    # Create a mock file
    file_content = b"This is a test PDF file content"
    mock_file = Mock(spec=UploadFile)
    mock_file.filename = "test_document.pdf"
    mock_file.content_type = "application/pdf"
    mock_file.read = Mock(return_value=file_content)
    
    print("Test 1: Validate file (PDF - allowed)")
    try:
        validate_file(mock_file)
        print("✓ Validation passed\n")
    except Exception as e:
        print(f"✗ Validation failed: {e}\n")
    
    print("Test 2: Validate file (invalid type)")
    mock_file.content_type = "application/x-executable"
    try:
        validate_file(mock_file)
        print("✗ Should have rejected .exe\n")
    except Exception as e:
        print(f"✓ Correctly rejected: {type(e).__name__}\n")
    
    print("Test 3: File size tracking")
    test_file = MEDIA_ROOT / "test_size_check.txt"
    test_file.write_bytes(b"x" * 1000)
    size = test_file.stat().st_size
    print(f"✓ Created {size} byte file at {test_file}\n")
    
    # Cleanup
    test_file.unlink()
    print("✓ Cleanup successful")

if __name__ == "__main__":
    asyncio.run(test_file_flow())

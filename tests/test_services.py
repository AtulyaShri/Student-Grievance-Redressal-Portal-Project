"""
Unit tests for core services (security, storage, email).
"""
import pytest
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_token,
)
from app.core.storage import validate_file
from unittest.mock import Mock
from fastapi import HTTPException


class TestSecurityService:
    """Test password hashing and JWT functions."""

    def test_password_hash_and_verify(self):
        """Test password hashing and verification."""
        password = "TestPassword123!"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed)
        assert not verify_password("WrongPassword", hashed)

    def test_different_hashes_for_same_password(self):
        """Test that same password produces different hashes."""
        password = "TestPassword123!"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        assert hash1 != hash2
        assert verify_password(password, hash1)
        assert verify_password(password, hash2)

    def test_create_access_token(self):
        """Test JWT token creation."""
        data = {"sub": "1", "email": "test@example.com"}
        token = create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_token_success(self):
        """Test JWT token decoding."""
        data = {"sub": "1", "email": "test@example.com"}
        token = create_access_token(data)
        
        payload = decode_token(token)
        assert payload["sub"] == "1"
        assert payload["email"] == "test@example.com"
        assert "exp" in payload

    def test_decode_invalid_token(self):
        """Test decoding invalid token."""
        with pytest.raises(Exception):
            decode_token("invalid.token.here")

    def test_decode_expired_token(self):
        """Test decoding expired token (requires modified expiry)."""
        from datetime import timedelta
        data = {"sub": "1", "email": "test@example.com"}
        # Create token that expires in -1 minute (already expired)
        token = create_access_token(data, expires_delta=timedelta(minutes=-1))
        
        with pytest.raises(Exception):
            decode_token(token)


class TestStorageService:
    """Test file validation."""

    def test_validate_pdf_file(self):
        """Test validation of allowed PDF file."""
        mock_file = Mock()
        mock_file.filename = "document.pdf"
        mock_file.content_type = "application/pdf"
        
        # Should not raise
        validate_file(mock_file)

    def test_validate_image_file(self):
        """Test validation of allowed image file."""
        mock_file = Mock()
        mock_file.filename = "photo.jpg"
        mock_file.content_type = "image/jpeg"
        
        # Should not raise
        validate_file(mock_file)

    def test_validate_invalid_file_type(self):
        """Test validation of disallowed file type."""
        mock_file = Mock()
        mock_file.filename = "malware.exe"
        mock_file.content_type = "application/x-executable"
        
        with pytest.raises(HTTPException) as exc_info:
            validate_file(mock_file)
        assert exc_info.value.status_code == 400

    def test_validate_script_file(self):
        """Test validation of script file."""
        mock_file = Mock()
        mock_file.filename = "script.sh"
        mock_file.content_type = "application/x-sh"
        
        with pytest.raises(HTTPException) as exc_info:
            validate_file(mock_file)
        assert exc_info.value.status_code == 400

    def test_allowed_content_types(self):
        """Test all allowed content types."""
        allowed = [
            "application/pdf",
            "image/jpeg",
            "image/png",
            "image/gif",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ]
        
        for content_type in allowed:
            mock_file = Mock()
            mock_file.filename = "test.bin"
            mock_file.content_type = content_type
            validate_file(mock_file)  # Should not raise

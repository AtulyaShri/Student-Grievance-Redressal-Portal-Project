"""
Integration tests for file upload/download endpoints.
"""
import pytest
from httpx import AsyncClient
from io import BytesIO


class TestFiles:
    """Test file management flows."""

    @pytest.mark.asyncio
    async def test_upload_file_success(
        self,
        async_client: AsyncClient,
        test_user_data,
        test_file_data,
    ):
        """Test successful file upload."""
        # Register and login
        await async_client.post("/api/v1/auth/register", json=test_user_data)
        login_response = await async_client.post("/api/v1/auth/login", json=test_user_data)
        token = login_response.json()["access_token"]

        # Upload file
        files = {"file": (test_file_data["filename"], test_file_data["content"])}
        response = await async_client.post(
            "/api/v1/files/upload",
            files=files,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["filename"] == test_file_data["filename"]
        assert data["file_size"] > 0
        assert data["id"] > 0

    @pytest.mark.asyncio
    async def test_upload_file_unauthorized(self, async_client: AsyncClient, test_file_data):
        """Test file upload without authentication."""
        files = {"file": (test_file_data["filename"], test_file_data["content"])}
        response = await async_client.post("/api/v1/files/upload", files=files)
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_upload_invalid_file_type(
        self,
        async_client: AsyncClient,
        test_user_data,
    ):
        """Test uploading invalid file type."""
        # Register and login
        await async_client.post("/api/v1/auth/register", json=test_user_data)
        login_response = await async_client.post("/api/v1/auth/login", json=test_user_data)
        token = login_response.json()["access_token"]

        # Try to upload .exe file
        files = {"file": ("malware.exe", b"MZ\x90\x00...", "application/x-executable")}
        response = await async_client.post(
            "/api/v1/files/upload",
            files=files,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 400
        assert "not allowed" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_download_file_success(
        self,
        async_client: AsyncClient,
        test_user_data,
        test_file_data,
    ):
        """Test successful file download."""
        # Register and login
        await async_client.post("/api/v1/auth/register", json=test_user_data)
        login_response = await async_client.post("/api/v1/auth/login", json=test_user_data)
        token = login_response.json()["access_token"]

        # Upload file
        files = {"file": (test_file_data["filename"], test_file_data["content"])}
        upload_response = await async_client.post(
            "/api/v1/files/upload",
            files=files,
            headers={"Authorization": f"Bearer {token}"},
        )
        file_id = upload_response.json()["id"]

        # Download file
        response = await async_client.get(
            f"/api/v1/files/{file_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.content == test_file_data["content"]

    @pytest.mark.asyncio
    async def test_download_nonexistent_file(
        self,
        async_client: AsyncClient,
        test_user_data,
    ):
        """Test downloading non-existent file."""
        # Register and login
        await async_client.post("/api/v1/auth/register", json=test_user_data)
        login_response = await async_client.post("/api/v1/auth/login", json=test_user_data)
        token = login_response.json()["access_token"]

        # Try to download non-existent file
        response = await async_client.get(
            "/api/v1/files/999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_file_success(
        self,
        async_client: AsyncClient,
        test_user_data,
        test_file_data,
    ):
        """Test successful file deletion."""
        # Register and login
        await async_client.post("/api/v1/auth/register", json=test_user_data)
        login_response = await async_client.post("/api/v1/auth/login", json=test_user_data)
        token = login_response.json()["access_token"]

        # Upload file
        files = {"file": (test_file_data["filename"], test_file_data["content"])}
        upload_response = await async_client.post(
            "/api/v1/files/upload",
            files=files,
            headers={"Authorization": f"Bearer {token}"},
        )
        file_id = upload_response.json()["id"]

        # Delete file
        response = await async_client.delete(
            f"/api/v1/files/{file_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 204

        # Verify file is deleted
        get_response = await async_client.get(
            f"/api/v1/files/{file_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert get_response.status_code == 404

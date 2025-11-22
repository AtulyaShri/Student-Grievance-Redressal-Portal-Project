"""
Integration tests for complete workflows.
"""
import pytest
from httpx import AsyncClient


class TestFullWorkflow:
    """Test end-to-end workflows combining multiple features."""

    @pytest.mark.asyncio
    async def test_complete_grievance_workflow(
        self,
        async_client: AsyncClient,
    ):
        """
        Complete workflow:
        1. Register user
        2. Login
        3. Upload supporting document
        4. Create grievance with file reference
        5. Retrieve grievance
        6. Update status
        7. Resolve grievance
        """
        # Step 1: Register
        user_data = {"email": "workflow@example.com", "password": "WorkflowPass123!"}
        register_response = await async_client.post(
            "/api/v1/auth/register",
            json=user_data,
        )
        assert register_response.status_code == 201
        user_id = register_response.json()["id"]

        # Step 2: Login
        login_response = await async_client.post(
            "/api/v1/auth/login",
            json=user_data,
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Step 3: Upload file
        file_data = b"%PDF-1.4 test document content"
        files = {"file": ("supporting_doc.pdf", file_data)}
        upload_response = await async_client.post(
            "/api/v1/files/upload",
            files=files,
            headers=headers,
        )
        assert upload_response.status_code == 201
        file_id = upload_response.json()["id"]

        # Step 4: Create grievance
        grievance_data = {
            "title": "Workflow Test Grievance",
            "category": "Academic",
            "description": f"Test grievance with file attachment (ID: {file_id})",
            "dept_id": 1,
        }
        create_response = await async_client.post(
            "/api/v1/grievances",
            json=grievance_data,
            headers=headers,
        )
        assert create_response.status_code == 201
        grievance = create_response.json()
        grievance_id = grievance["id"]
        assert grievance["status"] == "submitted"

        # Step 5: Retrieve grievance
        get_response = await async_client.get(
            f"/api/v1/grievances/{grievance_id}",
            headers=headers,
        )
        assert get_response.status_code == 200
        retrieved = get_response.json()
        assert retrieved["id"] == grievance_id
        assert retrieved["title"] == grievance_data["title"]

        # Step 6: Update status
        update_response = await async_client.patch(
            f"/api/v1/grievances/{grievance_id}",
            json={"status": "in_progress"},
            headers=headers,
        )
        assert update_response.status_code == 200
        updated = update_response.json()
        assert updated["status"] == "in_progress"

        # Step 7: Resolve grievance
        resolve_response = await async_client.post(
            f"/api/v1/grievances/{grievance_id}/resolve",
            json={"resolution": "Issue addressed in meeting with department head"},
            headers=headers,
        )
        assert resolve_response.status_code == 200
        resolved = resolve_response.json()
        assert resolved["status"] == "resolved"

    @pytest.mark.asyncio
    async def test_multiple_users_isolation(
        self,
        async_client: AsyncClient,
    ):
        """Test that different users cannot access each other's resources."""
        # User 1: Register and create grievance
        user1_data = {"email": "user1@example.com", "password": "Pass123!User1"}
        user1_reg = await async_client.post("/api/v1/auth/register", json=user1_data)
        user1_token = (await async_client.post("/api/v1/auth/login", json=user1_data)).json()[
            "access_token"
        ]
        user1_headers = {"Authorization": f"Bearer {user1_token}"}

        grievance_data = {
            "title": "User 1 Grievance",
            "category": "Test",
            "description": "User 1's private grievance",
        }
        user1_grievance = (
            await async_client.post(
                "/api/v1/grievances",
                json=grievance_data,
                headers=user1_headers,
            )
        ).json()

        # User 2: Register and try to access User 1's grievance
        user2_data = {"email": "user2@example.com", "password": "Pass123!User2"}
        user2_reg = await async_client.post("/api/v1/auth/register", json=user2_data)
        user2_token = (await async_client.post("/api/v1/auth/login", json=user2_data)).json()[
            "access_token"
        ]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}

        # User 2 tries to access User 1's grievance (should fail)
        response = await async_client.get(
            f"/api/v1/grievances/{user1_grievance['id']}",
            headers=user2_headers,
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_file_and_grievance_combined(
        self,
        async_client: AsyncClient,
    ):
        """Test uploading files, then using them in grievance context."""
        # Setup user
        user_data = {"email": "fileuser@example.com", "password": "FilePass123!"}
        await async_client.post("/api/v1/auth/register", json=user_data)
        login = await async_client.post("/api/v1/auth/login", json=user_data)
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Upload multiple files
        file_ids = []
        for i in range(3):
            files = {"file": (f"document_{i}.pdf", b"%PDF test content")}
            response = await async_client.post(
                "/api/v1/files/upload",
                files=files,
                headers=headers,
            )
            assert response.status_code == 201
            file_ids.append(response.json()["id"])

        # Create grievance mentioning files
        grievance_data = {
            "title": "Multi-file Grievance",
            "category": "Documentation",
            "description": f"Submitted with files: {', '.join(map(str, file_ids))}",
        }
        grievance_response = await async_client.post(
            "/api/v1/grievances",
            json=grievance_data,
            headers=headers,
        )
        assert grievance_response.status_code == 201

        # Verify all files are still downloadable
        for file_id in file_ids:
            response = await async_client.get(
                f"/api/v1/files/{file_id}",
                headers=headers,
            )
            assert response.status_code == 200

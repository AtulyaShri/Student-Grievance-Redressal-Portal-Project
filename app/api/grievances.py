from fastapi import APIRouter, BackgroundTasks, HTTPException, status, Depends
from pydantic import BaseModel
from app.api.deps import get_current_user
from app.services.notifications import (
    notify_grievance_created,
    notify_grievance_status_changed,
    notify_grievance_assigned,
    notify_grievance_resolved,
)
from app.core.config import settings

router = APIRouter(prefix="/api/v1/grievances", tags=["grievances"])


class GrievanceCreate(BaseModel):
    title: str
    category: str
    description: str
    dept_id: int = None


class GrievanceUpdate(BaseModel):
    status: str


class GrievanceResponse(BaseModel):
    id: int
    title: str
    category: str
    description: str
    status: str
    student_id: int


# In-memory store for demo; replace with DB
_grievances = {}
_next_id = 1


@router.post("/", status_code=201, response_model=GrievanceResponse)
async def create_grievance(
    req: GrievanceCreate,
    current_user: dict = Depends(get_current_user),
    background_tasks: BackgroundTasks = None,
):
    """
    Create a new grievance. Notifies admin and student asynchronously.
    """
    global _next_id
    
    grievance_id = _next_id
    grievance = {
        "id": grievance_id,
        "title": req.title,
        "category": req.category,
        "description": req.description,
        "status": "submitted",
        "student_id": int(current_user["sub"]),
        "student_email": current_user.get("email", "student@example.com"),
        "dept_id": req.dept_id,
    }
    _grievances[grievance_id] = grievance
    _next_id += 1
    
    # Schedule background notification tasks
    if background_tasks:
        background_tasks.add_task(
            notify_grievance_created,
            grievance_id=grievance_id,
            student_email=grievance["student_email"],
            student_name=f"Student {current_user['sub']}",
            title=req.title,
            admin_email=settings.ADMIN_EMAIL,
        )
    
    return GrievanceResponse(**grievance)


@router.get("/{grievance_id}", response_model=GrievanceResponse)
async def get_grievance(
    grievance_id: int,
    current_user: dict = Depends(get_current_user),
):
    """
    Retrieve a grievance. Only the student who created it or admin can view.
    """
    grievance = _grievances.get(grievance_id)
    if not grievance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grievance not found")
    
    # Authorization check (simplified)
    if grievance["student_id"] != int(current_user["sub"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this grievance",
        )
    
    return GrievanceResponse(**grievance)


@router.patch("/{grievance_id}", response_model=GrievanceResponse)
async def update_grievance(
    grievance_id: int,
    req: GrievanceUpdate,
    current_user: dict = Depends(get_current_user),
    background_tasks: BackgroundTasks = None,
):
    """
    Update grievance status. Notifies student of status change asynchronously.
    (Admin/handler only in real app)
    """
    grievance = _grievances.get(grievance_id)
    if not grievance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grievance not found")
    
    old_status = grievance["status"]
    grievance["status"] = req.status
    
    # Schedule notification for status change
    if background_tasks and old_status != req.status:
        background_tasks.add_task(
            notify_grievance_status_changed,
            grievance_id=grievance_id,
            student_email=grievance["student_email"],
            student_name=f"Student {grievance['student_id']}",
            old_status=old_status,
            new_status=req.status,
            title=grievance["title"],
        )
    
    return GrievanceResponse(**grievance)


@router.post("/{grievance_id}/assign", status_code=200)
async def assign_grievance(
    grievance_id: int,
    handler_id: int,
    background_tasks: BackgroundTasks = None,
):
    """
    Assign a grievance to a handler. Notifies handler asynchronously.
    (Admin only in real app)
    """
    grievance = _grievances.get(grievance_id)
    if not grievance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grievance not found")
    
    grievance["handler_id"] = handler_id
    
    # Schedule notification for assignment
    if background_tasks:
        background_tasks.add_task(
            notify_grievance_assigned,
            grievance_id=grievance_id,
            handler_email=f"handler_{handler_id}@example.com",
            handler_name=f"Handler {handler_id}",
            grievance_title=grievance["title"],
        )
    
    return {"status": "assigned", "grievance_id": grievance_id, "handler_id": handler_id}


@router.post("/{grievance_id}/resolve", status_code=200)
async def resolve_grievance(
    grievance_id: int,
    resolution: str = "",
    background_tasks: BackgroundTasks = None,
):
    """
    Mark a grievance as resolved. Notifies student asynchronously.
    """
    grievance = _grievances.get(grievance_id)
    if not grievance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grievance not found")
    
    grievance["status"] = "resolved"
    grievance["resolution"] = resolution
    
    # Schedule notification for resolution
    if background_tasks:
        background_tasks.add_task(
            notify_grievance_resolved,
            grievance_id=grievance_id,
            student_email=grievance["student_email"],
            student_name=f"Student {grievance['student_id']}",
            title=grievance["title"],
            resolution=resolution,
        )
    
    return {"status": "resolved", "grievance_id": grievance_id}

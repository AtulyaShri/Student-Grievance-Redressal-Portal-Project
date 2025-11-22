"""
Notification service for grievance lifecycle events.
Designed to work with FastAPI BackgroundTasks and migrate to Celery/RQ.
"""
from app.core.email import send_email_async
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


def notify_grievance_created(
    grievance_id: int,
    student_email: str,
    student_name: str,
    title: str,
    admin_email: str = settings.ADMIN_EMAIL,
) -> None:
    """Notify admin and student that a new grievance was created."""
    admin_subject = f"New Grievance Submitted: {title}"
    admin_body = f"""
Hello Admin,

A new grievance has been submitted.

Grievance ID: {grievance_id}
Student: {student_name} ({student_email})
Title: {title}

Please log in to review and take action.

Best regards,
Grievance Portal
"""
    send_email_async(admin_email, admin_subject, admin_body)
    
    student_subject = f"Grievance Received: {title}"
    student_body = f"""
Hello {student_name},

Your grievance has been successfully submitted and assigned ID: {grievance_id}.

Title: {title}

You can track the status at any time. We will notify you of updates.

Best regards,
Grievance Portal Team
"""
    send_email_async(student_email, student_subject, student_body)
    logger.info(f"Grievance {grievance_id} notifications sent to {student_email} and admin")


def notify_grievance_status_changed(
    grievance_id: int,
    student_email: str,
    student_name: str,
    old_status: str,
    new_status: str,
    title: str,
) -> None:
    """Notify student when grievance status changes."""
    subject = f"Grievance Status Update: {title}"
    body = f"""
Hello {student_name},

The status of your grievance (ID: {grievance_id}) has been updated.

Previous Status: {old_status}
New Status: {new_status}
Title: {title}

Please log in for more details.

Best regards,
Grievance Portal Team
"""
    send_email_async(student_email, subject, body)
    logger.info(f"Grievance {grievance_id} status changed notification sent to {student_email}")


def notify_grievance_assigned(
    grievance_id: int,
    handler_email: str,
    handler_name: str,
    grievance_title: str,
) -> None:
    """Notify handler/staff when a grievance is assigned to them."""
    subject = f"New Grievance Assigned: {grievance_title}"
    body = f"""
Hello {handler_name},

A grievance has been assigned to you for resolution.

Grievance ID: {grievance_id}
Title: {grievance_title}

Please review and take necessary action.

Best regards,
Grievance Portal
"""
    send_email_async(handler_email, subject, body)
    logger.info(f"Grievance {grievance_id} assignment notification sent to {handler_email}")


def notify_grievance_resolved(
    grievance_id: int,
    student_email: str,
    student_name: str,
    title: str,
    resolution: str = "",
) -> None:
    """Notify student when their grievance is resolved."""
    subject = f"Grievance Resolved: {title}"
    body = f"""
Hello {student_name},

Your grievance (ID: {grievance_id}) has been marked as resolved.

Title: {title}
Resolution: {resolution}

Thank you for bringing this matter to our attention.

Best regards,
Grievance Portal Team
"""
    send_email_async(student_email, subject, body)
    logger.info(f"Grievance {grievance_id} resolution notification sent to {student_email}")

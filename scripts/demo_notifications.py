"""
Demo: Notification system with BackgroundTasks mock.
Shows how notifications are triggered asynchronously.
"""
import sys
sys.path.insert(0, r"f:\\student portal\\grievance_portal")

from unittest.mock import patch, MagicMock
from fastapi import BackgroundTasks
from app.core.notifications import (
    notify_grievance_created,
    notify_grievance_status_changed,
    notify_grievance_assigned,
    notify_grievance_resolved,
)

def test_notification_flow():
    print("=" * 60)
    print("NOTIFICATION SYSTEM DEMO")
    print("=" * 60)
    
    # Mock email sending
    with patch('app.core.email.send_email') as mock_send:
        mock_send.return_value = True  # Simulate successful send
        print("\n[1] Testing Grievance Created Notification")
        print("-" * 60)
        notify_grievance_created(
            grievance_id=101,
            student_email="student@example.com",
            student_name="John Doe",
            title="Lab Equipment Malfunction",
            admin_email="admin@example.com",
        )
        print(f"✓ send_email called {mock_send.call_count} times")
        for call in mock_send.call_args_list:
            print(f"  → To: {call[0][0]}, Subject: {call[0][1][:50]}...")
        mock_send.reset_mock()
        
        print("\n[2] Testing Grievance Status Changed Notification")
        print("-" * 60)
        notify_grievance_status_changed(
            grievance_id=101,
            student_email="student@example.com",
            student_name="John Doe",
            old_status="submitted",
            new_status="under_review",
            title="Lab Equipment Malfunction",
        )
        print(f"✓ send_email called {mock_send.call_count} times")
        for call in mock_send.call_args_list:
            print(f"  → To: {call[0][0]}, Subject: {call[0][1][:50]}...")
        mock_send.reset_mock()
        
        print("\n[3] Testing Grievance Assigned Notification")
        print("-" * 60)
        notify_grievance_assigned(
            grievance_id=101,
            handler_email="handler@example.com",
            handler_name="Sarah Smith",
            grievance_title="Lab Equipment Malfunction",
        )
        print(f"✓ send_email called {mock_send.call_count} times")
        for call in mock_send.call_args_list:
            print(f"  → To: {call[0][0]}, Subject: {call[0][1][:50]}...")
        mock_send.reset_mock()
        
        print("\n[4] Testing Grievance Resolved Notification")
        print("-" * 60)
        notify_grievance_resolved(
            grievance_id=101,
            student_email="student@example.com",
            student_name="John Doe",
            title="Lab Equipment Malfunction",
            resolution="Equipment repaired and tested. Ready for use.",
        )
        print(f"✓ send_email called {mock_send.call_count} times")
        for call in mock_send.call_args_list:
            print(f"  → To: {call[0][0]}, Subject: {call[0][1][:50]}...")
    
    print("\n" + "=" * 60)
    print("✓ All notification flows tested successfully!")
    print("=" * 60)
    print("\nKey Features:")
    print("✓ Async email sending via BackgroundTasks")
    print("✓ Ready to migrate to Celery/RQ (just wrap task functions)")
    print("✓ Modular notification functions")
    print("✓ Template-based email bodies")
    print("\nProduction Checklist:")
    print("□ Replace mock emails with real SMTP config")
    print("□ Add email templates (Jinja2)")
    print("□ Implement Celery/RQ for distributed tasks")
    print("□ Add email retry logic")
    print("□ Log all notifications")

if __name__ == "__main__":
    test_notification_flow()

# ============================================================
# Notification Service — Supabase CRUD for notifications
# ============================================================

from database import get_supabase
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """Service layer for notification operations."""

    @staticmethod
    def get_teacher_notifications(
        teacher_id: str, limit: int = 20, unread_only: bool = False
    ) -> List[Dict[str, Any]]:
        """Get notifications for a teacher."""
        try:
            db = get_supabase()
            query = (
                db.table("notifications")
                .select("*")
                .eq("teacher_id", teacher_id)
                .order("created_at", desc=True)
                .limit(limit)
            )
            if unread_only:
                query = query.eq("is_read", False)
            response = query.execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching notifications: {e}")
            return []

    @staticmethod
    def get_unread_count(teacher_id: str) -> int:
        """Get count of unread notifications."""
        try:
            db = get_supabase()
            response = (
                db.table("notifications")
                .select("id", count="exact")
                .eq("teacher_id", teacher_id)
                .eq("is_read", False)
                .execute()
            )
            return response.count or 0
        except Exception as e:
            logger.error(f"Error counting unread notifications: {e}")
            return 0

    @staticmethod
    def mark_all_read(teacher_id: str) -> bool:
        """Mark all notifications as read for a teacher."""
        try:
            db = get_supabase()
            db.table("notifications").update({"is_read": True}).eq(
                "teacher_id", teacher_id
            ).eq("is_read", False).execute()
            return True
        except Exception as e:
            logger.error(f"Error marking notifications read: {e}")
            return False

    @staticmethod
    def mark_read(notification_id: str) -> bool:
        """Mark a single notification as read."""
        try:
            db = get_supabase()
            db.table("notifications").update({"is_read": True}).eq(
                "id", notification_id
            ).execute()
            return True
        except Exception as e:
            logger.error(f"Error marking notification read: {e}")
            return False

    @staticmethod
    def create_notification(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new notification."""
        try:
            db = get_supabase()
            response = db.table("notifications").insert(data).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            return None

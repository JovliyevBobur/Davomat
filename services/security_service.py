# ============================================================
# Security Service — Supabase CRUD for security events
# ============================================================

from database import get_supabase
from typing import Optional, Dict, Any, List
from datetime import date
import logging

logger = logging.getLogger(__name__)


class SecurityService:
    """Service layer for security event operations."""

    @staticmethod
    def get_teacher_security_events(
        teacher_id: str, school_id: Optional[str] = None, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get security events for a teacher."""
        try:
            db = get_supabase()
            query = (
                db.table("security_events")
                .select(
                    "*, "
                    "schools(id, name), "
                    "classes:class_id(id, name)"
                )
                .eq("teacher_id", teacher_id)
                .order("created_at", desc=True)
                .limit(limit)
            )
            if school_id:
                query = query.eq("school_id", school_id)
            response = query.execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching security events: {e}")
            return []

    @staticmethod
    def get_teacher_today_events(
        teacher_id: str, school_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get today's security events for a teacher."""
        try:
            db = get_supabase()
            today_str = date.today().isoformat()
            query = (
                db.table("security_events")
                .select(
                    "*, "
                    "schools(id, name), "
                    "classes:class_id(id, name)"
                )
                .eq("teacher_id", teacher_id)
                .gte("created_at", f"{today_str}T00:00:00")
                .lte("created_at", f"{today_str}T23:59:59")
                .order("created_at", desc=True)
            )
            if school_id:
                query = query.eq("school_id", school_id)
            response = query.execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching today's security events: {e}")
            return []

    @staticmethod
    def create_security_event(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a security event.

        NOTE: In production, security events are primarily created by the
        Railway backend during attendance validation. This method exists
        for completeness.
        """
        try:
            db = get_supabase()
            response = db.table("security_events").insert(data).execute()
            if response.data:
                logger.warning(f"Security event created: {data.get('event_type')}")
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error creating security event: {e}")
            return None

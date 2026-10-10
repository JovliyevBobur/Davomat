# ============================================================
# School Service — Supabase CRUD for schools & memberships
# ============================================================

from database import get_supabase
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class SchoolService:
    """Service layer for school-related database operations."""

    @staticmethod
    def get_all_active() -> List[Dict[str, Any]]:
        """Get all active schools."""
        try:
            db = get_supabase()
            response = (
                db.table("schools")
                .select("*")
                .eq("status", "ACTIVE")
                .order("name")
                .execute()
            )
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching schools: {e}")
            return []

    @staticmethod
    def get_by_id(school_id: str) -> Optional[Dict[str, Any]]:
        """Get school by ID."""
        try:
            db = get_supabase()
            response = (
                db.table("schools")
                .select("*")
                .eq("id", school_id)
                .limit(1)
                .execute()
            )
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching school {school_id}: {e}")
            return None


class MembershipService:
    """Service layer for school membership operations."""

    @staticmethod
    def get_teacher_memberships(teacher_id: str) -> List[Dict[str, Any]]:
        """Get all school memberships for a teacher."""
        try:
            db = get_supabase()
            response = (
                db.table("school_memberships")
                .select("*, schools(id, name, short_name, address, status)")
                .eq("teacher_id", teacher_id)
                .order("created_at", desc=True)
                .execute()
            )
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching memberships for teacher {teacher_id}: {e}")
            return []

    @staticmethod
    def get_approved_memberships(teacher_id: str) -> List[Dict[str, Any]]:
        """Get approved school memberships for a teacher."""
        try:
            db = get_supabase()
            response = (
                db.table("school_memberships")
                .select("*, schools(id, name, short_name)")
                .eq("teacher_id", teacher_id)
                .eq("status", "APPROVED")
                .execute()
            )
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching approved memberships: {e}")
            return []

    @staticmethod
    def get_membership(teacher_id: str, school_id: str) -> Optional[Dict[str, Any]]:
        """Check if a membership exists."""
        try:
            db = get_supabase()
            response = (
                db.table("school_memberships")
                .select("*")
                .eq("teacher_id", teacher_id)
                .eq("school_id", school_id)
                .limit(1)
                .execute()
            )
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error checking membership: {e}")
            return None

    @staticmethod
    def create_membership(teacher_id: str, school_id: str) -> Optional[Dict[str, Any]]:
        """Create a new school membership with PENDING status."""
        try:
            db = get_supabase()
            response = (
                db.table("school_memberships")
                .insert({
                    "teacher_id": teacher_id,
                    "school_id": school_id,
                    "status": "PENDING",
                })
                .execute()
            )
            if response.data:
                logger.info(f"Membership created: teacher={teacher_id}, school={school_id}")
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error creating membership: {e}")
            return None

    @staticmethod
    def get_school_id_from_membership(teacher_id: str) -> Optional[str]:
        """Get the first approved school ID for a teacher."""
        memberships = MembershipService.get_approved_memberships(teacher_id)
        if memberships:
            return memberships[0].get("school_id")
        return None

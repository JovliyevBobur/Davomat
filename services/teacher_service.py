# ============================================================
# Teacher Service — Supabase CRUD for teachers
# ============================================================

from database import get_supabase
from models import Teacher, TelegramConnectionStatus
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class TeacherService:
    """Service layer for teacher-related database operations."""

    @staticmethod
    def get_by_telegram_id(telegram_id: int) -> Optional[Dict[str, Any]]:
        """Find a teacher by their Telegram ID."""
        try:
            db = get_supabase()
            response = (
                db.table("teachers")
                .select("*")
                .eq("telegram_id", telegram_id)
                .limit(1)
                .execute()
            )
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching teacher by telegram_id={telegram_id}: {e}")
            return None

    @staticmethod
    def create(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new teacher record."""
        try:
            db = get_supabase()
            response = db.table("teachers").insert(data).execute()
            if response.data:
                logger.info(f"Teacher created: {data.get('first_name')} {data.get('last_name')}")
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error creating teacher: {e}")
            return None

    @staticmethod
    def update(teacher_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a teacher record."""
        try:
            db = get_supabase()
            response = (
                db.table("teachers")
                .update(data)
                .eq("id", teacher_id)
                .execute()
            )
            if response.data:
                logger.info(f"Teacher updated: {teacher_id}")
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error updating teacher {teacher_id}: {e}")
            return None

    @staticmethod
    def link_telegram(
        teacher_id: str,
        telegram_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Link Telegram account to teacher profile."""
        data = {
            "telegram_id": telegram_id,
            "telegram_username": username,
            "telegram_first_name": first_name,
            "telegram_last_name": last_name,
        }
        return TeacherService.update(teacher_id, data)

    @staticmethod
    def get_by_id(teacher_id: str) -> Optional[Dict[str, Any]]:
        """Get teacher by ID."""
        try:
            db = get_supabase()
            response = (
                db.table("teachers")
                .select("*")
                .eq("id", teacher_id)
                .limit(1)
                .execute()
            )
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching teacher {teacher_id}: {e}")
            return None

    @staticmethod
    def get_teacher_subjects(teacher_id: str, school_id: str) -> list:
        """Get subjects assigned to a teacher at a specific school."""
        try:
            db = get_supabase()
            response = (
                db.table("teacher_subjects")
                .select("*, subjects(id, name, code)")
                .eq("teacher_id", teacher_id)
                .eq("school_id", school_id)
                .execute()
            )
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching teacher subjects: {e}")
            return []

    @staticmethod
    def get_teacher_classes(teacher_id: str, school_id: str) -> list:
        """Get classes assigned to a teacher at a specific school."""
        try:
            db = get_supabase()
            response = (
                db.table("teacher_classes")
                .select("*, classes(id, name, grade, section)")
                .eq("teacher_id", teacher_id)
                .eq("school_id", school_id)
                .execute()
            )
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching teacher classes: {e}")
            return []

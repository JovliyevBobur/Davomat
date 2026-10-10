# ============================================================
# Attendance Service — Supabase CRUD for attendance records
# ============================================================

from database import get_supabase
from typing import Optional, Dict, Any, List
from datetime import datetime, date, timedelta
import logging

logger = logging.getLogger(__name__)


class AttendanceService:
    """Service layer for attendance record operations."""

    @staticmethod
    def get_teacher_attendance_today(
        teacher_id: str, school_id: str
    ) -> List[Dict[str, Any]]:
        """Get today's attendance records for a teacher."""
        try:
            db = get_supabase()
            today_str = date.today().isoformat()
            response = (
                db.table("attendance_records")
                .select(
                    "*, "
                    "lessons(id, start_time, end_time, day_of_week), "
                    "subjects:subject_id(id, name), "
                    "classes:class_id(id, name), "
                    "rooms:room_id(id, name)"
                )
                .eq("teacher_id", teacher_id)
                .eq("school_id", school_id)
                .gte("created_at", f"{today_str}T00:00:00")
                .lte("created_at", f"{today_str}T23:59:59")
                .order("scheduled_start")
                .execute()
            )
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching today's attendance: {e}")
            return []

    @staticmethod
    def get_teacher_attendance_range(
        teacher_id: str,
        school_id: str,
        start_date: str,
        end_date: str,
    ) -> List[Dict[str, Any]]:
        """Get attendance records for a date range."""
        try:
            db = get_supabase()
            response = (
                db.table("attendance_records")
                .select(
                    "*, "
                    "subjects:subject_id(id, name), "
                    "classes:class_id(id, name), "
                    "rooms:room_id(id, name)"
                )
                .eq("teacher_id", teacher_id)
                .eq("school_id", school_id)
                .gte("created_at", f"{start_date}T00:00:00")
                .lte("created_at", f"{end_date}T23:59:59")
                .order("created_at", desc=True)
                .execute()
            )
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching attendance range: {e}")
            return []

    @staticmethod
    def get_teacher_attendance_summary(
        teacher_id: str, school_id: str, start_date: str, end_date: str
    ) -> Dict[str, int]:
        """Get attendance summary (present/late/missing counts)."""
        records = AttendanceService.get_teacher_attendance_range(
            teacher_id, school_id, start_date, end_date
        )
        summary = {"present": 0, "late": 0, "missing": 0, "total": len(records)}
        for rec in records:
            status = rec.get("status", "").upper()
            if status == "PRESENT":
                summary["present"] += 1
            elif status == "LATE":
                summary["late"] += 1
            elif status == "MISSING":
                summary["missing"] += 1
        return summary

    @staticmethod
    def check_existing_attendance(
        teacher_id: str, lesson_id: str, attendance_date: str
    ) -> Optional[Dict[str, Any]]:
        """Check if attendance already exists for a lesson today."""
        try:
            db = get_supabase()
            response = (
                db.table("attendance_records")
                .select("*")
                .eq("teacher_id", teacher_id)
                .eq("lesson_id", lesson_id)
                .gte("created_at", f"{attendance_date}T00:00:00")
                .lte("created_at", f"{attendance_date}T23:59:59")
                .limit(1)
                .execute()
            )
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error checking existing attendance: {e}")
            return None

    @staticmethod
    def create_attendance_record(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create an attendance record.

        NOTE: In production, this should ONLY be called by the Railway backend
        after full validation. This method exists for the bot to display
        pending/submitted scans. The authoritative record is written by Railway.
        """
        try:
            db = get_supabase()
            response = db.table("attendance_records").insert(data).execute()
            if response.data:
                logger.info(f"Attendance record created: {data.get('teacher_id')}")
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error creating attendance record: {e}")
            return None

    @staticmethod
    def get_weekly_summary(
        teacher_id: str, school_id: str
    ) -> Dict[str, int]:
        """Get this week's attendance summary."""
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        return AttendanceService.get_teacher_attendance_summary(
            teacher_id,
            school_id,
            start_of_week.isoformat(),
            today.isoformat(),
        )

    @staticmethod
    def get_monthly_summary(
        teacher_id: str, school_id: str
    ) -> Dict[str, int]:
        """Get this month's attendance summary."""
        today = date.today()
        start_of_month = today.replace(day=1)
        return AttendanceService.get_teacher_attendance_summary(
            teacher_id,
            school_id,
            start_of_month.isoformat(),
            today.isoformat(),
        )

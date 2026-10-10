# ============================================================
# Schedule Service — Supabase CRUD for lessons/schedules
# ============================================================

from database import get_supabase
from typing import Optional, Dict, Any, List
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

DAY_MAP = {
    0: "MONDAY",
    1: "TUESDAY",
    2: "WEDNESDAY",
    3: "THURSDAY",
    4: "FRIDAY",
    5: "SATURDAY",
    6: "SUNDAY",
}


class ScheduleService:
    """Service layer for schedule/lesson database operations."""

    @staticmethod
    def get_teacher_schedule_for_day(
        teacher_id: str, school_id: str, day_of_week: str
    ) -> List[Dict[str, Any]]:
        """Get all lessons for a teacher at a school on a specific day."""
        try:
            db = get_supabase()
            response = (
                db.table("lessons")
                .select(
                    "*, "
                    "subjects(id, name, code), "
                    "classes(id, name, grade, section), "
                    "rooms(id, name, building, floor)"
                )
                .eq("teacher_id", teacher_id)
                .eq("school_id", school_id)
                .eq("day_of_week", day_of_week)
                .eq("is_active", True)
                .order("start_time")
                .execute()
            )
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching schedule: {e}")
            return []

    @staticmethod
    def get_teacher_weekly_schedule(
        teacher_id: str, school_id: str
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Get full weekly schedule for a teacher at a school."""
        try:
            db = get_supabase()
            response = (
                db.table("lessons")
                .select(
                    "*, "
                    "subjects(id, name, code), "
                    "classes(id, name, grade, section), "
                    "rooms(id, name, building, floor)"
                )
                .eq("teacher_id", teacher_id)
                .eq("school_id", school_id)
                .eq("is_active", True)
                .order("start_time")
                .execute()
            )
            # Group by day
            weekly: Dict[str, list] = {}
            for lesson in (response.data or []):
                day = lesson.get("day_of_week", "UNKNOWN")
                if day not in weekly:
                    weekly[day] = []
                weekly[day].append(lesson)
            return weekly
        except Exception as e:
            logger.error(f"Error fetching weekly schedule: {e}")
            return {}

    @staticmethod
    def get_today_day_name() -> str:
        """Get current day of week name."""
        today = datetime.now()
        return DAY_MAP.get(today.weekday(), "MONDAY")

    @staticmethod
    def get_teacher_today_schedule(
        teacher_id: str, school_id: str
    ) -> List[Dict[str, Any]]:
        """Get today's schedule for a teacher."""
        today = ScheduleService.get_today_day_name()
        return ScheduleService.get_teacher_schedule_for_day(
            teacher_id, school_id, today
        )

    @staticmethod
    def get_current_lesson(
        teacher_id: str, school_id: str
    ) -> Optional[Dict[str, Any]]:
        """Find the current or nearest upcoming lesson for a teacher."""
        try:
            now = datetime.now()
            today = DAY_MAP.get(now.weekday(), "MONDAY")
            current_time = now.strftime("%H:%M")

            lessons = ScheduleService.get_teacher_schedule_for_day(
                teacher_id, school_id, today
            )

            # Find lesson that covers current time
            for lesson in lessons:
                start = lesson.get("start_time", "")
                end = lesson.get("end_time", "")
                if start <= current_time <= end:
                    return lesson

            # Find next upcoming lesson
            for lesson in lessons:
                start = lesson.get("start_time", "")
                if start > current_time:
                    return lesson

            return None
        except Exception as e:
            logger.error(f"Error finding current lesson: {e}")
            return None

    @staticmethod
    def find_lesson_for_class_at_time(
        teacher_id: str, school_id: str, class_id: str
    ) -> Optional[Dict[str, Any]]:
        """Find a scheduled lesson for a teacher/class at the current time."""
        try:
            now = datetime.now()
            today = DAY_MAP.get(now.weekday(), "MONDAY")
            current_time = now.strftime("%H:%M")

            db = get_supabase()
            response = (
                db.table("lessons")
                .select(
                    "*, "
                    "subjects(id, name), "
                    "classes(id, name), "
                    "rooms(id, name)"
                )
                .eq("teacher_id", teacher_id)
                .eq("school_id", school_id)
                .eq("class_id", class_id)
                .eq("day_of_week", today)
                .eq("is_active", True)
                .execute()
            )

            for lesson in (response.data or []):
                start = lesson.get("start_time", "")
                end = lesson.get("end_time", "")
                # Allow 5 min before start
                # In production, this window comes from school settings
                if start and end:
                    if start <= current_time <= end:
                        return lesson

            return None
        except Exception as e:
            logger.error(f"Error finding lesson for class: {e}")
            return None

    @staticmethod
    def count_weekly_hours(teacher_id: str, school_id: str) -> float:
        """Calculate total weekly lesson hours."""
        try:
            weekly = ScheduleService.get_teacher_weekly_schedule(teacher_id, school_id)
            total_minutes = 0
            for day_lessons in weekly.values():
                for lesson in day_lessons:
                    start = lesson.get("start_time", "00:00")
                    end = lesson.get("end_time", "00:00")
                    try:
                        s_parts = start.split(":")
                        e_parts = end.split(":")
                        s_min = int(s_parts[0]) * 60 + int(s_parts[1])
                        e_min = int(e_parts[0]) * 60 + int(e_parts[1])
                        total_minutes += max(0, e_min - s_min)
                    except (ValueError, IndexError):
                        pass
            return round(total_minutes / 60, 1)
        except Exception as e:
            logger.error(f"Error counting weekly hours: {e}")
            return 0.0

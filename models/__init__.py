# ============================================================
# Type Definitions / Data Models
# ============================================================

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, time
from enum import Enum


# ── Enums ──────────────────────────────────────────────────

class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    SCHOOL_ADMIN = "SCHOOL_ADMIN"
    ZAVUCH = "ZAVUCH"
    TEACHER = "TEACHER"


class MembershipStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SUSPENDED = "SUSPENDED"


class SchoolStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    ARCHIVED = "ARCHIVED"


class QRStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"


class AttendanceStatus(str, Enum):
    PRESENT = "PRESENT"
    LATE = "LATE"
    MISSING = "MISSING"


class EntityStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


class TelegramConnectionStatus(str, Enum):
    CONNECTED = "CONNECTED"
    NOT_CONNECTED = "NOT_CONNECTED"


class SecurityEventType(str, Enum):
    OUTSIDE_SCHOOL = "OUTSIDE_SCHOOL"
    WRONG_CLASS = "WRONG_CLASS"
    NO_LESSON = "NO_LESSON"
    TOO_EARLY = "TOO_EARLY"
    LESSON_ENDED = "LESSON_ENDED"
    LOW_ACCURACY = "LOW_ACCURACY"
    LOCATION_PERMISSION_DENIED = "LOCATION_PERMISSION_DENIED"
    INVALID_QR = "INVALID_QR"
    DISABLED_QR = "DISABLED_QR"
    UNAUTHORIZED_TEACHER = "UNAUTHORIZED_TEACHER"
    DUPLICATE_SCAN = "DUPLICATE_SCAN"
    RATE_LIMITED = "RATE_LIMITED"
    SUSPICIOUS_LOCATION = "SUSPICIOUS_LOCATION"


class DayOfWeek(str, Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


class NotificationType(str, Enum):
    MEMBERSHIP_PENDING = "MEMBERSHIP_PENDING"
    MEMBERSHIP_APPROVED = "MEMBERSHIP_APPROVED"
    MEMBERSHIP_REJECTED = "MEMBERSHIP_REJECTED"
    MEMBERSHIP_SUSPENDED = "MEMBERSHIP_SUSPENDED"
    ATTENDANCE_PRESENT = "ATTENDANCE_PRESENT"
    ATTENDANCE_LATE = "ATTENDANCE_LATE"
    ATTENDANCE_MISSING = "ATTENDANCE_MISSING"
    SECURITY_WARNING = "SECURITY_WARNING"
    SCHEDULE_UPDATED = "SCHEDULE_UPDATED"
    QR_REGENERATED = "QR_REGENERATED"
    SYSTEM = "SYSTEM"


# ── Data Models ────────────────────────────────────────────

class Profile(BaseModel):
    id: str
    email: Optional[str] = None
    role: UserRole
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: Optional[str] = None


class School(BaseModel):
    id: str
    name: str
    short_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: str = "Asia/Tashkent"
    geofence_radius: int = 200
    max_gps_accuracy: int = 50
    attendance_window_minutes: int = 5
    missing_grace_minutes: int = 5
    status: SchoolStatus = SchoolStatus.ACTIVE
    created_at: Optional[str] = None


class Teacher(BaseModel):
    id: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    telegram_id: Optional[int] = None
    telegram_username: Optional[str] = None
    telegram_first_name: Optional[str] = None
    telegram_last_name: Optional[str] = None
    photo_url: Optional[str] = None
    employment_date: Optional[str] = None
    status: EntityStatus = EntityStatus.ACTIVE
    notes: Optional[str] = None
    created_at: Optional[str] = None


class SchoolMembership(BaseModel):
    id: str
    teacher_id: str
    school_id: str
    status: MembershipStatus = MembershipStatus.PENDING
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None
    created_at: Optional[str] = None
    # Joined fields
    school_name: Optional[str] = None
    teacher_name: Optional[str] = None


class Subject(BaseModel):
    id: str
    school_id: str
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    status: EntityStatus = EntityStatus.ACTIVE


class ClassRoom(BaseModel):
    """A class like 10-A, 11-B."""
    id: str
    school_id: str
    name: str
    grade: Optional[int] = None
    section: Optional[str] = None
    academic_year: Optional[str] = None
    status: EntityStatus = EntityStatus.ACTIVE


class Room(BaseModel):
    id: str
    school_id: str
    name: str
    building: Optional[str] = None
    floor: Optional[int] = None
    capacity: Optional[int] = None
    status: EntityStatus = EntityStatus.ACTIVE


class Lesson(BaseModel):
    id: str
    school_id: str
    teacher_id: str
    subject_id: str
    class_id: str
    room_id: Optional[str] = None
    day_of_week: DayOfWeek
    start_time: str  # HH:MM
    end_time: str    # HH:MM
    is_active: bool = True
    # Joined fields
    teacher_name: Optional[str] = None
    subject_name: Optional[str] = None
    class_name: Optional[str] = None
    room_name: Optional[str] = None


class ClassQRCode(BaseModel):
    id: str
    school_id: str
    class_id: str
    token: str
    status: QRStatus = QRStatus.ACTIVE
    generated_at: Optional[str] = None
    disabled_at: Optional[str] = None
    class_name: Optional[str] = None
    school_name: Optional[str] = None


class AttendanceRecord(BaseModel):
    id: str
    school_id: str
    teacher_id: str
    lesson_id: str
    class_id: str
    subject_id: Optional[str] = None
    room_id: Optional[str] = None
    scheduled_start: str
    scan_time: Optional[str] = None
    status: AttendanceStatus
    late_minutes: int = 0
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    gps_accuracy: Optional[float] = None
    distance_from_school: Optional[float] = None
    qr_token: Optional[str] = None
    request_id: Optional[str] = None
    created_at: Optional[str] = None
    # Joined
    teacher_name: Optional[str] = None
    class_name: Optional[str] = None
    subject_name: Optional[str] = None
    room_name: Optional[str] = None


class SecurityEvent(BaseModel):
    id: str
    school_id: str
    teacher_id: str
    class_id: Optional[str] = None
    lesson_id: Optional[str] = None
    event_type: SecurityEventType
    timestamp: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    gps_accuracy: Optional[float] = None
    distance_from_school: Optional[float] = None
    reason: Optional[str] = None
    request_id: Optional[str] = None
    created_at: Optional[str] = None
    # Joined
    teacher_name: Optional[str] = None
    class_name: Optional[str] = None
    school_name: Optional[str] = None


class Notification(BaseModel):
    id: str
    user_id: Optional[str] = None
    teacher_id: Optional[str] = None
    school_id: Optional[str] = None
    type: NotificationType
    title: str
    message: str
    is_read: bool = False
    channel: str = "telegram"
    created_at: Optional[str] = None

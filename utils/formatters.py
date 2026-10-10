# ============================================================
# Formatters — Output formatting utilities
# ============================================================

from datetime import datetime
from typing import Optional, Dict, Any
from locales.uz import t


# Status emoji mapping
STATUS_EMOJI = {
    "PENDING": "⏳",
    "APPROVED": "✅",
    "REJECTED": "❌",
    "SUSPENDED": "⛔",
    "PRESENT": "✅",
    "LATE": "⚠️",
    "MISSING": "❌",
    "ACTIVE": "🟢",
    "DISABLED": "🔴",
    "ARCHIVED": "📦",
}

# Status display names
STATUS_NAMES = {
    "PENDING": "Kutilmoqda",
    "APPROVED": "Tasdiqlangan",
    "REJECTED": "Rad etilgan",
    "SUSPENDED": "To'xtatilgan",
    "PRESENT": "Kelgan",
    "LATE": "Kechikkan",
    "MISSING": "Kelmagan",
    "ACTIVE": "Faol",
    "DISABLED": "O'chirilgan",
    "ARCHIVED": "Arxivlangan",
}

# Day names in Uzbek
DAY_NAMES = {
    "MONDAY": "Dushanba",
    "TUESDAY": "Seshanba",
    "WEDNESDAY": "Chorshanba",
    "THURSDAY": "Payshanba",
    "FRIDAY": "Juma",
    "SATURDAY": "Shanba",
    "SUNDAY": "Yakshanba",
}

# Security event type names
SECURITY_EVENT_NAMES = {
    "OUTSIDE_SCHOOL": "🌍 Maktab hududidan tashqarida",
    "WRONG_CLASS": "🚪 Noto'g'ri sinf",
    "NO_LESSON": "📭 Dars mavjud emas",
    "TOO_EARLY": "⏰ Juda erta",
    "LESSON_ENDED": "🔚 Dars tugagan",
    "LOW_ACCURACY": "📍 Past aniqlik",
    "LOCATION_PERMISSION_DENIED": "📍 Joylashuv ruxsati rad etilgan",
    "INVALID_QR": "❌ Noto'g'ri QR kod",
    "DISABLED_QR": "⛔ O'chirilgan QR kod",
    "UNAUTHORIZED_TEACHER": "🚫 Ruxsatsiz o'qituvchi",
    "DUPLICATE_SCAN": "🔄 Takroriy skanerlash",
    "RATE_LIMITED": "⏱ Tezlik cheklangan",
    "SUSPICIOUS_LOCATION": "⚠️ Shubhali joylashuv",
}

# Notification icons
NOTIFICATION_ICONS = {
    "MEMBERSHIP_PENDING": "📨",
    "MEMBERSHIP_APPROVED": "✅",
    "MEMBERSHIP_REJECTED": "❌",
    "MEMBERSHIP_SUSPENDED": "⛔",
    "ATTENDANCE_PRESENT": "✅",
    "ATTENDANCE_LATE": "⚠️",
    "ATTENDANCE_MISSING": "❌",
    "SECURITY_WARNING": "🔒",
    "SCHEDULE_UPDATED": "📅",
    "QR_REGENERATED": "🔄",
    "SYSTEM": "ℹ️",
}


def format_status(status: str) -> str:
    """Format a status with emoji."""
    emoji = STATUS_EMOJI.get(status, "❓")
    name = STATUS_NAMES.get(status, status)
    return f"{emoji} {name}"


def format_day(day: str) -> str:
    """Format a day of week name."""
    return DAY_NAMES.get(day, day)


def format_time(time_str: str) -> str:
    """Format a time string for display."""
    if not time_str:
        return "—"
    # Handle various formats
    try:
        if "T" in time_str:
            dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
            return dt.strftime("%H:%M")
        return time_str[:5]  # HH:MM
    except (ValueError, TypeError):
        return time_str


def format_datetime(dt_str: str) -> str:
    """Format a datetime string for display."""
    if not dt_str:
        return "—"
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y %H:%M")
    except (ValueError, TypeError):
        return dt_str


def format_date(dt_str: str) -> str:
    """Format a date string."""
    if not dt_str:
        return "—"
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        return dt_str


def format_teacher_name(teacher: Dict[str, Any]) -> str:
    """Format a teacher's full name."""
    parts = []
    if teacher.get("last_name"):
        parts.append(teacher["last_name"])
    if teacher.get("first_name"):
        parts.append(teacher["first_name"])
    if teacher.get("middle_name"):
        parts.append(teacher["middle_name"])
    return " ".join(parts) if parts else "Nomsiz"


def format_lesson(lesson: Dict[str, Any]) -> str:
    """Format a single lesson for display."""
    subject = lesson.get("subjects", {})
    cls = lesson.get("classes", {})
    room = lesson.get("rooms", {})

    subject_name = subject.get("name", "—") if subject else "—"
    class_name = cls.get("name", "—") if cls else "—"
    room_name = room.get("name", "—") if room else "—"
    start = format_time(lesson.get("start_time", ""))
    end = format_time(lesson.get("end_time", ""))

    return (
        f"⏰ <b>{start}–{end}</b>\n"
        f"   📚 {subject_name}\n"
        f"   🏫 {class_name}\n"
        f"   🚪 Xona: {room_name}"
    )


def format_attendance_record(record: Dict[str, Any]) -> str:
    """Format a single attendance record for display."""
    subject = record.get("subjects", record.get("subject_id", {}))
    cls = record.get("classes", record.get("class_id", {}))

    subject_name = "—"
    if isinstance(subject, dict) and subject:
        subject_name = subject.get("name", "—")

    class_name = "—"
    if isinstance(cls, dict) and cls:
        class_name = cls.get("name", "—")

    status = record.get("status", "MISSING")
    emoji = STATUS_EMOJI.get(status, "❓")
    status_name = STATUS_NAMES.get(status, status)
    scan_time = format_time(record.get("scan_time", ""))
    late = record.get("late_minutes", 0)
    scheduled = format_time(record.get("scheduled_start", ""))

    text = (
        f"⏰ <b>{scheduled}</b> | 📚 {subject_name} | 🏫 {class_name}\n"
        f"   📊 {emoji} <b>{status_name}</b>"
    )
    if scan_time and scan_time != "—":
        text += f" | 🕐 {scan_time}"
    if late and late > 0:
        text += f" | ⏱ +{late} daq."
    return text


def format_security_event(event: Dict[str, Any]) -> str:
    """Format a security event for display."""
    event_type = event.get("event_type", "UNKNOWN")
    event_name = SECURITY_EVENT_NAMES.get(event_type, event_type)

    school = event.get("schools", {})
    cls = event.get("classes", {})

    school_name = school.get("name", "—") if isinstance(school, dict) else "—"
    class_name = cls.get("name", "—") if isinstance(cls, dict) else "—"

    distance = event.get("distance_from_school")
    reason = event.get("reason", "—")
    time_str = format_datetime(event.get("created_at", ""))

    text = f"🔒 <b>{event_name}</b>\n"
    text += f"   🏫 {school_name}"
    if class_name != "—":
        text += f" | 🏫 {class_name}"
    text += "\n"
    if distance is not None:
        text += f"   📍 Masofa: {distance}m\n"
    text += f"   📝 {reason}\n"
    text += f"   🕐 {time_str}"
    return text


def format_notification(notif: Dict[str, Any]) -> str:
    """Format a notification for display."""
    ntype = notif.get("type", "SYSTEM")
    icon = NOTIFICATION_ICONS.get(ntype, "ℹ️")
    title = notif.get("title", "Bildirishnoma")
    message = notif.get("message", "")
    time_str = format_datetime(notif.get("created_at", ""))
    is_read = notif.get("is_read", False)

    read_marker = "" if is_read else "🔵 "
    return f"{read_marker}{icon} <b>{title}</b>\n   {message}\n   🕐 {time_str}"


def truncate_text(text: str, max_length: int = 4000) -> str:
    """Truncate text to fit Telegram's message limit."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."

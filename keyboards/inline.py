# ============================================================
# Inline Keyboards (callback-based keyboards)
# ============================================================

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Dict, Any, Optional


# ── Callback Data Prefixes ─────────────────────────────────
# Using structured prefixes for all callbacks

PREFIX_SCHOOL_SELECT = "school_sel:"
PREFIX_SCHOOL_JOIN = "school_join:"
PREFIX_SCHOOL_JOIN_CONFIRM = "school_join_confirm:"
PREFIX_SCHEDULE_SCHOOL = "sched_school:"
PREFIX_SCHEDULE_DAY = "sched_day:"
PREFIX_ATTENDANCE_SCHOOL = "att_school:"
PREFIX_ATTENDANCE_PERIOD = "att_period:"
PREFIX_WORKLOAD_SCHOOL = "wl_school:"
PREFIX_SECURITY_SCHOOL = "sec_school:"
PREFIX_NOTIF_READ_ALL = "notif_read_all"
PREFIX_NOTIF_READ = "notif_read:"
PREFIX_PROFILE_EDIT = "profile_edit:"
PREFIX_QR_SCAN_SUBMIT = "qr_submit:"
PREFIX_CONFIRM_YES = "confirm_yes:"
PREFIX_CONFIRM_NO = "confirm_no:"
PREFIX_BACK_MAIN = "back_main"
PREFIX_CLOSE = "close"


def close_button() -> InlineKeyboardButton:
    """Standard close/dismiss button."""
    return InlineKeyboardButton(text="❎ Yopish", callback_data=PREFIX_CLOSE)


def back_button(callback: str = PREFIX_BACK_MAIN) -> InlineKeyboardButton:
    """Standard back button."""
    return InlineKeyboardButton(text="🔙 Orqaga", callback_data=callback)


# ── School Selection ───────────────────────────────────────

def school_list_keyboard(
    schools: List[Dict[str, Any]],
    prefix: str = PREFIX_SCHOOL_SELECT,
) -> InlineKeyboardMarkup:
    """Build a keyboard listing schools."""
    builder = InlineKeyboardBuilder()
    for school in schools:
        school_id = school.get("id", "")
        name = school.get("name", school.get("short_name", "Maktab"))
        builder.row(
            InlineKeyboardButton(
                text=f"🏫 {name}",
                callback_data=f"{prefix}{school_id}",
            )
        )
    builder.row(close_button())
    return builder.as_markup()


def school_join_confirm_keyboard(school_id: str) -> InlineKeyboardMarkup:
    """Confirm joining a school."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="✅ Ha, so'rov yuborish",
            callback_data=f"{PREFIX_SCHOOL_JOIN_CONFIRM}{school_id}",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="❌ Yo'q",
            callback_data=PREFIX_CLOSE,
        ),
    )
    return builder.as_markup()


# ── My Schools ─────────────────────────────────────────────

def my_schools_keyboard() -> InlineKeyboardMarkup:
    """Actions for my schools page."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="➕ Yangi maktab qo'shish",
            callback_data="add_school",
        )
    )
    builder.row(close_button())
    return builder.as_markup()


# ── Schedule ───────────────────────────────────────────────

def schedule_school_keyboard(
    memberships: List[Dict[str, Any]],
) -> InlineKeyboardMarkup:
    """Select a school to view schedule."""
    builder = InlineKeyboardBuilder()
    for m in memberships:
        school = m.get("schools", {})
        if school:
            name = school.get("name", school.get("short_name", ""))
            builder.row(
                InlineKeyboardButton(
                    text=f"🏫 {name}",
                    callback_data=f"{PREFIX_SCHEDULE_SCHOOL}{school.get('id', '')}",
                )
            )
    builder.row(close_button())
    return builder.as_markup()


DAYS = [
    ("MONDAY", "Dushanba"),
    ("TUESDAY", "Seshanba"),
    ("WEDNESDAY", "Chorshanba"),
    ("THURSDAY", "Payshanba"),
    ("FRIDAY", "Juma"),
    ("SATURDAY", "Shanba"),
]


def schedule_day_keyboard(school_id: str) -> InlineKeyboardMarkup:
    """Select a day to view schedule."""
    builder = InlineKeyboardBuilder()
    for day_key, day_name in DAYS:
        builder.row(
            InlineKeyboardButton(
                text=f"📆 {day_name}",
                callback_data=f"{PREFIX_SCHEDULE_DAY}{school_id}:{day_key}",
            )
        )
    builder.row(
        back_button(f"{PREFIX_SCHEDULE_SCHOOL}back"),
        close_button(),
    )
    return builder.as_markup()


# ── Attendance ─────────────────────────────────────────────

def attendance_school_keyboard(
    memberships: List[Dict[str, Any]],
) -> InlineKeyboardMarkup:
    """Select a school to view attendance."""
    builder = InlineKeyboardBuilder()
    for m in memberships:
        school = m.get("schools", {})
        if school:
            name = school.get("name", school.get("short_name", ""))
            builder.row(
                InlineKeyboardButton(
                    text=f"🏫 {name}",
                    callback_data=f"{PREFIX_ATTENDANCE_SCHOOL}{school.get('id', '')}",
                )
            )
    builder.row(close_button())
    return builder.as_markup()


def attendance_period_keyboard(school_id: str) -> InlineKeyboardMarkup:
    """Select attendance period."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="📅 Bugun",
            callback_data=f"{PREFIX_ATTENDANCE_PERIOD}{school_id}:today",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="📆 Bu hafta",
            callback_data=f"{PREFIX_ATTENDANCE_PERIOD}{school_id}:week",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="📊 Bu oy",
            callback_data=f"{PREFIX_ATTENDANCE_PERIOD}{school_id}:month",
        ),
    )
    builder.row(
        back_button(f"{PREFIX_ATTENDANCE_SCHOOL}back"),
        close_button(),
    )
    return builder.as_markup()


# ── Workload ───────────────────────────────────────────────

def workload_school_keyboard(
    memberships: List[Dict[str, Any]],
) -> InlineKeyboardMarkup:
    """Select a school to view workload."""
    builder = InlineKeyboardBuilder()
    for m in memberships:
        school = m.get("schools", {})
        if school:
            name = school.get("name", school.get("short_name", ""))
            builder.row(
                InlineKeyboardButton(
                    text=f"🏫 {name}",
                    callback_data=f"{PREFIX_WORKLOAD_SCHOOL}{school.get('id', '')}",
                )
            )
    builder.row(close_button())
    return builder.as_markup()


# ── Security ──────────────────────────────────────────────

def security_school_keyboard(
    memberships: List[Dict[str, Any]],
) -> InlineKeyboardMarkup:
    """Select a school to view security events."""
    builder = InlineKeyboardBuilder()
    for m in memberships:
        school = m.get("schools", {})
        if school:
            name = school.get("name", school.get("short_name", ""))
            builder.row(
                InlineKeyboardButton(
                    text=f"🏫 {name}",
                    callback_data=f"{PREFIX_SECURITY_SCHOOL}{school.get('id', '')}",
                )
            )
    builder.row(close_button())
    return builder.as_markup()


# ── Profile ────────────────────────────────────────────────

def profile_actions_keyboard() -> InlineKeyboardMarkup:
    """Profile action buttons."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="📱 Telefonni o'zgartirish",
            callback_data=f"{PREFIX_PROFILE_EDIT}phone",
        ),
        InlineKeyboardButton(
            text="📧 Emailni o'zgartirish",
            callback_data=f"{PREFIX_PROFILE_EDIT}email",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="🏫 Maktablarim",
            callback_data="my_schools",
        ),
    )
    builder.row(close_button())
    return builder.as_markup()


# ── Notifications ──────────────────────────────────────────

def notifications_keyboard(has_unread: bool = False) -> InlineKeyboardMarkup:
    """Notification action buttons."""
    builder = InlineKeyboardBuilder()
    if has_unread:
        builder.row(
            InlineKeyboardButton(
                text="✅ Barchasini o'qilgan deb belgilash",
                callback_data=PREFIX_NOTIF_READ_ALL,
            ),
        )
    builder.row(close_button())
    return builder.as_markup()


# ── Confirmation ───────────────────────────────────────────

def confirm_action_keyboard(
    action_id: str, yes_text: str = "✅ Ha", no_text: str = "❌ Yo'q"
) -> InlineKeyboardMarkup:
    """Generic confirmation keyboard."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=yes_text,
            callback_data=f"{PREFIX_CONFIRM_YES}{action_id}",
        ),
        InlineKeyboardButton(
            text=no_text,
            callback_data=f"{PREFIX_CONFIRM_NO}{action_id}",
        ),
    )
    return builder.as_markup()

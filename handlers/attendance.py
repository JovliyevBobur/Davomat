# ============================================================
# Attendance Handler — Viewing attendance records
# ============================================================

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, Optional

from locales.uz import t
from keyboards.inline import (
    PREFIX_ATTENDANCE_SCHOOL,
    PREFIX_ATTENDANCE_PERIOD,
    PREFIX_CLOSE,
    attendance_school_keyboard,
    attendance_period_keyboard,
    close_button,
)
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.school_service import MembershipService
from services.attendance_service import AttendanceService
from utils.formatters import format_attendance_record

router = Router()


@router.message(F.text == "📊 Davomat")
@router.message(F.text == "/attendance")
async def cmd_attendance(
    message: Message,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """View attendance."""
    if not teacher:
        await message.answer(t("error_not_registered"), parse_mode="HTML")
        return

    memberships = MembershipService.get_approved_memberships(teacher["id"])

    if not memberships:
        await message.answer(t("schedule_no_approved"), parse_mode="HTML")
        return

    if len(memberships) == 1:
        school_id = memberships[0]["school_id"]
        school_name = memberships[0]["schools"]["name"]
        await message.answer(
            t("attendance_school_title", school_name=school_name),
            reply_markup=attendance_period_keyboard(school_id),
            parse_mode="HTML",
        )
    else:
        await message.answer(
            t("attendance_title"),
            reply_markup=attendance_school_keyboard(memberships),
            parse_mode="HTML",
        )


@router.callback_query(F.data == f"{PREFIX_ATTENDANCE_SCHOOL}back")
async def cb_attendance_school_back(
    callback: CallbackQuery,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """Back to school selection for attendance."""
    if not teacher:
        await callback.answer(t("error_not_registered"), show_alert=True)
        return
        
    memberships = MembershipService.get_approved_memberships(teacher["id"])
    await callback.message.edit_text(
        t("attendance_title"),
        reply_markup=attendance_school_keyboard(memberships),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith(PREFIX_ATTENDANCE_SCHOOL) and ~F.data.endswith("back"))
async def cb_attendance_school(
    callback: CallbackQuery,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """Selected a school for attendance."""
    if not teacher:
        await callback.answer(t("error_not_registered"), show_alert=True)
        return

    school_id = callback.data.replace(PREFIX_ATTENDANCE_SCHOOL, "")
    
    memberships = MembershipService.get_approved_memberships(teacher["id"])
    school_name = ""
    for m in memberships:
        if m["school_id"] == school_id:
            school_name = m["schools"].get("name", "")
            break

    await callback.message.edit_text(
        t("attendance_school_title", school_name=school_name),
        reply_markup=attendance_period_keyboard(school_id),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith(PREFIX_ATTENDANCE_PERIOD))
async def cb_attendance_period(
    callback: CallbackQuery,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """Selected a period for attendance."""
    if not teacher:
        await callback.answer(t("error_not_registered"), show_alert=True)
        return

    data_parts = callback.data.replace(PREFIX_ATTENDANCE_PERIOD, "").split(":")
    if len(data_parts) != 2:
        await callback.answer(t("error_generic"), show_alert=True)
        return
        
    school_id, period = data_parts
    
    memberships = MembershipService.get_approved_memberships(teacher["id"])
    school_name = ""
    for m in memberships:
        if m["school_id"] == school_id:
            school_name = m["schools"].get("name", "")
            break

    text = f"📊 <b>{school_name} — Davomat</b>\n\n"
    
    records = []
    summary = {}
    
    if period == "today":
        text += "📅 <b>Bugun:</b>\n"
        records = AttendanceService.get_teacher_attendance_today(teacher["id"], school_id)
        # Calculate summary manually for today
        summary = {"present": 0, "late": 0, "missing": 0, "total": len(records)}
        for r in records:
            s = r.get("status", "").upper()
            if s == "PRESENT": summary["present"] += 1
            elif s == "LATE": summary["late"] += 1
            elif s == "MISSING": summary["missing"] += 1
            
    elif period == "week":
        text += "📆 <b>Bu hafta:</b>\n"
        summary = AttendanceService.get_weekly_summary(teacher["id"], school_id)
        # We don't list all records for week to avoid huge messages, just summary
        
    elif period == "month":
        text += "📊 <b>Bu oy:</b>\n"
        summary = AttendanceService.get_monthly_summary(teacher["id"], school_id)
    
    # List records if today
    if period == "today":
        if not records:
            text += t("attendance_empty")
        else:
            for rec in records:
                text += "\n" + format_attendance_record(rec) + "\n"
    
    # Add summary
    text += t(
        "attendance_summary",
        present=summary.get("present", 0),
        late=summary.get("late", 0),
        missing=summary.get("missing", 0),
        total=summary.get("total", 0),
    )

    # Back button
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="🔙 Orqaga", 
            callback_data=f"{PREFIX_ATTENDANCE_SCHOOL}{school_id}"
        )
    )
    builder.row(close_button())

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )

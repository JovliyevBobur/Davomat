# ============================================================
# Workload Handler — Viewing teacher workload
# ============================================================

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, Optional

from locales.uz import t
from keyboards.inline import (
    PREFIX_WORKLOAD_SCHOOL,
    PREFIX_CLOSE,
    workload_school_keyboard,
    close_button,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.school_service import MembershipService
from services.teacher_service import TeacherService
from services.schedule_service import ScheduleService
from utils.formatters import format_teacher_name

router = Router()


@router.message(F.text == "📊 Ish yuklama")
@router.message(F.text == "/workload")
async def cmd_workload(
    message: Message,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """View workload."""
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
        
        await _show_workload(message, teacher, school_id, school_name)
    else:
        await message.answer(
            t("workload_title"),
            reply_markup=workload_school_keyboard(memberships),
            parse_mode="HTML",
        )


@router.callback_query(F.data.startswith(PREFIX_WORKLOAD_SCHOOL))
async def cb_workload_school(
    callback: CallbackQuery,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """Selected a school for workload."""
    if not teacher:
        await callback.answer(t("error_not_registered"), show_alert=True)
        return

    school_id = callback.data.replace(PREFIX_WORKLOAD_SCHOOL, "")
    
    memberships = MembershipService.get_approved_memberships(teacher["id"])
    school_name = ""
    for m in memberships:
        if m["school_id"] == school_id:
            school_name = m["schools"].get("name", "")
            break

    await callback.message.delete()
    await _show_workload(callback.message, teacher, school_id, school_name)


async def _show_workload(message: Message, teacher: Dict[str, Any], school_id: str, school_name: str):
    """Helper to display workload for a specific school."""
    
    subjects_data = TeacherService.get_teacher_subjects(teacher["id"], school_id)
    classes_data = TeacherService.get_teacher_classes(teacher["id"], school_id)
    
    subjects_list = [s.get("subjects", {}).get("name") for s in subjects_data if s.get("subjects")]
    classes_list = [c.get("classes", {}).get("name") for c in classes_data if c.get("classes")]
    
    subjects_str = ", ".join(subjects_list) if subjects_list else "Belgilanmagan"
    classes_str = ", ".join(classes_list) if classes_list else "Belgilanmagan"
    
    weekly_hours = ScheduleService.count_weekly_hours(teacher["id"], school_id)
    monthly_hours = round(weekly_hours * 4.2, 1)  # Rough estimate
    
    name = format_teacher_name(teacher)
    
    text = t(
        "workload_school_title",
        school_name=school_name,
        teacher_name=name,
        subjects=subjects_str,
        classes=classes_str,
        weekly_hours=weekly_hours,
        monthly_hours=monthly_hours
    )
    
    builder = InlineKeyboardBuilder()
    builder.row(close_button())
    
    await message.answer(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

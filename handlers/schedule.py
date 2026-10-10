# ============================================================
# Schedule Handler — Viewing teacher schedule
# ============================================================

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, Optional

from locales.uz import t
from keyboards.inline import (
    PREFIX_SCHEDULE_SCHOOL,
    PREFIX_SCHEDULE_DAY,
    PREFIX_CLOSE,
    schedule_school_keyboard,
    schedule_day_keyboard,
    close_button,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.school_service import MembershipService
from services.schedule_service import ScheduleService
from utils.formatters import format_lesson

router = Router()


@router.message(F.text == "📅 Dars jadvali")
@router.message(F.text == "/schedule")
async def cmd_schedule(
    message: Message,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """View schedule."""
    if not teacher:
        await message.answer(t("error_not_registered"), parse_mode="HTML")
        return

    memberships = MembershipService.get_approved_memberships(teacher["id"])

    if not memberships:
        await message.answer(t("schedule_no_approved"), parse_mode="HTML")
        return

    if len(memberships) == 1:
        # Only one school - jump directly to day selection
        school_id = memberships[0]["school_id"]
        school_name = memberships[0]["schools"]["name"]
        await message.answer(
            t("schedule_school_title", school_name=school_name),
            reply_markup=schedule_day_keyboard(school_id),
            parse_mode="HTML",
        )
    else:
        # Multiple schools - select school first
        await message.answer(
            t("schedule_title"),
            reply_markup=schedule_school_keyboard(memberships),
            parse_mode="HTML",
        )


@router.callback_query(F.data == f"{PREFIX_SCHEDULE_SCHOOL}back")
async def cb_schedule_school_back(
    callback: CallbackQuery,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """Back to school selection for schedule."""
    if not teacher:
        await callback.answer(t("error_not_registered"), show_alert=True)
        return
        
    memberships = MembershipService.get_approved_memberships(teacher["id"])
    await callback.message.edit_text(
        t("schedule_title"),
        reply_markup=schedule_school_keyboard(memberships),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith(PREFIX_SCHEDULE_SCHOOL) and ~F.data.endswith("back"))
async def cb_schedule_school(
    callback: CallbackQuery,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """Selected a school for schedule."""
    if not teacher:
        await callback.answer(t("error_not_registered"), show_alert=True)
        return

    school_id = callback.data.replace(PREFIX_SCHEDULE_SCHOOL, "")
    
    memberships = MembershipService.get_approved_memberships(teacher["id"])
    school_name = ""
    for m in memberships:
        if m["school_id"] == school_id:
            school_name = m["schools"].get("name", "")
            break

    await callback.message.edit_text(
        t("schedule_school_title", school_name=school_name),
        reply_markup=schedule_day_keyboard(school_id),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith(PREFIX_SCHEDULE_DAY))
async def cb_schedule_day(
    callback: CallbackQuery,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """Selected a day for schedule."""
    if not teacher:
        await callback.answer(t("error_not_registered"), show_alert=True)
        return

    data_parts = callback.data.replace(PREFIX_SCHEDULE_DAY, "").split(":")
    if len(data_parts) != 2:
        await callback.answer(t("error_generic"), show_alert=True)
        return
        
    school_id, day = data_parts
    
    # Get school name
    memberships = MembershipService.get_approved_memberships(teacher["id"])
    school_name = ""
    for m in memberships:
        if m["school_id"] == school_id:
            school_name = m["schools"].get("name", "")
            break

    lessons = ScheduleService.get_teacher_schedule_for_day(teacher["id"], school_id, day)
    
    day_name = t(f"day_{day}")
    text = t("schedule_day_title", school_name=school_name, day=day_name)
    
    if not lessons:
        text += t("schedule_empty")
    else:
        for lesson in lessons:
            text += format_lesson(lesson) + "\n"

    # Provide a back button to day selection
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="🔙 Orqaga", 
            callback_data=f"{PREFIX_SCHEDULE_SCHOOL}{school_id}"
        )
    )
    builder.row(close_button())

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML",
    )

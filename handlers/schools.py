# ============================================================
# Schools Handler — Selecting and joining schools
# ============================================================

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, Optional

from locales.uz import t
from keyboards.reply import main_menu_keyboard
from keyboards.inline import (
    PREFIX_SCHOOL_SELECT,
    PREFIX_SCHOOL_JOIN_CONFIRM,
    PREFIX_CLOSE,
    school_list_keyboard,
    school_join_confirm_keyboard,
    my_schools_keyboard,
)
from services.school_service import SchoolService, MembershipService
from services.notification_service import NotificationService
from utils.formatters import format_status

router = Router()


@router.message(F.text == "🏫 Maktablarim")
@router.message(F.text == "/schools")
async def cmd_schools(
    message: Message,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """View my schools."""
    if not teacher:
        await message.answer(t("error_not_registered"), parse_mode="HTML")
        return

    memberships = MembershipService.get_teacher_memberships(teacher["id"])

    if not memberships:
        await message.answer(
            t("my_schools_title") + t("my_schools_empty"),
            reply_markup=my_schools_keyboard(),
            parse_mode="HTML",
        )
        return

    text = t("my_schools_title")
    for m in memberships:
        school = m.get("schools", {})
        school_name = school.get("name", "Noma'lum maktab")
        status = m.get("status", "PENDING")
        status_text = t(f"status_{status}")
        emoji = t(f"attendance_status_{status}") if status in ["PRESENT", "LATE", "MISSING"] else "❓"
        if status == "PENDING":
            emoji = "⏳"
        elif status == "APPROVED":
            emoji = "✅"
        elif status == "REJECTED":
            emoji = "❌"
        elif status == "SUSPENDED":
            emoji = "⛔"

        text += t(
            "my_schools_item",
            school_name=school_name,
            status_emoji=emoji,
            status=status_text,
        )

    await message.answer(text, reply_markup=my_schools_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "add_school")
async def cb_add_school(
    callback: CallbackQuery,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """Start process to join a new school."""
    if not teacher:
        await callback.answer(t("error_not_registered"), show_alert=True)
        return

    schools = SchoolService.get_all_active()
    if not schools:
        await callback.message.edit_text(t("school_no_schools"), parse_mode="HTML")
        return

    await callback.message.edit_text(
        t("school_select"),
        reply_markup=school_list_keyboard(schools),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith(PREFIX_SCHOOL_SELECT))
async def cb_select_school(
    callback: CallbackQuery,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """User selected a school from the list."""
    if not teacher:
        await callback.answer(t("error_not_registered"), show_alert=True)
        return

    school_id = callback.data.replace(PREFIX_SCHOOL_SELECT, "")
    school = SchoolService.get_by_id(school_id)

    if not school:
        await callback.answer(t("error_generic"), show_alert=True)
        return

    # Check if already a member/pending
    existing = MembershipService.get_membership(teacher["id"], school_id)
    if existing:
        await callback.message.edit_text(
            t("school_already_member", school_name=school["name"]),
            reply_markup=my_schools_keyboard(),
            parse_mode="HTML",
        )
        return

    # Show confirmation
    await callback.message.edit_text(
        t("school_request_confirm", school_name=school["name"]),
        reply_markup=school_join_confirm_keyboard(school_id),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith(PREFIX_SCHOOL_JOIN_CONFIRM))
async def cb_join_school_confirm(
    callback: CallbackQuery,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """Confirm joining the school."""
    if not teacher:
        await callback.answer(t("error_not_registered"), show_alert=True)
        return

    school_id = callback.data.replace(PREFIX_SCHOOL_JOIN_CONFIRM, "")
    school = SchoolService.get_by_id(school_id)

    if not school:
        await callback.answer(t("error_generic"), show_alert=True)
        return

    # Create membership
    result = MembershipService.create_membership(teacher["id"], school_id)
    if result:
        await callback.message.edit_text(
            t("school_request_sent", school_name=school["name"]),
            parse_mode="HTML",
        )
    else:
        await callback.answer(t("error_generic"), show_alert=True)

# ============================================================
# Security Handler — Viewing security events
# ============================================================

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, Optional

from locales.uz import t
from keyboards.inline import (
    PREFIX_SECURITY_SCHOOL,
    PREFIX_CLOSE,
    security_school_keyboard,
    close_button,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.school_service import MembershipService
from services.security_service import SecurityService
from utils.formatters import format_security_event

router = Router()


@router.message(F.text == "🔒 Xavfsizlik")
@router.message(F.text == "/security")
async def cmd_security(
    message: Message,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """View security events."""
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
        
        await _show_security(message, teacher, school_id, school_name)
    else:
        await message.answer(
            t("security_title"),
            reply_markup=security_school_keyboard(memberships),
            parse_mode="HTML",
        )


@router.callback_query(F.data.startswith(PREFIX_SECURITY_SCHOOL))
async def cb_security_school(
    callback: CallbackQuery,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """Selected a school for security."""
    if not teacher:
        await callback.answer(t("error_not_registered"), show_alert=True)
        return

    school_id = callback.data.replace(PREFIX_SECURITY_SCHOOL, "")
    
    memberships = MembershipService.get_approved_memberships(teacher["id"])
    school_name = ""
    for m in memberships:
        if m["school_id"] == school_id:
            school_name = m["schools"].get("name", "")
            break

    await callback.message.delete()
    await _show_security(callback.message, teacher, school_id, school_name)


async def _show_security(message: Message, teacher: Dict[str, Any], school_id: str, school_name: str):
    """Helper to display security events for a specific school."""
    
    events = SecurityService.get_teacher_security_events(teacher["id"], school_id, limit=5)
    
    text = f"🔒 <b>{school_name} — Xavfsizlik</b>\n"
    
    if not events:
        text += "\n" + t("security_empty")
    else:
        for event in events:
            text += "\n" + format_security_event(event) + "\n"
    
    builder = InlineKeyboardBuilder()
    builder.row(close_button())
    
    await message.answer(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

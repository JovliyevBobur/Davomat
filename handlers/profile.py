# ============================================================
# Profile Handler — Viewing and editing profile
# ============================================================

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, Optional

from states import ProfileEditStates
from locales.uz import t
from keyboards.reply import main_menu_keyboard, cancel_keyboard
from keyboards.inline import PREFIX_PROFILE_EDIT, profile_actions_keyboard
from services.teacher_service import TeacherService
from utils.formatters import format_datetime, format_teacher_name
from utils.validators import validate_phone, validate_email

router = Router()


@router.message(F.text == "👤 Profilim")
@router.message(F.text == "/profile")
async def cmd_profile(
    message: Message,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """View profile."""
    if not teacher:
        await message.answer(t("error_not_registered"), parse_mode="HTML")
        return

    name = format_teacher_name(teacher)
    
    telegram_status = t("status_NOT_CONNECTED")
    if teacher.get("telegram_id"):
        telegram_status = t("status_CONNECTED")

    text = t(
        "profile_title",
        first_name=teacher.get("first_name", "—"),
        last_name=teacher.get("last_name", "—"),
        middle_name=teacher.get("middle_name", "—"),
        phone=teacher.get("phone", "—"),
        email=teacher.get("email", "—"),
        telegram_status=telegram_status,
        created_at=format_datetime(teacher.get("created_at", "")),
    )

    await message.answer(
        text,
        reply_markup=profile_actions_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith(PREFIX_PROFILE_EDIT))
async def cb_edit_profile(
    callback: CallbackQuery,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """Start profile edit flow."""
    if not teacher:
        await callback.answer(t("error_not_registered"), show_alert=True)
        return

    field = callback.data.replace(PREFIX_PROFILE_EDIT, "")
    
    if field == "phone":
        await state.set_state(ProfileEditStates.edit_phone)
        await callback.message.answer(
            t("profile_edit_phone"), 
            reply_markup=cancel_keyboard(),
            parse_mode="HTML"
        )
        await callback.answer()
    elif field == "email":
        await state.set_state(ProfileEditStates.edit_email)
        await callback.message.answer(
            t("profile_edit_email"), 
            reply_markup=cancel_keyboard(),
            parse_mode="HTML"
        )
        await callback.answer()
    else:
        await callback.answer("Noma'lum maydon", show_alert=True)


@router.message(ProfileEditStates.edit_phone)
async def process_edit_phone(message: Message, state: FSMContext, teacher: Optional[Dict[str, Any]] = None, **kwargs):
    """Process new phone number."""
    if message.text == "🚫 Bekor qilish":
        await state.clear()
        await message.answer(t("action_cancelled"), reply_markup=main_menu_keyboard(), parse_mode="HTML")
        return

    if not teacher:
        return

    phone = validate_phone(message.text or "")
    if not phone:
        await message.answer(t("reg_phone_invalid"), parse_mode="HTML")
        return

    TeacherService.update(teacher["id"], {"phone": phone})
    
    await state.clear()
    await message.answer(t("profile_edit_success"), reply_markup=main_menu_keyboard(), parse_mode="HTML")


@router.message(ProfileEditStates.edit_email)
async def process_edit_email(message: Message, state: FSMContext, teacher: Optional[Dict[str, Any]] = None, **kwargs):
    """Process new email."""
    if message.text == "🚫 Bekor qilish":
        await state.clear()
        await message.answer(t("action_cancelled"), reply_markup=main_menu_keyboard(), parse_mode="HTML")
        return

    if not teacher:
        return

    email = (message.text or "").strip()
    if not validate_email(email):
        await message.answer(t("reg_email_invalid"), parse_mode="HTML")
        return

    TeacherService.update(teacher["id"], {"email": email})
    
    await state.clear()
    await message.answer(t("profile_edit_success"), reply_markup=main_menu_keyboard(), parse_mode="HTML")

# ============================================================
# Registration Handler — Teacher registration FSM flow
# ============================================================

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, Optional

from states import RegistrationStates
from locales.uz import t
from keyboards.reply import (
    main_menu_keyboard,
    phone_keyboard,
    cancel_keyboard,
    confirm_keyboard,
    registration_keyboard,
)
from services.teacher_service import TeacherService
from utils.validators import validate_phone, validate_email, validate_name, sanitize_text

router = Router()


@router.message(F.text == "📝 Ro'yxatdan o'tish")
async def start_registration(
    message: Message,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """Begin registration flow."""
    if teacher:
        await message.answer(t("reg_already"), reply_markup=main_menu_keyboard(), parse_mode="HTML")
        return

    await state.set_state(RegistrationStates.first_name)
    await message.answer(t("reg_first_name"), reply_markup=cancel_keyboard(), parse_mode="HTML")


@router.message(RegistrationStates.first_name)
async def process_first_name(message: Message, state: FSMContext, **kwargs):
    """Process first name input."""
    if message.text == "🚫 Bekor qilish":
        await state.clear()
        await message.answer(t("action_cancelled"), reply_markup=registration_keyboard(), parse_mode="HTML")
        return

    name = sanitize_text(message.text or "")
    if not validate_name(name):
        await message.answer(
            "❌ Ism kamida 2 ta harfdan iborat bo'lishi kerak. Qaytadan kiriting:",
            parse_mode="HTML",
        )
        return

    await state.update_data(first_name=name.strip().title())
    await state.set_state(RegistrationStates.last_name)
    await message.answer(t("reg_last_name"), parse_mode="HTML")


@router.message(RegistrationStates.last_name)
async def process_last_name(message: Message, state: FSMContext, **kwargs):
    """Process last name input."""
    if message.text == "🚫 Bekor qilish":
        await state.clear()
        await message.answer(t("action_cancelled"), reply_markup=registration_keyboard(), parse_mode="HTML")
        return

    name = sanitize_text(message.text or "")
    if not validate_name(name):
        await message.answer(
            "❌ Familiya kamida 2 ta harfdan iborat bo'lishi kerak. Qaytadan kiriting:",
            parse_mode="HTML",
        )
        return

    await state.update_data(last_name=name.strip().title())
    await state.set_state(RegistrationStates.middle_name)
    await message.answer(t("reg_middle_name"), parse_mode="HTML")


@router.message(RegistrationStates.middle_name)
async def process_middle_name(message: Message, state: FSMContext, **kwargs):
    """Process middle name (otasining ismi) input."""
    if message.text == "🚫 Bekor qilish":
        await state.clear()
        await message.answer(t("action_cancelled"), reply_markup=registration_keyboard(), parse_mode="HTML")
        return

    if message.text and message.text.strip().lower() in ("/skip", "skip", "o'tkazish"):
        await state.update_data(middle_name="—")
    else:
        name = sanitize_text(message.text or "")
        if name and not validate_name(name):
            await message.answer(
                "❌ Noto'g'ri format. Qaytadan kiriting yoki /skip bosing:",
                parse_mode="HTML",
            )
            return
        await state.update_data(middle_name=name.strip().title() if name else "—")

    await state.set_state(RegistrationStates.phone)
    await message.answer(t("reg_phone"), reply_markup=phone_keyboard(), parse_mode="HTML")


@router.message(RegistrationStates.phone)
async def process_phone(message: Message, state: FSMContext, **kwargs):
    """Process phone number input."""
    if message.text == "🚫 Bekor qilish":
        await state.clear()
        await message.answer(t("action_cancelled"), reply_markup=registration_keyboard(), parse_mode="HTML")
        return

    phone = None
    # Handle shared contact
    if message.contact:
        phone = message.contact.phone_number
        if phone and not phone.startswith("+"):
            phone = f"+{phone}"
    elif message.text:
        phone = validate_phone(message.text)

    if not phone:
        await message.answer(t("reg_phone_invalid"), parse_mode="HTML")
        return

    # Re-validate the phone
    validated = validate_phone(phone)
    if not validated:
        await message.answer(t("reg_phone_invalid"), parse_mode="HTML")
        return

    await state.update_data(phone=validated)
    await state.set_state(RegistrationStates.email)
    await message.answer(t("reg_email"), reply_markup=cancel_keyboard(), parse_mode="HTML")


@router.message(RegistrationStates.email)
async def process_email(message: Message, state: FSMContext, **kwargs):
    """Process email input."""
    if message.text == "🚫 Bekor qilish":
        await state.clear()
        await message.answer(t("action_cancelled"), reply_markup=registration_keyboard(), parse_mode="HTML")
        return

    if message.text and message.text.strip().lower() in ("/skip", "skip", "o'tkazish"):
        await state.update_data(email="—")
    else:
        email = (message.text or "").strip()
        if email and not validate_email(email):
            await message.answer(t("reg_email_invalid"), parse_mode="HTML")
            return
        await state.update_data(email=email if email else "—")

    # Show confirmation
    data = await state.get_data()
    await state.set_state(RegistrationStates.confirm)
    await message.answer(
        t(
            "reg_confirm",
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            middle_name=data.get("middle_name", "—"),
            phone=data.get("phone", ""),
            email=data.get("email", "—"),
        ),
        reply_markup=confirm_keyboard(),
        parse_mode="HTML",
    )


@router.message(RegistrationStates.confirm)
async def process_confirm(message: Message, state: FSMContext, **kwargs):
    """Process registration confirmation."""
    if message.text == "🚫 Bekor qilish":
        await state.clear()
        await message.answer(t("action_cancelled"), reply_markup=registration_keyboard(), parse_mode="HTML")
        return

    if message.text != "✅ Tasdiqlash":
        await message.answer("✅ Tasdiqlash yoki 🚫 Bekor qilish tugmasini bosing.", parse_mode="HTML")
        return

    data = await state.get_data()
    user = message.from_user

    # Prepare teacher data
    teacher_data = {
        "first_name": data.get("first_name", ""),
        "last_name": data.get("last_name", ""),
        "middle_name": data.get("middle_name") if data.get("middle_name") != "—" else None,
        "phone": data.get("phone", ""),
        "email": data.get("email") if data.get("email") != "—" else None,
        "telegram_id": user.id,
        "telegram_username": user.username,
        "telegram_first_name": user.first_name,
        "telegram_last_name": user.last_name,
        "status": "ACTIVE",
    }

    # Create teacher in Supabase
    result = TeacherService.create(teacher_data)
    if result:
        await state.clear()
        await message.answer(
            t("reg_success"),
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML",
        )
    else:
        await state.clear()
        await message.answer(t("error_generic"), reply_markup=registration_keyboard(), parse_mode="HTML")

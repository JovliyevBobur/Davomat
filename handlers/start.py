# ============================================================
# Start Handler — /start command and main menu
# ============================================================

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, Optional

from locales.uz import t
from keyboards.reply import main_menu_keyboard, registration_keyboard
from keyboards.inline import PREFIX_BACK_MAIN, PREFIX_CLOSE
from utils.formatters import format_teacher_name
from services.notification_service import NotificationService

router = Router()


@router.message(CommandStart())
async def cmd_start(
    message: Message,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """Handle /start command."""
    # Clear any active FSM state
    await state.clear()

    if teacher:
        # Registered teacher — show welcome back + main menu
        name = format_teacher_name(teacher)
        unread = NotificationService.get_unread_count(teacher["id"])
        text = t("welcome_back", name=name)
        if unread > 0:
            text += f"\n\n🔔 {unread} ta yangi bildirishnoma"
        await message.answer(text, reply_markup=main_menu_keyboard(), parse_mode="HTML")
    else:
        # New user — show welcome + registration prompt
        await message.answer(
            t("welcome"),
            reply_markup=registration_keyboard(),
            parse_mode="HTML",
        )


@router.message(Command("menu"))
@router.message(F.text == "🏠 Asosiy menyu")
async def cmd_menu(
    message: Message,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """Show main menu."""
    await state.clear()
    if teacher:
        await message.answer(
            t("main_menu"),
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML",
        )
    else:
        await message.answer(
            t("welcome"),
            reply_markup=registration_keyboard(),
            parse_mode="HTML",
        )


@router.callback_query(F.data == PREFIX_BACK_MAIN)
async def cb_back_main(
    callback: CallbackQuery,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """Return to main menu via callback."""
    await state.clear()
    await callback.answer()
    if teacher:
        await callback.message.edit_text(
            t("main_menu"),
            parse_mode="HTML",
        )
    else:
        await callback.message.edit_text(
            t("error_not_registered"),
            parse_mode="HTML",
        )


@router.callback_query(F.data == PREFIX_CLOSE)
async def cb_close(callback: CallbackQuery, **kwargs):
    """Close/dismiss an inline message."""
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        await callback.message.edit_text("❎ Yopildi.")

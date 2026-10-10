# ============================================================
# Notifications Handler — Viewing notifications
# ============================================================

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, Optional

from locales.uz import t
from keyboards.inline import PREFIX_NOTIF_READ_ALL, notifications_keyboard, PREFIX_CLOSE
from services.notification_service import NotificationService
from utils.formatters import format_notification

router = Router()


@router.message(F.text == "🔔 Bildirishnomalar")
@router.message(F.text == "/notifications")
async def cmd_notifications(
    message: Message,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """View notifications."""
    if not teacher:
        await message.answer(t("error_not_registered"), parse_mode="HTML")
        return

    notifications = NotificationService.get_teacher_notifications(teacher["id"], limit=10)
    unread_count = NotificationService.get_unread_count(teacher["id"])
    
    text = t("notif_title")
    
    if unread_count > 0:
        text += t("notif_unread_count", count=unread_count) + "\n\n"
        
    if not notifications:
        text += t("notif_empty")
    else:
        for notif in notifications:
            text += format_notification(notif) + "\n\n"

    # Mark visible notifications as read
    for notif in notifications:
        if not notif.get("is_read"):
            NotificationService.mark_read(notif["id"])
            
    await message.answer(
        text,
        reply_markup=notifications_keyboard(has_unread=unread_count > 0),
        parse_mode="HTML"
    )


@router.callback_query(F.data == PREFIX_NOTIF_READ_ALL)
async def cb_notif_read_all(
    callback: CallbackQuery,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """Mark all notifications as read."""
    if not teacher:
        await callback.answer(t("error_not_registered"), show_alert=True)
        return

    NotificationService.mark_all_read(teacher["id"])
    
    await callback.answer(t("notif_mark_read"))
    
    # Reload notifications
    notifications = NotificationService.get_teacher_notifications(teacher["id"], limit=10)
    
    text = t("notif_title")
    if not notifications:
        text += t("notif_empty")
    else:
        for notif in notifications:
            text += format_notification(notif) + "\n\n"
            
    await callback.message.edit_text(
        text,
        reply_markup=notifications_keyboard(has_unread=False),
        parse_mode="HTML"
    )

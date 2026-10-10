# ============================================================
# Reply Keyboards (persistent bottom keyboards)
# ============================================================

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Main menu reply keyboard for registered teachers."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📅 Dars jadvali"),
                KeyboardButton(text="📊 Davomat"),
            ],
            [
                KeyboardButton(text="📷 QR Skanerlash"),
                KeyboardButton(text="🏫 Maktablarim"),
            ],
            [
                KeyboardButton(text="👤 Profilim"),
                KeyboardButton(text="📊 Ish yuklama"),
            ],
            [
                KeyboardButton(text="🔔 Bildirishnomalar"),
                KeyboardButton(text="🔒 Xavfsizlik"),
            ],
            [
                KeyboardButton(text="ℹ️ Yordam"),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def registration_keyboard() -> ReplyKeyboardMarkup:
    """Keyboard shown to unregistered users."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Ro'yxatdan o'tish")],
            [KeyboardButton(text="ℹ️ Yordam")],
        ],
        resize_keyboard=True,
    )


def phone_keyboard() -> ReplyKeyboardMarkup:
    """Keyboard for sharing phone number."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)],
            [KeyboardButton(text="🚫 Bekor qilish")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def location_keyboard() -> ReplyKeyboardMarkup:
    """Keyboard for sharing location."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)],
            [KeyboardButton(text="🚫 Bekor qilish")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def cancel_keyboard() -> ReplyKeyboardMarkup:
    """Simple cancel keyboard."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🚫 Bekor qilish")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def confirm_keyboard() -> ReplyKeyboardMarkup:
    """Confirmation keyboard."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="✅ Tasdiqlash"),
                KeyboardButton(text="🚫 Bekor qilish"),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def remove_keyboard() -> ReplyKeyboardRemove:
    """Remove reply keyboard."""
    return ReplyKeyboardRemove()

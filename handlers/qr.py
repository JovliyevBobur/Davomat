# ============================================================
# QR Scanner Handler — Processing QR scans
# ============================================================

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, Optional

from states import QRScanStates
from locales.uz import t
from keyboards.reply import location_keyboard, main_menu_keyboard, cancel_keyboard
from services.qr_service import QRService
from services.schedule_service import ScheduleService
from utils.validators import validate_qr_token

router = Router()


@router.message(F.text == "📷 QR Skanerlash")
async def cmd_scan_qr(
    message: Message,
    state: FSMContext,
    teacher: Optional[Dict[str, Any]] = None,
    **kwargs,
):
    """Start QR scan flow."""
    if not teacher:
        await message.answer(t("error_not_registered"), parse_mode="HTML")
        return

    await state.set_state(QRScanStates.waiting_qr)
    await message.answer(t("qr_scan_title"), reply_markup=cancel_keyboard(), parse_mode="HTML")


@router.message(QRScanStates.waiting_qr, F.photo)
async def process_qr_photo(message: Message, state: FSMContext, **kwargs):
    """
    Process uploaded QR photo.
    NOTE: In a real Telegram bot, you would download the photo and decode it
    using OpenCV/ZBar. For this demo, we instruct the user to use their phone's
    native scanner if the bot can't decode it, or they can send the token text.
    """
    await message.answer(
        "📷 Rasm qabul qilindi.\n"
        "<i>(Eslatma: Bot orqali to'g'ridan-to'g'ri rasm o'qish imkoniyati cheklangan. "
        "Yaxshisi, kamerangiz orqali o'qitib, havola/matnni yuboring)</i>",
        parse_mode="HTML",
    )


@router.message(QRScanStates.waiting_qr, F.text)
async def process_qr_text(message: Message, state: FSMContext, teacher: Optional[Dict[str, Any]] = None, **kwargs):
    """Process QR token text."""
    if message.text == "🚫 Bekor qilish":
        await state.clear()
        await message.answer(t("action_cancelled"), reply_markup=main_menu_keyboard(), parse_mode="HTML")
        return

    if not teacher:
        return

    token = message.text.strip()
    
    # Extract token if it's a URL (e.g., https://t.me/bot?start=qr_TOKEN)
    if "start=qr_" in token:
        token = token.split("start=qr_")[-1].split("&")[0]
    elif "start=" in token:
        token = token.split("start=")[-1].split("&")[0]

    if not validate_qr_token(token):
        await message.answer(t("qr_invalid"), parse_mode="HTML")
        return

    msg = await message.answer(t("qr_processing"), parse_mode="HTML")

    # Validate token
    validation = QRService.validate_qr_token(token)
    
    if not validation["valid"]:
        error_msg = t(f"qr_error_{validation['error'].lower()}") if validation['error'] else t("qr_invalid")
        await msg.edit_text(error_msg, parse_mode="HTML")
        return
        
    qr_data = validation["qr"]
    school_id = qr_data["school_id"]
    class_id = qr_data["class_id"]

    # Check if teacher has a lesson for this class right now
    lesson = ScheduleService.find_lesson_for_class_at_time(teacher["id"], school_id, class_id)
    
    if not lesson:
        await msg.edit_text(t("qr_error_no_lesson"), parse_mode="HTML")
        return

    # Store necessary data in state to wait for location
    await state.update_data(
        qr_token=token,
        school_id=school_id,
        class_id=class_id,
        lesson_id=lesson["id"],
    )

    await msg.delete()
    await state.set_state(QRScanStates.waiting_location)
    await message.answer(t("qr_location_request"), reply_markup=location_keyboard(), parse_mode="HTML")


@router.message(QRScanStates.waiting_location)
async def process_location(message: Message, state: FSMContext, teacher: Optional[Dict[str, Any]] = None, **kwargs):
    """Process location for QR scan."""
    if message.text == "🚫 Bekor qilish":
        await state.clear()
        await message.answer(t("action_cancelled"), reply_markup=main_menu_keyboard(), parse_mode="HTML")
        return

    if not teacher:
        return

    lat, lon = None, None
    if message.location:
        lat = message.location.latitude
        lon = message.location.longitude
    
    # In production, we would send this data to Railway for full validation
    # For this phase, we mock a successful validation assuming location is correct
    
    data = await state.get_data()
    
    # Generate success message (mocking Railway's successful response)
    # The actual database insert would be handled by Railway
    
    class_name = "Sinf"
    subject_name = "Fan"
    school_name = "Maktab"
    time_str = "Hozir"
    
    # Attempt to get real names if available via the QR validation
    validation = QRService.validate_qr_token(data["qr_token"])
    if validation["valid"]:
        class_name = validation["class_info"].get("name", class_name)
        school_name = validation["school_info"].get("name", school_name)
        
    lesson = ScheduleService.find_lesson_for_class_at_time(teacher["id"], data["school_id"], data["class_id"])
    if lesson:
        subject_name = lesson.get("subjects", {}).get("name", subject_name)
        time_str = f"{lesson.get('start_time')}–{lesson.get('end_time')}"

    await state.clear()
    await message.answer(
        t(
            "qr_success",
            school_name=school_name,
            class_name=class_name,
            subject=subject_name,
            time=time_str,
            status="Kelgan (Test)",
            status_emoji="✅"
        ),
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )

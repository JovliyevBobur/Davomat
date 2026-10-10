# ============================================================
# Uzbek Localization Strings
# ============================================================
# All user-facing text is centralized here for easy translation.

TEXTS = {
    # ── General ──
    "welcome": (
        "🎓 <b>Xush kelibsiz!</b>\n\n"
        "Bu bot orqali o'qituvchi sifatida maktabga ro'yxatdan o'tishingiz, "
        "dars jadvalingizni ko'rishingiz va davomat qaydlarini boshqarishingiz mumkin.\n\n"
        "Boshlash uchun <b>📝 Ro'yxatdan o'tish</b> tugmasini bosing."
    ),
    "welcome_back": (
        "👋 <b>Qaytganingizdan xursandmiz, {name}!</b>\n\n"
        "Quyidagi menyu orqali kerakli bo'limni tanlang."
    ),
    "main_menu": "🏠 <b>Asosiy menyu</b>\n\nKerakli bo'limni tanlang:",
    "loading": "⏳ Yuklanmoqda...",
    "error_generic": "❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.",
    "error_not_registered": "⚠️ Siz hali ro'yxatdan o'tmagansiz. /start buyrug'ini yuboring.",
    "error_no_school": "⚠️ Siz hech qanday maktabga biriktirilmagansiz.",
    "error_rate_limit": "⏱ Juda tez so'rov yuborilmoqda. Biroz kuting.",
    "action_cancelled": "🚫 Amal bekor qilindi.",
    "confirm_yes": "✅ Ha",
    "confirm_no": "❌ Yo'q",
    "back": "🔙 Orqaga",
    "cancel": "🚫 Bekor qilish",
    "close": "❎ Yopish",

    # ── Registration ──
    "reg_start": (
        "📝 <b>Ro'yxatdan o'tish</b>\n\n"
        "Keling, ma'lumotlaringizni kiritamiz.\n"
        "Ismingizni yuboring:"
    ),
    "reg_first_name": "Ismingizni kiriting:",
    "reg_last_name": "Familiyangizni kiriting:",
    "reg_middle_name": "Otangizning ismini kiriting (ixtiyoriy, o'tkazish uchun /skip):",
    "reg_phone": (
        "📱 Telefon raqamingizni yuboring.\n"
        "Tugmani bosing yoki qo'lda kiriting (+998XXXXXXXXX):"
    ),
    "reg_phone_invalid": "❌ Noto'g'ri telefon raqam formati. +998XXXXXXXXX shaklida kiriting.",
    "reg_email": "📧 Email manzilingizni kiriting (ixtiyoriy, o'tkazish uchun /skip):",
    "reg_email_invalid": "❌ Noto'g'ri email formati.",
    "reg_confirm": (
        "📋 <b>Ma'lumotlaringizni tasdiqlang:</b>\n\n"
        "👤 Ism: <b>{first_name}</b>\n"
        "👤 Familiya: <b>{last_name}</b>\n"
        "👤 Otasining ismi: <b>{middle_name}</b>\n"
        "📱 Telefon: <b>{phone}</b>\n"
        "📧 Email: <b>{email}</b>\n\n"
        "Tasdiqlaysizmi?"
    ),
    "reg_success": (
        "✅ <b>Ro'yxatdan muvaffaqiyatli o'tdingiz!</b>\n\n"
        "Endi maktab tanlashingiz mumkin."
    ),
    "reg_already": "ℹ️ Siz allaqachon ro'yxatdan o'tgansiz.",

    # ── School Selection ──
    "school_select": (
        "🏫 <b>Maktab tanlash</b>\n\n"
        "Qaysi maktabga qo'shilmoqchisiz?\n"
        "Ro'yxatdan tanlang:"
    ),
    "school_no_schools": "😕 Hozircha maktablar mavjud emas.",
    "school_request_sent": (
        "📨 <b>So'rov yuborildi!</b>\n\n"
        "🏫 Maktab: <b>{school_name}</b>\n"
        "📊 Holat: <b>⏳ Kutilmoqda</b>\n\n"
        "Maktab ma'muriyati so'rovingizni ko'rib chiqadi."
    ),
    "school_already_member": "ℹ️ Siz allaqachon <b>{school_name}</b> maktabiga so'rov yuborgansiz.",
    "school_request_confirm": "🏫 <b>{school_name}</b> maktabiga qo'shilish so'rovini yuborasizmi?",

    # ── My Schools ──
    "my_schools_title": "🏫 <b>Mening maktablarim</b>\n",
    "my_schools_empty": "😕 Siz hech qanday maktabga biriktirilmagansiz.\n\n🏫 Maktab tanlash uchun tugmani bosing.",
    "my_schools_item": (
        "\n🏫 <b>{school_name}</b>\n"
        "   📊 Holat: {status_emoji} <b>{status}</b>\n"
    ),

    # ── Membership Statuses ──
    "status_PENDING": "⏳ Kutilmoqda",
    "status_APPROVED": "✅ Tasdiqlangan",
    "status_REJECTED": "❌ Rad etilgan",
    "status_SUSPENDED": "⛔ To'xtatilgan",

    # ── Schedule ──
    "schedule_title": "📅 <b>Dars jadvali</b>\n\nMaktabni tanlang:",
    "schedule_school_title": "📅 <b>{school_name} — Dars jadvali</b>\n\nKunni tanlang:",
    "schedule_day_title": "📅 <b>{school_name}</b>\n📆 <b>{day}</b>\n",
    "schedule_empty": "📭 Bu kun uchun dars jadvalingiz topilmadi.",
    "schedule_item": (
        "\n⏰ <b>{start_time}–{end_time}</b>\n"
        "   📚 {subject}\n"
        "   🏫 {class_name}\n"
        "   🚪 Xona: {room}\n"
    ),
    "schedule_today": "📅 <b>Bugungi jadval</b>\n",
    "schedule_no_approved": "⚠️ Tasdiqlangan maktabingiz yo'q. Jadval ko'rish uchun avval maktabga qo'shiling.",

    # ── Days of Week ──
    "day_MONDAY": "Dushanba",
    "day_TUESDAY": "Seshanba",
    "day_WEDNESDAY": "Chorshanba",
    "day_THURSDAY": "Payshanba",
    "day_FRIDAY": "Juma",
    "day_SATURDAY": "Shanba",
    "day_SUNDAY": "Yakshanba",

    # ── Attendance ──
    "attendance_title": "📊 <b>Davomat</b>\n\nMaktabni tanlang:",
    "attendance_school_title": "📊 <b>{school_name} — Davomat</b>\n\nDavrni tanlang:",
    "attendance_today": "📊 <b>Bugungi davomat</b>\n",
    "attendance_empty": "📭 Davomat qaydlari topilmadi.",
    "attendance_item": (
        "\n⏰ <b>{scheduled_time}</b>\n"
        "   📚 {subject} | 🏫 {class_name}\n"
        "   📊 Holat: {status_emoji} <b>{status}</b>\n"
        "   🕐 Kirish: {scan_time}\n"
        "   ⏱ Kechikish: {late_min} daqiqa\n"
    ),
    "attendance_status_PRESENT": "✅ Kelgan",
    "attendance_status_LATE": "⚠️ Kechikkan",
    "attendance_status_MISSING": "❌ Kelmagan",
    "attendance_summary": (
        "\n📈 <b>Xulosa:</b>\n"
        "   ✅ Kelgan: {present}\n"
        "   ⚠️ Kechikkan: {late}\n"
        "   ❌ Kelmagan: {missing}\n"
        "   📊 Jami: {total}\n"
    ),

    # ── QR Code ──
    "qr_scan_title": (
        "📷 <b>QR kod skanerlash</b>\n\n"
        "Sinf xonasidagi QR kodni skanerlang.\n"
        "QR kod rasmini yuboring yoki matnini kiriting:"
    ),
    "qr_processing": "⏳ QR kod tekshirilmoqda...",
    "qr_invalid": "❌ Noto'g'ri QR kod. Iltimos, sinf xonasidagi to'g'ri QR kodni skanerlang.",
    "qr_success": (
        "✅ <b>Davomat qayd etildi!</b>\n\n"
        "🏫 Maktab: <b>{school_name}</b>\n"
        "🏫 Sinf: <b>{class_name}</b>\n"
        "📚 Fan: <b>{subject}</b>\n"
        "⏰ Vaqt: <b>{time}</b>\n"
        "📊 Holat: {status_emoji} <b>{status}</b>\n"
    ),
    "qr_error_no_lesson": "⚠️ Hozirda siz uchun rejalashtirilgan dars topilmadi.",
    "qr_error_disabled": "⛔ Bu QR kod o'chirilgan. Maktab ma'muriyatiga murojaat qiling.",
    "qr_error_outside": "📍 Siz maktab hududidan tashqaridasiz.",
    "qr_error_already": "ℹ️ Siz bu dars uchun allaqachon qayd etilgansiz.",
    "qr_location_request": (
        "📍 <b>Joylashuv talab qilinadi</b>\n\n"
        "Davomatni qayd etish uchun joylashuvingizni yuboring.\n"
        "Quyidagi tugmani bosing:"
    ),

    # ── Profile ──
    "profile_title": (
        "👤 <b>Mening profilim</b>\n\n"
        "👤 Ism: <b>{first_name}</b>\n"
        "👤 Familiya: <b>{last_name}</b>\n"
        "👤 Otasining ismi: <b>{middle_name}</b>\n"
        "📱 Telefon: <b>{phone}</b>\n"
        "📧 Email: <b>{email}</b>\n"
        "🔗 Telegram: <b>{telegram_status}</b>\n"
        "📅 Ro'yxatdan: <b>{created_at}</b>\n"
    ),
    "profile_edit_what": "✏️ Nimani tahrirlash kerak?",
    "profile_edit_phone": "📱 Yangi telefon raqamni kiriting:",
    "profile_edit_email": "📧 Yangi email kiriting:",
    "profile_edit_success": "✅ Ma'lumot yangilandi!",

    # ── Notifications ──
    "notif_title": "🔔 <b>Bildirishnomalar</b>\n",
    "notif_empty": "📭 Yangi bildirishnomalar yo'q.",
    "notif_item": "\n{icon} <b>{title}</b>\n   {message}\n   🕐 {time}\n",
    "notif_unread_count": "🔔 Siz <b>{count}</b> ta o'qilmagan bildirishnomangiz bor.",
    "notif_mark_read": "✅ Barcha o'qilgan deb belgilandi.",

    # ── Workload ──
    "workload_title": "📊 <b>Ish yuklama</b>\n\nMaktabni tanlang:",
    "workload_school_title": (
        "📊 <b>{school_name} — Ish yuklama</b>\n\n"
        "👤 O'qituvchi: <b>{teacher_name}</b>\n"
        "📚 Fanlar: {subjects}\n"
        "🏫 Sinflar: {classes}\n"
        "📅 Haftalik soatlar: <b>{weekly_hours}</b>\n"
        "📆 Oylik soatlar: <b>{monthly_hours}</b>\n"
    ),

    # ── Security ──
    "security_title": "🔒 <b>Xavfsizlik voqealari</b>\n",
    "security_empty": "📭 Xavfsizlik voqealari topilmadi.",
    "security_item": (
        "\n🔒 <b>{event_type}</b>\n"
        "   🏫 {school_name} | 🏫 {class_name}\n"
        "   📍 Masofa: {distance}m\n"
        "   📝 {reason}\n"
        "   🕐 {time}\n"
    ),

    # ── Help ──
    "help_text": (
        "ℹ️ <b>Yordam</b>\n\n"
        "<b>Asosiy buyruqlar:</b>\n"
        "/start — Botni ishga tushirish\n"
        "/menu — Asosiy menyu\n"
        "/profile — Profilim\n"
        "/schedule — Dars jadvali\n"
        "/attendance — Davomat\n"
        "/schools — Mening maktablarim\n"
        "/workload — Ish yuklama\n"
        "/notifications — Bildirishnomalar\n"
        "/help — Yordam\n\n"
        "<b>QR skanerlash:</b>\n"
        "Sinf xonasidagi QR kodni rasmga oling va botga yuboring.\n\n"
        "<b>Muammo bo'lsa:</b>\n"
        "Maktab ma'muriyatiga murojaat qiling."
    ),

    # ── Admin Notifications ──
    "admin_new_membership": (
        "🔔 <b>Yangi o'qituvchi so'rovi!</b>\n\n"
        "👤 O'qituvchi: <b>{teacher_name}</b>\n"
        "🏫 Maktab: <b>{school_name}</b>\n"
        "📱 Telefon: <b>{phone}</b>\n"
        "🕐 Vaqt: <b>{time}</b>\n"
    ),
}


def t(key: str, **kwargs) -> str:
    """Get localized text with optional formatting."""
    text = TEXTS.get(key, key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text

# ============================================================
# Validators — Input validation utilities
# ============================================================

import re
from typing import Optional


def validate_phone(phone: str) -> Optional[str]:
    """
    Validate and normalize an Uzbek phone number.
    Accepts formats: +998XXXXXXXXX, 998XXXXXXXXX, XXXXXXXXX
    Returns normalized +998XXXXXXXXX or None if invalid.
    """
    # Remove all non-digit characters
    digits = re.sub(r"\D", "", phone)

    # Handle different formats
    if digits.startswith("998") and len(digits) == 12:
        return f"+{digits}"
    elif len(digits) == 9 and digits[0] in "3456789":
        return f"+998{digits}"
    elif digits.startswith("+998") and len(digits) == 13:
        return f"+{digits[1:]}"

    return None


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email.strip()))


def validate_name(name: str) -> bool:
    """
    Validate a name (first, last, middle).
    Must be 2-50 characters, letters and spaces only.
    """
    if not name or len(name.strip()) < 2 or len(name.strip()) > 50:
        return False
    # Allow Cyrillic, Latin, apostrophes, hyphens, spaces
    pattern = r"^[a-zA-Zа-яА-ЯёЁўЎқҚғҒҳҲ\s'\-]+$"
    return bool(re.match(pattern, name.strip()))


def sanitize_text(text: str) -> str:
    """Remove potentially dangerous HTML/script content."""
    # Remove HTML tags
    clean = re.sub(r"<[^>]+>", "", text)
    # Remove script patterns
    clean = re.sub(r"javascript:", "", clean, flags=re.IGNORECASE)
    return clean.strip()


def validate_qr_token(token: str) -> bool:
    """
    Basic validation of a QR token format.
    QR tokens should be UUIDs or similar structured identifiers.
    """
    # Accept UUID format
    uuid_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    if re.match(uuid_pattern, token.strip().lower()):
        return True
    # Accept alphanumeric tokens (16-64 chars)
    if re.match(r"^[a-zA-Z0-9_-]{16,64}$", token.strip()):
        return True
    return False

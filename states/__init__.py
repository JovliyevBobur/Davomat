# ============================================================
# FSM States — Finite State Machine states for conversations
# ============================================================

from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    """States for teacher registration flow."""
    first_name = State()
    last_name = State()
    middle_name = State()
    phone = State()
    email = State()
    confirm = State()


class ProfileEditStates(StatesGroup):
    """States for profile editing."""
    edit_phone = State()
    edit_email = State()


class QRScanStates(StatesGroup):
    """States for QR scanning flow."""
    waiting_qr = State()
    waiting_location = State()


class SchoolJoinStates(StatesGroup):
    """States for school joining flow."""
    selecting_school = State()
    confirming = State()

# ============================================================
# QR Code Service — Supabase CRUD + QR operations
# ============================================================

from database import get_supabase
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class QRService:
    """Service layer for QR code operations."""

    @staticmethod
    def get_by_token(token: str) -> Optional[Dict[str, Any]]:
        """Look up a QR code record by its public token."""
        try:
            db = get_supabase()
            response = (
                db.table("class_qr_codes")
                .select(
                    "*, "
                    "classes(id, name, grade, section), "
                    "schools(id, name, short_name, latitude, longitude, "
                    "geofence_radius, max_gps_accuracy, attendance_window_minutes, "
                    "missing_grace_minutes)"
                )
                .eq("token", token)
                .limit(1)
                .execute()
            )
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error looking up QR token: {e}")
            return None

    @staticmethod
    def get_active_by_class(class_id: str) -> Optional[Dict[str, Any]]:
        """Get the active QR code for a class."""
        try:
            db = get_supabase()
            response = (
                db.table("class_qr_codes")
                .select("*")
                .eq("class_id", class_id)
                .eq("status", "ACTIVE")
                .limit(1)
                .execute()
            )
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error getting QR for class {class_id}: {e}")
            return None

    @staticmethod
    def validate_qr_token(token: str) -> Dict[str, Any]:
        """
        Validate a QR token and return the associated class/school info.
        Returns a dict with 'valid' bool and relevant data or error message.

        NOTE: This is a preliminary validation only.
        The authoritative validation happens in Railway backend.
        """
        result = {
            "valid": False,
            "error": None,
            "qr": None,
            "class_info": None,
            "school_info": None,
        }

        qr = QRService.get_by_token(token)
        if not qr:
            result["error"] = "INVALID_QR"
            return result

        if qr.get("status") != "ACTIVE":
            result["error"] = "DISABLED_QR"
            return result

        result["valid"] = True
        result["qr"] = qr
        result["class_info"] = qr.get("classes")
        result["school_info"] = qr.get("schools")

        return result

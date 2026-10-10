# ============================================================
# Database Layer - Supabase Client
# ============================================================

from supabase import create_client, Client
from config import get_settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)

_client: Optional[Client] = None


def get_supabase() -> Client:
    """Get or create Supabase client singleton."""
    global _client
    if _client is None:
        settings = get_settings()
        _client = create_client(
            settings.supabase_url,
            settings.supabase_anon_key,
        )
        logger.info("Supabase client initialized")
    return _client


def reset_client():
    """Reset the client (useful for testing)."""
    global _client
    _client = None

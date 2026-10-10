# ============================================================
# School ERP + Teacher CRM + Teacher Attendance Telegram Bot
# Configuration Module
# ============================================================

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # Telegram
    bot_token: str = Field(..., alias="BOT_TOKEN")
    bot_admin_ids: str = Field(default="", alias="BOT_ADMIN_IDS")

    # Supabase
    supabase_url: str = Field(..., alias="SUPABASE_URL")
    supabase_anon_key: str = Field(..., alias="SUPABASE_ANON_KEY")

    # Bot Settings
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    webhook_url: Optional[str] = Field(default=None, alias="WEBHOOK_URL")
    webhook_port: int = Field(default=8443, alias="WEBHOOK_PORT")

    # Rate Limiting
    rate_limit_seconds: int = Field(default=1, alias="RATE_LIMIT_SECONDS")

    # Localization
    default_language: str = Field(default="uz", alias="DEFAULT_LANGUAGE")

    @property
    def admin_ids(self) -> List[int]:
        """Parse comma-separated admin IDs."""
        if not self.bot_admin_ids:
            return []
        return [int(x.strip()) for x in self.bot_admin_ids.split(",") if x.strip()]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


def get_settings() -> Settings:
    """Get application settings singleton."""
    return Settings()

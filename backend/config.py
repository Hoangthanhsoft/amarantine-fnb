from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Amarantine AI — F&B Ops System"
    debug: bool = False

    # Database
    database_url: str = ""

    # AI Models
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    openai_model: str = "gpt-4o"

    # App
    default_venue_id: str = "demo-venue"
    content_cost_per_hour_aud: float = 85.0

    # Premium features (Full Version) — optional, empty by default
    google_drive_folder_id: str = ""
    google_credentials_json: str = ""
    google_sheet_id: str = ""
    canva_api_token: str = ""
    canva_template_square: str = ""
    canva_template_story: str = ""
    canva_template_signage: str = ""
    canva_template_menu: str = ""
    replicate_api_token: str = ""
    creatomate_api_key: str = ""
    creatomate_template_15s: str = ""
    creatomate_template_30s: str = ""
    fb_page_id: str = ""
    fb_page_access_token: str = ""

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict

class BaseConfig(BaseSettings):
    """Base configuration for app"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        env_file_encoding="utf-8",
        extra="allow",
    )

class Settings(BaseConfig):
    """Settings for app"""
    
    dev_mode: bool = True
    
    flet_host: str = "0.0.0.0"
    flet_port: int = 50002
    flet_slug: str = 'e_library'
    flet_secret_key: str = "flet_secret_key"
    flet_assets_dir: str = ""
    
    flet_prod_host: str = ""
    download_server_url: str = ""

def get_settings() -> Settings:
    "Get Settings for app"
    
    return Settings()
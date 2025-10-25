# src/App/Utility/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# Класс для настроек OAuth2 (оставляем, как было)
class SchoolAPISettings(BaseSettings):
    # ... (код для client_id, client_secret и URL'ов) ...
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    client_id: str = Field(..., validation_alias='SCHOOL_API_CLIENT_ID')
    client_secret: str = Field(..., validation_alias='SCHOOL_API_CLIENT_SECRET')
    redirect_uri: str = "https://localhost:8443/Auth/callback"
    authorize_url: str = "https://api.intra.42.fr/oauth/authorize"
    token_url: str = "https://api.intra.42.fr/oauth/token"

# НОВЫЙ КЛАСС: Общие настройки и Секретный ключ
class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # Секретный ключ для подписи куки-файлов или токенов сессий
    # КЛЮЧЕВОЙ АНАЛОГ $_SESSION['SECRET_KEY']
    secret_key: str = Field(..., validation_alias='APP_SECRET_KEY')

    # Добавьте сюда другие общие настройки (например, имя куки-файла)

app_settings = AppSettings()
oauth_settings = SchoolAPISettings()

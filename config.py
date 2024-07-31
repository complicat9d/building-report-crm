from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseSettings):
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_HOST: str = "db"
    DATABASE_PORT: int = 5432
    DATABASE_DB: str = "postgres"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    db: DbSettings = DbSettings()

    TOKEN: str
    BOT_NAME: str
    CHAR_LIMIT: int = 4096
    PHOTO_LIMIT: int = 10

    DEBUG_ENGINE: bool = False

    BREAK: int = 60
    BEFORE_BREAK_FINISH: int = 15
    SCHEDULER_DELAY: int = 1

    LOGIN: str = "admin"
    PASSWORD: str
    ENABLE_DOCS: bool = False


settings = Settings()

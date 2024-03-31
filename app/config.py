from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_type: str
    database_engine: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOSTNAME: str
    DATABASE_NAME: str
    DB_PORT: str
    model_config = SettingsConfigDict(env_file=".env")
    SECRTE_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


settings = Settings()

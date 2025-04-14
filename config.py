import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Bot
    BOT_TOKEN: str
    DEBUG: bool = False

    # Database
    PG_USERNAME: str
    PG_PASSWORD: str
    PG_HOSTNAME: str
    PG_PORT: str = '5432'
    PG_DB_NAME: str

    # Directories
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    LOGS_DIR: str = os.path.join(BASE_DIR, 'logs')
    LOGS_DIR_CHATS: str = os.path.join(LOGS_DIR, 'chats')
    LOG_DIRECTORIES: list[str] = [LOGS_DIR, LOGS_DIR_CHATS]

    # Other
    LOGS_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FORBIDDEN_WORDS: list[str] = ['key', 'token', 'secret', 'password']

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()

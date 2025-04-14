from config import settings


def get_db_url():
    return(f"postgresql+asyncpg://{settings.PG_USERNAME}:{settings.PG_PASSWORD}"
        f"@{settings.PG_HOSTNAME}:{settings.PG_PORT}/{settings.PG_DB_NAME}")

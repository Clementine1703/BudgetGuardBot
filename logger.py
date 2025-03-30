import os
import logging
from idlelib.iomenu import encoding

from config import settings


def setup_logger():
    def create_directories(directory_paths: list[str]) -> None:
        for directory in directory_paths:
            os.makedirs(directory, exist_ok=True)

    create_directories(settings.LOG_DIRECTORIES)
    logging.basicConfig(
        filename=f'{settings.LOGS_DIR}/main.log',
        level=logging.INFO,
        format=settings.LOGS_FORMAT,
        encoding='utf-8'
    )

    error_handler = logging.FileHandler(
        filename=f'{settings.LOGS_DIR}/error.log',
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)

    logger = logging.getLogger()
    logger.addHandler(error_handler)

    apply_filter_to_all_loggers(ForbiddenWordsFilter())

    if settings.DEBUG:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)


def get_current_chat_logger(chat_id: int):
    def remove_all_handlers(logger: logging.Logger):
        for handler in logger.handlers:
            logger.removeHandler(handler)

    logger = logging.getLogger(f'chat_{chat_id}')
    remove_all_handlers(logger)

    os.makedirs(settings.LOGS_DIR_CHATS, exist_ok=True)
    filepath = os.path.join(settings.LOGS_DIR_CHATS, f'{chat_id}.log')

    handler = logging.FileHandler(filename=filepath, encoding='utf-8')
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(settings.LOGS_FORMAT))

    logger.addHandler(handler)
    return logger


def apply_filter_to_all_loggers(filter):
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        handler.addFilter(filter)

    original_get_logger = logging.getLogger

    def custom_get_logger(name=None):
        logger = original_get_logger(name)
        for handler in logger.handlers:
            handler.addFilter(filter)
        return logger

    logging.getLogger = custom_get_logger


class ForbiddenWordsFilter(logging.Filter):
    def filter(self, record):
        return not any(word in record.getMessage() for word in settings.LOG_FORBIDDEN_WORDS)



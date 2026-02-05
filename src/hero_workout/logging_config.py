import logging

from hero_workout.config import LOG_LEVEL

def get_logger(name: str, level: int=LOG_LEVEL) -> logging.Logger:
    """
    Returns a logger that prints messages like:
    [CallingClass: LOGLEVEL]: message
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove default handler (pyttsx3 interferes)
    if logger.hasHandlers():
        logger.handlers.clear()

    # No duplicate logs
    logger.propagate = False

    # Avoid adding multiple handlers if called repeatedly
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(level)

        formatter = logging.Formatter(fmt='[%(name)s: %(levelname)s]: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

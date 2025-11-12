import logging
import sys
from typing import Optional

def get_logger(name: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """
    Create a colorless, concise logger suitable for CLI tools.
    """
    logger = logging.getLogger(name if name else "paginegialle")
    if logger.handlers:
        return logger

    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    fmt = "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
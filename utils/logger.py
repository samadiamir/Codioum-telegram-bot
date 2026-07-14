"""
Logging utility for the bot.
Provides consistent logging across all modules.
"""

import logging
import sys
from datetime import datetime

# Create logger
logger = logging.getLogger("codioum_bot")
logger.setLevel(logging.DEBUG)

# Create console handler with UTF-8 encoding
import io
console_stream = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
console_handler = logging.StreamHandler(console_stream)
console_handler.setLevel(logging.DEBUG)

# Create file handler
log_file = f"logs/bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
try:
    import os
    os.makedirs("logs", exist_ok=True)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
except Exception as e:
    print(f"Warning: Could not create log file handler: {e}")
    file_handler = None

# Create formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Add formatter to handlers
console_handler.setFormatter(formatter)
if file_handler:
    file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
if file_handler:
    logger.addHandler(file_handler)


def log_info(message):
    """Log info message."""
    logger.info(message)


def log_error(message, exception=None):
    """Log error message with optional exception."""
    if exception:
        logger.error(f"{message}: {exception}", exc_info=True)
    else:
        logger.error(message)


def log_warning(message):
    """Log warning message."""
    logger.warning(message)


def log_debug(message):
    """Log debug message."""
    logger.debug(message)

"""Logging setup."""

import logging


def setup_logging(log_level: int) -> None:
    """Set up logging with the given log level and a custom format string."""
    logging.basicConfig(level=log_level)
    if log_level == logging.INFO:
        formatter = logging.Formatter("%(levelname)s: %(message)s")
        logging.getLogger().handlers[0].setFormatter(formatter)

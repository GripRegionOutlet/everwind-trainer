from __future__ import annotations

import logging
import sys

from colorama import Fore, Style, init as colorama_init


class _ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
    }

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, "")
        base = super().format(record)
        return f"{color}{base}{Style.RESET_ALL}"


def setup_logger(level: str = "INFO") -> None:
    colorama_init()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(_ColorFormatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                                         datefmt="%H:%M:%S"))
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
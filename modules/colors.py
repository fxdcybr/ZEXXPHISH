"""
===========================================================
ZEXXPHISH
Advanced Phishing Analyzer

File: colors.py
===========================================================
"""

from colorama import Style, init

init(autoreset=True)


class Colors:

    # Theme Colors (24-bit ANSI)
    PURPLE = "\033[38;2;160;32;240m"      # Deep Neon Purple
    CYAN = "\033[38;2;0;255;255m"         # Electric Cyan
    WHITE = "\033[38;2;245;245;245m"

    # Status
    GREEN = "\033[38;2;57;255;20m"
    YELLOW = "\033[38;2;255;215;0m"
    RED = "\033[38;2;255;60;60m"

    # Misc
    BLUE = "\033[38;2;0;170;255m"

    RESET = "\033[0m"

    BRIGHT = Style.BRIGHT
    NORMAL = Style.NORMAL
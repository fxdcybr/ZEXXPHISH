"""
===========================================================
ZEXXPHISH
Advanced Phishing Analyzer

File: banner.py
Description:
Displays the startup banner.
===========================================================
"""

from modules.colors import Colors


def display_banner():
    banner = f"""{Colors.PURPLE}
███████╗███████╗██╗  ██╗██╗  ██╗██████╗ ██╗  ██╗██╗███████╗██╗  ██╗
╚══███╔╝██╔════╝╚██╗██╔╝╚██╗██╔╝██╔══██╗██║  ██║██║██╔════╝██║  ██║
  ███╔╝ █████╗   ╚███╔╝  ╚███╔╝ ██████╔╝███████║██║███████╗███████║
 ███╔╝  ██╔══╝   ██╔██╗  ██╔██╗ ██╔═══╝ ██╔══██║██║╚════██║██╔══██║
███████╗███████╗██╔╝ ██╗██╔╝ ██╗██║     ██║  ██║██║███████║██║  ██║
╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝
{Colors.RESET}
{Colors.CYAN}                     Advanced Phishing Analyzer{Colors.RESET}

{Colors.CYAN}══════════════════════════════════════════════════════════════════════════════{Colors.RESET}
{Colors.WHITE}                 Version 1.0.0 {Colors.CYAN}| {Colors.PURPLE}Developed by ZEXXF{Colors.RESET}
{Colors.CYAN}══════════════════════════════════════════════════════════════════════════════{Colors.RESET}
"""
    print(banner)
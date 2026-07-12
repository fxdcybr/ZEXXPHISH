"""
===========================================================
ZEXXPHISH
Advanced Phishing Analyzer

File: menu.py

Description:
Displays the main menu and handles user selection.
===========================================================
"""

from modules.colors import Colors


def display_menu():

    print(f"{Colors.CYAN}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.WHITE}{Colors.BRIGHT}                 MAIN MENU{Colors.RESET}")
    print(f"{Colors.CYAN}{'=' * 70}{Colors.RESET}")

    print()

    print(f"{Colors.CYAN}[1]{Colors.WHITE} Analyze URL")
    print(f"{Colors.CYAN}[2]{Colors.WHITE} Analyze Email Header")
    print(f"{Colors.CYAN}[3]{Colors.WHITE} View Scan History")
    print(f"{Colors.CYAN}[4]{Colors.WHITE} Generate Report")
    print(f"{Colors.CYAN}[5]{Colors.WHITE} Settings")
    print(f"{Colors.CYAN}[0]{Colors.RED} Exit")

    print()

    print(f"{Colors.CYAN}{'=' * 70}{Colors.RESET}")

    choice = input(
        f"{Colors.PURPLE}ZEXXPHISH > {Colors.WHITE}"
    )

    return choice
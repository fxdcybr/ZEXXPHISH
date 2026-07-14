"""
===========================================================
ZEXXPHISH
Advanced Phishing Analyzer

File: history_manager.py

Description:
Handles saving and viewing scan history.
===========================================================
"""

import json
import os
from datetime import datetime
from modules.colors import Colors

HISTORY_FILE = "history/history.json"


def initialize_history():
    """
    Creates the history file if it doesn't exist.
    """

    os.makedirs("history", exist_ok=True)

    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)


def save_scan(result):
    """
    Saves a scan to history.
    """

    initialize_history()

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        history = json.load(file)

    history.append(
        {
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "url": result["url"],
            "domain": result["domain"],
            "risk_score": result["risk_score"],
            "threat_level": result["threat_level"],
            "findings": result["findings"],
            "recommendation": result["recommendation"]
        }
    )

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)


def load_history():
    """
    Returns all saved scans.
    """

    initialize_history()

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def display_history():
    """
    Displays saved scan history.
    """

    history = load_history()

    print("\n" + "=" * 70)
    print(f"{Colors.CYAN}SCAN HISTORY{Colors.RESET}")
    print("=" * 70)

    if not history:
        print(f"{Colors.YELLOW}No scan history found.{Colors.RESET}")
        return

    for index, scan in enumerate(history, start=1):

        print(f"\n{Colors.PURPLE}Scan #{index}{Colors.RESET}")

        print(f"Time         : {scan['timestamp']}")
        print(f"URL          : {scan['url']}")
        print(f"Domain       : {scan['domain']}")
        print(f"Risk Score   : {scan['risk_score']}/100")
        print(f"Threat Level : {scan['threat_level']}")

        print("-" * 70)
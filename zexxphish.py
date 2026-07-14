from modules.banner import display_banner
from modules.utils import loading_screen, clear_screen
from modules.menu import display_menu
from modules.url_analyzer import analyze_url, display_url_report
from modules.history_manager import (
    save_scan,
    display_history,
    load_history
)
from modules.report_generator import generate_pdf_report

first_launch = True

while True:

    clear_screen()

    display_banner()

    if first_launch:
        loading_screen()
        first_launch = False
    else:
        print("\033[38;2;57;255;20m[✓] Ready.\033[0m\n")

    choice = display_menu()

    if choice == "1":

        print("\nEnter the URL to analyze:\n")

        url = input("URL > ")

        result = analyze_url(url)

        display_url_report(result)

        if result["valid"]:
            save_scan(result)

        input("\nPress Enter to return to the menu...")

    elif choice == "2":

        print("\n" + "=" * 70)
        print("📧 Email Header Analyzer")
        print("=" * 70)

        print("\nComing Soon 👾\n")

        print("Planned features:")
        print(" • Gmail 'Show Original' analysis")
        print(" • .eml file analysis")
        print(" • SPF validation")
        print(" • DKIM validation")
        print(" • DMARC validation")
        print(" • Sender spoofing detection")
        print(" • Reply-To mismatch detection")
        print(" • Email phishing risk scoring")

        input("\nPress Enter to continue...")

    elif choice == "3":

        display_history()

        input("\nPress Enter to continue...")

    elif choice == "4":

        history = load_history()

        if not history:

            print("\nNo scan history found.")

        else:

            latest = history[-1]

            report_path = generate_pdf_report(
                {
                    "url": latest["url"],
                    "domain": latest["domain"],
                    "https": latest["url"].startswith("https"),
                    "risk_score": latest["risk_score"],
                    "threat_level": latest["threat_level"],
                    "findings": latest["findings"],
                    "recommendation": latest["recommendation"]
                }
            )

            print("\nPDF generated successfully! ✅")
            print(f"\nSaved to: {report_path}")

        input("\nPress Enter to continue...")

    elif choice == "5":

        print("\nSettings")
        print("=" * 70)
        print("\nComing Soon 👾")

        input("\nPress Enter to continue...")

    elif choice == "0":

        print("\n" + "═" * 70)
        print("\nThank you for using ZEXXPHISH.\n")
        print("Stay vigilant. Think before you click 👾\n")
        print("═" * 70)

        break

    else:

        print("\nInvalid option.")

        input("\nPress Enter to continue...")
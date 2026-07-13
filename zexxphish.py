from modules.banner import display_banner
from modules.utils import loading_screen, clear_screen
from modules.menu import display_menu
from modules.url_analyzer import analyze_url, display_url_report 


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

        input("\nPress Enter to return to the menu...")

    elif choice == "2":
        print("\nEmail Header Analyzer coming soon...")
        input("\nPress Enter to continue...")

    elif choice == "3":
        print("\nHistory Viewer coming soon...")
        input("\nPress Enter to continue...")

    elif choice == "4":
        print("\nPDF Report Generator coming soon...")
        input("\nPress Enter to continue...")

    elif choice == "5":
        print("\nSettings coming soon...")
        input("\nPress Enter to continue...")

    elif choice == "0":
        print("\nThank you for using ZEXXPHISH.")
        break

    else:
        print("\nInvalid option.")
        input("\nPress Enter to continue...")   
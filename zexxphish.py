from modules.banner import display_banner
from modules.utils import loading_screen
from modules.menu import display_menu

display_banner()
loading_screen()

while True:

    choice = display_menu()

    if choice == "1":
        print("\nURL Analyzer coming soon...\n")

    elif choice == "2":
        print("\nEmail Header Analyzer coming soon...\n")

    elif choice == "3":
        print("\nHistory Viewer coming soon...\n")

    elif choice == "4":
        print("\nPDF Report Generator coming soon...\n")

    elif choice == "5":
        print("\nSettings coming soon...\n")

    elif choice == "0":
        print("\nThank you for using ZEXXPHISH.\n")
        break

    else:
        print("\nInvalid option.\n")
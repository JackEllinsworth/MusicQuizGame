from handlers.misc.menu import Menu
from handlers.db.db_models import Account
from handlers.db.db_manager import Database
from interface import auth_menu
from interface.options import score_menu, admin_menu

AUTH_OPTIONS = ["Login", "Create Account"]
MENU_OPTIONS = ["Play game", "Configuration", "View Scores", "Log-out"]


def activate(database: Database, account: Account):
    options = MENU_OPTIONS.copy()

    # Detects account permission for additional menu access
    if account.retrieve("permission") == "Administrator":
        options.append("Admin Panel")

    # Displays options and retrieves input
    menu = Menu("MAIN MENU", [
        {
            "description": "Please select an option below",
            "options": options,
            "response_type": int,
            "back_menu": False
        }
    ])

    success, responses = menu.get_responses()
    selected_option = responses[0]

    if selected_option == 1:
        print("playing game...")
    elif selected_option == 2:
        print("configuration...")
    elif selected_option == 3:
        score_menu.activate(database, account)
    elif selected_option == 4:
        print("[SUCCESS] Logging out...")
        return auth_menu.activate(database)
    elif selected_option == 5:
        admin_menu.activate(database, account)

    # Restarts menu for additional selection.
    return activate(database, account)

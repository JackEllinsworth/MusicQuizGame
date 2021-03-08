from handlers.misc.menu import Menu
from handlers.db.db_manager import Database
from handlers.queries import account_queries
from interface import menu_init

AUTH_OPTIONS = ["Login", "Create Account"]


def login(database: Database, username, password):
    # Retrieves accounts matching name
    accounts = account_queries.get_account_by_name(database, username)

    # Displays weather there was an account found or not
    if len(accounts) >= 1:
        # Checks which account matches the password with the same username, and logs into main menu.
        for i in range(len(accounts)):
            if accounts[i].retrieve("password") == password:
                print("[SUCCESS] Welcome, " + accounts[i].retrieve("username") + " (ID: " + str(
                    accounts[i].retrieve("userId")) + ")")
                return True, accounts[i]

    print("[ERR] Incorrect username/password, restarting;")
    return False, None


def activate(database: Database):
    menu = Menu("AUTHORIZATION: STEP 1", [
        {
            "description": "Please respond with your choice below.",
            "options": AUTH_OPTIONS,
            "response_type": int,
            "back_menu": False
        }
    ])

    success, selected_option = menu.get_responses()
    selected_option = selected_option[0]

    # Response 1: Login to previous account
    if selected_option == 1:
        menu = Menu("AUTHORIZATION", [
            {
                "description": "Please respond with your account name (reply with 'menu' to cancel)",
                "options": None,
                "response_type": str,
                "back_menu": True
            },
            {
                "description": "Please respond with the password for your account (reply with 'menu' to cancel)",
                "options": None,
                "response_type": str,
                "back_menu": True
            }
        ])

        success, responses = menu.get_responses()
        if not success: return activate(database)

        # Attempts to login to account, and authenticate
        login_success, account = login(database, responses[0], responses[1])

        if not login_success:
            return activate(database)
        else:
            return menu_init.activate(database, account)

    # Response 2: Create account
    elif selected_option == 2:
        # Checks for admin accounts, if there is non the next new account will be admin
        admins_check = account_queries.check_for_admins(database)
        permission = "Normal"

        if not admins_check:
            permission = "Administrator"

        menu = Menu("AUTHORIZATION", [
            {
                "description": "Please respond with your new account name (reply with 'menu' to cancel)",
                "options": None,
                "response_type": str,
                "back_menu": True
            },
            {
                "description": "Please respond with your new account password (reply with 'menu' to cancel)",
                "options": None,
                "response_type": str,
                "back_menu": True
            }
        ])

        success, responses = menu.get_responses()
        if not success: return activate(database)

        # Attempts to create new account (any return false would probably mean that the account
        # exists already with the same user & password.
        # This system supports multiple accounts with the same username, as long as they don't have the same password.
        success = account_queries.create_new_account(database, responses[0], responses[1], permission)

        # Displays type of account created, and success/fail
        if success:
            if not admins_check:
                print("[SUCCESS] Successfully created new administrator account (no current admins - overridden)")
            else:
                print("[SUCCESS] Successfully created new account")

            # Logs into account after creation, and displays menu
            login_success, account = login(database, responses[0], responses[1])

            if login_success:
                return menu_init.activate(database, account)
        else:
            print("[ERR] An error occurred while creating your account")

        return activate(database)

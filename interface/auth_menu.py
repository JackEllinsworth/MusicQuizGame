from handlers.misc import menu
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
    # Creates default main menu
    menu.create_menu("AUTHORIZATION: STEP 1", "Please respond with your choice below.", AUTH_OPTIONS, False, int)
    response = menu.get_menu_response(int, [1, len(AUTH_OPTIONS)], False)

    # Response 1: Login to previous account
    if response == 1:
        # Creates new response menu for username authentication
        menu.send_title_display("AUTHORIZATION: STEP 2",
                                "Please respond with your account name, or reply with 'menu' to go back.\n")
        username = menu.get_menu_response(str, None, True)
        if username == "Menu": return activate(database)

        # Creates new response menu for the password authentication.
        menu.send_title_display("AUTHORIZATION: STEP 3",
                                "Please respond with the password for your account, or reply with 'menu' to go back.\n")
        password = menu.get_menu_response(str, None, True)
        if password == "Menu": return activate(database)

        # Attempts to login to account, and authenticate
        login_success, account = login(database, username, password)

        if not login_success:
            return activate(database)
        else:
            return menu_init.activate(database, account)

    # Response 2: Create account
    elif response == 2:
        # Checks for admin accounts, if there is non the next new account will be admin
        admins_check = account_queries.check_for_admins(database)
        permission = "Normal"

        if not admins_check:
            permission = "Administrator"

        # Sends separator message and retrieves user input.
        menu.send_title_display("AUTHORIZATION: STEP 2",
                                "Please respond with your new account name, or reply with 'menu' to go back.\n")
        username = menu.get_menu_response(str, None, True)
        if username == "Menu": return activate(database)

        # Retrieves account password.
        menu.send_title_display("AUTHORIZATION: STEP 3",
                                "Please respond with your new account password, or reply with 'menu' to go back.\n")
        password = menu.get_menu_response(str, None, True)
        if password == "Menu": return activate(database)

        # Attempts to create new account (any return false would probably mean that the account
        # exists already with the same user & password.
        # This system supports multiple accounts with the same username, as long as they don't have the same password.
        success = account_queries.create_new_account(database, username, password, permission)

        # Displays type of account created, and success/fail
        if success:
            if not admins_check:
                print("[SUCCESS] Successfully created new administrator account (no current admins - overridden)")
            else:
                print("[SUCCESS] Successfully created new account")

            # Logs into account after creation, and displays menu
            login_success, account = login(database, username, password)

            if login_success:
                return menu_init.activate(database, account)
        else:
            print("[ERR] An error occurred while creating your account")

        return activate(database)

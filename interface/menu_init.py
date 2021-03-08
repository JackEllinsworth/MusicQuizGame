from handlers.misc import menu
from handlers.db.db_models import Account
from handlers.db.db_manager import Database
from handlers.queries import account_queries
from interface import admin_menu

AUTH_OPTIONS = ["Login", "Create Account"]
MENU_OPTIONS = ["Play game", "Configuration", "Log-out"]


def auth_menu(database: Database):
    # Creates default main menu
    menu.create_menu("AUTHORIZATION: STEP 1", "Please respond with your choice below.", AUTH_OPTIONS, False, int)
    response = menu.get_menu_response(int, [1, len(AUTH_OPTIONS)], False)

    # Response 1: Login to previous account
    if response == 1:
        menu.send_title_display("AUTHORIZATION: STEP 2",
                                "Please respond with your account name, or reply with 'menu' to go back.\n")
        response = menu.get_menu_response(str, None, True)
        if response == "Menu": return auth_menu(database)

        # Retrieves accounts with that username
        accounts = account_queries.get_account_by_name(database, response)

        # Displays weather there was an account found or not
        if len(accounts) <= 0:
            print("[ERR] No account with that username exists! - restarting")
            return auth_menu(database)
        else:
            # Creates new response menu for the password authentication.
            menu.send_title_display("AUTHORIZATION: STEP 3",
                                    "Please respond with the password for your account, or reply with 'menu' to go back.\n")
            response = menu.get_menu_response(str, None, True)
            if response == "Menu": return auth_menu(database)

            # Checks which account matches the password with the same username, and logs into main menu.
            for i in range(len(accounts)):
                if accounts[i].retrieve("password") == response:
                    print("[SUCCESS] Welcome, " + accounts[i].retrieve("username") + " (ID: " + str(accounts[i].retrieve("userId")) + ")")
                    return main_menu(database, accounts[i])

            print("[ERR] Incorrect password! - restarting")
            return auth_menu(database)

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
        if username == "Menu": return auth_menu(database)

        # Retrieves account password.
        menu.send_title_display("AUTHORIZATION: STEP 3",
                                "Please respond with your new account password, or reply with 'menu' to go back.\n")
        password = menu.get_menu_response(str, None, True)
        if password == "Menu": return auth_menu(database)

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
        else:
            print("[ERR] An error occurred while creating your account")

        return auth_menu(database)


def main_menu(database: Database, account: Account):
    options = MENU_OPTIONS.copy()

    # Detects account permission for additional menu access
    if account.retrieve("permission") == "Administrator":
        options.append("Admin Panel")

    # Displays options and retrieves input
    menu.create_menu("MAIN MENU", "Please select an option below", options, False, int)
    selected_option = menu.get_menu_response(int, [1, len(options)], False)

    if selected_option == 1:
        print("playing game...")
    elif selected_option == 2:
        print("configuration...")
    elif selected_option == 3:
        print("[SUCCESS] Logging out...")
        return auth_menu(database)
    elif selected_option == 4:
        admin_menu.activate(database, account)

    # Restarts menu for additional selection.
    return main_menu(database, account)

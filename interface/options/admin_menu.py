from handlers.db.db_models import Account
from handlers.db.db_manager import Database
from handlers.queries import song_queries, account_queries
from handlers.misc.menu import Menu, formatting

ADMIN_OPTIONS = ["Add Song", "Remove Song", "Update Song", "Display Songs", "Give User Admin"]
INNER_SONG_OPTIONS = ["Name", "Artist"]


def activate(database: Database, account: Account):
    # Double checks user's permission.
    if not account.retrieve("permission") == "Administrator": return
    menu = Menu("ADMIN PANEL", [
        {
            "description": "Please select an option below (reply with 'menu' to cancel)",
            "options": ADMIN_OPTIONS,
            "response_type": int,
            "back_menu": True
        }
    ])

    success, responses = menu.get_responses()
    if not success: return

    selected_option = responses[0]

    if selected_option == 1:
        menu = Menu("ADMIN PANEL: Add Song", [
            {
                "description": "Please respond with your new song name (reply with 'menu' to cancel)",
                "options": None,
                "response_type": str,
                "back_menu": True
            },
            {
                "description": "Please respond with your new songs artist name(s) (reply with 'menu' to cancel)",
                "options": None,
                "response_type": str,
                "back_menu": True
            }
        ])

        success, responses = menu.get_responses()
        if not success: return

        # Attempts to create new song, any error would probably result in the song existing already
        success = song_queries.create_new_song(database, responses[0], responses[1])

        # Displays status
        if success:
            return print("[SUCCESS] Created song: " + responses[0] + " successfully.")
        else:
            return print("[ERR] An error occurred whilst creating the song.")

    elif selected_option == 2:
        menu = Menu("ADMIN PANEL: Remove Song", [
            {
                "description": "Please respond with the song name to remove (reply with 'menu' to cancel)",
                "options": None,
                "response_type": str,
                "back_menu": True
            }
        ])

        success, responses = menu.get_responses()
        if not success: return

        # Attempts to remove the song by that name
        success = song_queries.remove_song_by_name(database, responses[0])

        # Displays success or error on the removal of the song.
        if success:
            return print("[SUCCESS] Removed song: " + responses[0] + " successfully.")
        else:
            return print("[ERR] An error occurred whilst removing the song.")

    elif selected_option == 3:
        menu = Menu("ADMIN PANEL: Update Song", [
            {
                "description": "Please respond with the song name to update (reply with 'menu' to cancel)",
                "options": None,
                "response_type": str,
                "back_menu": True
            },
            {
                "description": "Please respond with what you want to change (reply with 'menu' to cancel)",
                "options": INNER_SONG_OPTIONS,
                "response_type": str,
                "back_menu": True
            },
            {
                "description": "Please respond with the song value to update (reply with 'menu' to cancel)",
                "options": None,
                "response_type": str,
                "back_menu": True
            }
        ])

        success, responses = menu.get_responses()
        if not success: return

        # Retrieves song by name, and returns if invalid
        song = song_queries.get_song_by_name(database, responses[0])
        if not song: return print("[ERR] An error occurred whilst finding the song.")

        # If the option is name, it checks to see if the song with that name already exists, if so it returns an error.
        if responses[1].lower() == "name":
            exists_already = song_queries.get_song_by_name(database, responses[2])
            if exists_already: return print("[ERR] A song with that name exists already.")

        # Updates song with lowered option (for the model key), and updates with new value
        song.update(responses[1].lower(), responses[2])
        # Saves song and overwrites all values
        success = song_queries.overwrite_existing_song(database, song)

        # Outputs success or error of update
        if success:
            return print("[SUCCESS] Updated song: " + responses[0] + " successfully.")
        else:
            return print("[ERR] An error occurred whilst updating the song.")

    elif selected_option == 4:
        # Displays formatted songs to user
        songs = song_queries.get_formatted_songs(database)
        formatting.send_separator_message("ADMIN PANEL: Display Songs")
        print("Below are all the current songs stored on the database.\n")

        for i in range(len(songs)):
            print(songs[i])
        print()

        return
    elif selected_option == 5:
        success_update = False

        menu = Menu("ADMIN PANEL: Give User Admin", [
            {
                "description": "Please respond with username of the person to give administrator privileges"
                               " (reply with 'menu' to cancel)",
                "options": None,
                "response_type": str,
                "back_menu": True
            }
        ])

        success, responses = menu.get_responses()
        if not success: return

        accounts = account_queries.get_account_by_name(database, responses[0])

        if not accounts: return print("[ERR] No accounts have been found matching that name")

        if len(accounts) > 1:
            accountIds = []

            for i in range(len(accounts)):
                accountIds.append(str(accounts[i].retrieve("userId")))

            menu = Menu("ADMIN PANEL: Give User Admin > Selection", [
                {
                    "description": "Please respond with what userId you want to give administrator privileges",
                    "options": accountIds,
                    "response_type": int,
                    "back_menu": True
                }
            ])

            success_selec, response_selec = menu.get_responses()
            if not success_selec: return

            account = account_queries.get_account_by_id(database, accountIds[response_selec[0]-1])
            if account:
                account.update("permission", "Administrator")
                success_update = account_queries.overwrite_existing_account(database, account)

        else:
            account = accounts[0]
            account.update("permission", "Administrator")
            success_update = account_queries.overwrite_existing_account(database, account)

        if success_update:
            return print("[SUCCESS] Updated account matching userId " + str(account.retrieve("userId")) +
                         " permission to Administrator.")
        else:
            return print("[ERR] An error occurred whilst changing that users permission.")

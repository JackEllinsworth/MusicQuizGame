from handlers.db.db_models import Account
from handlers.db.db_manager import Database
from handlers.queries import song_queries
from handlers.misc import formatting, menu

ADMIN_OPTIONS = ["Add Song", "Remove Song", "Update Song", "Display Songs"]
INNER_SONG_OPTIONS = ["Name", "Artist"]


def activate(database: Database, account: Account):
    if not account.retrieve("permission") == "Administrator": return

    menu.create_menu("ADMIN PANEL", "Please select an option below", ADMIN_OPTIONS, True, int)
    selected_option = menu.get_menu_response(int, [1, len(ADMIN_OPTIONS)], True)

    if selected_option == "Menu": return

    # Add Song
    if selected_option == 1:
        menu.send_title_display("ADMIN PANEL: Add Song",
                                "Please respond with your new song name, or reply with 'menu' to go back.\n")
        song_name = menu.get_menu_response(str, None, True)
        if song_name == "Menu": return

        menu.send_title_display("ADMIN PANEL: Add Song",
                                "Please respond with your new song's artist name(s), or reply with 'menu' to go back.\n")
        artist_name = menu.get_menu_response(str, None, True)
        if artist_name == "Menu": return

        success = song_queries.create_new_song(database, song_name, artist_name)

        if success:
            return print("[SUCCESS] Created song: " + song_name + " successfully.")
        else:
            return print("[ERR] An error occurred whilst creating the song.")

    elif selected_option == 2:
        menu.send_title_display("ADMIN PANEL: Remove Song",
                                "Please respond with the song name to remove, or reply with 'menu' to go back.\n")
        song_name = menu.get_menu_response(str, None, True)
        if song_name == "Menu": return

        success = song_queries.remove_song_by_name(database, song_name)

        if success:
            return print("[SUCCESS] Removed song: " + song_name + " successfully.")
        else:
            return print("[ERR] An error occurred whilst removing the song.")

    elif selected_option == 3:
        menu.send_title_display("ADMIN PANEL: Update Song",
                                "Please respond with the song name to update, or reply with 'menu' to go back.\n")
        song_name = menu.get_menu_response(str, None, True)
        if song_name == "Menu": return

        song = song_queries.get_song_by_name(database, song_name)
        if not song: return print("[ERR] An error occurred whilst finding the song.")

        menu.create_menu("ADMIN PANEL: Update Song",
                         "Please respond with what you want to change, or reply with 'menu' to go back.",
                         INNER_SONG_OPTIONS, True, str)

        option = menu.get_menu_response(str, INNER_SONG_OPTIONS, True)

        if option == "Menu": return

        menu.send_title_display("ADMIN PANEL: Update Song",
                                "Please respond with the song value to update, or reply with 'menu' to go back.\n")
        new_value = menu.get_menu_response(str, None, True)
        if new_value == "Menu": return

        if option == "name":
            exists_already = song_queries.get_song_by_name(database, new_value)
            if exists_already: return print("[ERR] A song with that name exists already.")

        song.update(option.lower(), new_value)
        success = song_queries.overwrite_existing_song(database, song)

        if success:
            return print("[SUCCESS] Updated song: " + song_name + " successfully.")
        else:
            return print("[ERR] An error occurred whilst updating the song.")

    elif selected_option == 4:
        songs = song_queries.get_formatted_songs(database)
        menu.send_title_display("ADMIN PANEL: Display Songs",
                                "Below are all the current songs stored on the database.\n")

        for i in range(len(songs)):
            print(songs[i])
        print()

        return











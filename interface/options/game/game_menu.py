from interface.options.game.game import Game
from handlers.misc.menu import Menu
from handlers.db.db_manager import Database
from handlers.db.db_models import Account, Points
from handlers.queries import points_queries, song_queries

SAVE_POINTS = True


def get_unique_song(songs, index):
    # Attempts to retrieve the index of the next song
    try:
        return songs[index], index + 1
    except:
        # If no index in songs found, either returns that no
        # songs are in the database, or that a re-order is required
        if len(songs) <= 0:
            return False, "NoSong"
        else:
            return False, "Restart"


def activate(database: Database, account: Account):
    user_points = 0
    play_again = True
    songs = song_queries.get_all_songs_randomized(database)
    next_song_index = 0

    while play_again:
        play_again = False

        # Re-order songs & ensure all songs are different until restart
        unique_song, new_index = None, None
        next_song_index += 1

        unique_song, new_index = get_unique_song(songs, next_song_index)

        if not unique_song:
            next_song_index = 0
            # No songs in database
            if new_index == "NoSong":
                return print("[ERR] No songs found on database!")
            elif new_index == "Restart":
                # Restarting index and re-ordering songs
                songs = song_queries.get_all_songs_randomized(database)
                unique_song, new_index = get_unique_song(songs, next_song_index)

        # Initiate game
        game = Game(unique_song)

        # Retrieves result from game session
        success, guessed_correctly = game.startup()

        # Increments points based on amount of guesses
        if guessed_correctly:
            if game.guesses == 1:
                user_points += 3
            elif game.guesses == 2:
                user_points += 1

        # If the user has no points, it ends the game
        if user_points <= 0:
            return print("[END] Game over - no points scored")

        if not success: return

        def end_game_display_save():
            if SAVE_POINTS:
                score_set = Points(account.retrieve("userId"), user_points)
                points_queries.create_score_set(database, score_set)
            print("[END] You scored a total of " + str(user_points) +
                  " point(s)! - Saved if enabled; Thanks for playing!")

        # User guessed correctly, so user can play again
        if guessed_correctly:
            menu = Menu("GAME MENU: Play again?", [
                {
                    "description": "Would you like to play again?",
                    "options": ["Yes", "No"],
                    "response_type": int,
                    "back_menu": False
                }
            ])

            # Retrieves response
            success, responses = menu.get_responses()
            response = responses[0]

            if response == 1:
                # Reactivates rounds
                play_again = True
                print("[END] Playing another round... (your score will be added altogether)")
            elif response == 2:
                # Ends the game and saves final score.
                end_game_display_save()
                return
        else:
            # Ends game automatically due to failure to guess song after 2 guesses
            print("[END] Ending game - 2 failed guesses")
            end_game_display_save()
            return

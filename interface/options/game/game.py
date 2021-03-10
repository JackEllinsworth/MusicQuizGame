from handlers.db.db_models import Song
from handlers.misc.menu import Menu


FREE_SPACE_CHAR = "_"
MAX_GUESSES = 2


def retrieve_formatted_desc(song, guesses):
    # Split song name into words
    song_name_split = song.retrieve("name").split(" ")
    song_name_formatted = ""

    # Loops through the words in the song name
    for i in range(len(song_name_split)):
        # Retrieves first char of the word
        word_char = song_name_split[i][0].upper()
        # Retrieves the length of the word
        word_len = len(song_name_split[i])
        # Concatenates CHAR_____ (_ = additional chars)
        song_name_formatted += (word_char + (FREE_SPACE_CHAR * (word_len - 1)) + " ")

    # Concatenates description together
    description_formatted = "Please respond with your guess of the song name\nArtist Name: " + \
                            song.retrieve("artist") + "\nSong Name: (Guess the full name!): " \
                            + song_name_formatted + "\nGuesses Left: " + str(MAX_GUESSES - guesses)

    return description_formatted


class Game:

    def __init__(self, song: Song):
        self.song = song
        self.guesses = 0
        self.guessed = False

    def startup(self):
        # Keeps asking for guess until the guesses amount has not been
        # reached and user hasn't guessed correctly
        while self.guesses < MAX_GUESSES and not self.guessed:
            success, response = self.check_guess()
            if not success: return False, False

        if self.guessed:
            return True, True
        else:
            return True, False

    def check_guess(self):

        menu = Menu("GAME MENU: Guess the song name (reply with 'menu' to cancel)", [
            {
                "description": retrieve_formatted_desc(self.song, self.guesses),
                "options": None,
                "response_type": str,
                "back_menu": True
            }
        ])

        # Retrieves response
        success, responses = menu.get_responses()
        if not success: return False, None

        # Increments guesses and single response is ready
        response = responses[0]
        self.guesses += 1

        # Compare user input to see if the song name was correct.
        if response.lower() == self.song.retrieve("name").lower():
            print("[CORRECT] Well done, you got it right with " + str(self.guesses) + " guess/es!")
            self.guessed = True
            return True, True
        else:
            print("[WRONG] Oh no! You got it wrong - you have " + str(MAX_GUESSES-self.guesses) + " guess/es left.")
            return True, False



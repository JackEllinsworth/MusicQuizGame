import sqlite3


# Setup functions for database tables
def setup_songs(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS SONGS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME TEXT NOT NULL,
        ARTIST TEXT NOT NULL
    );""")

    cursor.close()


def setup_points(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS POINTS (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    USERID INTEGER NOT NULL,
    POINTS INTEGER NOT NULL,
    TIME TEXT NOT NULL
    );""")

    cursor.close()


def setup_accounts(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS ACCOUNTS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USERNAME TEXT NOT NULL,
        PASSWORD TEXT NOT NULL,
        PERMISSION TEXT NOT NULL
    );""")

    cursor.close()


class Database:

    def __init__(self):
        # Initializes connection to database
        self.connection = sqlite3.connect("music_game.db")

    def load(self):
        # Sets up default tables
        setup_songs(self.connection.cursor())
        setup_accounts(self.connection.cursor())
        setup_points(self.connection.cursor())

    def save(self):
        # Commits changes to database
        self.connection.commit()




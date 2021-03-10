from handlers.db.db_manager import Database
from handlers.db.db_models import Song


def get_all_songs_randomized(database: Database):
    cursor = database.connection.cursor()
    cursor.execute("SELECT * FROM SONGS ORDER BY RANDOM()")
    results = cursor.fetchall()
    songs = []

    for row in results:
        song = Song(row[0], row[1], row[2])
        songs.append(song)

    cursor.close()

    return songs


def get_formatted_songs(database: Database):
    # Formats all songs in an array, ready for display
    cursor = database.connection.cursor()
    cursor.execute("SELECT * FROM SONGS")

    formatted_list = []

    for row in cursor:
        formatted_list.append("Name: " + row[1] + " | Artist: " + row[2] + " - (ID: " + str(row[0]) + ")")

    cursor.close()

    return formatted_list


def get_song_by_name(database: Database, song_name: str):
    cursor = database.connection.cursor()
    cursor.execute("SELECT * FROM SONGS WHERE NAME = ?", (song_name,))
    song = cursor.fetchone()

    # Returns first song found matching that name
    if not song:
        return False
    else:
        song = Song(song[0], song[1], song[2])

    cursor.close()
    return song


def overwrite_existing_song(database: Database, song: Song):
    cursor = database.connection.cursor()

    try:
        # Updates songs and sets to updated values via song object
        cursor.execute("""UPDATE SONGS SET name = ?, artist = ? WHERE ID = ?""",
                       (song.retrieve("name"), song.retrieve("artist"), song.retrieve("songId")))

        cursor.close()
        database.save()
        return True
    except:
        return False


def create_new_song(database: Database, name: str, artist: str):
    cursor = database.connection.cursor()

    try:
        # Retrieves song by name, checking it it exists already
        song = get_song_by_name(database, name)

        # If the song exists, it returns false (error)
        if song:
            return False
        else:
            # Executes query and creates song
            cursor.execute("""INSERT INTO SONGS (NAME, ARTIST) \
                            VALUES (?,?)""", (name, artist))

        # Saves data and ceases current session
        cursor.close()
        database.save()
        return True
    except:
        return False


def remove_song_by_name(database: Database, song_name: str):
    cursor = database.connection.cursor()

    try:
        song = get_song_by_name(database, song_name)
        if not song: return False

        # Removes song from database via ID, from song object
        cursor.execute("""DELETE FROM SONGS WHERE ID = ?""", (song.retrieve("songId"),))
        cursor.close()
        database.save()
        return True
    except:
        return False

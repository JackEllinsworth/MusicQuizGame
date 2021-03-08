import datetime


# Song interface
class Song:

    def __init__(self, song_id: int, name: str, artist: str):
        self.data = {
            "songId": song_id,
            "name": name,
            "artist": artist
        }

    def update(self, conf_type: str, conf_value):
        self.data[conf_type] = conf_value

    def retrieve(self, conf_type):
        return self.data[conf_type]


# Points interface
class Points:

    def __init__(self, user_id: str, points: int):
        self.data = {
            "userId": user_id,
            "points": points,
            "time": (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        }

    def update(self, conf_type: str, conf_value):
        self.data[conf_type] = conf_value

    def retrieve(self, conf_type):
        return self.data[conf_type]


# Account interface
class Account:

    def __init__(self, user_id: int, username: str, password: str, permission: str):
        self.data = {
            "userId": user_id,
            "username": username,
            "password": password,
            "permission": permission
        }

    def update(self, conf_type, conf_value):
        self.data[conf_type] = conf_value

    def retrieve(self, conf_type):
        return self.data[conf_type]

import datetime


# Song interface
class Song:

    def __init__(self, song_id, name, artist):
        self.data = {
            "songId": song_id,
            "name": name,
            "artist": artist
        }

    def update(self, conf_type, conf_value):
        self.data[conf_type] = conf_value

    def retrieve(self, conf_type):
        return self.data[conf_type]


# Points interface
class Points:

    def __init__(self, user_id, points):
        self.data = {
            "userId": user_id,
            "points": points,
            "time": (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        }

    def update(self, conf_type, conf_value):
        self.data[conf_type] = conf_value

    def retrieve(self, conf_type):
        return self.data[conf_type]


# Account interface
class Account:

    def __init__(self, user_id, username, password, permission):
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

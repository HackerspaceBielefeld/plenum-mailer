import requests
from urllib.parse import quote


class Matrix(object):
    __slots__ = ["access_token", "homeserver", "room_id", "events", "error"]

    def __init__(self, username: str, password: str, homeserver: str, room_id: str):
        self.homeserver = homeserver
        self.room_id = quote(room_id)

        body = requests.post(
            url=f"https://{self.homeserver}/_matrix/client/r0/login",
            json={
                "user": username,
                "password": password,
                "type": "m.login.password"
            }
        ).json()

        self.access_token = body.get("access_token")
        self.error = body.get("error")

        if not self.access_token:
            print(f"[ERROR]: {self.error}\n^--{body}")

    def send(self, message: str, html_message: str) -> None:
        requests.post(
            url=f"https://{self.homeserver}/_matrix/client/r0/rooms/{self.room_id}/send/m.room.message?access_token={self.access_token}",
            json={
                "body": message,
                "msgtype": "m.text",
                "format": "org.matrix.custom.html",
                "formatted_body": html_message
            }
        )
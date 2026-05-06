from PyQt5.QtCore import *

from logic.encryptor import Encryptor


class Authenticator(QObject):

    def __init__(self, encryptor: Encryptor):
        super().__init__()
        self.loged_user: str = None
        self.encryptor = encryptor

    def login(self, username: str, password: str):
        user_exists = self.encryptor.check_user(username)

        if not user_exists:
            return

        user = self.encryptor.read_from_txt(username)

        if user.username != username or user.password != password:
            return

        self.loged_user = username

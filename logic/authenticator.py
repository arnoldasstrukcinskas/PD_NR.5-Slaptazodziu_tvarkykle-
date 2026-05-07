from PyQt5.QtCore import *

from logic.encryptor import Encryptor, User


class Authenticator(QObject):

    def __init__(self, encryptor: Encryptor):
        super().__init__()
        self.loged_user: User = None
        self.encryptor = encryptor

    def login(self, username: str, password: str):
        user = self.check_user(username)

        if not user:
            return

        if self.verify_user(user, username, password):
            programs = self.encryptor.read_programs_from_txt(username)
            self.loged_user = User(
                username=username, password=password, programs=programs
            )

    def logout(self):
        self.loged_user = None

    def check_user(self, username: str) -> User:
        users = self.encryptor.read_users_from_txt()

        for user_data in users:
            username_salt, username_hash = user_data.username.split("$")

            new_username_salt, new_username_hash = self.encryptor.hash(
                username, username_salt
            )

            if username_hash == new_username_hash:
                return user_data

        return None

    def verify_user(self, user: User, username: str, password: str) -> bool:
        username_salt, username_hash = user.username.split("$")
        password_salt, password_hash = user.password.split("$")

        new_username_salt, new_username_hash = self.encryptor.hash(
            username, username_salt
        )
        new_password_salt, new_password_hash = self.encryptor.hash(
            password, password_salt
        )

        if username_hash == new_username_hash and password_hash == new_password_hash:
            return True

        return False

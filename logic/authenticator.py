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

        if not self.verify_user(user, username, password):
            return False

        self.encryptor.user_key = password
        programs = self.encryptor.aes_decipher_programs(username)

        self.loged_user = User(username=username, password=password, programs=programs)

        return True

    def logout(self):
        username = self.loged_user.username
        self.encryptor.aes_cipher_programs(username)
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

    def create_random_password(self) -> str:
        generated_password = self.encryptor.generate_password()
        return generated_password

    def load_programs(self):
        programs = self.encryptor.read_programs_from_txt(self.loged_user.username)

        self.loged_user.programs = programs

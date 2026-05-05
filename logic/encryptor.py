import os
from dataclasses import dataclass

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from PyQt5.QtCore import *

BITS128 = 128
BITS192 = 192
BITS256 = 256


@dataclass
class User:
    username: str
    name: str
    password: str
    url: str
    nots: str


class Encryptor(QObject):
    def __init__(self):
        super().__init__()
        self.key_length = BITS256
        self.user_key: str = None
        self.iv: bytes = None
        self.generated_key: str = None

        self.passwords: list = []
        self.save_dir: str = "data"

        print("encryptor started")

    def aes_cipher(self, user: User):
        bytes = self.key_length / 8
        key = PBKDF2(self.user_key, "fixedSalt", dkLen=bytes, count=10000)
        iv = os.urandom(16)
        self.iv = iv
        self.generated_key = key

        cipher = AES.new(key, AES.MODE_CFB)
        cyphered_text = cipher.encrypt(user.password.encode("utf-8"))

        return cyphered_text

    def write_to_txt(self):
        file_path = os.path.join(self.save_dir, "passwords.txt")

        with open(file_path, "w", encoding="utf-8") as file:
            for password in self.passwords:
                file.write(f"{password}\n")

    def read_from_txt(self):
        self.passwords = []

        file_path = os.path.join(self.save_dir, "passwords.txt")

        with open(file_path, "r", encoding="utf-8") as file:
            for password in file:
                self.passwords.append(password)

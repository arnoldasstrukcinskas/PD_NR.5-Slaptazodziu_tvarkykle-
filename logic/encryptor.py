import json
import os
from dataclasses import asdict, dataclass

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from PyQt5.QtCore import *

BITS128 = 128
BITS192 = 192
BITS256 = 256


@dataclass
class Program:
    name: str
    password: str
    url: str
    notes: str


@dataclass
class User:
    username: str
    password: str
    programs: list[Program]


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

    def create_user(self, user: User):
        print(user)
        self.write_to_txt(user)

    def write_to_txt(self, user: User):
        file_path = os.path.join(self.save_dir, f"{user.username}.txt")

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(asdict(user), file, indent=4)

    def check_user(self, username: str) -> bool:
        file_path = os.path.join(self.save_dir, f"{username}.txt")

        if not os.path.exists(file_path):
            return False

        return True

    def read_from_txt(self, username: str):
        file_path = os.path.join(self.save_dir, f"{username}.txt")

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        programs: list[Program] = []

        for program_data in data["programs"]:
            program = Program(
                name=program_data["name"],
                password=program_data["password"],
                url=program_data["url"],
                notes=program_data["notes"],
            )
            programs.append(program)

        user = User(
            username=data["username"], password=data["password"], programs=programs
        )

        return user

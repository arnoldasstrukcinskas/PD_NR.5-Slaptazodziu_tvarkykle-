import base64
import hmac
import json
import os
from dataclasses import asdict, dataclass, field

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2, scrypt
from Crypto.Random import get_random_bytes
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
    programs: list[Program] = field(default_factory=list)


class Encryptor(QObject):
    def __init__(self):
        super().__init__()
        self.key_length = BITS256
        self.user_key: str = None
        self.iv: bytes = None
        self.generated_key: str = None

        self.passwords: list = []
        self.programs_save_dir: str = "data/programs"
        self.save_dir: str = "data"

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
        self.write_user_to_txt(user)
        self.add_program(user.username, user.programs[0])

    def write_user_to_txt(self, user_data: User):
        os.makedirs(self.save_dir, exist_ok=True)
        file_path = os.path.join(self.save_dir, "users.txt")

        username_salt_hash, username_hash = self.hash(user_data.username)
        password_salt_hash, password_hash = self.hash(user_data.password)

        user = User(
            username=self.format_uset_file_text(username_salt_hash, username_hash),
            password=self.format_uset_file_text(password_salt_hash, password_hash),
        )

        users = self.read_users_from_txt()
        users.append(user)

        # Converting users to dict for writing to txt

        users_dict = []

        for user_object in users:
            user_dict = {
                "username": user_object.username,
                "password": user_object.password,
            }
            users_dict.append(user_dict)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(users_dict, file, indent=4)

    def read_users_from_txt(self) -> list[User]:
        file_path = os.path.join(self.save_dir, "users.txt")
        users: list[User] = []

        if not os.path.exists(file_path):
            return users

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        for user_data in data:
            user = User(username=user_data["username"], password=user_data["password"])
            users.append(user)

        return users

    def add_program(self, useranme: str, program: Program):
        self.add_program_to_txt(useranme, program)

    def add_program_to_txt(self, username: str, program: Program):
        os.makedirs(self.programs_save_dir, exist_ok=True)
        file_path = os.path.join(self.programs_save_dir, f"{username}.txt")

        programs = self.read_programs_from_txt(username)

        if not programs:
            programs = []
        programs.append(program)

        programs_dict = [asdict(p) for p in programs]

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(programs_dict, file, indent=4)

    def read_programs_from_txt(self, username: str) -> list[Program]:
        file_path = os.path.join(self.programs_save_dir, f"{username}.txt")

        if not os.path.exists(file_path):
            return

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        programs: list[Program] = []

        for program_data in data:
            program = Program(
                name=program_data["name"],
                password=program_data["password"],
                url=program_data["url"],
                notes=program_data["notes"],
            )
            programs.append(program)

        return programs

    def hash(self, data: str, salt: str = None) -> str:
        if not salt:
            salt = get_random_bytes(16)
        else:
            salt = base64.b64decode(salt)

        key = scrypt(data, salt, key_len=32, N=2**14, r=8, p=1)

        salt_hash = base64.b64encode(salt).decode()
        hash = base64.b64encode(key).decode()
        return salt_hash, hash

    def format_uset_file_text(self, salt_hash, data_hash) -> str:
        return f"{salt_hash}${data_hash}"

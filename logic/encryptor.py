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
    iv: str | None = None


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

        self.programs_save_dir: str = "data/programs"
        self.save_dir: str = "data"

    def aes_cipher_programs(self, username: str):
        key_bytes = self.key_length // 8
        programs = self.read_programs_from_txt(username)

        if not programs:
            self.write_programs_to_txt(username, [])
            return

        key = PBKDF2(self.user_key, b"fixedSalt", dkLen=key_bytes, count=10000)

        ciphered_programs: list[Program] = []

        for program in programs:
            iv = self.iv_from_str(program.iv)

            cipher = AES.new(key, AES.MODE_CFB, iv=iv)

            cyphered_name = cipher.encrypt(program.name.encode("utf-8"))
            cyphered_password = cipher.encrypt(program.password.encode("utf-8"))
            cyphered_url = cipher.encrypt(program.url.encode("utf-8"))
            cyphered_notes = cipher.encrypt(program.notes.encode("utf-8"))

            ciphered_program = Program(
                name=base64.b64encode(cyphered_name).decode("utf-8"),
                password=base64.b64encode(cyphered_password).decode("utf-8"),
                url=base64.b64encode(cyphered_url).decode("utf-8"),
                notes=base64.b64encode(cyphered_notes).decode("utf-8"),
                iv=program.iv,
            )

            ciphered_programs.append(ciphered_program)

        self.write_programs_to_txt(username, ciphered_programs)

    def aes_decipher_programs(self, username: str):
        bytes = self.key_length // 8
        ciphered_programs = self.read_programs_from_txt(username)
        print("check")
        print(ciphered_programs)
        key = PBKDF2(self.user_key, "fixedSalt", dkLen=bytes, count=10000)
        deciphered_programs: list[Program] = []

        for ciphered_program in ciphered_programs:
            iv = self.iv_from_str(ciphered_program.iv)

            decipher = AES.new(key, AES.MODE_CFB, iv=iv)

            deciphered_name = decipher.decrypt(
                base64.b64decode(ciphered_program.name)
            ).decode("utf-8")

            deciphered_password = decipher.decrypt(
                base64.b64decode(ciphered_program.password)
            ).decode("utf-8")

            deciphered_url = decipher.decrypt(
                base64.b64decode(ciphered_program.url)
            ).decode("utf-8")

            deciphered_notes = decipher.decrypt(
                base64.b64decode(ciphered_program.notes)
            ).decode("utf-8")

            deciphered_program = Program(
                name=deciphered_name,
                password=deciphered_password,
                url=deciphered_url,
                notes=deciphered_notes,
                iv=ciphered_program.iv,
            )

            deciphered_programs.append(deciphered_program)

            self.write_programs_to_txt(username, deciphered_programs)

        return deciphered_programs

    def create_user(self, user: User):
        self.write_user_to_txt(user)

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

    def add_program_to_txt(self, username: str, program: Program, empty: bool = False):
        os.makedirs(self.programs_save_dir, exist_ok=True)
        file_path = os.path.join(self.programs_save_dir, f"{username}.txt")

        if empty:
            empty_list: list[Program] = []
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(empty_list, file, indent=4)
            return

        programs = self.read_programs_from_txt(username)

        iv = os.urandom(16)
        program.iv = self.iv_to_str(iv)
        programs.append(program)

        if not programs:
            programs = []

        programs_dict = []

        for program in programs:
            program_dict = {
                "name": program.name,
                "password": program.password,
                "url": program.url,
                "notes": program.notes,
                "iv": program.iv,
            }
            programs_dict.append(program_dict)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(programs_dict, file, indent=4)

    def write_programs_to_txt(self, username: str, programs: list[Program]):
        os.makedirs(self.programs_save_dir, exist_ok=True)
        file_path = os.path.join(self.programs_save_dir, f"{username}.txt")

        programs_dict = []

        for program in programs:
            programs_dict.append(
                {
                    "name": program.name,
                    "password": program.password,
                    "url": program.url,
                    "notes": program.notes,
                    "iv": program.iv,
                }
            )

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(programs_dict, file, indent=4)

    def remove_program_from_txt(self, username: str, program_name: str):
        programs = self.read_programs_from_txt(username)

        updated_programs = []

        for program in programs:
            if program.name != program_name:
                updated_programs.append(program)

        self.write_programs_to_txt(username, updated_programs)

    def read_programs_from_txt(self, username: str) -> list[Program]:
        file_path = os.path.join(self.programs_save_dir, f"{username}.txt")

        if not os.path.exists(file_path):
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        programs: list[Program] = []

        for program_data in data:
            program = Program(
                name=program_data["name"],
                password=program_data["password"],
                url=program_data["url"],
                notes=program_data["notes"],
                iv=program_data["iv"],
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

    def iv_to_str(self, iv: bytes) -> str:
        return base64.b64encode(iv).decode("utf-8")

    def iv_from_str(self, iv: str) -> bytes:
        return base64.b64decode(iv.encode("utf-8"))

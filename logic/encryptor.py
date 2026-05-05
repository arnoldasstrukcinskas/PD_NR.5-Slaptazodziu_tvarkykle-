from PyQt5.QtCore import *


class Encryptor(QObject):
    def __init__(self):
        super().__init__()
        print("encryptor started")

from PyQt5.QtCore import *


class Authenticator(QObject):

    def __init__(self):
        super().__init__()
        self.loged_user: str = None

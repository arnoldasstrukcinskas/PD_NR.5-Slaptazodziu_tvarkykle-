from typing import TYPE_CHECKING

from PyQt5.QtWidgets import *

from gui.form_ui import Ui_Form
from logic.authenticator import Authenticator
from logic.encryptor import Encryptor

if TYPE_CHECKING:
    from main.mainwindow import MainWindow

BITS128 = 128
BITS192 = 192
BITS256 = 256


class FormWidget(Ui_Form, QWidget):

    def __init__(
        self, parent: "MainWindow", encryptor: Encryptor, authenticator: Authenticator
    ):
        super().__init__(parent=parent)
        self.setMaximumSize(800, 800)
        self.setupUi(self)
        self._mainwindow = parent
        self.encryptor = encryptor
        self.authenticator = authenticator

        self.logoutPushButton.clicked.connect(self.logout)

    def logout(self):
        self.authenticator.logout()
        self._mainwindow.set_login_window()

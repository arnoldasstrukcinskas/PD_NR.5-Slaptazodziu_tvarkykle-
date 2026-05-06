from typing import TYPE_CHECKING

from PyQt5.QtWidgets import *

from gui.login.login_ui import Ui_Form
from logic.authenticator import Authenticator

if TYPE_CHECKING:
    from main.mainwindow import MainWindow


class LoginWidget(Ui_Form, QWidget):

    def __init__(self, parent: "MainWindow", authenticator: Authenticator):
        super().__init__(parent=parent)
        self.setMaximumSize(400, 400)
        self.setupUi(self)
        self.authenticator = authenticator
        print("login")

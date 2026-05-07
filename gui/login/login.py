from typing import TYPE_CHECKING

from PyQt5.QtWidgets import *

from gui.login.login_ui import Ui_Form
from logic.authenticator import Authenticator
from logic.encryptor import Encryptor

if TYPE_CHECKING:
    from main.mainwindow import MainWindow


class LoginWidget(Ui_Form, QWidget):

    def __init__(self, parent: "MainWindow", authenticator: Authenticator):
        super().__init__(parent=parent)
        self.setMaximumSize(400, 300)
        self.setupUi(self)
        self._mainWindow = parent
        self.authenticator = authenticator

        self.registrationPushButton.clicked.connect(
            self._mainWindow.set_register_window
        )
        self.loginPushButton.clicked.connect(self.login)

    def login(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()

        self.authenticator.login(username, password)

        if not self.authenticator.loged_user:
            QMessageBox.information(self, "Klaida", "Neteisingi prisijungimo duomenys")
            return

        self._mainWindow.set_main_window()
        self._mainWindow.load_form_widget()
        self.clear_ui()

    def clear_ui(self):
        self.usernameLineEdit.setText("")
        self.passwordLineEdit.setText("")

from typing import TYPE_CHECKING

from PyQt5.QtWidgets import *

from gui.register.register_ui import Ui_Form
from logic.encryptor import Encryptor, Program, User

if TYPE_CHECKING:
    from main.mainwindow import MainWindow


class RegisterWidget(Ui_Form, QWidget):

    def __init__(self, parent: "MainWindow", encryptor: Encryptor):
        super().__init__(parent=parent)
        self._mainwindow = parent
        self.encryptor = encryptor
        self.setMaximumSize(400, 400)
        self.setupUi(self)

        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.passwordRetypeLineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.backPushButton.clicked.connect(self._mainwindow.set_login_window)
        self.registerPushButton.clicked.connect(self.register)

    def register(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        repassword = self.passwordRetypeLineEdit.text()

        if not self.validate_fields():
            QMessageBox.information(self, "Klaida", "Ne visi laukai užpildyti")
            return

        if not password == repassword:
            QMessageBox.critical(self, "Klaida", "slaptažodžiai nesutampa")
            return

        user = User(username, password)

        self.encryptor.create_user(user)
        self._mainwindow.set_login_window()
        self.clear_fields()
        self.reset_ui()

    def clear_fields(self):
        # reset fields
        self.usernameLineEdit.setText("")
        self.passwordLineEdit.setText("")
        self.passwordRetypeLineEdit.setText("")

    def reset_ui(self):
        self.usernameLabel.setStyleSheet("")
        self.passwordLabel.setStyleSheet("")
        self.passwordRetypeLabel.setStyleSheet("")

    def validate_fields(self) -> bool:
        self.reset_ui()
        fields_correct = True

        if not self.usernameLineEdit.text():
            self.usernameLabel.setStyleSheet("color: red;")
            fields_correct = False

        if not self.passwordLineEdit.text():
            self.passwordLabel.setStyleSheet("color: red;")
            fields_correct = False

        if not self.passwordRetypeLineEdit.text():
            self.passwordRetypeLabel.setStyleSheet("color: red;")
            fields_correct = False

        return fields_correct

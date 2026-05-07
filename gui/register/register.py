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
        self.setMaximumSize(600, 600)
        self.setupUi(self)

        # Register widget buttons
        self.backPushButton.clicked.connect(self._mainwindow.set_login_window)

        self.registerPushButton.clicked.connect(self.register)

    def register(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        repassword = self.passwordRetypeLineEdit.text()
        programName = self.nameLineEdit.text()
        programPassword = self.programPasswordLineEdit.text()
        url = self.urlLineEdit.text()
        notes = self.notesPlainTextEdit.toPlainText()
        programs = []

        if not self.validate_fields():
            QMessageBox.information(self, "Klaida", "Ne visi laukai užpildyti")
            return

        if not password == repassword:
            QMessageBox.critical(self, "Klaida", "slaptažodžiai nesutampa")
            return

        user = User(username, password)
        program = Program(programName, programPassword, url, notes)

        user.programs.append(program)
        self.encryptor.create_user(user)
        self._mainwindow.set_login_window()
        self.clear_fields()
        self.reset_ui()

    def clear_fields(self):
        # reset fields
        self.usernameLineEdit.setText("")
        self.passwordLineEdit.setText("")
        self.passwordRetypeLineEdit.setText("")
        self.nameLineEdit.setText("")
        self.programPasswordLineEdit.setText("")
        self.urlLineEdit.setText("")
        self.notesPlainTextEdit.setPlainText("")

    def reset_ui(self):
        self.usernameLabel.setStyleSheet("")
        self.passwordLabel.setStyleSheet("")
        self.passwordRetypeLabel.setStyleSheet("")
        self.nameLabel.setStyleSheet("")
        self.programPasswordLabel.setStyleSheet("")
        self.urlLabel.setStyleSheet("")
        self.notesLabel.setStyleSheet("")

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

        if not self.nameLineEdit.text():
            self.nameLabel.setStyleSheet("color: red;")
            fields_correct = False

        if not self.programPasswordLineEdit.text():
            self.programPasswordLabel.setStyleSheet("color: red;")
            fields_correct = False

        if not self.urlLineEdit.text():
            self.urlLabel.setStyleSheet("color: red;")
            fields_correct = False

        if not self.notesPlainTextEdit.toPlainText():
            self.notesLabel.setStyleSheet("color: red;")
            fields_correct = False

        return fields_correct

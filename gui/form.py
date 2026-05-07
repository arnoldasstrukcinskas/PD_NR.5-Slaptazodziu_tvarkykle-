from typing import TYPE_CHECKING

from PyQt5.QtWidgets import *

from gui.form_ui import Ui_Form
from logic.authenticator import Authenticator
from logic.encryptor import Encryptor, Program

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
        self.newPgogramPushButton.clicked.connect(self.new_program)
        self.programsComboBox.currentTextChanged.connect(self.load_program)
        self.showPasswordCheckBox.clicked.connect(self.hide_password)
        self.findProgramPushButton.clicked.connect(self.find_program)
        self.addProgramPushButton.clicked.connect(self.add_program)
        self.removeProgramPushButton.clicked.connect(self.remove_program)
        self.programPasswordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)

    def load_form(self):
        active_username = self.authenticator.loged_user.username
        self.load_user_programs()
        self.userDataLabel.setText(f"Prisijungęs vartotojas - {active_username}")

    def load_program(self, program_name: str):
        programs = self.authenticator.loged_user.programs

        if not programs:
            return

        for program in programs:
            if program.name == program_name:
                self.programNameLineEdit.setText(program.name)
                self.programPasswordLineEdit.setText(program.password)
                self.programUrlLineEdit.setText(program.url)
                self.programNotesTextEdit.setPlainText(program.notes)
                return

    def find_program(self):
        programs = self.authenticator.loged_user.programs
        program_name = self.findProgramLineEdit.text()

        for program in programs:
            if program.name == program_name:
                self.load_program(program_name)
                return
            else:
                QMessageBox.information(self, "Klaida", "Tokios programos nėra")

    def hide_password(self):
        if not self.showPasswordCheckBox.isChecked():
            self.programPasswordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            self.programPasswordLineEdit.setEchoMode(QLineEdit.EchoMode.Normal)

    def load_user_programs(self):
        user = self.authenticator.loged_user

        if not user:
            return

        if not user.programs:
            return

        self.programsComboBox.clear()
        self.programsComboBox.addItem("Pasirinkite")

        for program in user.programs:
            self.programsComboBox.addItem(program.name)

    def new_program(self):
        self.programNameLineEdit.setText("")
        self.programPasswordLineEdit.setText("")
        self.programUrlLineEdit.setText("")
        self.programNotesTextEdit.setPlainText("")

    def add_program(self):
        username = self.authenticator.loged_user.username
        program_name = self.programNameLineEdit.text()
        program_password = self.programPasswordLineEdit.text()
        program_url = self.programUrlLineEdit.text()
        program_notes = self.programNotesTextEdit.toPlainText()

        program = Program(
            name=program_name,
            password=program_password,
            url=program_url,
            notes=program_notes,
        )

        self.encryptor.add_program_to_txt(username, program)
        self.load_user_programs()

        QMessageBox.information(self, "Pranešimas", "Programa sėkmingai pridėta")

    def remove_program(self):
        username = self.authenticator.loged_user.username
        program_name = self.programNameLineEdit.text()

        self.encryptor.remove_program_from_txt(username, program_name)

        QMessageBox.information(self, "Pranešimas", "Programa sėkmingai ištrinta")

    def logout(self):
        self.authenticator.logout()
        self._mainwindow.set_login_window()

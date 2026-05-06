import ctypes
import os
import platform

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from gui.form import FormWidget
from gui.login.login import LoginWidget
from gui.register.register import RegisterWidget
from logic.authenticator import Authenticator
from logic.encryptor import Encryptor
from main.mainwindow_ui import Ui_MainWindow

# Fixes window sizing glitches
if platform.system() == "Windows" and int(platform.release()) >= 8:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.encryptor = Encryptor()
        self.authenticator = Authenticator(self.encryptor)
        self.formWidget = FormWidget(self, self.encryptor)
        self.registerWidget = RegisterWidget(self, self.encryptor)
        self.loginWidget = LoginWidget(self, self.authenticator)
        self.program_ui_initializer()

        # Login widget buttons

        # Main window buttons
        self.formWidget.logoutPushButton.clicked.connect(self.logout)
        self.formWidget.findProgramPushButton.clicked.connect(self.find_program)
        self.formWidget.newPgogramPushButton.clicked.connect(self.new_program)
        self.formWidget.showPasswordCheckBox.clicked.connect(self.show_password)
        self.formWidget.updatePasswordPushButton.clicked.connect(self.update_password)
        self.formWidget.addProgramPushButton.clicked.connect(self.add_program)
        self.formWidget.removeProgramPushButton.clicked.connect(self.remove_program)

        # Action buttons
        self.actionSave.triggered.connect(self.save_to_txt)
        self.actionOpen.triggered.connect(self.open_txt)

    def program_ui_initializer(self):
        self.verticalLayout_2.addWidget(self.loginWidget)
        self.resize(400, 400)
        self.formWidget.hide()
        self.registerWidget.hide()

    def set_register_window(self):
        self.verticalLayout_2.removeWidget(self.loginWidget)
        self.loginWidget.hide()

        self.verticalLayout_2.addWidget(self.registerWidget)
        self.registerWidget.show()
        self.resize(600, 600)

    def set_login_window(self):
        self.verticalLayout_2.removeWidget(self.registerWidget)
        self.registerWidget.hide()

        self.verticalLayout_2.addWidget(self.loginWidget)
        self.loginWidget.show()
        self.resize(400, 400)

    def set_main_window(self):
        self.verticalLayout_2.removeWidget(self.loginWidget)
        self.loginWidget.hide()

        self.verticalLayout_2.addWidget(self.formWidget)
        self.formWidget.show()

        self.resize(800, 800)

    def find_program(self):
        print("searching")

    def new_program(self):
        print("new program")

    def add_program(self):
        print("add program")

    def update_password(self):
        print("renewing password")

    def remove_program(self):
        print("remove program")

    def show_password(self):
        print("showing password")

    def logout(self):
        self.set_login_window()

    def save_to_txt(self):
        self.formWidget.save_to_txt()

    def open_txt(self):
        self.formWidget.open_txt()

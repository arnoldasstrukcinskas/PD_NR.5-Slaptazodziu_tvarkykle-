import ctypes
import os
import platform

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
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
        self.formWidget = FormWidget(self, self.encryptor, self.authenticator)
        self.registerWidget = RegisterWidget(self, self.encryptor)
        self.loginWidget = LoginWidget(self, self.authenticator)
        self.program_ui_initializer()

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
        self.resize(400, 400)

    def set_login_window(self):
        self.verticalLayout_2.removeWidget(self.registerWidget)
        self.registerWidget.hide()

        self.verticalLayout_2.removeWidget(self.formWidget)
        self.formWidget.hide()

        self.verticalLayout_2.addWidget(self.loginWidget)
        self.loginWidget.show()
        self.resize(400, 300)

    def set_main_window(self):
        self.verticalLayout_2.removeWidget(self.loginWidget)
        self.loginWidget.hide()

        self.verticalLayout_2.addWidget(self.formWidget)
        self.formWidget.show()

        self.resize(800, 800)

    def load_form_widget(self):
        self.formWidget.load_form()

    def logout(self):
        self.set_login_window()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.authenticator.logout()
        event.accept()

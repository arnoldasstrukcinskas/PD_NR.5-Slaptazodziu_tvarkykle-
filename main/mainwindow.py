import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from gui.form import FormWidget
from gui.login.login import LoginWidget
from gui.register.register import RegisterWidget
from main.mainwindow_ui import Ui_MainWindow


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.stack = QStackedWidget()
        self.formWidget = FormWidget(self)
        self.registerWidget = RegisterWidget(self)
        self.loginWidget = LoginWidget(self)
        self.verticalLayout_2.addWidget(self.stack)
        self.stack.addWidget(self.loginWidget)
        self.stack.addWidget(self.registerWidget)
        self.stack.addWidget(self.formWidget)
        self.set_login_window()

        # Login widget buttons
        self.loginWidget.registrationPushButton.clicked.connect(
            self.set_register_window
        )
        self.loginWidget.loginPushButton.clicked.connect(self.set_main_window)

        # Register widget buttons
        self.registerWidget.backPushButton.clicked.connect(self.set_login_window)
        self.registerWidget.registerPushButton.clicked.connect(self.set_login_window)
        # Main window buttons

    def set_register_window(self):
        self.stack.setCurrentWidget(self.registerWidget)

        # self.verticalLayout_2.removeWidget(self.loginWidget)
        # self.loginWidget.hide()

        # self.verticalLayout_2.addWidget(self.registerWidget)
        # self.registerWidget.show()

    def set_login_window(self):
        self.stack.setCurrentWidget(self.loginWidget)

        # self.verticalLayout_2.removeWidget(self.registerWidget)
        # self.registerWidget.hide()

        # self.verticalLayout_2.addWidget(self.loginWidget)
        # self.loginWidget.show()

    def set_main_window(self):
        self.stack.setCurrentWidget(self.formWidget)

        # self.verticalLayout_2.removeWidget(self.loginWidget)
        # self.loginWidget.hide()

        # self.verticalLayout_2.addWidget(self.formWidget)
        # self.formWidget.show()

        # self.actionSave.triggered.connect(self.save_to_txt)
        # self.actionOpen.triggered.connect(self.open_txt)

    # def save_to_txt(self):
    #     self.formWidget.save_to_txt()

    # def open_txt(self):
    #     self.formWidget.open_txt()

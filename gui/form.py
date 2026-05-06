from typing import TYPE_CHECKING

from PyQt5.QtWidgets import *

from gui.form_ui import Ui_Form
from logic.encryptor import Encryptor

if TYPE_CHECKING:
    from main.mainwindow import MainWindow

BITS128 = 128
BITS192 = 192
BITS256 = 256


class FormWidget(Ui_Form, QWidget):

    def __init__(self, parent: "MainWindow", encryptor: Encryptor):
        super().__init__(parent=parent)
        self.setMaximumSize(800, 800)
        self.setupUi(self)
        self.encryptor = encryptor

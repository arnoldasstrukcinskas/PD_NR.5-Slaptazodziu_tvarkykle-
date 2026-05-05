import sys

from PyQt5.QtWidgets import QApplication

from main.mainwindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    screen = MainWindow()
    screen.resize(400, 400)
    screen.show()

    sys.exit(app.exec_())

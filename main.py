from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


def window():
    app = QApplication(sys.argv)
    win = QMainWindow()

    win.setGeometry(250, 200, 940, 680)
    win.setWindowTitle("Annotation tool")

    button = QtWidgets.QPushButton(win)
    button.setText("Hello World!")
    button.move(50, 20)

    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    window()

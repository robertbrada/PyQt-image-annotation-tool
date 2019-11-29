import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget

# ======================================================================

# folder with images we want to label (don't forget "/" at the end)
input_folder = './data/images1/'

# labels we want to use
labels = ["label1", "label2", "label3"]

# output csv file
output_file = 'output.csv'

# allowed file extensions
file_extensions = ('.jpg', '.png', '.jpeg')


# ======================================================================
def get_img_paths(dir, extensions=''):
    '''
    :param dir: folder with files
    :param extensions: tuple with file endings. e.g. ('.jpg', '.png')
    :return: list of all filenames
    '''

    filenames = []

    for filename in os.listdir(dir):
        if filename.lower().endswith(extensions):
            filenames.append(dir + filename)

    return filenames


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 - Annotation tool'
        self.left = 200
        self.top = 200
        self.width = 960
        self.height = 540
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create button
        button = QtWidgets.QPushButton(self)
        button.setText("Hello World!")
        button.move(50, 20)

        # apply styles
        sshFile = "./styles/button.qss"
        with open(sshFile, "r") as fh:
            self.setStyleSheet(fh.read())


if __name__ == '__main__':
    # get paths to images
    img_paths = get_img_paths(input_folder, file_extensions)

    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())

import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

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
    # get paths to images
    img_paths = get_img_paths(input_folder, file_extensions)

    window()

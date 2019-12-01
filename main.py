import csv
import os
import shutil
import sys

import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

# ======================================================================

# folder with images we want to label (don't forget "/" at the end)
input_folder = './data/images1/'

# labels we want to use
labels = ["label1", "label2", "label3", "label4", "label5", "label6", "label7", "label8", "label9", "label10",
          "label11", "label12"]

# select one of the following modes: copy, move, none
# 1. copy: Creates folder for each label. Labeled images are copied to these folders
# 2. move: Creates folder for each label. Labeled images are moved to these folders
# 3. csv: Images in input_folder are just labeled and then csv file with assigned labels is generated
mode = 'csv'  # 'copy', 'move', 'csv'

# allowed file extensions
file_extensions = ('.jpg', '.png', '.jpeg')


# ======================================================================
def get_img_paths(dir, extensions=''):
    '''
    :param dir: folder with files
    :param extensions: tuple with file endings. e.g. ('.jpg', '.png')
    :return: list of all filenames
    '''

    img_paths = []

    for filename in os.listdir(dir):
        if filename.lower().endswith(extensions):
            img_paths.append(os.path.join(dir, filename))

    return img_paths


def make_folder(directory):
    """
    Make folder if it doesn't already exist
    :param directory: The folder destination path
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


class App(QWidget):
    def __init__(self, labels, img_paths):
        super().__init__()

        # init UI state
        self.title = 'PyQt5 - Annotation tool for assigning image classes'
        self.left = 200
        self.top = 200
        self.width = 1000
        self.height = 760
        self.img_panel_width = 800

        # state variables
        self.counter = 0
        self.img_paths = img_paths
        self.labels = labels
        self.num_labels = len(labels)
        self.num_images = len(img_paths)

        self.label_buttons = []
        self.assigned_labels = {}

        # Initialize Labels
        self.image_box = QLabel(self)
        self.img_name_label = QLabel(self)
        self.progress_bar = QLabel(self)
        self.csv_note = QLabel('(csv will be also generated automatically after closing the app)', self)
        self.csv_generated_message = QLabel(self)

        # init UI
        self.initUI()

    def initUI(self):


        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.initButtons()

        # image name label
        self.img_name_label.setGeometry(20, 10, self.img_panel_width, 20)

        # progress bar (how many images have I labeled so far)
        self.progress_bar.setGeometry(20, 30, self.img_panel_width, 20)

        # csv note
        self.csv_note.setGeometry(20, 680, self.img_panel_width, 20)
        self.csv_note.setAlignment(Qt.AlignCenter)

        # message that csv was generated
        self.csv_generated_message.setGeometry(20, 710, self.img_panel_width, 20)
        self.csv_generated_message.setStyleSheet('color: #43A047')
        self.csv_generated_message.setAlignment(Qt.AlignCenter)

        # show image
        self.set_image(self.img_paths[0])
        self.image_box.move(20, 60)

        # image name
        self.img_name_label.setText(img_paths[self.counter])

        # progress bar
        self.progress_bar.setText(f'image 1 of {self.num_images}')

        # apply styles
        sshFile = "./styles/custom_styles.qss"
        with open(sshFile, "r") as fh:
            self.setStyleSheet(fh.read())

    def initButtons(self):

        # Add "Prev Image" and "Next Image" buttons
        prev_im_btn = QtWidgets.QPushButton("Prev", self)
        prev_im_btn.move(320, 580)
        prev_im_btn.clicked.connect(self.show_prev_image)

        next_im_btn = QtWidgets.QPushButton("Next", self)
        next_im_btn.move(430, 580)
        next_im_btn.clicked.connect(self.show_next_image)

        # Add "generate csv file" button
        next_im_btn = QtWidgets.QPushButton("Generate csv", self)
        next_im_btn.move(375, 640)
        next_im_btn.clicked.connect(self.generate_csv)
        next_im_btn.setObjectName("generateCsvButton")

        # Create label button
        for i, label in enumerate(self.labels):
            self.label_buttons.append(QtWidgets.QPushButton(label, self))
            button = self.label_buttons[i]
            # 80 is button width, 10 is spacing between buttons
            button.move(self.width - 190, (30 + 10) * i + 60)

            # https://stackoverflow.com/questions/35819538/using-lambda-expression-to-connect-slots-in-pyqt
            button.clicked.connect(lambda state, x=label: self.set_label(x))

    def set_label(self, label):
        # get image filename from path (./data/images/img1.jpg → img1.jpg)
        filename = os.path.split(self.img_paths[self.counter])[-1]

        # check if this file was already labeled.
        # If so, save prevous label, so I can change the images's location in case 'copy' or 'move' mode is enabled
        prev_label = None
        if filename in self.assigned_labels.keys():
            prev_label = self.assigned_labels[filename]

        # set new label
        self.assigned_labels[filename] = label

        # copy/move the image into appropriate label folder
        if mode == 'copy':
            self._copy_image(label, prev_label, self.img_paths[self.counter])
        elif mode == 'move':
            self._move_image(label, prev_label, self.img_paths[self.counter])

        # load next image
        self.show_next_image()

    def show_next_image(self):

        if self.counter < self.num_images - 1:
            self.counter += 1

            path = self.img_paths[self.counter]
            filename = os.path.split(path)[-1]

            # If we have already assigned label to this image and mode is 'move', change the input path.
            # The reason is that the image was moved from '.../input_folder' to '.../input_folder/label'
            if mode == 'move' and filename in self.assigned_labels.keys():
                path = os.path.join(input_folder, self.assigned_labels[filename], filename)

            self.set_image(path)
            self.img_name_label.setText(path)
            self.progress_bar.setText(f'image {self.counter + 1} of {self.num_images}')
            self.set_button_color(path)
            self.csv_generated_message.setText('')


        # change button color if this is last image in dataset
        elif self.counter == self.num_images - 1:
            path = self.img_paths[self.counter]
            self.set_button_color(path)

    def show_prev_image(self):
        if self.counter > 0:
            self.counter -= 1

            if self.counter < self.num_images:
                path = self.img_paths[self.counter]
                filename = os.path.split(path)[-1]

                # If we have already assigned label to this image and mode is 'move', change the input path.
                # The reason is that the image was moved from '.../input_folder' to '.../input_folder/label'
                if mode == 'move' and filename in self.assigned_labels.keys():
                    path = os.path.join(input_folder, self.assigned_labels[filename], filename)

                self.set_image(path)
                self.img_name_label.setText(path)
                self.progress_bar.setText(f'{self.counter + 1} of {self.num_images}')

                self.set_button_color(path)
                self.csv_generated_message.setText('')

    def set_image(self, path):
        pixmap = QPixmap(path).scaled(750, self.img_panel_width, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.image_box.setPixmap(pixmap)

    def generate_csv(self):
        filename = 'assigned_classes.csv'

        path_to_save = os.path.join(input_folder, 'csv_ouput')
        make_folder(path_to_save)
        with open(os.path.join(path_to_save, filename), "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')

            # write header
            writer.writerow(['img'] + self.labels)

            # write one-hot labels
            for img_name, label in self.assigned_labels.items():
                label_one_hot = self.__number_to_one_hot(self.labels.index(label), self.num_labels)
                writer.writerow([img_name] + list(label_one_hot))

        self.csv_generated_message.setText(f'csv saved to: {os.path.abspath(os.path.join(path_to_save, filename))}')
        print(f'csv saved to: {os.path.abspath(os.path.join(path_to_save, filename))}')

    def set_button_color(self, img_path):
        for button in self.label_buttons:
            button.setStyleSheet('background-color: None; height: 40px')

        filename = os.path.split(img_path)[-1]
        if filename in self.assigned_labels.keys():
            label_index = self.labels.index(self.assigned_labels[filename])
            self.label_buttons[label_index].setStyleSheet(
                'border: 1px solid #43A047; background-color: #4CAF50; color: white; height: 40px')

    def closeEvent(self, event):
        print("closing App")
        self.generate_csv()

    @staticmethod
    def __number_to_one_hot(number, num_classes):
        one_hot_arr = np.zeros([num_classes], dtype=int)
        one_hot_arr[number] = 1
        return one_hot_arr

    @staticmethod
    def _copy_image(label, prev_label, file_path):
        """
        Copies a file to a new label folder using the shutil library. The file will be copied into a
        subdirectory called label in the input folder.
        :param label: The label
        :param file_path: Path of the original image
        """

        img_filename = os.path.split(file_path)[-1]

        output_path = os.path.join(input_folder, label, img_filename)
        shutil.copy(file_path, output_path)

        # remove image from it's previous location
        if prev_label:
            os.remove(os.path.join(input_folder, prev_label, img_filename))

    @staticmethod
    def _move_image(label, prev_label, file_path):
        """
        Moves a file to a new label folder using the shutil library. The file will be moved into a
        subdirectory called label in the input folder.
        :param label: The label
        :param file_path: Path of the original image
        """

        img_filename = os.path.split(file_path)[-1]

        # if the image was labeled before, it means it was moved to another directory (named as prev_label)
        # for that reason you have to change the path to the image file (= file_path)
        if prev_label:
            file_path = os.path.join(input_folder, prev_label, img_filename)

        output_path = os.path.join(input_folder, label, img_filename)

        shutil.move(file_path, output_path)


if __name__ == '__main__':
    # get paths to images in input_folder
    img_paths = get_img_paths(input_folder, file_extensions)

    # create folders for each label if 'copy' or 'move' modes are selected
    if mode == 'copy' or mode == 'move':
        for label in labels:
            make_folder(os.path.join(input_folder, label))

    app = QApplication(sys.argv)
    ex = App(labels, img_paths)
    ex.show()
    sys.exit(app.exec_())

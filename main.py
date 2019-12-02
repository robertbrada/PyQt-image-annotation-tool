import csv
import os
import shutil
import sys

import math
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QCheckBox, QFileDialog, QDesktopWidget, QLineEdit, \
    QInputDialog

# ======================================================================
# SET THESE PARAMETERS AND RUN main.py SCRIPT

# folder with images we want to label (don't forget "/" at the end)
input_folder = './data/images/'

# labels we want to use
labels = ["label 1", "label 2", "label 3", "label 4", "label 5", "label 6", "label 7", "label 8", "label 9", "label 10",
          "label 11", "label 12", "label 13"]

# select one of the following modes: copy, move, none
# 1. copy: Creates folder for each label. Labeled images are copied to these folders
# 2. move: Creates folder for each label. Labeled images are moved to these folders
# 3. csv: Images in input_folder are just labeled and then csv file with assigned labels is generated
mode = 'csv'  # 'copy', 'move', 'csv'

# allowed file extensions (images in INPUT_FOLDER with these extensions will be loaded)
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


class SetParametersDialog(QWidget):
    def __init__(self):
        super().__init__()

        # window variables
        self.width = 800
        self.height = 800

        # state variables
        self.selectedFolder = ''
        self.num_labels = 0
        self.label_inputs = []
        self.label_headlines = []

        # init UI components
        self.headlineFolder = QLabel('1. Select folder with images you want to label', self)
        self.selectedFolderLabel = QLabel(self)
        self.browse_button = QtWidgets.QPushButton("Browse", self)

        self.headlineNumLabels = QLabel('2. How many unique labels do you want to assign?', self)
        self.numLabelsInput = QLineEdit(self)
        self.confirmNumLabels = QtWidgets.QPushButton("Ok", self)

        self.next_button = QtWidgets.QPushButton("Next", self)

        self.headlineLabelInputs = QLabel(self)
        self.onlyInt = QIntValidator()

        self.initUI()

    def initUI(self):
        # self.selectFolderDialog = QFileDialog.getExistingDirectory(self, 'Select directory')
        self.setWindowTitle('PyQt5 - Annotation tool - Parameters setup')
        self.setGeometry(0, 0, self.width, self.height)
        self.centerOnScreen()

        self.headlineFolder.setGeometry(60, 40, 300, 20)

        self.selectedFolderLabel.setGeometry(60, 76, 582, 26)
        self.selectedFolderLabel.setObjectName("selectedFolderLabel")

        self.browse_button.move(self.width -60 - 100, 75)
        self.browse_button.clicked.connect(self.pick_new)

        # Create textbox
        self.headlineNumLabels.move(60, 140)
        self.numLabelsInput.setGeometry(60, 171, 60, 26)
        self.numLabelsInput.setValidator(self.onlyInt)
        self.confirmNumLabels.move(118, 170)
        self.confirmNumLabels.clicked.connect(self.generate_label_inputs)

        self.next_button.move(360, 720)
        self.next_button.clicked.connect(self.continue_app)

        # self.getInteger()

        # apply custom styles
        try:
            styles_path = "./styles.qss"
            with open(styles_path, "r") as fh:
                self.setStyleSheet(fh.read())
        except:
            print("Can't load custom stylesheet.")

    def centerOnScreen(self):
        """
        Centers the window on the screen.
        """
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def pick_new(self):
        """
        shows a dialog to choose folder with images to label
        """
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "Select Folder")

        self.selectedFolderLabel.setText(folder_path)
        self.selectedFolder = folder_path

    def generate_label_inputs(self):
        if self.numLabelsInput.text() != '':
            self.num_labels = int(self.numLabelsInput.text())

            # delete previously generated widgets
            for input, headline in zip(self.label_inputs, self.label_headlines):
                input.deleteLater()
                headline.deleteLater()

            self.label_inputs = []
            self.label_headlines = []

            self.headlineLabelInputs.setText('3. Fill in the labels and click "Next"')
            self.headlineLabelInputs.setGeometry(60, 230, 300, 20)

            x_shift = 0  # variable that helps to compute x-coordinate of label in UI
            for i in range(self.num_labels):
                self.label_inputs.append(QtWidgets.QLineEdit(self))
                self.label_headlines.append(QLabel(f'label {i+1}:', self))

                label_input = self.label_inputs[i]
                label = self.label_headlines[i]

                # place button in GUI (create multiple columns if there is more than 10 button)
                y_shift = (30 + 10) * (i % 10)
                if i != 0 and i % 10 == 0:
                    x_shift += 240
                    y_shift = 0

                # place input and labels
                label_input.setGeometry(60 + 60 + x_shift, y_shift + 280, 120, 26)
                label.setGeometry(60 + x_shift, y_shift + 280, 60, 26)

                label_input.show()
                label.show()

    def continue_app(self):
        self.close()
        App(labels, img_paths).show()


class App(QWidget):
    def __init__(self, labels, img_paths):
        super().__init__()

        # init UI state
        self.title = 'PyQt5 - Annotation tool for assigning image classes'
        self.left = 200
        self.top = 200
        self.width = 1220
        self.height = 760
        self.img_panel_width = 800
        self.img_panel_height = 750

        # state variables
        self.counter = 0
        self.img_paths = img_paths
        self.labels = labels
        self.num_labels = len(labels)
        self.num_images = len(img_paths)
        self.assigned_labels = {}

        # initialize list to save all label buttons
        self.label_buttons = []

        # Initialize Labels
        self.image_box = QLabel(self)
        self.img_name_label = QLabel(self)
        self.progress_bar = QLabel(self)
        self.csv_note = QLabel('(csv will be also generated automatically after closing the app)', self)
        self.csv_generated_message = QLabel(self)
        self.showNextCheckBox = QCheckBox("Automatically show next image when labeled", self)

        # init UI
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # self.selectFolderDialog.setGeometry(20, 800, 300, 20)
        # create buttons
        self.initButtons()

        # create checkbox
        self.showNextCheckBox.setChecked(True)
        self.showNextCheckBox.setGeometry(300, 64, 300, 20)

        # image name label
        self.img_name_label.setGeometry(20, 10, self.img_panel_width, 20)

        # progress bar (how many images have I labeled so far)
        self.progress_bar.setGeometry(20, 30, self.img_panel_width, 20)

        # csv note
        self.csv_note.setGeometry(self.img_panel_width + 20, 640, 400, 20)

        # message that csv was generated
        self.csv_generated_message.setGeometry(self.img_panel_width + 20, 660, 800, 20)
        self.csv_generated_message.setStyleSheet('color: #43A047')

        # show image
        self.set_image(self.img_paths[0])
        self.image_box.setGeometry(20, 100, self.img_panel_width, self.img_panel_height)
        self.image_box.setAlignment(Qt.AlignTop)

        # image name
        self.img_name_label.setText(img_paths[self.counter])

        # progress bar
        self.progress_bar.setText(f'image 1 of {self.num_images}')

        # apply custom styles
        try:
            styles_path = "./styles.qss"
            with open(styles_path, "r") as fh:
                self.setStyleSheet(fh.read())
        except:
            print("Can't load custom stylesheet.")

    def initButtons(self):

        num_columns = int(math.ceil(self.num_labels / 10))

        # Add "Prev Image" and "Next Image" buttons
        prev_im_btn = QtWidgets.QPushButton("Prev", self)
        prev_im_btn.move(20, 60)
        prev_im_btn.clicked.connect(self.show_prev_image)

        next_im_btn = QtWidgets.QPushButton("Next", self)
        next_im_btn.move(130, 60)
        next_im_btn.clicked.connect(self.show_next_image)

        # Add "generate csv file" button
        next_im_btn = QtWidgets.QPushButton("Generate csv", self)
        next_im_btn.move(self.img_panel_width + 20, 600)
        next_im_btn.clicked.connect(lambda state, filename='assigned_classes.csv': self.generate_csv(filename))
        next_im_btn.setObjectName("generateCsvButton")

        # Create button for each label
        x_shift = 0  # variable that helps to compute x-coordinate of button in UI
        for i, label in enumerate(self.labels):
            self.label_buttons.append(QtWidgets.QPushButton(label, self))
            button = self.label_buttons[i]

            # create click event (set label)
            # https://stackoverflow.com/questions/35819538/using-lambda-expression-to-connect-slots-in-pyqt
            button.clicked.connect(lambda state, x=label: self.set_label(x))

            # place button in GUI (create multiple columns if there is more than 10 button)
            y_shift = (30 + 10) * (i % 10)
            if (i != 0 and i % 10 == 0):
                x_shift += 120
                y_shift = 0

            button.move(self.img_panel_width + 20 + x_shift, y_shift + 100)

    def set_label(self, label):
        """
        Sets the label for just loaded image
        :param label: selected label
        """

        # get image filename from path (./data/images/img1.jpg → img1.jpg)
        filename = os.path.split(self.img_paths[self.counter])[-1]

        # check if this file was already labeled.
        # If so, save previous label, so I can change the images's location in case 'copy' or 'move' mode is enabled
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
        if self.showNextCheckBox.isChecked():
            self.show_next_image()
        else:
            self.set_button_color(filename)

    def show_next_image(self):
        """
        loads and shows next image in dataset
        """
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
            self.set_button_color(filename)
            self.csv_generated_message.setText('')


        # change button color if this is last image in dataset
        elif self.counter == self.num_images - 1:
            path = self.img_paths[self.counter]
            self.set_button_color(os.path.split(path)[-1])

    def show_prev_image(self):
        """
        loads and shows previous image in dataset
        """
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
                self.progress_bar.setText(f'image {self.counter + 1} of {self.num_images}')

                self.set_button_color(filename)
                self.csv_generated_message.setText('')

    def set_image(self, path):
        """
        displays the image in GUI
        :param path: relative path to the image that should be show
        """

        # create pixmap and scale it appropriately, so that images stay in the dedicated area no matter the resolution
        pixmap = QPixmap(path).scaled(self.img_panel_height, self.img_panel_width, Qt.KeepAspectRatio,
                                      Qt.FastTransformation)

        self.image_box.setPixmap(pixmap)

    def generate_csv(self, out_filename):
        """
        Generates and saves csv file with assigned labels.
        Assigned label is represented as one-hot vector.
        :param out_filename: name of csv file to be generated
        """
        path_to_save = os.path.join(input_folder, 'csv_ouput')
        make_folder(path_to_save)
        with open(os.path.join(path_to_save, out_filename), "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')

            # write header
            writer.writerow(['img'] + self.labels)

            # write one-hot labels
            for img_name, label in self.assigned_labels.items():
                label_one_hot = self.__number_to_one_hot(self.labels.index(label), self.num_labels)
                writer.writerow([img_name] + list(label_one_hot))

        message = f'csv saved to: {os.path.abspath(os.path.join(path_to_save, out_filename))}'
        self.csv_generated_message.setText(message)
        print(message)

    def set_button_color(self, filename):
        """
        changes color of button which corresponds to selected label
        :filename filename of loaded image:
        """
        for button in self.label_buttons:
            button.setStyleSheet('background-color: None')

        if filename in self.assigned_labels.keys():
            label_index = self.labels.index(self.assigned_labels[filename])
            self.label_buttons[label_index].setStyleSheet(
                'border: 1px solid #43A047; background-color: #4CAF50; color: white')

    def closeEvent(self, event):
        """
        This function is executed when the app is closed.
        It automatically generates csv file in case the user forgot to do that
        """
        print("closing the App..")
        self.generate_csv('assigned_classes_automatically_generated.csv')

    @staticmethod
    def __number_to_one_hot(number, num_classes):
        """
        Convert number to one-hot vector
        :param number: number which represents for example class index
        :param num_classes: number of classes in dataset so I know how long the vector should be
        :return:
        """
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

        # get image filename (e.g. img_1.jpg)
        img_filename = os.path.split(file_path)[-1]

        output_path = os.path.join(input_folder, label, img_filename)

        # copy image to a new location
        shutil.copy(file_path, output_path)

        # remove image from it's previous location if the image was labeled before
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

        # get image filename (e.g. img_1.jpg)
        img_filename = os.path.split(file_path)[-1]

        # if the image was labeled before, it means it was moved to another directory (named as prev_label)
        # for that reason you have to change the path to the image file (= file_path)
        if prev_label:
            file_path = os.path.join(input_folder, prev_label, img_filename)

        output_path = os.path.join(input_folder, label, img_filename)

        # move image to a new location
        shutil.move(file_path, output_path)


if __name__ == '__main__':
    # get paths to images in input_folder
    img_paths = get_img_paths(input_folder, file_extensions)

    # throw an exception when n files found
    if len(img_paths) == 0:
        raise Exception(f'No images found in {input_folder}')

    # create folders for each label if 'copy' or 'move' modes are selected
    if mode == 'copy' or mode == 'move':
        for label in labels:
            make_folder(os.path.join(input_folder, label))

    # run the application
    app = QApplication(sys.argv)
    ex = SetParametersDialog()
    ex.show()
    sys.exit(app.exec_())

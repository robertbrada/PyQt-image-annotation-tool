# PyQt Image Annotation Tool

This app is used to label images in a given directory.
Labeled images can be moved or copied into sub-directories, which are named as assigned labels.
The app is just a single Python script with GUI.

![PyQt Image Annotation Tool GUI](https://i.stack.imgur.com/iihhf.png)

## What can this app do
For example you have folder ./data/images/ with a lot of images and you need to assign some
label(s) to these images.

- it can assign multiple labels to one image
- it allows you to choose number and names of your labels
- it can move/copy images to folders that are named as desired labels.
- it can generate .csv file with assigned labels.
- it can generate .xlsx file with assigned labels.
- all settings are handled via GUI

## Installation and usage

1. Clone the project:
    ```bash
    git clone https://github.com/robertbrada/PyQt-image-annotation-tool.git
    ```

2. Enter the directory and install the dependencies (you might need to use ```pip3``` instead of ```pip```):
    ```bash
    cd PyQt-image-annotation-tool
    pip install -r requirements.txt
    ```
3. Run the app (use ```python3``` for Python 3)
   ```bash
    python main.py
    ```

## Keyboard shortcuts

- N: Next image
- P: Previous image
- 1-9: Select label

## Contributing

Pull requests are welcomed.

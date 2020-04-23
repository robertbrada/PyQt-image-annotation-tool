# PyQt Image Annotation Tool

This app is used to label images in a directory.
Labeled images can be moved/copied into directories, which are named as assigned labels.
It's a single Python script with GUI.

For example you have folder ./data/images/ with a lot of images and you need to assign some
label(s) to these images.

![PyQt Image Annotation Tool GUI](https://i.stack.imgur.com/iihhf.png)

## What can this app do

- it can assign multiple labels to one image
- it allows you to choose number and names of your labels
- it can move/copy images to folders that are named as desired labels.
- it can generate .csv file with assigned labels.
- it can generate .xlsx file with assigned labels.
- all settings are handled via GUI

## How to use it

1. Download **main.py** file
2. You can also download **styles.qss** file and save it to the same directory as **main.py** file.
   This step is not required, but recommended.
3. install packages mentioned in **Requiremens** section.
4. Run **main.py** and GUI with instructions should appear.

## Requirements

Code is tested on Windows 10 and Ubuntu 18.04
. Code is written in Python 3.7.4 using following external libraries:

- numpy 1.17.4
- PyQt 5.9.2
- XlsxWriter 1.2.6

## Keyboard shortcuts

- N: Next image
- P: Previous image
- 1-9: Select label

## Contributing

Pull requests are welcome.

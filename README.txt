WHAT IS IT? 

This app is used to label images in a directory and move/copy these labeled images
to a separate directory.

For example you have folder ./data/images/ with a lot of images and you need to assign some
label(s) to these images.

What can this app do:
  - it can assign multiple labels to one image
  - it allows you to choose number and names of your labels
  - it can move/copy images to folders that are named as desired labels.
  - it can generate .csv file with assigned labels.
  - it can generate .xlsx file with assigned labels.
  - all settings are handled via GUI

-------------------------------------------------------------------------------------------------------------

HOW TO USE IT?

1. Download main.py file
2. You can also download styles.qss file and save it to the same directory as main.py file.
   This step is not required, but recommended - application will work without file styles.qss.
3. install packages mentioned in REQUIREMENTS section.  
4. Run main.py and GUI with instructions should appear.

-------------------------------------------------------------------------------------------------------------

REQUIREMENTS

Code is tested on Windows 10 and Ubuntu 18.04
Code is written in Python 3.7.4 using following external libraries:
- numpy 1.17.4
- PyQt 5.9.2
- XlsxWriter 1.2.6

-------------------------------------------------------------------------------------------------------------

KEYBOARD SHORTCUTS

N: Next image
P: Previous image
1-9: Select label


import pytest
from PyQt5.QtWidgets import QApplication
from app.main import LabelerWindow

@pytest.fixture
def app(qtbot):
    test_app = LabelerWindow(labels=['landschaft', 'menschen'], input_folder='test_folder', mode='csv')
    qtbot.addWidget(test_app)
    return test_app

def test_generate_csv_german(app, qtbot, tmpdir):
    # Set up the environment for the test
    app.german_format_check_box.setChecked(True)
    app.assigned_labels = {
        'test1.jpg': ['landschaft'],
        'test2.BMP': ['landschaft'],
        'test3.jpg': ['menschen'],
        'test4.gif': ['menschen']
    }
    output_csv = "test_output"
    app.generate_csv(output_csv)

    with open(r"test_folder/output/" + output_csv + ".csv") as f:
        lines = f.readlines()

    assert lines[0].strip() == 'img;landschaft;menschen'
    assert lines[1].strip() == 'test1.jpg;1;0'
    assert lines[2].strip() == 'test2.BMP;1;0'
    assert lines[3].strip() == 'test3.jpg;0;1'
    assert lines[4].strip() == 'test4.gif;0;1'

def test_generate_csv_no_german_format(app, qtbot, tmpdir):
    # Set up the environment for the test
    app.german_format_check_box.setChecked(False)
    app.assigned_labels = {
        'test1.jpg': ['landschaft'],
        'test2.BMP': ['landschaft'],
        'test3.jpg': ['menschen'],
        'test4.gif': ['menschen']
    }
    output_csv = "test_output"
    app.generate_csv(output_csv)

    with open(r"test_folder/output/" + output_csv + ".csv") as f:
        lines = f.readlines()

    assert lines[0].strip() == 'img,landschaft,menschen'
    assert lines[1].strip() == 'test1.jpg,1,0'
    assert lines[2].strip() == 'test2.BMP,1,0'
    assert lines[3].strip() == 'test3.jpg,0,1'
    assert lines[4].strip() == 'test4.gif,0,1'
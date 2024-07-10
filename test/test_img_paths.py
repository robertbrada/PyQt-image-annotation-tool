import os
import pytest
from app.main import get_img_paths
from PyQt5.QtGui import QImageReader

def test_supported_image_formats(tmpdir):
    # Get supported image formats from QImageReader
    # This will return a tuple of which represent the supported image file extensions (e.g., '.jpg', '.png')
    expected_formats = tuple('.' + extension.data().decode('utf-8') for extension in QImageReader.supportedImageFormats())
    
    # Create a temporary directory with dummy image files of each supported format
    # Using the tmpdir fixture from pytest to create a temporary directory that will be automatically cleaned up
    for fmt in expected_formats:
        # Construct the file path for a dummy image file with the given format
        file_path = os.path.join(tmpdir, f'test_image{fmt}')
        # Create an empty file with the specified format
        open(file_path, 'a').close()
    
    # Get image paths using the updated get_img_paths function
    # This function should return a list of paths to the image files in the directory that match the supported formats
    img_paths = get_img_paths(tmpdir)
    
    # Ensure all supported image formats are detected
    # The number of detected image paths should match the number of supported formats
    assert len(img_paths) == len(expected_formats)
    # Verify that each detected image path has an extension that is in the expected formats
    for path in img_paths:
        assert os.path.splitext(path)[1] in expected_formats

def test_no_images_found(tmpdir):
    # Create a temporary directory with no image files
    # Using the tmpdir fixture from pytest to create a temporary directory
    # This time, we do not create any image files in the directory
    img_paths = get_img_paths(tmpdir)
    
    # Ensure no images are found
    # Since no image files were created in the directory, get_img_paths should return an empty list
    assert img_paths == []
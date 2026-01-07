# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import json
import os

import numpy as np
import cv2
from locator import annotate_image
from locator import annotate_directory



if __name__ == "__main__":
    # create a simple white dummy image (H, W, C)
    folder_path = "images"
    annotations_json = annotate_directory(folder_path, window_name="Annotate Images")
    annotations = json.loads(annotations_json)
    with open(os.path.join(folder_path, "annotation.json"), "w", encoding="utf-8") as f:
        json.dump(annotations, f, indent=2)

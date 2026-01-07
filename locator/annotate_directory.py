from locator import annotate_image
import os
import glob
import json
import cv2
import numpy as np


def annotate_directory(directory: str, window_name: str = "find holds") -> str:


    # collect png files
    pattern = os.path.join(directory, "*.png")
    files = sorted(glob.glob(pattern))
    if not files:
        return json.dumps([])

    imgs = []
    max_h = 0
    max_w = 0

    # load and normalize channels -> BGR (3 channels)
    for fp in files:
        img = cv2.imread(fp, cv2.IMREAD_UNCHANGED)
        if img is None:
            continue
        if img.ndim == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        elif img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        h, w = img.shape[:2]
        max_h = max(max_h, h)
        max_w = max(max_w, w)
        imgs.append(img)

    if not imgs:
        return json.dumps([])

    # resize all images to same size (largest found)
    resized = [cv2.resize(im, (max_w, max_h), interpolation=cv2.INTER_LINEAR) for im in imgs]
    batch = np.stack(resized, axis=0).astype(np.uint8)

    # call existing annotator (returns JSON string)
    annotations_json = annotate_image(batch, window_name=window_name)

    # attach filenames and save result
    annotations = json.loads(annotations_json)
    for i, ann in enumerate(annotations):
        if i < len(files):
            ann["filename"] = os.path.basename(files[i])
        else:
            ann["filename"] = f"image_{i}"

    # out_path = os.path.join(directory, filename)
    # with open(out_path, "w", encoding="utf-8") as files:
    #     json.dump(annotations, files, indent=2)

    return json.dumps(annotations)

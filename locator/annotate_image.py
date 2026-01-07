# python
import json
from typing import List, Dict, Any
import numpy as np
import cv2

def annotate_image(images, window_name: str = "find holds") -> str:
    """
    Manual point annotation with size trackbar and click position display.
    Controls:
      - Left click: add point (uses current trackbar size)
      - Right click: remove last point
      - Number keys 1-9: set point size (also updates trackbar)
      - n: next image
      - b: back
      - s: save & exit (returns JSON)
      - q: quit (returns current annotations)
    Returns:
      JSON string of annotations for each image.
    """
    if not isinstance(images, np.ndarray):
        raise ValueError("Unsupported ndarray shape for images")
    if images.dtype == np.uint8:
        images = images.astype(np.float32) / 255.0
    if images.ndim == 4:
        images_list = [images[i] for i in range(images.shape[0])]
    elif images.ndim in (2, 3):
        images_list = [images]
    else:
        raise ValueError("Unsupported ndarray shape for images")

    if len(images_list) == 0:
        return json.dumps([])

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)

    annotations: List[Dict[str, Any]] = [{"image_index": i, "points": []} for i in range(len(images_list))]
    current_image_index = 0
    current_trackbar_size = 5
    max_size = 100
    last_click = None  # (x, y) of last left-click
    current_point = None
    current_points: List[Dict[str, int]] = annotations[current_image_index]["points"]

    # trackbar callback
    def trackbar_cb(val):
        nonlocal current_trackbar_size
        current_trackbar_size = max(1, int(val))
        if len(current_points) > 0:
            current_points[-1]["size"] = current_trackbar_size
        redraw(images_list[current_image_index], current_points, window_name, "", current_trackbar_size=current_trackbar_size)

    # create trackbar (acts like a scrollbar for size)
    cv2.createTrackbar("Size", window_name, current_trackbar_size, max_size, trackbar_cb)

    def mouse_cb(event, x, y, flags, param):
        nonlocal current_points, last_click, current_point
        if event == cv2.EVENT_LBUTTONDOWN:
            current_point = {"x": int(x), "y": int(y), "size": int(current_trackbar_size)}
            current_points.append(current_point)
            last_click = (int(x), int(y))
            redraw(images_list[current_image_index], current_points, window_name, "", current_trackbar_size=current_trackbar_size)
        elif event == cv2.EVENT_RBUTTONDOWN and current_points:
            current_points.pop()
            print("Removed last point new length:", len(current_points))
            if len(current_points) > 0 :
                last_click = current_points[-1]["x"]
            redraw(images_list[current_image_index], current_points, window_name, "", current_trackbar_size=current_trackbar_size)

    cv2.setMouseCallback(window_name, mouse_cb)
    redraw(images_list[current_image_index], current_points, window_name, "", current_trackbar_size=current_trackbar_size)

    while True:
        key = cv2.waitKey(20) & 0xFF
        if key == 255:
            continue

        # number keys override size (and update trackbar)
        if ord("1") <= key <= ord("9"):
            current_trackbar_size = int(chr(key))
            cv2.setTrackbarPos("Size", window_name, current_trackbar_size)
            redraw(images_list[current_image_index], current_points, window_name, "", current_trackbar_size=current_trackbar_size)
            continue

        if key == ord("n"):
            annotations[current_image_index]["points"] = current_points.copy()
            if current_image_index < len(images_list) - 1:
                current_image_index += 1
                current_points = annotations[current_image_index]["points"]
                last_click = None
            redraw(images_list[current_image_index], current_points, window_name, "", current_trackbar_size=current_trackbar_size)
            continue

        if key == ord("b"):
            annotations[current_image_index]["points"] = current_points.copy()
            if current_image_index > 0:
                current_image_index -= 1
                current_points = annotations[current_image_index]["points"]
                last_click = None
            redraw(images_list[current_image_index], current_points, window_name, "", current_trackbar_size=current_trackbar_size)
            continue

        if key == ord("s"):
            annotations[current_image_index]["points"] = current_points.copy()
            cv2.destroyWindow(window_name)
            return json.dumps(annotations)

        if key == ord("q"):
            annotations[current_image_index]["points"] = current_points.copy()
            cv2.destroyWindow(window_name)
            return json.dumps(annotations)

    cv2.destroyWindow(window_name)
    return json.dumps(annotations)

def to_display(img: np.ndarray) -> np.ndarray:
    if img is None:
        return np.zeros((480, 640, 3), dtype=np.uint8)
    if img.ndim == 2:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if img.shape[2] == 4:
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img.copy()

def redraw(
        image:np.ndarray,
        current_points: List[Dict[str, int]],
        window_name:str,
        text:str="text",
        current_trackbar_size:int = 5
) -> None:
    disp = to_display(image).copy()
    # draw annotated points
    for point in current_points:
        cv2.circle(disp, (int(point["x"]), int(point["y"])), int(point["size"]), (0, 255, 0), thickness=2)

    if text:
        cv2.putText(disp, "text", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.imshow(window_name, disp)
    cv2.setTrackbarPos("Size", window_name, int(current_trackbar_size))

# python
from ultralytics import YOLO
import cv2
import numpy as np

MODEL_PATH = "train_detector/best (2).pt"
model = YOLO(MODEL_PATH)

def detect_holds(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return {"error": "Invalid image data"}

    results = model.predict(
        source=img,
        imgsz=800,
        conf=0.55,
        save=False,
        verbose=False
    )

    holds = []
    for box in results[0].boxes:
        x, y, w, h = box.xywh[0].tolist()
        holds.append({
            "position": [int(x), int(y)],
            "size": [int(w), int(h)],
        })

    return {"holds": holds}

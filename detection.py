# python
from ultralytics import YOLO
import cv2
import numpy as np
from io import BytesIO

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
    annotated_img = img.copy()
    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        x, y, w, h = box.xywh[0].tolist()
        holds.append({
            "position": [int(x), int(y)],
            "is_selected": False
        })
        cv2.rectangle(annotated_img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    _, img_encoded = cv2.imencode('.jpg', annotated_img)
    annotated_bytes = img_encoded.tobytes()

    return {"holds": holds, "annotated_image": annotated_bytes}

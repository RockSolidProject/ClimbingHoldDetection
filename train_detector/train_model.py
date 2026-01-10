from ultralytics import YOLO
import torch
from pathlib import Path
import sys


def main():
    print("=== YOLOv8 TRAINING ===")
    print("Torch version:", torch.__version__)
    print("CUDA available:", torch.cuda.is_available())

    if torch.cuda.is_available():
        print("GPU:", torch.cuda.get_device_name(0))

    data_path = Path(__file__).resolve().parent / "data.yml"
    if not data_path.exists():
        raise FileNotFoundError(f"data.yml not found at: {data_path}")

    model = YOLO("yolov8m.pt")

    model.train(
        data=str(data_path),

        epochs=150,
        patience=20,

        imgsz=800,
        batch=16,

        device=0 if torch.cuda.is_available() else "cpu",
        workers=8,
        amp=True,

        optimizer="AdamW",
        lr0=0.001,
        weight_decay=0.0005,

        hsv_h=0.02,
        hsv_s=0.4,
        hsv_v=0.3,
        degrees=3,
        translate=0.08,
        scale=0.3,
        fliplr=0.5,

        project="runs/holds1",
        name="yolov8_hold_detector_v3",
        pretrained=True,
        verbose=True
    )


if __name__ == "__main__":
    main()

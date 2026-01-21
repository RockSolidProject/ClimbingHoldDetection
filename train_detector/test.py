from ultralytics import YOLO

model = YOLO('train_detector/best (2).pt')
metrics = model.val(data='train_detector/data.yml', split='test', iou=0.5, conf=0.5)
mp, mr, map50, _map = metrics.box.mean_results()
print(metrics)
print(f"Precision: {mp:.4f}")
print(f"Recall:    {mr:.4f}")
print(f"mAP50:     {map50:.4f}")
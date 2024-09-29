from typing import TypedDict

from ultralytics import YOLO

MODELPATH = "./plaite/best.pt"
model = YOLO(MODELPATH)


class DetectionResult(TypedDict):
    label: str
    confidence: float
    bbox: tuple[int, int, int, int]


def detect(image) -> list[DetectionResult]:
    predictions = model(image)

    results = []
    for pred in predictions[0].boxes:
        bbox = map(int, pred.xyxy[0].tolist())
        confidence = pred.conf.item()
        class_id = int(pred.cls.item())
        label = model.names[class_id]
        results.append({"label": label, "confidence": confidence, "bbox": bbox})

    return results

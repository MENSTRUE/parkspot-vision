from pathlib import Path

import numpy as np
from PIL import Image
from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "parkspot_yolo11n_best.pt"
)


def load_model(
    model_path: Path = DEFAULT_MODEL_PATH,
):
    model_path = Path(model_path)

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model tidak ditemukan: {model_path}"
        )

    return YOLO(str(model_path))


def predict_image(
    image: Image.Image,
    model_path: Path = DEFAULT_MODEL_PATH,
    confidence: float = 0.25,
):
    model = load_model(model_path)

    image = image.convert("RGB")

    results = model.predict(
        source=np.array(image),
        conf=confidence,
        verbose=False,
    )

    result = results[0]

    counts = {
        "space-empty": 0,
        "space-occupied": 0,
    }

    detections = []

    if (
        result.boxes is not None
        and len(result.boxes) > 0
    ):
        class_ids = (
            result.boxes.cls
            .detach()
            .cpu()
            .numpy()
            .astype(int)
        )

        confidences = (
            result.boxes.conf
            .detach()
            .cpu()
            .numpy()
        )

        boxes = (
            result.boxes.xyxy
            .detach()
            .cpu()
            .numpy()
        )

        names = result.names

        for (
            class_id,
            score,
            box,
        ) in zip(
            class_ids,
            confidences,
            boxes,
        ):
            class_name = names[
                int(class_id)
            ]

            if class_name in counts:
                counts[class_name] += 1

            detections.append(
                {
                    "class": class_name,
                    "confidence": float(score),
                    "box": [
                        float(value)
                        for value in box
                    ],
                }
            )

    vacant = counts["space-empty"]
    occupied = counts["space-occupied"]

    total = vacant + occupied

    occupancy_rate = (
        occupied / total
        if total > 0
        else 0.0
    )

    annotated_bgr = result.plot()

    annotated_rgb = annotated_bgr[
        :, :, ::-1
    ]

    annotated_image = Image.fromarray(
        annotated_rgb
    )

    return {
        "annotated_image": annotated_image,
        "vacant": vacant,
        "occupied": occupied,
        "total": total,
        "occupancy_rate": occupancy_rate,
        "detections": detections,
    }
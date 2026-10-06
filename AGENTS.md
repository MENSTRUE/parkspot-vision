# AGENTS.md — ParkSpot Vision

This file defines rules and source-of-truth assumptions for AI coding agents working on ParkSpot Vision.

---

## 1. Product Identity

ParkSpot Vision is a Computer Vision system for **parking-slot occupancy monitoring** from fixed-camera imagery.

Core question:

```text
Which parking slots are OCCUPIED and which are VACANT?
```

The current product is not merely a generic vehicle detector.

---

## 2. Current Product Direction

Target MVP:

```text
Fixed Parking Image
→ Parking Slot ROI / Polygon
→ Per-Slot Crop
→ Occupancy Classifier
→ OCCUPIED / VACANT
→ Reconstruct on Full Image
→ Occupancy Count
```

Long-term direction:

```text
Camera / CCTV
→ Video Stream
→ Slot Occupancy
→ Temporal Smoothing
→ Availability Database
→ Dashboard
→ Driver Information Layer
```

Do not describe the current MVP as a production smart-parking platform.

---

## 3. Primary Dataset

Planned baseline:

```text
PKLot
```

Use the verified dataset structure as source of truth after inspection.

Never invent image counts, split counts, camera counts, weather counts, annotation formats, or class distributions.

---

## 4. Core Modeling Rule

Preferred baseline:

```text
slot ROI / polygon
→ crop parking slot
→ classify OCCUPIED / VACANT
```

Do not reduce the logic to:

```text
vehicle count = occupied slot count
```

A visible vehicle may overlap multiple slots, be in a driving lane, be partially occluded, or not correspond to a valid parking space.

---

## 5. Optional Detector Baseline

A detector may be used as comparison:

```text
vehicle detection
→ ROI overlap
→ occupancy assignment
```

If used, document overlap / IoU rules, center-point rules, ambiguous overlap handling, duplicate handling, and failure cases.

---

## 6. Split / Leakage Rule

Critical:

```text
do not blindly random-split near-identical slot crops
```

Preferred split unit:

```text
camera / day / sequence
```

Goal:

```text
reduce visual leakage between train / val / test
```

---

## 7. Evaluation Rules

Do not report accuracy only.

Prefer:

```text
Accuracy
Macro F1
Occupied Precision / Recall / F1
Vacant Precision / Recall / F1
Confusion Matrix
```

Product-level evaluation should also include frame-level occupied and vacant count error.

If inference time is reported, include hardware and CPU/GPU context.

---

## 8. Confidence Rule

Classifier confidence means model confidence for:

```text
OCCUPIED / VACANT
```

It does not mean legal permission to park, reservation status, payment status, or physical certainty.

---

## 9. Human / System Control

Product lesson:

```text
Delegate only the part AI can reasonably assist with.
```

AI may:
- classify slot occupancy,
- count available slots,
- flag uncertain slots.

Human/system owns:
- parking-layout definition,
- slot ROI mapping,
- camera setup,
- slot-map verification,
- operational decisions.

---

## 10. Parking Slot Geometry

Parking geometry is a first-class part of this project.

Possible representation:

```text
polygon
rectangle
ROI mask
```

Do not replace precise polygons with rough boxes unless the simplification is intentional and documented.

---

## 11. Reconstruction Rule

Predictions should be reconstructable on the full parking image.

Preferred visualization:

```text
VACANT    -> green polygon
OCCUPIED  -> red polygon
UNCERTAIN -> yellow/orange if implemented
```

Also display:

```text
Total Slots
Occupied
Vacant
Occupancy Rate
```

Compute these values from actual predictions.

---

## 12. Project Structure

```text
parkspot-vision/
├── assets/
├── data/
├── models/
├── notebooks/
├── reports/
├── src/
│   ├── check_dataset.py
│   ├── prepare_slots.py
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
├── app.py
├── AGENTS.md
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

---

## 13. File Responsibilities

### `src/check_dataset.py`
- inspect dataset structure,
- validate images and annotations,
- count valid records,
- detect missing image/annotation pairs.

### `src/prepare_slots.py`
- read slot annotations,
- extract polygons / ROIs,
- create per-slot crops,
- preserve camera/day/sequence metadata,
- prepare leakage-aware splits.

### `src/train.py`
- train occupancy classifier,
- save checkpoints,
- log real metrics.

### `src/evaluate.py`
- calculate per-class metrics,
- produce confusion matrix,
- evaluate count error if full-frame metadata is available.

### `src/predict.py`
- load exported model,
- predict occupied / vacant,
- return confidence / probabilities.

### `app.py`
- local demo,
- visualize input,
- draw slot overlays,
- display occupancy counts.

---

## 14. Training Reproducibility

Record:
- dataset source,
- verified counts,
- split strategy,
- seed,
- architecture,
- image size,
- augmentation,
- optimizer,
- learning rate,
- epochs,
- class balance,
- metrics.

Never invent results.

---

## 15. Model Selection

Initial baseline may use:

```text
EfficientNet-B0
```

or:

```text
MobileNetV3
```

Choose based on task fit, training cost, inference speed, and deployment direction.

---

## 16. External Validation

Before claiming robust performance, test another camera view, another day, different lighting, shadows, rain, partial occlusion, large vehicles, unusual slot markings, and vehicles crossing but not parking.

Document failures too.

---

## 17. Temporal Rule

A single-frame result is only a frame-level prediction.

Future video systems should use:

```text
multiple consecutive frames
→ temporal smoothing
→ stable occupancy state
```

---

## 18. UI Rules

The demo should show:
- uploaded frame,
- predicted slot states,
- confidence,
- occupancy counts.

Prefer wording such as:

```text
Estimated occupied slots
Estimated vacant slots
```

until real-world validation is stronger.

---

## 19. Git Rules

Do not commit raw PKLot data, Kaggle credentials, local environments, caches, large temporary slot crops, or unrelated model weights.

If a final model is intentionally committed, unignore only that exact file.

---

## 20. Engineering Rules

Before modifying code:

1. Read `README.md`.
2. Read `AGENTS.md`.
3. Inspect current assumptions.
4. Inspect working code.
5. Preserve working behavior unless a change is requested.
6. Make the smallest valid change.
7. Test the affected path.
8. Update documentation if behavior changes.

Avoid unrelated refactors.

---

## 21. Source-of-Truth Priority

When information conflicts:

```text
1. verified runtime behavior
2. verified dataset structure
3. evaluation reports
4. current source code
5. README.md
6. AGENTS.md
7. old assumptions
```

---

## 22. Roadmap Discipline

Expected evolution:

```text
v0.1 static image occupancy
v0.2 external validation
v0.3 video input
v0.4 temporal smoothing
v0.5 multi-camera support
v0.6 parking-layout management
v0.7 operator dashboard
v0.8 real-time stream
v0.9 edge deployment
v1.0 integrated smart-parking monitoring
```

Do not overclaim unimplemented capabilities.

---

## 23. Current Status

Verified:

```text
✅ repository initialized
✅ project structure created
✅ README / AGENTS foundation
```

Not yet verified:

```text
❌ PKLot structure
❌ slot annotation parser
❌ crop preparation
❌ model training
❌ evaluation
❌ full-frame reconstruction
❌ Streamlit occupancy demo
```

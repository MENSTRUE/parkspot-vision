# 🚗 ParkSpot Vision

ParkSpot Vision is a Computer Vision MVP for parking-slot occupancy monitoring from fixed-camera images.

The goal is to answer:

> **Which parking slots are occupied, which are vacant, and how many spaces are still available?**

The current version is intentionally scoped as a **slot occupancy analysis system**, not yet a full real-time smart-parking platform.

---

## 🎯 Problem

Drivers waste time searching for empty parking spaces, while parking operators need a more structured way to monitor occupancy from fixed cameras.

ParkSpot Vision explores a Computer Vision workflow that can:

- identify parking-slot regions,
- classify each slot as **OCCUPIED** or **VACANT**,
- count available and occupied slots,
- visualize occupancy on the original parking image,
- support operator verification.

---

## 👥 Target Users

### Primary
- parking operators
- mall / office / campus parking managers
- smart-city parking operators

### Secondary
- drivers
- facility managers
- mobility platforms

---

## 🧠 Current MVP Direction

```text
Fixed Parking Camera Image
        ↓
Parking Slot ROI / Polygon Map
        ↓
Crop Each Slot
        ↓
Occupancy Classifier
        ↓
OCCUPIED / VACANT
        ↓
Reconstruct Predictions on Full Image
        ↓
Occupied Count / Vacant Count
```

Expected MVP output:

- slot annotations,
- occupancy status per slot,
- available-slot count,
- occupied-slot count,
- occupancy percentage,
- per-slot confidence where available.

---

## 🧪 Dataset

Planned baseline dataset:

```text
PKLot
```

PKLot is selected because it fits fixed-camera parking occupancy analysis and includes parking-space annotations with occupancy labels.

The verified dataset path, exact counts, annotation format, and split strategy will be documented after inspection.

---

## 🧩 Modeling Strategy

Primary baseline:

```text
Parking slot polygon
→ crop slot image
→ EfficientNet-B0 / MobileNetV3
→ OCCUPIED / VACANT
```

Optional comparison baseline:

```text
Vehicle detector
→ ROI overlap / geometry rule
→ occupied-slot assignment
```

The product question is:

> “Is this parking slot occupied?”

not simply:

> “How many cars are visible?”

---

## 📊 Evaluation Plan

Planned evaluation:

```text
Per-slot Accuracy
Occupied Precision / Recall / F1
Vacant Precision / Recall / F1
Macro F1
Frame-level count error
Inference time
```

Frame-level count error matters because the product ultimately reports parking availability.

---

## ⚠️ Data Leakage Rule

Fixed-camera datasets can contain many near-identical consecutive frames.

Therefore:

```text
random crop-level splitting is risky
```

Preferred split unit:

```text
camera / day / sequence
```

This reduces train/validation/test leakage.

---

## 🧑‍💼 Human-in-the-Loop

Product principle:

```text
AI assists occupancy monitoring.
Human/operator defines and verifies operational rules.
```

AI may:
- classify slot occupancy,
- count available slots,
- flag uncertain slots.

Human/operator remains responsible for:
- parking-layout definition,
- camera setup,
- ROI validation,
- reviewing uncertain predictions,
- operational decisions.

---

## 🚧 Current Scope

Planned v0.1:

```text
✅ fixed-camera parking image
✅ parking-slot ROI / polygon
✅ slot occupancy classification
✅ occupied / vacant count
✅ annotated output
```

Not yet supported:

```text
❌ live CCTV stream
❌ multi-camera fusion
❌ license-plate recognition
❌ reservation
❌ payment integration
❌ navigation to a slot
❌ production dashboard
```

---

## 🔮 Product Roadmap

```text
v0.1  Static Image Slot Occupancy
v0.2  External Validation
v0.3  Video Input
v0.4  Temporal Occupancy Smoothing
v0.5  Multi-Camera Support
v0.6  Parking Layout Management
v0.7  Operator Dashboard
v0.8  Real-Time Camera Stream
v0.9  Edge Deployment
v1.0  Integrated Smart Parking Monitoring
```

Future pipeline:

```text
Fixed Camera / CCTV
        ↓
Video Stream
        ↓
Frame Sampling
        ↓
Slot Occupancy Analysis
        ↓
Temporal Smoothing
        ↓
Parking Availability Database
        ↓
Operator Dashboard
        ↓
Driver Information Layer
```

---

## 📂 Project Structure

```text
parkspot-vision/
├── assets/
├── data/
│   └── README.md
├── models/
│   └── README.md
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

## 🛠 Planned Development Flow

```text
inspect PKLot
→ understand annotation format
→ visualize slot polygons
→ create occupied / vacant crops
→ split without leakage
→ train classifier
→ evaluate
→ reconstruct predictions
→ build Streamlit demo
```

---

## 📌 Product Lesson — Delegate

For this iteration:

```text
AI:
- occupancy classification
- available-slot counting
- uncertainty indication

Human / system:
- parking-layout definition
- camera setup
- ROI validation
- operational decision
```

---

## 📈 Progress

```text
3% — ParkSpot Vision
```

The percentage represents personal growth and learning progress, not a project count.

---

## 👨‍💻 Author

**Wafa Bila Syaefurokhman**

GitHub: `@MENSTRUE`

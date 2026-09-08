# Raspberry Pi YOLO Object Detection 🎯

Real-time computer vision pipeline running edge inference on a Raspberry Pi using Picamera2 and Ultralytics YOLO, with automated Discord webhook notifications.

---

### ⚙️ Features

- **Edge Inference:** Lightweight YOLO model optimized for Raspberry Pi hardware.
- **Camera Integration:** Hardware-accelerated frame capture via `picamera2` and OpenCV.
- **Alert System:** Automated HTTP payload delivery to Discord webhooks upon target detection.

---

### 📦 Prerequisites

```bash
pip install ultralytics opencv-python requests

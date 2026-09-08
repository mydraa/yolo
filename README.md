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
```

*(Ensure `picamera2` is installed via your Raspberry Pi OS package manager or virtual environment).*

---

### 🚀 Setup & Usage

1. Clone the repository:
```bash
git clone https://github.com/mydraa/yolo.git
cd yolo
```

2. Configure your webhook URL in `yolo_project.py`:
```python
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"
```

3. Run the detection script:
```bash
python yolo_project.py
``` 
 

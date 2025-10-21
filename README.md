# VolumeChangerCV

Hand‑gesture volume control for Windows using OpenCV, MediaPipe Hands, and pycaw.

## What It Does
- Tracks your hand and measures the thumb–index distance.
- Normalizes by hand width so moving closer/farther from the camera doesn’t affect volume.
- Maps “fingers touching → fully stretched” to 0–100% system volume.

## Requirements
- Windows 10/11 (pycaw is Windows‑only)
- Python 3.10+
- Webcam

## Setup
1. (Recommended) Create and activate a virtual environment.
2. Install dependencies:
   - `pip install opencv-python mediapipe numpy pycaw comtypes`

## Run
- From the repo root:
  - `python src/VolumeChanger.py`

## Controls & Calibration
- Pinch distance controls volume. A vertical bar shows the current level.
- Tune the gesture range in `src/VolumeChanger.py`:
  - `TOUCH_NORM`: normalized distance when fingers touch (start of range)
  - `STRETCH_NORM`: normalized distance when fully stretched (end of range)

## Notes
- Hand tracker is a minimal wrapper (`handDetector`) with `findHands` and `findPosition` (in `src/HandTrackerModule.py`).
- For higher FPS: keep 640×480, disable extra drawing, and prefer `CAP_DSHOW` on Windows.

## Troubleshooting
- Import/COM errors: `pip install comtypes` and ensure 64‑bit Python.
- No camera: close other apps using the webcam.
- Volume changes too sensitive: increase `TOUCH_NORM` or `STRETCH_NORM` for a wider range.

import cv2 as cv
import numpy as np
import mediapipe as mp
import time
import math
from HandTrackerModule import HandTracker
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

device = AudioUtilities.GetSpeakers()
interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Scale-invariant mapping: tune these so touching = 0%, fully stretched = 100%
TOUCH_NORM = 0.25   # normalized distance when fingers touch
STRETCH_NORM = 1.05 # normalized distance when fully stretched
# print(f"Audio output: {device.FriendlyName}")
# print(f"- Muted: {bool(volume.GetMute())}")
# print(f"- Volume level: {volume.GetMasterVolumeLevel()} dB")
# print(f"- Volume range: {volume.GetVolumeRange()[0]} dB - {volume.GetVolumeRange()[1]} dB")
# volume.SetMasterVolumeLevel(-20.0, None)

vol = 0
volBar = 400
volPer = 0
tracker = HandTracker(detectionCon=0.6)
video = cv.VideoCapture(0)
video.set(cv.CAP_PROP_FRAME_WIDTH, 640)
video.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
cTime, pTime = 0, 0
while True:
    success, img = video.read()
    if not success:
        break
    tracker.findHands(img, draw=False)
    lmList = tracker.findPosition(img, draw=False)
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv.circle(img, (x1, y1), 15, (0, 0, 255), cv.FILLED)
        cv.circle(img, (x2, y2), 15, (0, 0, 255), cv.FILLED)
        cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

        length = math.hypot(x2 - x1, y2 - y1)
        ref = math.hypot(lmList[17][1] - lmList[5][1], lmList[17][2] - lmList[5][2])
        norm = length / max(ref, 1e-6)
        norm_clamped = np.clip(norm, TOUCH_NORM, STRETCH_NORM)

        # Use scalar volume for smoother 0.0–1.0 control
        scalar = np.interp(norm_clamped, [TOUCH_NORM, STRETCH_NORM], [0.0, 1.0])
        volBar = np.interp(norm_clamped, [TOUCH_NORM, STRETCH_NORM], [400, 150])
        volPer = np.interp(norm_clamped, [TOUCH_NORM, STRETCH_NORM], [0, 100])
        volume.SetMasterVolumeLevelScalar(float(scalar), None)

    cv.rectangle(img, (50, 150), (85, 400), (0, 0, 255), 3)
    cv.rectangle(img, (50, int(volBar)), (85, 400), (0, 0, 255), cv.FILLED)
    cv.putText(img, f'{str(int(volPer))} %',  (40, 450), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
    cTime = time.time()
    fps = (1 / (cTime - pTime))
    pTime = cTime
    cv.putText(img, str(fps), (10,70), cv.FONT_HERSHEY_COMPLEX, 3, (255, 255, 0), 3)
    cv.imshow('Video', img)
    cv.waitKey(1)

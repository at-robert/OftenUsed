import cv2
import numpy as np
import os
from datetime import timedelta

# === 參數設定 ===
VIDEO_PATH = "test.mp4"   # 影片路徑，如果要用攝影機請改成 0
OUTPUT_DIR = "black_frames"
BRIGHTNESS_THRESHOLD = 30     # 全黑判斷亮度門檻
MIN_BLACK_PIXELS_RATIO = 0.90 # 黑色比例 >90% 判斷為黑屏
BRIGHTNESS_DROP_RATIO = 0.5   # 亮度驟降比例 (50%)

os.makedirs(OUTPUT_DIR, exist_ok=True)

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print("無法開啟影片或攝影機")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) if VIDEO_PATH != 0 else None
print(f"FPS: {fps}, 總幀數: {frame_count}")

frame_index = 0
prev_avg_brightness = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 計算影片時間
    video_time = frame_index / fps
    time_str = str(timedelta(seconds=int(video_time)))

    # 轉灰階
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # === 1. 全黑檢測 ===
    black_pixels = np.sum(gray < BRIGHTNESS_THRESHOLD)
    total_pixels = gray.size
    black_ratio = black_pixels / total_pixels
    is_black = black_ratio > MIN_BLACK_PIXELS_RATIO

    # === 2. 亮度驟降檢測 ===
    avg_brightness = np.mean(gray)
    is_brightness_drop = False
    if prev_avg_brightness is not None and prev_avg_brightness > 0:
        drop_ratio = avg_brightness / prev_avg_brightness
        if drop_ratio < BRIGHTNESS_DROP_RATIO:
            is_brightness_drop = True
    prev_avg_brightness = avg_brightness

    # === 紀錄異常畫面 ===
    if is_black or is_brightness_drop:
        event_type = "black" if is_black else "drop"
        filename = f"{OUTPUT_DIR}/{event_type}_{time_str.replace(':', '-')}.jpg"
        cv2.imwrite(filename, frame)
        print(f"發現異常 ({event_type}): {time_str}, 已存檔: {filename}")

    frame_index += 1

cap.release()
print("檢測完成")

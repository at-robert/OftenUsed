import cv2
import numpy as np
import os
import time

# ======= 參數設定 =======
BRIGHTNESS_THRESHOLD = 30     # 全黑判斷亮度門檻
MIN_BLACK_PIXELS_RATIO = 0.90 # 黑色比例 >90% 判斷為黑屏
BRIGHTNESS_DROP_RATIO = 0.5   # 亮度驟降比例 (50%)
OUTPUT_DIR = "detected_frames"  # 儲存抓到黑畫面的資料夾
# =======================

os.makedirs(OUTPUT_DIR, exist_ok=True)

def is_black_frame(frame, prev_brightness=None):
    """判斷是否為黑畫面或亮度驟降"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray)

    # 計算黑色比例
    black_pixels_ratio = np.sum(gray < BRIGHTNESS_THRESHOLD) / gray.size

    # 判斷全黑
    if avg_brightness < BRIGHTNESS_THRESHOLD and black_pixels_ratio > MIN_BLACK_PIXELS_RATIO:
        return True, avg_brightness

    # 判斷亮度驟降
    if prev_brightness is not None:
        if avg_brightness < prev_brightness * BRIGHTNESS_DROP_RATIO:
            return True, avg_brightness

    return False, avg_brightness


def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"無法開啟影片: {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    prev_brightness = None
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        is_black, current_brightness = is_black_frame(frame, prev_brightness)
        prev_brightness = current_brightness
        frame_count += 1

        if is_black:
            timestamp_sec = frame_count / fps
            timestamp_str = time.strftime("%H-%M-%S", time.gmtime(timestamp_sec))
            filename = os.path.join(OUTPUT_DIR, f"black_{timestamp_str}.jpg")
            cv2.imwrite(filename, frame)
            print(f"偵測到黑畫面: {filename}")

    cap.release()
    print("分析完成")


def preview_camera_and_capture():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("無法開啟攝影機")
        return

    print("按 's' 開始錄影檢測黑畫面，按 'q' 離開")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Camera Preview", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            break
        elif key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return

    print("開始檢測黑畫面...")
    prev_brightness = None
    frame_count = 0
    fps = cap.get(cv2.CAP_PROP_FPS) or 30  # 有些攝影機不回傳 FPS，預設 30

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        is_black, current_brightness = is_black_frame(frame, prev_brightness)
        prev_brightness = current_brightness
        frame_count += 1

        if is_black:
            timestamp_sec = frame_count / fps
            timestamp_str = time.strftime("%H-%M-%S", time.gmtime(timestamp_sec))
            filename = os.path.join(OUTPUT_DIR, f"black_{timestamp_str}.jpg")
            cv2.imwrite(filename, frame)
            print(f"偵測到黑畫面: {filename}")

        cv2.imshow("Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    path = input("輸入影片路徑 (留空使用攝影機): ").strip()
    if path:
        process_video(path)
    else:
        preview_camera_and_capture()

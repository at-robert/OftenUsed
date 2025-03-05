import cv2
import os
import sys

def extract_frames(video_path, output_folder, frame_interval=30, start_time=0):
    # 確保輸出資料夾存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 讀取影片
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: 無法開啟影片檔案！")
        return
    
    # 設定開始時間（秒數）
    cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)
    
    frame_count = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    image_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # 影片結束
        
        if frame_count % frame_interval == 0:
            image_path = os.path.join(output_folder, f"frame_{image_count:04d}.jpg")
            cv2.imwrite(image_path, frame)
            # print(f"已保存: {image_path}")
            image_count += 1
        
        frame_count += 1
        
        # 顯示進度
        progress = (frame_count / total_frames) * 100
        print(f"處理進度: {progress:.2f}%")
    
    cap.release()
    print("影格擷取完成！")

# 使用範例
pwd = os.path.expanduser('~') + '/'
filedir = pwd + 'Downloads/'
# video_file = "Fire Salamander LEGO 31129 Digital Build.mp4"  # 影片檔案路徑
video_file = sys.argv[1]
output_directory = "output_frames"  # 存放圖片的資料夾
frame_interval = 45  # 每 30 個影格擷取一張
start_time = 180  # 從 10 秒開始擷取

extract_frames(filedir + video_file, filedir + output_directory, frame_interval, start_time)
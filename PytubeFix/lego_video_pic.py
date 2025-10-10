import cv2
import sys
import os
from pytubefix import YouTube
from pytubefix.cli import on_progress


def extract_frames(video_path, output_folder, frame_interval=30, start_time=0, end_time=None):
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

    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # 計算結束影格數
    end_frame = total_frames if end_time is None else int(end_time * fps)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # 影片結束

        if frame_count >= end_frame:
            break  # 達到結束時間
        
        if frame_count % frame_interval == 0:
            image_path = os.path.join(output_folder, f"frame_{image_count:04d}.png")
            cv2.imwrite(image_path, frame)
            # print(f"已保存: {image_path}")
            image_count += 1
        
        frame_count += 1
        
        # 顯示進度
        progress = (frame_count / total_frames) * 100
        print(f"處理進度: {progress:.2f}%")
    
    cap.release()
    print("影格擷取完成！")

pwd = os.path.expanduser('~') + '/'
filedir = pwd + 'Downloads/'

# Get the YouTube video URL from command-line arguments
youtube_url = sys.argv[1]

url = youtube_url

yt = YouTube(url, on_progress_callback=on_progress)
print(yt.title)

# ys = yt.streams.get_highest_resolution()
# ys.download(output_path=filedir)

res_str = None
# 列出可用的串流
for stream in yt.streams:
    if(stream.resolution == "720p" or stream.resolution == "1080p"):
        res_str = stream.resolution
    print(stream.resolution)
    if stream.resolution == "1080p":
        break


if res_str != None:
    filename_ = yt.streams.filter(res=res_str).first().download(output_path=filedir)
    print(" Output file Name = {}".format(filename_))

    output_directory = "output_frames"  # 存放圖片的資料夾

    # frame_interval = 45  # 每 30 個影格擷取一張
    # start_time = 205  # 從 10 秒開始擷取
    # end_time = 860 # 結束時間
    frame_interval = int(sys.argv[2])
    start_time = int(sys.argv[3])
    end_time = int(sys.argv[4])
    
    extract_frames(filename_, filedir + output_directory, frame_interval, start_time, end_time)
else:
    print("There is No HD or FHD video")
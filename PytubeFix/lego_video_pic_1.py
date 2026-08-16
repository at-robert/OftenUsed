import cv2
import sys
import os
import yt_dlp

def parse_time(time_str):
    """支援輸入 秒數(例如 '145') 或 時間格式(例如 '2:25' 或 '1:02:25') 並轉換為總秒數"""
    if ':' in str(time_str):
        parts = list(map(int, time_str.split(':')))
        if len(parts) == 2:    # 分:秒
            return parts[0] * 60 + parts[1]
        elif len(parts) == 3:  # 時:分:秒
            return parts[0] * 3600 + parts[1] * 60 + parts[2]
    return int(time_str)

def extract_frames(video_path, output_folder, frame_interval=30, start_time=0, end_time=None):
    os.makedirs(output_folder, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: 無法開啟影片檔案！")
        return
    
    cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)
    
    frame_count = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    image_count = 0

    fps = cap.get(cv2.CAP_PROP_FPS)
    end_frame = total_frames if end_time is None else int(end_time * fps)
    
    while True:
        ret, frame = cap.read()
        if not ret or frame_count >= end_frame:
            break
        
        if frame_count % frame_interval == 0:
            image_path = os.path.join(output_folder, f"frame_{image_count:04d}.png")
            cv2.imwrite(image_path, frame)
            image_count += 1
        
        frame_count += 1
        
        progress = (frame_count / total_frames) * 100
        print(f"處理進度: {progress:.2f}%", end="\r")
    
    cap.release()
    print("\n影格擷取完成！")

pwd = os.path.expanduser('~') + '/'
filedir = pwd + 'Downloads/'

youtube_url = sys.argv[1]
frame_interval = int(sys.argv[2])
start_time = parse_time(sys.argv[3])  # 自動支援 2:25 或 145
end_time = parse_time(sys.argv[4])    # 自動支援 16:45 或 1005

output_directory = "output_frames"

# 使用 yt-dlp 下載 1080p 影片（若無則自動尋找最佳畫質）
ydl_opts = {
    'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'outtmpl': os.path.join(filedir, '%(title)s.%(ext)s'),
    'merge_output_format': 'mp4',
    'quiet': False
}

print("正在使用 yt-dlp 下載影片...")
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(youtube_url, download=True)
    filename_ = ydl.prepare_filename(info_dict)
    print(f"\n影片下載成功: {filename_}")

# 開始擷取影格
extract_frames(filename_, os.path.join(filedir, output_directory), frame_interval, start_time, end_time)
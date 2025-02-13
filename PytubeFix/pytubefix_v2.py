import os
from pytubefix import YouTube

def download_youtube_video(url, resolution="highest", save_path="./"):
    try:
        # 建立 YouTube 物件
        yt = YouTube(url)
        
        # 根據使用者指定的解析度選擇影片
        if resolution == "highest":
            stream = yt.streams.get_highest_resolution()
        else:
            stream = yt.streams.filter(res=resolution, progressive=True).first()
            if not stream:
                print(f"找不到解析度為 {resolution} 的影片，將下載最高解析度。")
                stream = yt.streams.get_highest_resolution()
        
        print(f"正在下載: {yt.title} ({stream.resolution})")
        
        # 下載影片
        stream.download(output_path=save_path)
        
        print("下載完成！")
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    pwd = os.path.expanduser('~') + '/'
    filedir = pwd + 'Downloads'

    video_url = input("請輸入 YouTube 影片網址: ")
    resolution = input("請輸入解析度 (例如 720p, 1080p，或輸入 'highest' 下載最高畫質): ")
    download_youtube_video(video_url, resolution, filedir)
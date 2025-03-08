import sys
import os
from pytubefix import YouTube
from pytubefix.cli import on_progress


pwd = os.path.expanduser('~') + '/'
filedir = pwd + 'Downloads'

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
    yt.streams.filter(res=res_str).first().download(output_path=filedir)
else:
    print("There is No HD or FHD video")
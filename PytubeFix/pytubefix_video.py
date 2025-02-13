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

yt.streams.filter(res="1080p").first().download(output_path=filedir)
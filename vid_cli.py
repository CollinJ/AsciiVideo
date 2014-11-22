from app_lib import Run
from sys import argv
from audio import PlayStream
from time import time
import livestreamer

uri = argv[1]

streams = livestreamer.streams(uri)
audio_streams = [i for i in streams if "audio" in i]
if len(audio_streams) > 0:
    audio_url = streams[audio_streams[-1]].url
else:
    print "No audio stream found."
video_url = streams['best'].url

start = int(time()*1000)
if len(audio_streams) > 0:
    PlayStream(audio_url)
Run(video_url,start)

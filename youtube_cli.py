from app_lib import Run
from sys import argv
from audio import PlayStream
import pafy

vid = pafy.new(argv[1])
vid_url = vid.getbest().url
audio_url = vid.getbestaudio().url
audio_length = vid.length

PlayStream(audio_url,audio_length)
Run(vid_url)

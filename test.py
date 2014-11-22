import pygst
pygst.require("0.10")
import gst
import pygtk
import gtk
import pafy
import threading
import gobject
from multiprocessing import Process
from time import sleep

video_url = 'https://www.youtube.com/watch?v=2H58iuBY4ys'
stream_url = pafy.new(video_url).getbestaudio().url

class _player:
    def __init__(self,url):
        self.src = gst.element_factory_make('playbin2')
        self.src.set_property('uri', url)
        self.src.set_state(gst.STATE_PLAYING)

def stream_audio_thread(uri):
    start=_player(uri)
    gtk.main()

def StreamAudio(uri):
    return Process(target = lambda:stream_audio_thread(uri)).start()

print "Streaming."
StreamAudio(stream_url)
print "Sleeping."
sleep(10)
print "Dying."

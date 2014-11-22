import pygst
pygst.require("0.10")
import gst
import pygtk
import gtk
import pafy
import threading
import gobject
import glib
from multiprocessing import Process
from time import sleep

def _play_stream(uri, stream_length):
    def start(*args):
        src = gst.element_factory_make('playbin2')
        src.set_property('uri', uri)
        src.set_state(gst.STATE_PLAYING)
        return False
    def die(*args):
        exit()
    gobject.timeout_add(0, start)
    if stream_length > 0:
        gobject.timeout_add(1000 * (stream_length+1), die)
    loop = glib.MainLoop()
    loop.run()

def PlayStream(uri, stream_length = -1):
    p = Process(target=lambda:_play_stream(uri, stream_length))
    p.start()
    return p

if __name__ == '__main__':
    video_url = 'https://www.youtube.com/watch?v=vuy9EpLdiqw'
    vid_data = pafy.new(video_url)
    stream_url = vid_data.getbestaudio().url
    stream_length = vid_data.length
    PlayStream(stream_url, stream_length)
    print "sleeping"
    sleep(10)
    print "done"

import pafy
import curses
import numpy as np
import cv2
import cv2.cv as cv
from time import sleep, time
from optparse import OptionParser
from audio import PlayStream
from sys import argv


def configure(filename):
  def main(stdscr):
    init(stdscr)
    drawVideo(filename, stdscr)
    stdscr.getch()
  return main

def drawImage(img, stdscr):
  maxY, maxX = stdscr.getmaxyx()
  maxY -= 1
  maxX -= 1
  height = len(img)
  width = len(img[0])
  for y in xrange(height):
    for x in xrange(width):
      if x >= maxX or y >= maxY:
        continue
      rgb = img[y][x]
      stdscr.addstr(y,x,str(" "), curses.color_pair(RGBtoColor(rgb)))
  stdscr.refresh()

def drawVideo(file, stdscr):
  if file.isdigit():
    file = int(file)
  cap = cv2.VideoCapture(file)
  pixel_width = int(cap.get(cv.CV_CAP_PROP_FRAME_WIDTH))
  pixel_height = int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
  max_height, max_width = stdscr.getmaxyx()
  max_height -= 3
  max_width -= 3
  
  width = min(pixel_width, max_width)
  height = int(pixel_height*width/2/pixel_width)

    

  char_pixel_width = int(pixel_width/(1.0*width))
  char_pixel_height = int(pixel_height/(1.0*height))

  nframes=int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
  fps= int(cap.get(cv.CV_CAP_PROP_FPS))
  if fps == 0:
    exit()
  milliesconds_per_frame=int(1000.0/fps)

  zoom = .08
  x = 0
  y = 0
  dx = 10
  dy = 5

  sleep_debt = 0

  oldstart, start, end = None, None, None

  while(True):
    oldstart, start = start, int(time()*1000)

    ret, frameimg=cap.read()
    if not ret:
      break
    frameimg = cv2.resize(frameimg,(int(pixel_width*2*zoom), int(pixel_height*zoom)))
    
    w = width
    h = height
    max_y, max_x = stdscr.getmaxyx()
    frameimg = frameimg[y:y+h, x:x+w*2]
    drawImage(frameimg, stdscr)

    h,w,_ = np.shape(frameimg)
    cv2.waitKey(1)
    c = stdscr.getch()
    if c == ord('+'):
      zoom *= 1.1
    elif c == ord ('-') and w > max_x:
      zoom /= 1.1
      stdscr.clear()
    elif c == curses.KEY_RIGHT:
      x = x + dx if w > max_x else x-(max_x-w)
    elif c == curses.KEY_LEFT:
      x = x-dx if x-dx > 0 else 0
    elif c == curses.KEY_DOWN:
      y = y+dy if h >= max_y else y
    elif c == curses.KEY_UP:
      y = y-dy if y-dy > 0 else 0
    elif c == ord('q'):
      debug(stdscr)
      exit()
    if w < max_x and x > 0:
      x = x - dx
    if h < max_y and y > 0:
      y = y - dy

    if end:
        sleep_time = (milliesconds_per_frame-(end-oldstart))/1000.0
        if sleep_time > 0:
            if sleep_time <= sleep_debt:
                sleep_debt -= sleep_time
            else:
                sleep(sleep_time - sleep_debt)
                sleep_debt = 0
        else:
            sleep_debt -= sleep_time
    end = int(time()*1000)

  cap.release()
  cv2.destroyAllWindows()


def RGBtoColor(rgb):
  r = int(rgb[2])
  g = int(rgb[1])
  b = int(rgb[0])
  if curses.COLORS == 256:
    i = ((r/32) << 5 |
           ((g/32) << 2) |
           ((b/64)))
    if i == 255:
      return 0
    if i == 0:
      return 255
    return i
  else: 
    return ((r/128)<<2 |
            (g/128)<<1 |
            (b/128)<<0)

def init(stdscr):
  curses.noecho()
  curses.cbreak()
  stdscr.keypad(1)
  stdscr.nodelay(1)
  curses.curs_set(0)
  curses.start_color()
  curses.use_default_colors()
  if curses.COLORS == 256:
    for i in range(0,curses.COLORS):
      r = (i >> 5) & 7
      g = (i >> 2) & 7
      b = (i) & 3
      curses.init_color(i, r*142, g*142, int(b*333.334))
    curses.init_color(curses.COLORS-1, 0,0,0)
    for i in range(0, curses.COLORS):
      curses.init_pair(i, 0, i)
  else:
    for i in range(0,curses.COLORS):
      r = (i >> 2) & 1
      g = (i >> 1) & 1
      b = (i) & 1
      curses.init_color(i, r*1000, g*1000, b*1000)
    curses.init_color(curses.COLORS-1, 1000,1000,1000)
    for i in range(0, curses.COLORS):
      curses.init_pair(i, 0, i)

def debug(stdscr):
  curses.nocbreak()
  stdscr.keypad(0)
  curses.echo()
  curses.endwin()

def Run(filename):
    curses.wrapper(configure(filename))

if __name__ == '__main__':
    Run(argv[1])

#!/usr/bin/python
import curses
import numpy as np
import cv2
import cv2.cv as cv
from time import sleep

def main(stdscr):
  init(stdscr)
  drawVideo("test.mp4", stdscr)
  stdscr.getch()

def drawImage(img, stdscr):
  maxY, maxX = stdscr.getmaxyx()
  maxY -= 20
  maxX -= 20
  height = len(img)
  width = len(img[0])
  for y in xrange(height):
    for x in xrange(width):
      if x >= maxX or y >= maxY:
        continue
      rgb = img[y][x]
      stdscr.addstr(y,x,str(" "), curses.color_pair(RGBto256Color(rgb)))
  stdscr.refresh()

def drawVideo(file, stdscr):
  cap = cv2.VideoCapture(file)
  pixel_width = int(cap.get(cv.CV_CAP_PROP_FRAME_WIDTH))
  pixel_height = int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
  max_height, max_width = stdscr.getmaxyx()
  max_height -= 3
  max_width -= 3
  
  width = min(pixel_width, max_width)
  height = int(width/2)
  if (height > max_height):
    height = max_height
    width = height*2

    

  char_pixel_width = int(pixel_width/(1.0*width))
  char_pixel_height = int(pixel_height/(1.0*height))

  nframes=int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
  fps= int(cap.get(cv.CV_CAP_PROP_FPS))
  print "total frame",cap.get(cv.CV_CAP_PROP_FRAME_COUNT)
  print "fps" ,fps
  print " currpos of videofile",cap.get(cv.CV_CAP_PROP_POS_MSEC)
  waitpermillisecond=int(1*1000/fps)
  print "waitpermillisecond",waitpermillisecond
  print cap.get(cv.CV_CAP_PROP_FOURCC)

  while(cap.isOpened()):
    ret, frameimg=cap.read()
    if not ret:
      break
    sleep(waitpermillisecond/1000.0)
    print " currpos of videofile",cap.get(cv.CV_CAP_PROP_POS_MSEC)
    print " index of frame",cap.get(cv.CV_CAP_PROP_POS_FRAMES)
    drawImage(cv2.resize(frameimg,(width, height)), stdscr)
    cv2.waitKey(1)

  cap.release()
  cv2.destroyAllWindows()


def RGBto256Color(rgb):
  r = int(rgb[2])
  g = int(rgb[1])
  b = int(rgb[0])
  i = ((r/32) << 5 |
         ((g/32) << 2) |
         ((b/64)))
  if i == 255:
    return 0
  if i == 0:
    return 255
  return i

def init(stdscr):
  curses.noecho()
  curses.cbreak()
  stdscr.keypad(1)
  curses.curs_set(0)
  curses.start_color()
  curses.use_default_colors()
  for i in range(0,256):
    r = (i >> 5) & 7
    g = (i >> 2) & 7
    b = (i) & 3
    curses.init_color(i, r*142, g*142, int(b*333.334))
  curses.init_color(255, 0,0,0)
  for i in range(0, 256):
    curses.init_pair(i, -1, i)

curses.wrapper(main)

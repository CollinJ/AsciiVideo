#!/usr/bin/python
import curses
import numpy as np
import cv2
import cv2.cv as cv
from time import sleep
from optparse import OptionParser

import features

parser = OptionParser()
parser.add_option("-f", "--file", dest="file", help="file to convert to ascii")
(options, args) = parser.parse_args()

def main(stdscr):
  init(stdscr)
  drawVideo(options.file, stdscr)
  stdscr.getch()

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
      stdscr.addstr(y,x,str(" "), curses.color_pair(RGBto256Color(rgb)))
  stdscr.refresh()

def drawVideo(file, stdscr):
  cap = cv2.VideoCapture('http://r4---sn-o097zne7.googlevideo.com/videoplayback?source=youtube&upn=YzYrUiQtB0g&signature=A98AFA572C9D34E4EE30EBC9E3AECC17DD19A505.AF16232C224A7BCEE7E2DE4E13E76FD0E6A758D5&key=yt5&initcwndbps=3925000&ratebypass=yes&fexp=902411%2C907259%2C914066%2C922246%2C923347%2C927622%2C932404%2C941004%2C941561%2C943909%2C947209%2C947215%2C948124%2C952302%2C952605%2C952901%2C953912%2C957103%2C957105%2C957201%2C960000&itag=22&mt=1416644726&mv=m&sparams=id%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Cmm%2Cms%2Cmv%2Cratebypass%2Csource%2Cupn%2Cexpire&ms=au&ip=136.152.36.24&expire=1416666483&ipbits=0&mm=31&id=o-ALZmnoQCpZjKduG2R6Lu_yMZbuhyZT2KAKp74_culphr&sver=3')
  pixel_width = int(cap.get(cv.CV_CAP_PROP_FRAME_WIDTH))
  pixel_height = int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
  max_height, max_width = stdscr.getmaxyx()
  max_height -= 3
  max_width -= 3
  
  width = min(pixel_width, max_width)
  height = int(pixel_height*width/2/pixel_width)
  if (height > max_height):
    height = max_height
    width = pixel_width*height*2/pixel_height

    

  char_pixel_width = int(pixel_width/(1.0*width))
  char_pixel_height = int(pixel_height/(1.0*height))

  """
  nframes=int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
  fps= int(cap.get(cv.CV_CAP_PROP_FPS))
  print "total frame",cap.get(cv.CV_CAP_PROP_FRAME_COUNT)
  print "fps" ,fps
  print " currpos of videofile",cap.get(cv.CV_CAP_PROP_POS_MSEC)
  waitpermillisecond=int(1*1000/fps)
  print "waitpermillisecond",waitpermillisecond
  print cap.get(cv.CV_CAP_PROP_FOURCC)
  """

  while(True):
    ret, frameimg=cap.read()
    if not ret:
      break
    #sleep(waitpermillisecond/1000.0)
    #print " currpos of videofile",cap.get(cv.CV_CAP_PROP_POS_MSEC)
    #print " index of frame",cap.get(cv.CV_CAP_PROP_POS_FRAMES)
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
    curses.init_pair(i, 255, i)

curses.wrapper(main)

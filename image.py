#!/usr/bin/python

import cv2
import numpy as np
import cv2.cv as cv
import sys
from time import sleep
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-w", "--width", dest="width", help="number of characters wide the video should be")
(options, args) = parser.parse_args()


def drawVideo(file, stdscr):
  cap = cv2.VideoCapture(file)
  pixel_width = int(cap.get(cv.CV_CAP_PROP_FRAME_WIDTH))
  pixel_height = int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
  width = pixel_width
  if options.width:
    width = int(options.width)

  height = int(width/2.5)
    

  char_pixel_width = int(pixel_width/(1.0*width))
  char_pixel_height = int(pixel_height/(1.0*height))

  print "Pixels: %sx%s" % (pixel_width, pixel_height)
  print "Chars: %sx%s" % (width, height)
  print "Char: %sx%s" % (char_pixel_width, char_pixel_height)
  exit()

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
    cv2.imshow("hcq",frameimg)
    cv2.waitKey(1)

  cap.release()
  cv2.destroyAllWindows()


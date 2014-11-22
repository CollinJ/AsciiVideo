#!/usr/bin/python
import curses
import numpy as np
import cv2
from time import sleep


def main(stdscr):
  init(stdscr)
  img = cv2.imread('test2.jpg')
  drawImage(img, stdscr)
  stdscr.getch()

def drawImage(img, stdscr):
  maxY, maxX = stdscr.getmaxyx()
  maxY -= 20
  maxX -= 20
  height = len(img)
  width = len(img[0])
  stdscr.clear()
  for y in xrange(height):
    for x in xrange(width):
      if x >= maxX or y >= maxY:
        continue
      rgb = img[y][x]
      stdscr.addstr(y,x,str(" "), curses.color_pair(RGBto256Color(rgb)))
  stdscr.refresh()


def RGBto256Color(rgb):
  r = int(rgb[0])
  g = int(rgb[1])
  b = int(rgb[2])
  return ((r/32) << 5 |
         ((g/32) >> 3) |
         ((b/64)))

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
  for i in range(0, curses.COLORS):
    curses.init_pair(i + 1, -1, i)

curses.wrapper(main)

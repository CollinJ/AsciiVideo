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



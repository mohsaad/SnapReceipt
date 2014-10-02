import os

import win32file
import win32event
import win32con

import subprocess
import dropbox
from transform import four_point_transform
import imutils
from skimage.filter import threshold_adaptive
import numpy as np 
import argparse
import cv2
import datetime
import json
from pywatch import watcher
from os.path import exists

path_to_watch = os.path.abspath ("C:\\Users\\MOHAMMAD\\Dropbox\\reciepts_photos")

#
# FindFirstChangeNotification sets up a handle for watching
#  file changes. The first parameter is the path to be
#  watched; the second is a boolean indicating whether the
#  directories underneath the one specified are to be watched;
#  the third is a list of flags as to what kind of changes to
#  watch for. We're just looking at file additions / deletions.
#
change_handle = win32file.FindFirstChangeNotification (
  path_to_watch,
  0,
  win32con.FILE_NOTIFY_CHANGE_FILE_NAME
)

numAdded = 0
#
# Loop forever, listing any file changes. The WaitFor... will
#  time out every half a second allowing for keyboard interrupts
#  to terminate the loop.
#
try:

  old_path_contents = dict ([(f, None) for f in os.listdir (path_to_watch)])
  while 1:
    result = win32event.WaitForSingleObject (change_handle, 500)

    #
    # If the WaitFor... returned because of a notification (as
    #  opposed to timing out or some error) then look for the
    #  changes in the directory contents.
    #
    # also start subprocess of CV stuff
    if result == win32con.WAIT_OBJECT_0:
      new_path_contents = dict ([(f, None) for f in os.listdir (path_to_watch)])
      added = [f for f in new_path_contents if not f in old_path_contents]
      deleted = [f for f in old_path_contents if not f in new_path_contents]
      if added: 
      	print "Added: ", ", ".join (added)
      	instr = ["C:/Python27/python", "reciept_scanner.py", "--image", "image.jpg"]
      	print "start"
      	instr_process = subprocess.Popen(instr, stderr = subprocess.STDOUT, stdout=subprocess.PIPE)
      	print "end"
      	outputstring = instr_process.communicate()[0]
      if deleted: print "Deleted: ", ", ".join (deleted)

      


      

      old_path_contents = new_path_contents
      win32file.FindNextChangeNotification (change_handle)

finally:
  win32file.FindCloseChangeNotification (change_handle)
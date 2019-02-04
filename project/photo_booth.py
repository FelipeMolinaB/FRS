# USAGE
# python photo_booth.py --output output

# import the necessary packages
from __future__ import print_function
from pyimagesearch.photoboothapp import PhotoBoothApp
from imutils.video import VideoStream
import argparse
import time
import cv2,dlib
import sys

# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-o", "--output", required=True,
# 	help="path to output directory to store snapshots")
# ap.add_argument("-p", "--picamera", type=int, default=-1,
# 	help="whether or not the Raspberry Pi camera should be used")
# args = vars(ap.parse_args())

# initialize the video stream and allow the camera sensor to warmup
# print("[INFO] warming up camera...")
# vs = VideoStream(usePiCamera=args["picamera"] > 0).start()

# vs = cv2.VideoCapture(0)
#
# # Check if OpenCV is able to read feed from camera
# if (vs.isOpened() is False):
# 	print("Unable to connect to camera")
# 	sys.exit()



try:
    cam_n = sys.argv[1]
    time.sleep(2.0)
    pba = PhotoBoothApp(cam_n)
    pba.start_upd_client()
    pba.root.mainloop()
except:
    quit()
    raise SystemExit
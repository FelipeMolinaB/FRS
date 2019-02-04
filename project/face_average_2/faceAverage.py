#!/usr/bin/python
# Copyright 2017 BIG VISION LLC ALL RIGHTS RESERVED
#
# This code is made available to the students of
# the online course titled "Computer Vision for Faces"
# by Satya Mallick for personal non-commercial use.
#
# Sharing this code is strictly prohibited without written
# permission from Big Vision LLC.
#
# For licensing and other inquiries, please email
# spmallick@bigvisionllc.com
#
import os
import sys
import cv2
import dlib
import numpy as np
import faceBlendCommon as fbc
import face_average_utilities as fa_utl
import os, random



if __name__ == '__main__':
  cedula = 1014193765
  fa_utl.generate_fake_dataset(cedula)

  cedula = 1014193765
  fa_utl.generate_true_dataset(cedula)






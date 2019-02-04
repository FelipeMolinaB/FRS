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
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


import cv2,dlib
from renderFace import renderFace
import numpy as np
import time
import gc
from sklearn.externals import joblib
import copy
from PIL import ImageTk
import Tkinter as tki
from server_udp.client import CameraClient, ImageClient
from server_udp import variables
import thread

class CascadeClassifier(object):
    def __init__(self,gruop_clf,specific_clfs):
        self.gruop_clf = gruop_clf
        self.specific_clfs = specific_clfs

    def predict(self, x):
        group = self.gruop_clf.predict(x)
        y = []
        for i,g in enumerate(group):
            y.append(self.specific_clfs["G"+str(g)].predict(x[i].reshape(1, -1))[0])
        return y

class face_detection():
    def __init__(self):
        self.faceDescriptors = ""
        self.personas = []
        rootdir = "/root/openface/demos/web/project/list_persons_availables"
        users_file_path = os.path.join(rootdir, "dict_pers.pkl")
        self.dict_pers = joblib.load(users_file_path)
        self.name = ""
        self.open_door = False
        self.users = {}
        self.show = multiple
        self.camera_client = CameraClient()
        self.image_client = ImageClient()
        self.im = None
        self.start_send_image()
        self.cc = ""
        self.face_area = 0
        self.ratio = 0
        self.send_msg = False
        self.start_request_open_door()

    def video_service(self, cam_n):
        PREDICTOR_PATH = "../../models/shape_predictor_68_face_landmarks.dat"
        RESIZE_HEIGHT = 480
        SKIP_FRAMES = 2

        FACE_RECOGNITION_MODEL_PATH = '/root/openface/demos/web/project/models/dlib_face_recognition_resnet_model_v1.dat'
        # Load face detection and pose estimation models
        faceRecognizer = dlib.face_recognition_model_v1(FACE_RECOGNITION_MODEL_PATH)

        try:
            # Create an imshow window
            winName = "Fast Facial Landmark Detector"

            # Create a VideoCapture object
            cap = cv2.VideoCapture(cam_n)
            #cap = cv2.VideoCapture(0)

            # Check if OpenCV is able to read feed from camera
            if (cap.isOpened() is False):
                print("Unable to connect to camera")
                sys.exit()

            # Just a place holder. Actual value calculated after 100 frames.
            fps = 30.0

            # Get first frame
            ret, im = cap.read()

            # We will use a fixed height image as input to face detector
            if ret == True:
                im_center = np.array((im.shape[1]/2,im.shape[0]/2))
                height = im.shape[0]
                # calculate resize scale
                RESIZE_SCALE = float(height) / RESIZE_HEIGHT
                size = im.shape[0:2]
            else:
                print("Unable to read frame")
                sys.exit()

            # Load face detection and pose estimation models
            detector = dlib.get_frontal_face_detector()
            predictor = dlib.shape_predictor(PREDICTOR_PATH)
            # initiate the tickCounter
            t = cv2.getTickCount()
            count = 0

            rootdir = "/root/openface/demos/web/project/general_svm"
            name_file = "cascade_clf.pkl"
            file_path = os.path.join(rootdir, name_file)
            clf = joblib.load(file_path)

            rootdir = "/root/openface/demos/web/project/logitic_regression_bagging_boosting"
            # Grab and process frames until the main window is closed by the user.
            face_center = np.array((0,0))
            faces = None
            while (True):
                if count == 0:
                    t = cv2.getTickCount()
                # Grab a frame
                ret, im = cap.read()
                # create imSmall by resizing image by resize scale
                imSmall = cv2.resize(im, None, fx=1.0 / RESIZE_SCALE, fy=1.0 / RESIZE_SCALE, interpolation=cv2.INTER_LINEAR)

                # Process frames at an interval of SKIP_FRAMES.
                # This value should be set depending on your system hardware
                # and camera fps.
                # To reduce computations, this value should be increased
                if (count % SKIP_FRAMES == 0):
                    # Detect faces
                    faces = detector(imSmall, 0)

                faceDescriptors = None

                identified_persons = []
                cont_face = 0

                # Iterate over faces
                personas = []
                rects = []
                for face in faces:
                    # Since we ran face detection on a resized image,
                    # we will scale up coordinates of face rectangle
                    newRect = dlib.rectangle(int(face.left() * RESIZE_SCALE),
                                                                     int(face.top() * RESIZE_SCALE),
                                                                     int(face.right() * RESIZE_SCALE),
                                                                     int(face.bottom() * RESIZE_SCALE))
                    rects.append(newRect)

                if multiple:
                    print("The system detects {} people".format(len(rects)))
                    for rect in rects:
                        # Find face landmarks by providing reactangle for each face
                        shape = predictor(im, rect)

                        # It is a 128D vector that describes the face in img identified by shape.
                        # Compute face descriptor using neural network defined in Dlib.
                        faceDescriptor = faceRecognizer.compute_face_descriptor(im, shape)
                        faceDescriptorList = [x for x in faceDescriptor]
                        faceDescriptorNdarray = np.asarray(faceDescriptorList, dtype=np.float64)
                        faceDescriptorNdarray = faceDescriptorNdarray[np.newaxis, :]
                        # Stack face descriptors (1x128) for each face in images, as rows
                        if faceDescriptors is None:
                            faceDescriptors = faceDescriptorNdarray
                        else:
                            faceDescriptors = np.concatenate((faceDescriptors, faceDescriptorNdarray), axis=0)

                else:

                    biggest_rect = None
                    for rect in rects:
                        try:
                            if rect.area() > biggest_rect.area():
                                biggest_rect = rect
                        except AttributeError:
                            biggest_rect = rect

                    if biggest_rect is not None:
                        if biggest_rect.area() >= variables.min_area:
                            face_area = biggest_rect.area()
                            shape = predictor(im, biggest_rect)
                            faceDescriptors = faceRecognizer.compute_face_descriptor(im, shape)
                            faceDescriptors = [x for x in faceDescriptors]
                            faceDescriptors = np.asarray(faceDescriptors, dtype=np.float64)
                            faceDescriptors = faceDescriptors[np.newaxis, :]
                            face_center[0] =  biggest_rect.center().x
                            face_center[1] =  biggest_rect.center().y

                if faceDescriptors is not None:
                    y_pred = clf.predict(faceDescriptors)

                    for cedula in y_pred:
                        person = []
                        person.append(cedula)

                        model_best = joblib.load(os.path.join(rootdir, "logistic_bb_" + str(cedula) + ".pkl"))
                        bagging_1 = model_best[0]
                        y_pred_bagging_1 = bagging_1.predict(faceDescriptors)

                        y_pred_2 = []
                        for i in range(0, len(y_pred_bagging_1)):
                            #if y_pred_bagging_1[i] == 1 and y_pred_bagging_2[i] == 1 and y_pred_binary_svm[i] == 1 :
                            if y_pred_bagging_1[i] == 1: #and y_pred_binary_svm[i] == 1:
                                y_pred_2.append(1)
                            else:
                                y_pred_2.append(0)
                        person.append(y_pred_2)

                        # Draw facial landmarks
                        if self.show:
                            im = renderFace(im, shape)

                        personas.append(person)
                        gc.enable()
                        gc.collect()

                self.personas = personas
                self.name = ""
                users_in_frame = []
                try:
                    UK_detected = False
                    for j in xrange(0, len(self.personas)):
                        #print ("self.personas %s" %self.personas[j])
                        valido = int(self.personas[j][1][j])
                        if valido == 1:
                            cedula = int(self.personas[j][0])
                            name = self.dict_pers[cedula]
                            if not multiple:
                                users_in_frame.append([cedula, name, face_area, face_area/np.linalg.norm(im_center-face_center)])
                            else:
                                users_in_frame.append([cedula, name])
                        else:
                            name = "Desconocido"
                            UK_detected = True
                            if not multiple:
                                self.cc = "UK"
                                self.face_area = face_area
                                self.ratio = face_area/np.linalg.norm(im_center-face_center)
                                self.send_msg = True
                        if multiple:
                            cv2.putText(im, name, (10, 30*(j+1)), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
                        else:
                            if self.show and not show_outside:
                                area = biggest_rect.area()
                                distance = np.linalg.norm(im_center-face_center)
                                ratio = area/distance
                                cv2.putText(im, "{}, A: {}, d: {}, r: {}".format(name,area,distance,ratio), (10, 30*(j+1)), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
                except Exception as e:
                    raise

                if len(users_in_frame) == 0 and not(multiple) and not(UK_detected):
                    self.show = False

                keys_to_delete = []
                if bool(self.users): # the dictionary is not empty, as something
                    for key in self.users:
                        key_present = False
                        for user_info in users_in_frame:
                            if key == user_info[0]:
                                key_present = True
                                continue
                        if key_present == False:
                            keys_to_delete.append(key)

                for i in range(0, len(keys_to_delete)):
                    del self.users[keys_to_delete[i]]

                for user in users_in_frame:
                    cedula = user[0]
                    name = user[1]
                    if not multiple:
                        user_face_area = user[2]
                        user_face_ratio = user[3]
                    if not (cedula in self.users):  # la cedula no esta y se pone por primera vez
                        if not multiple:
                            self.users[cedula] = [name, 1,[user_face_area],[user_face_ratio]]
                        else:
                            self.users[cedula] = [name, 1]
                    else: # cedula is already in self.users therefore its count is increased
                        self.users[cedula][1] += 1  # la cedula ay esta. aumenta el contador de veces que se detecta seguido el usuario
                        if not multiple:
                            self.users[cedula][2].append(user_face_area)
                            self.users[cedula][3].append(user_face_ratio)
                        # check for continuity o validated user in frames
                        if self.users[cedula][1] >= variables.n_verificacion:
                        #print ("usuario validado %s" %self.users[cedula])
                            self.users[cedula][1] = 0
                        #self.users = {}
                            self.cc = cedula
                            self.face_area = np.mean(self.users[cedula][2])
                            self.ratio = np.mean(self.users[cedula][3])
                            self.send_msg = True
                            print("OK".center(300,'*'))


                if self.show:
                    # Put fps at which we are processinf camera feed on frame
                    cv2.putText(im, "{0:.2f}-fps".format(fps), (10, size[0] - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
                    # Display it all on the screen

                    # Wait for keypress
                    if show_outside:
                        self.im = im
                        # cv2.imshow(winName, self.im)
                    else:
                        cv2.imshow(winName, im)
                    key = cv2.waitKey(1) & 0xFF

                    # Stop the program.
                    if key == 27:    # ESC
                        # If ESC is pressed, exit.
                        sys.exit()

                    # increment frame counter
                count = count + 1
                # calculate fps at an interval of 100 frames
                if (count == 100):
                    t = (cv2.getTickCount() - t) / cv2.getTickFrequency()
                    fps = 100.0 / t
                    count = 0
                gc.enable()
                gc.collect

            # end while true
            cv2.destroyAllWindows()
            cap.release()

        except Exception as e:
            raise

    def request_open_door(self):
        while True:
            if self.send_msg:
                try:
                    msg = str(cam_n) + "/" + str(self.cc) + "/" + str(self.face_area) + "/" + str(self.ratio) #
                    if is_an_entrance:
                        msg+="/entrance"
                    else:
                        msg+="/exit"

                    print(msg.center(100,'*'))
                    show_image = self.camera_client.send_data_to_udp_server(msg)

                    if show_outside:
                        self.show = show_image


                    self.cc = None
                    self.face_area = None
                    self.ratio = None
                    self.send_msg = False
                    # if not multiple:
                    #     if face_area == 0 and ratio == 0 :
                    #         cv2.destroyAllWindows()
                    #         self.show = False
                    #     else:
                    #         if show_image:
                    #             self.show = True
                    #         else:
                    #             self.show = False
                    #             cv2.destroyAllWindows()

                except Exception as e:
                    print(e)
                    raise
            else:
                time.sleep(0.05)

    def send_image(self):
        while True:
            if not(self.im is None):
                # try:
                image_recieved = self.image_client.send_image(self.im)
                if not image_recieved:
                    print("Problem with FSR GUI")
                    time.sleep(0.05)
                else:
                    self.im = None
                # except Exception as e:
                #     raise
            else:
                time.sleep(0.05)

    def start_request_open_door(self):
        thread.start_new_thread(self.request_open_door, ())

    def start_send_image(self):
        thread.start_new_thread(self.send_image,())

if __name__ == "__main__":
    cam_n = 3
    is_an_entrance = True
    multiple = True
    show_outside = False

    cmd = None
    value = None
    try:
        if len(sys.argv[1:])>1:
            for arg in sys.argv[1:]:
                if cmd is None:
                    cmd = arg.lower()
                else:
                    if cmd == "-c":
                        cam_n = int(arg)
                        cmd = None
                    elif cmd == "-e":
                        is_an_entrance = bool(int(arg))
                        cmd = None
                    elif cmd == "-m":
                        multiple = bool(int(arg))
                        cmd = None
                    elif cmd == "-so":
                        show_outside = bool(int(arg))
                        cmd = None
                    else:
                        print("ERROR: Invalid command '{}'".format(cmd))
                        exit()
    except Exception as e:
        raise

    msg = "Starting "
    if is_an_entrance:
        msg += "entrance node "
    else:
        msg += "exit node "
    msg += "with camera number {}, ".format(cam_n)
    if multiple:
        msg += "multiple recognition actived."
    else:
        msg += "single recognition actived."
    print(msg)

    fd1 = face_detection()
    fd1.video_service(cam_n)

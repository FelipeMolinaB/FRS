import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import dlib
import cv2
import numpy as np
import time
from sklearn.externals import joblib


# Path to landmarks and face recognition model files
PREDICTOR_PATH = '/root/face_course/project/models/shape_predictor_68_face_landmarks.dat'
FACE_RECOGNITION_MODEL_PATH = '/root/face_course/project/models/dlib_face_recognition_resnet_model_v1.dat'

# Initialize face detector, facial landmarks detector and face recognizer
faceDetector = dlib.get_frontal_face_detector()
shapePredictor = dlib.shape_predictor(PREDICTOR_PATH)
faceRecognizer = dlib.face_recognition_model_v1(FACE_RECOGNITION_MODEL_PATH)

def get_users_path_data():
    rootdir = "/root/face_course/project"
    rootdir_data  = os.path.join(rootdir, "data")
    users_path = []

    for root, dirs, files in os.walk(rootdir_data):
        for name in files:
            if name.endswith(".jpg"):
                users_path.append(root)
                break

    # for i in xrange(0, len(users_path)):
    #     print users_path[i]


    return users_path

def get_images_path(root_dir_path_user):
    imagePaths = []

    for x in os.listdir(root_dir_path_user):
        xpath = os.path.join(root_dir_path_user, x)
        if x.endswith('jpg'):
            imagePaths.append(xpath)
    return imagePaths

def get_descriptor(imagePath):
    # Process images one by one
    # We will store face descriptors in an ndarray (faceDescriptors)
    # and their corresponding labels in dictionary (index)
    index = {}
    i = 0
    faceDescriptors = None

    print("processing: {}".format(imagePath))
    # read image and convert it to RGB
    img = cv2.imread(imagePath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # detect faces in image
    faces = faceDetector(img, 1)

    # Now process each face we found
    for k, face in enumerate(faces):

        start = time.time()

        # Find facial landmarks for each detected face
        shape = shapePredictor(img, face)

        # convert landmarks from Dlib's format to list of (x, y) points
        landmarks = [(p.x, p.y) for p in shape.parts()]

        shape_landmarks = time.time()
        # print("time shape_landmarks %s" % (shape_landmarks - start))

        # Compute face descriptor using neural network defined in Dlib.
        # It is a 128D vector that describes the face in img identified by shape.
        faceDescriptor = faceRecognizer.compute_face_descriptor(img, shape)


        time_faceDescriptor = time.time()
        # print("time_faceDescriptor %s" % (time_faceDescriptor-shape_landmarks))
        # Convert face descriptor from Dlib's format to list, then a NumPy array
        faceDescriptorList = [x for x in faceDescriptor]
        faceDescriptorNdarray = np.asarray(faceDescriptorList, dtype=np.float64)
        faceDescriptorNdarray = faceDescriptorNdarray[np.newaxis, :]

        # Stack face descriptors (1x128) for each face in images, as rows
        if faceDescriptors is None:
            faceDescriptors = faceDescriptorNdarray
        else:
            faceDescriptors = np.concatenate((faceDescriptors, faceDescriptorNdarray), axis=0)

        #print faceDescriptors
        # save the label for this face in index. We will use it later to identify
        # person name corresponding to face descriptors stored in NumPy Array
        index[i] = imagePath
        i += 1

        end = time.time()
        #print("total time elapsed %s" % (end - start))

    return faceDescriptors


def save_descriptors_user (root_dir_path_user):
    descriptors_array = []
    imagePaths = get_images_path(root_dir_path_user)

    for i in xrange(0, len(imagePaths)):
        try:
            faceDescriptors = get_descriptor(imagePaths[i])
            print ("faceDescriptors %s" % faceDescriptors)
            descriptors_array.append(faceDescriptors)
        except:
            print "error"


    name_descriptors =  root_dir_path_user.split("/")[-1] + ".pkl"
    file_path = os.path.join(root_dir_path_user, name_descriptors)

    print len(descriptors_array)
    print file_path

    joblib.dump(descriptors_array, file_path)

    print ("save to ")
    print file_path

def load_descriptors_user (root_dir_path_user):
    name_descriptors =  root_dir_path_user.split("/")[-1] + ".pkl"
    file_path = os.path.join(root_dir_path_user, name_descriptors)

    descriptors_array = joblib.load( file_path)
    return descriptors_array


import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import cv2
import dlib
import faceBlendCommon as fbc
import numpy as np
import random
from random import randint

import gc
import time
from multiprocessing import Pool
import multiprocessing

from random import randint

def get_folder_others():
    rootdir = "/root/face_course/project"
    rootdir_data = os.path.join(rootdir, "data", "muct")

    false_users_path = []

    for root, dirs, files in os.walk(rootdir_data):
        for name in files:
            if name.endswith(".jpg"):
                false_users_path.append(root)
                break

    return false_users_path

def get_folder_users():
    rootdir = "/root/face_course/project"
    rootdir_data = os.path.join(rootdir, "data")
    users_path = []

    for root, dirs, files in os.walk(rootdir_data):
        for name in files:
            if name.endswith(".jpg"):
                if root.split("/")[-2] == "muct" or root.split("/")[-1].split("_")[-1] == "fake":
                    pass
                else:
                    users_path.append(root)
                break

    return users_path



def generate_average_face(imagePaths):
        PREDICTOR_PATH = "/root/face_course/project/models/shape_predictor_68_face_landmarks.dat"


        # Get the face detector
        faceDetector = dlib.get_frontal_face_detector()
        # The landmark detector is implemented in the shape_predictor class
        landmarkDetector = dlib.shape_predictor(PREDICTOR_PATH)

        if len(imagePaths) == 0:
            print('No images found with extension jpg or jpeg')
            return None

        # Read images and perform landmark detection.
        images = []
        allPoints = []

        for imagePath in imagePaths:
            print imagePath
            im = cv2.imread(imagePath)
            if im is None:
                print("image:{} not read properly".format(imagePath))
                return None
            else:
                points = fbc.getLandmarks(faceDetector, landmarkDetector, im)
                if len(points) > 0:
                    allPoints.append(points)

                    im = np.float32(im) / 255.0
                    images.append(im)
                else:
                    print("Couldn't detect face landmarks")
                    return None

        if len(images) == 0:
            print("No images found")
            return None

        # Dimensions of output image
        w = 600
        h = 600

        # 8 Boundary points for Delaunay Triangulation
        boundaryPts = fbc.getEightBoundaryPoints(h, w)

        numImages = len(imagePaths)
        numLandmarks = len(allPoints[0])

        # Variables to store normalized images and points.
        imagesNorm = []
        pointsNorm = []

        # Initialize location of average points to 0s
        pointsAvg = np.zeros((numLandmarks, 2), dtype=np.float32)

        # Warp images and trasnform landmarks to output coordinate system,
        # and find average of transformed landmarks.
        for i, img in enumerate(images):
            points = allPoints[i]
            points = np.array(points)

            img, points = fbc.normalizeImagesAndLandmarks((h, w), img, points)

            # Calculate average landmark locations
            pointsAvg = pointsAvg + (points / (1.0 * numImages))

            # Append boundary points. Will be used in Delaunay Triangulation
            points = np.concatenate((points, boundaryPts), axis=0)

            pointsNorm.append(points)
            imagesNorm.append(img)

        # Append boundary points to average points.
        pointsAvg = np.concatenate((pointsAvg, boundaryPts), axis=0)

        # Delaunay triangulation
        rect = (0, 0, w, h)
        dt = fbc.calculateDelaunayTriangles(rect, pointsAvg)

        # Output image
        output = np.zeros((h, w, 3), dtype=np.float)

        # Warp input images to average image landmarks
        for i in xrange(0, numImages):
            imWarp = fbc.warpImage(imagesNorm[i], pointsNorm[i], pointsAvg.tolist(), dt)

            # Add image intensities for averaging
            output = output + imWarp

        # Divide by numImages to get average
        output = output / (1.0 * numImages)

        output = cv2.convertScaleAbs(output * 255)



        #  cv2.imwrite('/root/imagenes_enrolamiento/1014193765_fake/fake_3.jpg', output)

        # cv2.imwrite('/root/openface/demos/web/db/imagenes_enrolamiento/1014193765_fake/fake_2.jpg', output)

        # # Display result
        # cv2.imshow('image', output)
        # cv2.waitKey(0)
        return output
   # except Exception, e:
     #   return None


def get_folder_todos_excepto_coincidencia(rootdir, coincidencia):

    import os
    import numpy as np
    folder_array = []
    for subdir, dirs, files in os.walk(rootdir):
        split_subdir = subdir.split("/")
        if split_subdir[-1].isdigit() and coincidencia != int(split_subdir[-1]):
            folder_array.append(subdir)
    return folder_array

def get_folder_todos(rootdir):
    folder_array = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith('.jpg'):
                folder_array.append(os.path.join(rootdir, file))
    return folder_array

def wrapper_fake_dataset_parallel(args):
    return fake_dataset_parallel(*args)
def fake_dataset_parallel(face_persona_path, face_false_path, cedula, fake):

    imagePaths = []
    # imagePaths.append(face_persona_path[i])
    print ("fake_dataset_parallel persona %s" % face_persona_path)
    print ("fake_dataset_parallel false %s" % face_false_path)
    imagePaths.append(face_persona_path)
    imagePaths.append(face_persona_path)
    imagePaths.append(face_persona_path)
    imagePaths.append(face_persona_path)
    imagePaths.append(face_false_path)
    imagePaths.append(face_false_path)
    imagePaths.append(face_false_path)

    try:
        output = generate_average_face(imagePaths)

        if output == None:
            print  "es none"
            return

        rootdir = '/root/openface/demos/web/db/imagenes_enrolamiento/'
        folder_fake = str(cedula) + fake  # "_fake"
        folder_fake = os.path.join(rootdir, folder_fake)
        # if not os.path.exists(folder_fake):
        #     os.makedirs(folder_fake)
        name = face_persona_path.split("/")[-1].split(".")[0]
        image_fake = str(name) + '.jpg'
        path_image_fake = os.path.join(folder_fake, image_fake)
        print ("path_image_fake %s" % path_image_fake)
        cv2.imwrite(path_image_fake, output)
    except:
        print ("error generate_average_face")


def wrapper_true_dataset_parallel(args):
    return true_dataset_parallel(*args)
def true_dataset_parallel(face_persona_path_1, face_persona_path_2, cedula):

    imagePaths = []
    # imagePaths.append(face_persona_path[i])
    print ("fake_dataset_parallel persona %s" % face_persona_path_1)
    print ("fake_dataset_parallel false %s" % face_persona_path_2)
    imagePaths.append(face_persona_path_1)
    imagePaths.append(face_persona_path_2)

    try:
        output = generate_average_face(imagePaths)

        if output == None:
            print  "es none"
            return

        rootdir = '/root/openface/demos/web/db/imagenes_enrolamiento/'
        folder_true = str(cedula) + "_true"  # "_fake"
        folder_true = os.path.join(rootdir, folder_true)
        # if not os.path.exists(folder_fake):
        #     os.makedirs(folder_fake)
        name = face_persona_path_1.split("/")[-1].split(".")[0]
        image_true = str(name) + '.jpg'
        path_image_true = os.path.join(folder_true, image_true)
        print ("path_image_true %s" % path_image_true)
        cv2.imwrite(path_image_true, output)
    except:
        print ("error generate_average_face")



def generate_fake_dataset_from_db(cedula, fake):

    print ("generate_fake_dataset")
    rootdir = "/root/openface/demos/web/db/imagenes_enrolamiento"
    coincidencia = cedula

    path_face_persona = os.path.join(rootdir, str(cedula))
    face_persona_path = get_folder_todos(path_face_persona)

    rootdir = "/root/openface/demos/web/db/imagenes_enrolamiento"
    path_false_i = os.path.join(rootdir, str(cedula) + "_false_i")
    face_false_path = get_folder_todos(path_false_i)

    parallel_face_path = []
    for i in xrange(0, len(face_persona_path)):
        print ("generate_fake_dataset")


        path_faces =(face_persona_path[i], face_false_path[i], cedula, fake)
        parallel_face_path.append(path_faces)



    # for i in xrange(0, len(parallel_face_path)):
    #     fake_dataset_parallel(parallel_face_path[i])


    rootdir = '/root/openface/demos/web/db/imagenes_enrolamiento/'
    folder_fake = str(cedula) + fake  # "_fake"
    folder_fake = os.path.join(rootdir, folder_fake)
    if not os.path.exists(folder_fake):
        os.makedirs(folder_fake)

    t1 = time.time()
    p = Pool()
    p.map(wrapper_fake_dataset_parallel, parallel_face_path)
    p.close()
    p.join()
    print ("parallel fake dataset - pool took: %s" % (time.time() - t1))







def generate_true_dataset_from_db(cedula):


    print ("generate_true_dataset_from_db")
    rootdir = "/root/openface/demos/web/db/imagenes_enrolamiento"
    coincidencia = cedula

    path_face_persona = os.path.join(rootdir, str(cedula))
    face_persona_path = get_folder_todos(path_face_persona)



    parallel_face_path = []
    for i in xrange(0, len(face_persona_path)):
        print ("generate_fake_dataset")
        j = np.random.randint(0,len(face_persona_path) -1)

        path_faces =(face_persona_path[i], face_persona_path[j], cedula)
        parallel_face_path.append(path_faces)



    # for i in xrange(0, len(parallel_face_path)):
    #     fake_dataset_parallel(parallel_face_path[i])


    rootdir = '/root/openface/demos/web/db/imagenes_enrolamiento/'
    folder_true = str(cedula) + "_true"  # "_fake"
    folder_true = os.path.join(rootdir, folder_true)
    if not os.path.exists(folder_true):
        os.makedirs(folder_true)

    t1 = time.time()
    p = Pool()
    p.map(wrapper_true_dataset_parallel, parallel_face_path)
    p.close()
    p.join()
    print ("parallel true dataset - pool took: %s" % (time.time() - t1))





def generate_fake_dataset(cedula, fake):

    print ("generate_fake_dataset")
    rootdir = "/root/openface/demos/web/db/imagenes_enrolamiento"
    coincidencia = cedula

    path_face_persona = os.path.join(rootdir, str(coincidencia))
    face_persona_path =get_folder_todos(path_face_persona)

    for i in xrange(0, len(face_persona_path)):
        print ("generate_fake_dataset")
        folder_otros = (get_folder_todos_excepto_coincidencia(rootdir, coincidencia))

    #for j in xrange(0, 1):#len(folder_otros)):
        j = (randint(0, len(folder_otros) - 1))
        print ("l %s i %s j %s " %(len(face_persona_path), i, j))
        path_face_otro = os.path.join(folder_otros[j], random.choice(os.listdir(folder_otros[j])))
        imagePaths = []
        #imagePaths.append(face_persona_path[i])
        imagePaths.append(face_persona_path[i])
        imagePaths.append(face_persona_path[i])
        imagePaths.append(face_persona_path[i])
        imagePaths.append(face_persona_path[i])
        imagePaths.append(path_face_otro)
        imagePaths.append(path_face_otro)
        imagePaths.append(path_face_otro)

        try:
            output = generate_average_face(imagePaths)

            if output != None:
                rootdir = '/root/openface/demos/web/db/imagenes_enrolamiento/'
                folder_fake = str(cedula) + fake #"_fake"
                folder_fake = os.path.join(rootdir, folder_fake)
                if not os.path.exists(folder_fake):
                    os.makedirs(folder_fake)
                image_fake = str(i) + '_' + str(j) + '.jpg'
                image_fake = os.path.join(rootdir, folder_fake, image_fake)
                cv2.imwrite(image_fake, output)

        except:
            print ("error in generate_fake_dataset with cedula %s" %cedula)




def generate_true_dataset(cedula):
    print ("generate_true_dataset")
    rootdir = "/root/openface/demos/web/db/imagenes_enrolamiento"
    coincidencia = cedula

    path_face_persona = os.path.join(rootdir, str(coincidencia))
    face_persona_path = get_folder_todos(path_face_persona)

    for i in xrange(0, len(face_persona_path)):

        print ("generate_true_dataset")

        j = (randint(0, len(face_persona_path) - 1))
        print ("l %s i %s j %s " % (len(face_persona_path), i, j))
        imagePaths = []
        imagePaths.append(face_persona_path[i])
        imagePaths.append(face_persona_path[j])

        try:
            output = generate_average_face(imagePaths)

            if output != None:
                rootdir = '/root/openface/demos/web/db/imagenes_enrolamiento/'
                folder_fake = str(cedula) + "_true"
                folder_fake = os.path.join(rootdir, folder_fake)

                if not os.path.exists(folder_fake):
                    os.makedirs(folder_fake)

                image_fake = str(i) + '_' + str(j) + '.jpg'
                image_fake = os.path.join(rootdir, folder_fake, image_fake)
                cv2.imwrite(image_fake, output)

        except:
            print ("error in generate_true_dataset with cedula %s" % cedula)




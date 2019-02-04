import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#import utilities as db_utl
import face_average_utilities_dos as fa_utl
#from confirmacion_identidad import identidad_utilities
from random import randint
import cv2
import dlib

def generate_face_average_image(imagePaths, i):

    rootdir = "/root/face_course/project/data"
    name_folder = imagePaths[0].split("/")[-2] + "_fake"

    print imagePaths[0]
    print imagePaths[1]

    folder_path = os.path.join(rootdir, name_folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    image_fake_name = imagePaths[0].split("/")[-1]  + "_fake_" +  str(i) + ".jpg"

    path_image_fake = os.path.join(folder_path, image_fake_name)



    output = fa_utl.generate_average_face(imagePaths)
    cv2.imwrite(path_image_fake, output)

    print ("face average done for %s" %path_image_fake)

def db_operations(op):
    print op
    if op == "face_average":

        imagePaths = []
        imagePaths.append("/root/face_course/project/data/Camilo/7_171.jpg")
        #imagePaths.append("/root/face_course/project/data/Paulo_Andres/20_14012.jpg")
        imagePaths.append("/root/face_course/project/data/muct/000/i000qb-fn.jpg")

        output = fa_utl.generate_average_face(imagePaths)

        folder_fake = "/root/face_course/project/data/Camilo_fake"
        if not os.path.exists(folder_fake):
            os.makedirs(folder_fake)
        name =  "fake_1.jpg" #face_persona_path.split("/")[-1].split(".")[0]
        #image_fake = str(name) + '.jpg'
        image_fake = "fake_1.jpg"
        path_image_fake = os.path.join(folder_fake, name)

        print ("path_image_fake %s" % path_image_fake)
        cv2.imwrite(path_image_fake, output)

    elif op == "generate_fake_dataset":

        false_users_paths = fa_utl.get_folder_others()

        users_path =fa_utl.get_folder_users()

        for i in xrange (0, len(users_path)):
            print users_path[i]

            if users_path [i] == "/root/face_course/project/data/Carlos" or users_path [i] == "/root/face_course/project/data/Juan_Carlos" or users_path [i] == "/root/face_course/project/data/Jhon_Joya" or users_path [i] == "/root/face_course/project/data/Jhon_Garzon" or users_path [i] == "/root/face_course/project/data/Camilo" or users_path [i] == "/root/face_course/project/data/Jhon_Estevez":
                pass
            else:
                index_image = 0
                rootdir_data =  users_path[i]
                print rootdir_data

                for root, dirs, files in os.walk(rootdir_data):
                    for name in files:
                        if name.endswith(".jpg"):
                            imagePaths = []
                            true_file_path = os.path.join(rootdir_data, name)

                            imagePaths.append(true_file_path)

                            rand_false_user = randint(0, len(false_users_paths)-1)
                            false_user_path = false_users_paths[rand_false_user]

                            false_user_images = []
                            for root_f, dirs_f, files_f in os.walk(false_user_path):
                                for name_f in files_f:
                                    if name_f.endswith(".jpg"):
                                        false_user_images.append(name_f)
                                if len(false_user_images) > 0:
                                    break

                            rand_false_user_image = randint(0, len(false_user_images) - 1)
                            false_user_image = false_user_images[rand_false_user_image]

                            false_file_path = os.path.join(false_user_path, false_user_image)

                            imagePaths.append(false_file_path)

                #             print ("imagePaths %s" %imagePaths)
                            index_image = index_image + 1
                            #print index_image
                            try:
                                generate_face_average_image(imagePaths, index_image)
                            except:
                                print ("error")






    else:
        print "opcion no valida ..."


if __name__ == "__main__":


    #db_operations("face_average")
    db_operations("generate_fake_dataset")





import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from generate_descriptors_dataset import descriptor_utilities as des_utl
from sklearn.externals import joblib
import numpy as np


def aux_save_training_testing_validation(path_original, path_datasets, set_name):

    path_dataset_training = path_datasets[0]
    path_dataset_testing = path_datasets[1]
    path_dataset_validation = path_datasets[2]

    descriptors_original = []
    descriptors = des_utl.load_descriptors_user(path_original)

    for j in xrange(0, len(descriptors)):
        try:
            #print descriptors[j][0]
            descriptors_original.append(descriptors[j][0])
        except:
            print "error"

    n = len(descriptors_original)
    descriptors_original_training = descriptors_original[0:int(n * 0.6)]
    descriptors_original_testing = descriptors_original[int(n * 0.6): int(n * 0.8)]
    descriptors_original_validation = descriptors_original[int(n * 0.8): n]

    print n
    print ("descriptors_original_training %s" %len(descriptors_original_training))
    print ("descriptors_original_testing %s" % len(descriptors_original_testing))
    print ("descriptors_original_validation %s" % len(descriptors_original_validation))

    name_file = set_name + "_training.pkl"
    file_path = os.path.join(path_dataset_training, name_file)
    joblib.dump(descriptors_original_training, file_path)

    name_file = set_name + "_testing.pkl"
    file_path = os.path.join(path_dataset_testing, name_file)
    joblib.dump(descriptors_original_testing, file_path)

    name_file = set_name + "_validation.pkl"
    file_path = os.path.join(path_dataset_validation, name_file)
    joblib.dump(descriptors_original_validation, file_path)


def save_training_testing_validation(name_original):
    rootdir = "/root/face_course/project/data"
    #name_original = users_path[i].split("/")[-1]
    name_fake = name_original + "_fake"
    name_dataset = name_original + "_datasets"

    path_original = os.path.join(rootdir, name_original)
    path_fake = os.path.join(rootdir, name_fake)

    path_dataset_training = os.path.join(rootdir, name_dataset, "training")
    path_dataset_testing = os.path.join(rootdir, name_dataset, "testing")
    path_dataset_validation = os.path.join(rootdir, name_dataset, "validation")

    if not os.path.exists(path_dataset_training):
        os.makedirs(path_dataset_training)

    if not os.path.exists(path_dataset_testing):
        os.makedirs(path_dataset_testing)

    if not os.path.exists(path_dataset_validation):
        os.makedirs(path_dataset_validation)

    path_datasets = []
    path_datasets.append(path_dataset_training)
    path_datasets.append(path_dataset_testing)
    path_datasets.append(path_dataset_validation)



    aux_save_training_testing_validation(path_original, path_datasets, "original")
    aux_save_training_testing_validation(path_fake, path_datasets, "fake")

def load_descriptor(users_path_i, set, set_2):
    #descriptor = load_descriptor(users_path[i], "training", "original_")

    file_path = os.path.join(users_path_i, set, set_2 + set + ".pkl")
    descriptor = joblib.load(file_path)
    return descriptor

def test_cases(op):
    print ("test case: %s" %op)

    if op == "get_users_path_data":
        users_path = des_utl.get_users_path_data()
        for i in xrange(0, len(users_path)):
            print users_path[i]

    elif op == "get_images_path":
        root_dir_path_user = "/root/face_course/project/data/camilo"
        imagePaths = des_utl.get_images_path(root_dir_path_user)
        for i in xrange (0, len(imagePaths)):
            print imagePaths[i]

    elif op == "get_descriptor":
        root_dir_path_user = "/root/face_course/project/data/camilo"
        imagePaths = des_utl.get_images_path(root_dir_path_user)
        for i in xrange (0, len(imagePaths)):
            faceDescriptors = des_utl.get_descriptor(imagePaths[i])
            print ("faceDescriptors %s" %faceDescriptors[0])

            print ("faceDescriptors %s" % len(faceDescriptors[0]))

    elif op == "save_descriptors_user":
        root_dir_path_user = "/root/face_course/project/data/camilo"
        root_dir_path_user = "/root/face_course/project/data/Paulo_Andres_fake"

        des_utl.save_descriptors_user(root_dir_path_user)

    elif op == "save_descriptors_ALL_users":
        users_path = des_utl.get_users_path_data()
        for i in xrange(0, len(users_path)):
            print users_path[i]
            root_dir_path_user = users_path[i]

            try:
                des_utl.save_descriptors_user(root_dir_path_user)
            except:
                print "################################################### error"

    elif op == "load_descriptors_user":
        root_dir_path_user = "/root/face_course/project/data/camilo"
        descriptors_array = des_utl.load_descriptors_user(root_dir_path_user)
        for i in xrange (0, len(descriptors_array)):
            print descriptors_array[i]


    elif op == "load_descriptors_ALL_users":
        users_path = des_utl.get_users_path_data()
        for i in xrange(0, len(users_path)):
            print users_path[i]
            root_dir_path_user = users_path[i]

            try:
                descriptors_array = des_utl.load_descriptors_user(root_dir_path_user)
                print len(descriptors_array)
            except:
                print "################################################### error"

    elif op == "datasets_users":
        users_path = des_utl.get_users_path_data()
        for i in xrange(0, len(users_path)):
            if users_path[i].split("/")[-2] == "muct":
                pass
                #print users_path[i]
            elif users_path[i].split("/")[-1].split("_")[-1] != "fake":
                rootdir = "/root/face_course/project/data"
                name_original = users_path[i].split("/")[-1]
                print name_original
                save_training_testing_validation(name_original)


    elif op == "datasets_unknown":
        users_path = des_utl.get_users_path_data()
        unknown_folders = []
        for i in xrange(0, len(users_path)):
            if users_path[i].split("/")[-2] == "muct":
                unknown_folders.append(users_path[i])

        unknown_descriptos = []

        for i in xrange (0, len(unknown_folders)):
            #print unknown_folders[i]
            descriptors = des_utl.load_descriptors_user(unknown_folders[i])
            for j in xrange(0, len(descriptors)):
                try:
                    #print descriptors[j][0]
                    unknown_descriptos.append(descriptors[j][0])
                except:
                    print "error"


        # for i in xrange (0, len(unknown_descriptos)):
        #     print unknown_descriptos[i]

        print len(unknown_descriptos)

        rootdir = "/root/face_course/project/data"
        # name_original = users_path[i].split("/")[-1]

        path_unknown = os.path.join(rootdir, "unknown_datasets")

        path_dataset_training = os.path.join(path_unknown, "training")
        path_dataset_testing = os.path.join(path_unknown, "testing")
        path_dataset_validation = os.path.join(path_unknown, "validation")

        if not os.path.exists(path_dataset_training):
            os.makedirs(path_dataset_training)

        if not os.path.exists(path_dataset_testing):
            os.makedirs(path_dataset_testing)

        if not os.path.exists(path_dataset_validation):
            os.makedirs(path_dataset_validation)

        n = len(unknown_descriptos)
        descriptors_training = unknown_descriptos[0:int(n * 0.6)]
        descriptors_testing = unknown_descriptos[int(n * 0.6): int(n * 0.8)]
        descriptors_validation = unknown_descriptos[int(n * 0.8): n]
        set_name = "unknown"
        name_file = set_name + "_training.pkl"
        file_path = os.path.join(path_dataset_training, name_file)
        joblib.dump(descriptors_training, file_path)

        name_file = set_name + "_testing.pkl"
        file_path = os.path.join(path_dataset_testing, name_file)
        joblib.dump(descriptors_testing, file_path)

        name_file = set_name + "_validation.pkl"
        file_path = os.path.join(path_dataset_validation, name_file)
        joblib.dump(descriptors_validation, file_path)


    elif op == "dataset_general_svm":

        rootdir = "/root/face_course/project"
        rootdir_data = os.path.join(rootdir, "data")


        path_svm_datasets = os.path.join(rootdir, "data", "svm_datasets")

        path_dataset_training = os.path.join(path_svm_datasets, "training")
        path_dataset_testing = os.path.join(path_svm_datasets, "testing")
        path_dataset_validation = os.path.join(path_svm_datasets, "validation")

        if not os.path.exists(path_dataset_training):
            os.makedirs(path_dataset_training)

        if not os.path.exists(path_dataset_testing):
            os.makedirs(path_dataset_testing)

        if not os.path.exists(path_dataset_validation):
            os.makedirs(path_dataset_validation)

        users_path = []

        for root, dirs, files in os.walk(rootdir_data):
            users_path.append(root)

        svm_original_training_datasets = []
        svm_original_testing_datasets = []
        svm_original_validation_datasets = []

        svm_fake_training_datasets = []
        svm_fake_testing_datasets = []
        svm_fake_validation_datasets = []

        for i in xrange(0, len(users_path)):
            if users_path[i].split("/")[-1].split("_")[-1] == "datasets":
                if users_path[i].split("/")[-1].split("_")[-2] != "unknown":
                    if users_path[i].split("/")[-1].split("_")[-2] != "svm":
                        print users_path[i]
                        name = users_path[i].split("/")[-1].split("_")
                        label = ""
                        for k in xrange(0, len(name)):
                            if name[k] != "datasets":
                                label = label + name[k] + "_"
                        #print label

                        descriptor = load_descriptor(users_path[i], "training", "original_")
                        for j in xrange(0, len(descriptor)): svm_original_training_datasets.append([descriptor[j], label])

                        descriptor = load_descriptor(users_path[i], "testing", "original_")
                        for j in xrange(0, len(descriptor)): svm_original_testing_datasets.append([descriptor[j], label])

                        descriptor = load_descriptor(users_path[i], "validation", "original_")
                        for j in xrange(0, len(descriptor)): svm_original_validation_datasets.append([descriptor[j], label])

                        descriptor = load_descriptor(users_path[i], "training", "fake_")
                        for j in xrange(0, len(descriptor)): svm_fake_training_datasets.append([descriptor[j], label + "fake"])

                        descriptor = load_descriptor(users_path[i], "testing", "fake_")
                        for j in xrange(0, len(descriptor)): svm_fake_testing_datasets.append([descriptor[j], label+ "fake"])

                        descriptor = load_descriptor(users_path[i], "validation", "fake_")
                        for j in xrange(0, len(descriptor)): svm_fake_validation_datasets.append([descriptor[j], label+ "fake"])

        # print len(svm_original_training_datasets)
        # print len(svm_original_testing_datasets)
        # print len(svm_original_validation_datasets)
        #
        # print len(svm_fake_training_datasets)
        # print len(svm_fake_testing_datasets)
        # print len(svm_fake_validation_datasets)

        file_path = os.path.join(path_dataset_training, "original" + "_training.pkl")
        joblib.dump(svm_original_training_datasets, file_path)
        file_path = os.path.join(path_dataset_training, "fake" + "_training.pkl")
        joblib.dump(svm_fake_training_datasets, file_path)

        file_path = os.path.join(path_dataset_testing, "original" + "_testing.pkl")
        joblib.dump(svm_original_testing_datasets, file_path)
        file_path = os.path.join(path_dataset_testing, "fake" + "_testing.pkl")
        joblib.dump(svm_fake_testing_datasets, file_path)

        file_path = os.path.join(path_dataset_validation, "original" + "_validation.pkl")
        joblib.dump(svm_original_validation_datasets, file_path)
        file_path = os.path.join(path_dataset_validation, "fake" + "_validation.pkl")
        joblib.dump(svm_fake_validation_datasets, file_path)

        svm_unknown_training_datasets = []
        svm_unknown_testing_datasets = []
        svm_unknown_validation_datasets = []

        for i in xrange(0, len(users_path)):
            if users_path[i].split("/")[-1].split("_")[-1] == "datasets":
                if users_path[i].split("/")[-1].split("_")[-2] == "unknown":

                        print users_path[i]

                        file_path = os.path.join(users_path[i], "training", "unknown_training.pkl")
                        descriptor = joblib.load(file_path)
                        for j in xrange(0, len(descriptor)): svm_unknown_training_datasets.append([descriptor[j], "unknown"])

                        file_path = os.path.join(users_path[i], "testing", "unknown_testing.pkl")
                        descriptor = joblib.load(file_path)
                        for j in xrange(0, len(descriptor)): svm_unknown_testing_datasets.append([descriptor[j], "unknown"])

                        file_path = os.path.join(users_path[i], "validation", "unknown_validation.pkl")
                        descriptor = joblib.load(file_path)
                        for j in xrange(0, len(descriptor)): svm_unknown_validation_datasets.append([descriptor[j], "unknown"])



        file_path = os.path.join(path_dataset_training, "unknown_training.pkl")
        joblib.dump(svm_unknown_training_datasets, file_path)

        file_path = os.path.join(path_dataset_testing, "unknown_testing.pkl")
        joblib.dump(svm_unknown_testing_datasets, file_path)

        file_path = os.path.join(path_dataset_validation, "unknown_validation.pkl")
        joblib.dump(svm_unknown_validation_datasets, file_path)



    else:
        print ("not valid option for test_cases")


if __name__ == "__main__":
    #test_cases("get_users_path_data")
    #test_cases("get_images_path")
    test_cases("get_descriptor")
    #test_cases("save_descriptors_user")
    #test_cases("save_descriptors_ALL_users")
    #test_cases("load_descriptors_user")
    #test_cases("load_descriptors_ALL_users")
    #test_cases("datasets_users")
    #test_cases("datasets_unknown")
    #test_cases("dataset_general_svm")












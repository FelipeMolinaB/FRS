import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import shutil
from sklearn.externals import joblib
from sklearn import svm
from generate_descriptors_dataset import descriptor_utilities as des_utl


import numpy as np
from sklearn.grid_search import GridSearchCV
from sklearn import datasets, svm
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn import metrics


#from generate_descriptors_dataset import descriptor_utilities as des_utl
def get_images_path(root_muct_camera):
    imagePaths = []
    for x in os.listdir(root_muct_camera):
        xpath = os.path.join(root_muct_camera, x)
        if x.endswith('jpg'):
            imagePaths.append(xpath)
    return imagePaths

def save_organize_muct_dataset(root_muct_original):
    #root_muct_original = "/Users/mac/Documents/face_course/cv4faces/project/muct/jpg_1"
    imagePaths = get_images_path(root_muct_original)

    for i in xrange (0, len(imagePaths)):
        list_char = list(imagePaths[i].split("/")[-1])
        name = list_char[1] + list_char[2] + list_char[3]

        root_muct = "/Users/mac/Documents/face_course/cv4faces/project/data/muct"
        directory = os.path.join(root_muct, name)
        if not os.path.exists(directory):
            os.makedirs(directory)

        src = imagePaths[i]
        dst = directory
        shutil.copy2(src, dst)

def train_general_svm(svm_original_training_datasets, svm_unknown_training_datasets):
    X_train = []
    y_train = []

    for i in xrange(0, len(svm_original_training_datasets)):
        X_train.append(svm_original_training_datasets[i][0])
        y_train.append(svm_original_training_datasets[i][1])

    for i in xrange(0, len(svm_unknown_training_datasets)):
        X_train.append(svm_unknown_training_datasets[i][0])
        y_train.append(svm_unknown_training_datasets[i][1])

    parameter_candidates = [
        {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
        {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
    ]

    clf = GridSearchCV(estimator=svm.SVC(), param_grid=parameter_candidates, n_jobs=-1)
    clf.fit(X_train, y_train)

    # View the accuracy score
    print('Best score for data1:', clf.best_score_)

    rootdir = "/root/face_course/project"
    path_svm_model = os.path.join(rootdir, "data", "svm_datasets")

    if not os.path.exists(path_svm_model):
        os.makedirs(path_svm_model)

    name_file = "svm_general.pkl"
    file_path = os.path.join(path_svm_model, name_file)
    joblib.dump(clf, file_path)


def test_general_svm(svm_original_testing_datasets, svm_unknown_testing_datasets):
    X_test = []
    y_test = []

    for i in xrange(0, len(svm_original_testing_datasets)):
        X_test.append(svm_original_testing_datasets[i][0])
        y_test.append(svm_original_testing_datasets[i][1])

    for i in xrange(0, len(svm_unknown_testing_datasets)):
        X_test.append(svm_unknown_testing_datasets[i][0])
        y_test.append(svm_unknown_testing_datasets[i][1])


    rootdir = "/root/face_course/project"
    path_svm_model = os.path.join(rootdir, "data", "svm_datasets")
    name_file = "svm_general.pkl"
    file_path = os.path.join(path_svm_model, name_file)
    clf = joblib.load(file_path)

    y_pred = clf.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    f1_score = metrics.f1_score(y_test, y_pred, average="micro")
    precision = metrics.precision_score(y_test, y_pred, average="micro")
    recall = metrics.recall_score(y_test, y_pred, average="micro")

    print ("cm %s " % cm)
    print ("acc %s " % acc)
    print ("f1_score %s " % f1_score)
    print ("precision %s " % precision)
    print ("recall %s " % recall)




def test_cases(op):
    print ("test case: %s" %op)

    if op == "muct_dataset":
        root_muct_original = "/Users/mac/Documents/face_course/cv4faces/project/muct/jpg_1"
        save_organize_muct_dataset(root_muct_original)

        root_muct_original = "/Users/mac/Documents/face_course/cv4faces/project/muct/jpg_2"
        save_organize_muct_dataset(root_muct_original)

        root_muct_original = "/Users/mac/Documents/face_course/cv4faces/project/muct/jpg_3"
        save_organize_muct_dataset(root_muct_original)

        root_muct_original = "/Users/mac/Documents/face_course/cv4faces/project/muct/jpg_4"
        save_organize_muct_dataset(root_muct_original)

        root_muct_original = "/Users/mac/Documents/face_course/cv4faces/project/muct/jpg_5"
        save_organize_muct_dataset(root_muct_original)


    elif op == "train_general_svm":

        rootdir = "/root/face_course/project"
        rootdir_data = os.path.join(rootdir, "data")

        path_svm_datasets = os.path.join(rootdir, "data", "svm_datasets")

        path_dataset_training = os.path.join(path_svm_datasets, "training")
        path_dataset_testing = os.path.join(path_svm_datasets, "testing")
        path_dataset_validation = os.path.join(path_svm_datasets, "validation")


        file_path = os.path.join(path_dataset_training, "original" + "_training.pkl")
        svm_original_training_datasets = joblib.load(file_path)
        file_path = os.path.join(path_dataset_training, "fake" + "_training.pkl")
        svm_fake_training_datasets = joblib.load(file_path)

        file_path = os.path.join(path_dataset_testing, "original" + "_testing.pkl")
        svm_original_testing_datasets = joblib.load(file_path)
        file_path = os.path.join(path_dataset_testing, "fake" + "_testing.pkl")
        svm_fake_testing_datasets = joblib.load(file_path)

        file_path = os.path.join(path_dataset_validation, "original" + "_validation.pkl")
        svm_original_validation_datasets = joblib.load(file_path)
        file_path = os.path.join(path_dataset_validation, "fake" + "_validation.pkl")
        svm_fake_validation_datasets = joblib.load(file_path)

        file_path = os.path.join(path_dataset_training, "unknown_training.pkl")
        svm_unknown_training_datasets = joblib.load(file_path)

        file_path = os.path.join(path_dataset_testing, "unknown_testing.pkl")
        svm_unknown_testing_datasets = joblib.load( file_path)

        file_path = os.path.join(path_dataset_validation, "unknown_validation.pkl")
        svm_unknown_validation_datasets = joblib.load( file_path)

        # print svm_original_training_datasets[0]
        # print len(svm_original_training_datasets)
        # print len(svm_original_testing_datasets)
        # print len(svm_original_validation_datasets)
        #
        # print svm_fake_training_datasets[0]
        # print len(svm_fake_training_datasets)
        # print len(svm_fake_testing_datasets)
        # print len(svm_fake_validation_datasets)
        #
        # print svm_unknown_training_datasets[0]
        # print len(svm_unknown_training_datasets)
        # print len(svm_unknown_testing_datasets)
        # print len(svm_unknown_validation_datasets)

        #train_general_svm(svm_original_training_datasets, svm_unknown_training_datasets)
        test_general_svm(svm_original_testing_datasets, svm_unknown_testing_datasets)
        print len(svm_original_testing_datasets)
        print len(svm_unknown_testing_datasets)




    else:
        print ("not valid option for test_cases")


if __name__ == "__main__":
    #test_cases("muct_dataset")
    test_cases("train_general_svm")


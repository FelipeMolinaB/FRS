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
def get_datasets_path():
    paths = []
    root_dir = "/root/face_course/project/data"
    for subdir, dirs, files in os.walk(root_dir):
        if subdir.split("_")[-1] == "datasets" and subdir.split("/")[-1].split("_")[0] != "unknown" and subdir.split("/")[-1].split("_")[0] != "svm":
            paths .append(subdir)
        # for file in files:
        #     # print os.path.join(subdir, file)
        #     filepath = subdir + os.sep + file
        #
        #     if filepath.endswith(".asm"):
        #         print (filepath)
    return paths

def train_particular_svm():
    paths = get_datasets_path()
    for path in paths:
        print path
        name_dataset = "original_training.pkl"
        file_path = os.path.join(path, "training", name_dataset)
        dataset_original = joblib.load(file_path)

        name_dataset = "fake_training.pkl"
        file_path = os.path.join(path, "training", name_dataset)
        dataset_fake = joblib.load(file_path)

        name_dataset = "unknown_training.pkl"
        unknown_dataset = "/root/face_course/project/data/unknown_datasets"
        file_path = os.path.join(unknown_dataset, "training", name_dataset)
        dataset_unknown = joblib.load(file_path)



        #print ("original %s fake %s unknown %s" %(len(dataset_original), len(dataset_fake), len(dataset_unknown)))

        X_train = []
        y_train = []

        for i in xrange(0, len(dataset_original)):
            X_train.append(dataset_original[i])
            y_train.append(1)

        for i in xrange(0, len(dataset_fake)):
            X_train.append(dataset_fake[i])
            y_train.append(0)

        for i in xrange(0, len(dataset_unknown)):
            X_train.append(dataset_unknown[i])
            y_train.append(0)

        parameter_candidates = [
            {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
            {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
        ]

        clf = GridSearchCV(estimator=svm.SVC(), param_grid=parameter_candidates, n_jobs=-1)
        clf.fit(X_train, y_train)

        # View the accuracy score
        print('Best score for data1:', clf.best_score_)


        path_svm_model = os.path.join(path)
        name_file = "svm_particular.pkl"
        file_path = os.path.join(path_svm_model, name_file)
        joblib.dump(clf, file_path)


def test_particular_svm():

    paths = get_datasets_path()
    for path in paths:
        print path
        name_dataset = "original_testing.pkl"
        file_path = os.path.join(path, "testing", name_dataset)
        dataset_original = joblib.load(file_path)

        name_dataset = "fake_testing.pkl"
        file_path = os.path.join(path, "testing", name_dataset)
        dataset_fake = joblib.load(file_path)

        name_dataset = "unknown_testing.pkl"
        unknown_dataset = "/root/face_course/project/data/unknown_datasets"
        file_path = os.path.join(unknown_dataset, "testing", name_dataset)
        dataset_unknown = joblib.load(file_path)

        # print ("original %s fake %s unknown %s" %(len(dataset_original), len(dataset_fake), len(dataset_unknown)))

        X_test = []
        y_test = []

        for i in xrange(0, len(dataset_original)):
            X_test.append(dataset_original[i])
            y_test.append(1)

        # for i in xrange(0, len(dataset_fake)):
        #     X_test.append(dataset_fake[i])
        #     y_test.append(0)

        for i in xrange(0, len(dataset_unknown)):
            X_test.append(dataset_unknown[i])
            y_test.append(0)

        path_svm_model = os.path.join(path)
        name_file = "svm_particular.pkl"
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


    if op == "train_general_svm":
        #train_particular_svm()
        test_particular_svm()


        # rootdir = "/root/face_course/project"
        # rootdir_data = os.path.join(rootdir, "data")
        #
        # path_svm_datasets = os.path.join(rootdir, "data", "svm_datasets")
        #
        # path_dataset_training = os.path.join(path_svm_datasets, "training")
        # path_dataset_testing = os.path.join(path_svm_datasets, "testing")
        # path_dataset_validation = os.path.join(path_svm_datasets, "validation")
        #
        #
        # file_path = os.path.join(path_dataset_training, "original" + "_training.pkl")
        # svm_original_training_datasets = joblib.load(file_path)
        # file_path = os.path.join(path_dataset_training, "fake" + "_training.pkl")
        # svm_fake_training_datasets = joblib.load(file_path)
        #
        # file_path = os.path.join(path_dataset_testing, "original" + "_testing.pkl")
        # svm_original_testing_datasets = joblib.load(file_path)
        # file_path = os.path.join(path_dataset_testing, "fake" + "_testing.pkl")
        # svm_fake_testing_datasets = joblib.load(file_path)
        #
        # file_path = os.path.join(path_dataset_validation, "original" + "_validation.pkl")
        # svm_original_validation_datasets = joblib.load(file_path)
        # file_path = os.path.join(path_dataset_validation, "fake" + "_validation.pkl")
        # svm_fake_validation_datasets = joblib.load(file_path)
        #
        # file_path = os.path.join(path_dataset_training, "unknown_training.pkl")
        # svm_unknown_training_datasets = joblib.load(file_path)
        #
        # file_path = os.path.join(path_dataset_testing, "unknown_testing.pkl")
        # svm_unknown_testing_datasets = joblib.load( file_path)
        #
        # file_path = os.path.join(path_dataset_validation, "unknown_validation.pkl")
        # svm_unknown_validation_datasets = joblib.load( file_path)
        #
        # # print svm_original_training_datasets[0]
        # # print len(svm_original_training_datasets)
        # # print len(svm_original_testing_datasets)
        # # print len(svm_original_validation_datasets)
        # #
        # # print svm_fake_training_datasets[0]
        # # print len(svm_fake_training_datasets)
        # # print len(svm_fake_testing_datasets)
        # # print len(svm_fake_validation_datasets)
        # #
        # # print svm_unknown_training_datasets[0]
        # # print len(svm_unknown_training_datasets)
        # # print len(svm_unknown_testing_datasets)
        # # print len(svm_unknown_validation_datasets)
        #
        # #train_general_svm(svm_original_training_datasets, svm_unknown_training_datasets)
        # test_general_svm(svm_original_testing_datasets, svm_unknown_testing_datasets)
        # print len(svm_original_testing_datasets)
        # print len(svm_unknown_testing_datasets)
        #



    else:
        print ("not valid option for test_cases")


if __name__ == "__main__":
    #test_cases("muct_dataset")
    test_cases("train_general_svm")


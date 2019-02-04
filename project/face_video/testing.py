import os
from sklearn.externals import joblib

rootdir = "/root/openface/demos/web/project"
users_file_path = os.path.join(rootdir, "users.pkl")
users = joblib.load(users_file_path)
name = ""
dict_pers = {}
for user in users:
    name = user[1]
    dict_pers[int(user[0])] = name
    print (int(user[0]))

dict_pers[1020751687] = "Jennifer"
dict_pers[1032423806] = "Paulo Andres Cifuentes"
dict_pers[80203712] = "Julian Andres Medina"



rootdir = "/root/openface/demos/web/project"
users_file_path = os.path.join(rootdir, "dict_pers.pkl")
joblib.dump(dict_pers, users_file_path)

rootdir = "/root/openface/demos/web/project"
users_file_path = os.path.join(rootdir, "dict_pers.pkl")
dict_pers = joblib.load(users_file_path)
# print dict_pers[1022344753]
# print dict_pers[1014193765]
# print dict_pers[1020751687]

cont = 0
for i in dict_pers:
    print cont, i, dict_pers[i]
    cont +=1
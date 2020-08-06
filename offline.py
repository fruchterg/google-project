import re
import os

dict_data = {}
dictFile = {}
listString = []


def ignorecharacter(string):

    return re.sub('[^a-z0-9' ']+', '', string.lower())


def read_from_file():
    for root, dirs, files in os.walk('gi', topdown=True):
        for i, file in enumerate(files, 1):
            dictFile[i] = root + '\\' + file
            init_data(root + '\\' + file, i)


def init_data(file, indexsource):

    with open(file, encoding='UTF-8') as the_file:
        temp_list_string = the_file.read().split("\n")
    for i, str in enumerate(temp_list_string, 1):
        listString.append({"sentence": str, "source": indexsource, "offset": i})


def init_sub():

     for j in range(len(listString)):
         for i in range(len(listString[j]["sentence"]) + 1):
             for k in range(i+1, len(listString[j]["sentence"])+1):
                dict_data.setdefault(ignorecharacter(listString[j]["sentence"][i:k]), set()).add(j)
                dict_data.setdefault(ignorecharacter(listString[j]["sentence"][k:i]), set()).add(j)


def sort_best_complete():
    for sentence in dict_data.keys():
        dict_data[sentence] = list(dict_data[sentence])
        dict_data[sentence] = sorted(dict_data[sentence],
            key=lambda k: listString[k]["sentence"])


read_from_file()
init_sub()
sort_best_complete()





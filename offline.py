import re
import os
import shelve

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
    db_file = shelve.open('sucsses.db', writeback=True)
    for j in range(len(listString)):
        for i in range(len(listString[j]["sentence"]) + 1):
            for k in range(i + 1, len(listString[j]["sentence"]) + 1):
                try:
                    db_file[ignorecharacter(listString[j]["sentence"][i:k])].add(j)
                    db_file[ignorecharacter(listString[j]["sentence"][k:i])].add(j)
                except:
                    db_file[ignorecharacter(listString[j]["sentence"][i:k])] = set()
                    db_file[ignorecharacter(listString[j]["sentence"][k:i])] = set()
    db_file.close()


def sort_best_complete():
    db_file = shelve.open('sucsses.db', writeback=True)
    for sentence in db_file.keys():
        db_file[sentence] = list(db_file[sentence])
        db_file[sentence] = sorted(db_file[sentence], key=lambda k: listString[k]["sentence"])
    db_file.close()


read_from_file()
init_sub()
sort_best_complete()

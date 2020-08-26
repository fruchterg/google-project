from offline import dictFile
from offline import listString
from autocomplete import Autocomplete
import shelve

db_file = shelve.open('sucsses.db', writeback=True)


def get(sub):
    try:
        return db_file[sub]
    except:
        return None


def is_exit_compltion(list_dict, completeString):
    for dict in list_dict:
        if listString[dict["index"]]["sentence"] == completeString:
            return False
    return True


def addcompltion(count, sub, score, list_dict):
    for istring in db_file[sub]:
        if is_exit_compltion(list_dict, listString[istring]["sentence"]) and count < 5:
            list_dict.append({"index": istring, "score": score})
            count = count + 1


def get_Score(index):
    return 5 - index if index < 5 else 1


def change(string, count, list_dict):
    index = len(string)
    for lenghString, word in enumerate(string[::-1], 1):
        index = index - 1
        for x in range(ord('a'), ord('z') + 1):
            newSub = string[:-lenghString] + chr(x) + string[len(string) - lenghString + 1:]
            if get(newSub):
                if chr(x) != string[-lenghString]:
                    addcompltion(count, newSub, 2 * len(string) - get_Score(index), list_dict)


def add(string, count, list_dict):
    index = len(string)
    for word in string[::-1]:
        index = index - 1
        for x in range(ord('a'), ord('z') + 1):
            newSub = string.replace(word, chr(x) + word)
            if get(newSub):
                addcompltion(count, newSub, 2 * len(string) - 2 * get_Score(index), list_dict)


def delete(string, count, list_dict):
    index = len(string)
    for lenghString, word in enumerate(string[::-1], 1):
        index = index - 1
        newSub = string[:-lenghString] + string[len(string) - lenghString + 1:]
        if get(newSub):
            addcompltion(count, newSub, 2 * len(string) - 2 * get_Score(index), list_dict)


def changeInput(string, count, list_dict):
    change(string, count, list_dict)
    delete(string, count, list_dict)
    add(string, count, list_dict)
    list_dict = sorted(list_dict, key=lambda k: k["score"], reverse=True)


def autocompleteData(string):
    list1 = []
    list_dict = []
    count = 0
    if get(string):
        for index in db_file[string]:
            if count < 5:
                list_dict.append({"index": index, "score": 2 * len(string)})
                count = count + 1
        if count < 5:
            changeInput(string, count, list_dict)
    else:
        changeInput(string, count, list_dict)
    i = 0

    for dict in list_dict:
        if i < 5:
            i = i + 1
            list1.append(Autocomplete(listString[dict["index"]]["sentence"],
                                      dictFile[listString[dict["index"]]["source"]],
                                      listString[dict["index"]]["offset"], dict["score"]))

    return list1

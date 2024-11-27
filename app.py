import csv
from subprocess import check_output, CalledProcessError
import json
from utils import betterLevenshtein, levenshteinRecursive

def english_to_ipa(text):
    """Converts English text to IPA using espeak-ng."""
    try:
        ipa = check_output(['espeak-ng', '-q', '--ipa', text], universal_newlines=True).strip()
        return ipa
    except CalledProcessError as e:
        return f"Error: {e}"
    
nameList = []
def loadHashIPA():
    f = open("database.csv", "r")
    c = csv.reader(f)
    nameHashed = [row for row in c]


    for i in nameHashed:    
        nameList.append(i)

def findNear(mainName):
    

    # nameList = findNearbyHashes(mainName)
    # start_time = time.time()
    
    # mainIpa = english_to_ipa(mainName)

    # l = []
    # for i in nameList:
    #     p = betterLevenshtein(levenshteinRecursive(i[2], mainIpa, len(i[2]), len(mainIpa)), len(mainName), len(i[2]))
    #     if p > 0.7:
    #         l.append([i, p])
    
    # lSorted = sorted(l, key=lambda x: x[1], reverse=True)
    # # print(lSorted)
    # print(list(map(lambda x: x[0],lSorted[0:10])))
    return mainName
    # print("--- %s seconds ---" % round(time.time() - start_time, 3))
    # print(mainIpa)
    # l = []
    # print(nameList)
    # print(l)
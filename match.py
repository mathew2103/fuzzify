from phonetics import soundex
import csv
# import requests
# import json
# import panphon
# import time
from noel import english_to_ipa
import Levenshtein

def levenshteinRecursive(str1, str2, m, n):
    if m == 0:
        return n
    if n == 0:
        return m
    if str1[m - 1] == str2[n - 1]:
        return levenshteinRecursive(str1, str2, m - 1, n - 1)
    return 1 + min(
          # Insert     
        levenshteinRecursive(str1, str2, m, n - 1),
        min(
              # Remove
            levenshteinRecursive(str1, str2, m - 1, n),
          # Replace
            levenshteinRecursive(str1, str2, m - 1, n - 1))
    )

def betterLevenshtein(lev, l1, l2):
    return (l1 + l2 - lev) / (l1 + l2)

hashIPA_list = [[]] * 26
def loadHashIPA():
    f = open("IndianNamesIPA.csv", "r")
    c = csv.reader(f)
    nameHashed = [row for row in c]

    for i in nameHashed:    
        hashIPA_list[ord(i[0][0]) - ord('a')].append(i)



hasIPADict = {}
def loadHashDict():
    f = open("IndianNamesIPA.csv", "r")
    c = csv.reader(f)
    nameHashed = [row for row in c]

    for i in nameHashed:    
        if i[0][0] in hasIPADict.keys():
            hasIPADict[i[0][0]].append(i)
        else:
            hasIPADict[i[0][0]] = [i]
    

def fasterChecker(name):
    mainHash = soundex(name)
    print(mainHash)
    l = []
    for i in hashIPA_list[ord(name[0]) - ord('a')]:
        if i[0][0] != mainHash[0]:
            continue
        p = levenshteinRecursive(i[1], mainHash, len(i[1]), len(mainHash))
        if p <= 1:
            l.append(i)
    return l
    # lSorted = sorted(l, key=lambda x: x[1])
    # return lSorted


def newChecker(name):
    print('1')
    mainIpa = english_to_ipa(name)
    # mainReq = requests.post("https://api2.unalengua.com/ipav3", json={"text": name, "lang":"en-GB-WLS", "mode": "true"})
    # mainIpa = json.loads(mainReq.text)['ipa']
    # print(mainIpa)
    l = []
    # print(hasIPADict) 
    # print(len(hasIPADict[mainIpa[0]]))
    for i in hasIPADict[name[0]]:
        # p = betterLevenshtein(levenshteinRecursive(i[2], mainIpa, len(i[2]), len(mainIpa)), len(name), len(i[2]))
        p = Levenshtein.ratio(name, i[0])

        if p > 0.7:
            l.append([i[0], i[1], p])
    
    lSorted = sorted(l, key=lambda x: x[1], reverse=True)
    return lSorted[0:5]




# def main():
    
#     mainName = input("Enter name: ").lower()
#     # nearHashes = findNearbyHashes(mainName)
#     start_time = time.time()
#     nearHashes = fasterChecker(mainName)
#     mainReq = requests.post("https://api2.unalengua.com/ipav3", json={"text": mainName, "lang":"en-GB-WLS", "mode": "true"})
#     mainIpa = json.loads(mainReq.text)['ipa']

#     l = []
#     for i in nearHashes:
#         p = betterLevenshtein(levenshteinRecursive(i[2], mainIpa, len(i[2]), len(mainIpa)), len(mainName), len(i[2]))
#         if p > 0.7:
#             l.append([i[0], p])
    
#     lSorted = sorted(l, key=lambda x: x[1], reverse=True)
#     # print(lSorted)
#     print(list(map(lambda x: x[0],lSorted[0:10])))
#     print("--- %s seconds ---" % round(time.time() - start_time, 3))
#     # print(mainIpa)
#     # l = []
#     # print(nearHashes)
#     # print(l)
# loadHashIPA()
# while True:
    
#     main()
    
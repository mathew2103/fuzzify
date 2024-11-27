from csv import reader,writer

# Only use when converting the names database to hashed database

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


def convertAlltoHash(): 
    f = open("IndianNamesUnique.csv", "r")
    f2 = open("IndianNamesHashed.csv", "w")
    c2 = writer(f2)
    c = reader(f,delimiter="\n")
    names = [row[0] for row in c]

    for i in names:
        try:
            c2.writerow([i.lower(), soundex(i.lower())])
        except IndexError:
            print(i)

# Only use when converting names to IPA
def convertAlltoIPA():
    f = open("IndianNamesHashed.csv", "r")
    f2 = open("IndianNamesIPA.csv", "r+")
    
    x = len(f2.readlines())
    
    for i in range(x):
        
        f.readline()

    c = reader(f)
    c2 = writer(f2)

    names = [row for row in c]
    num = 0
    
    nameReqs = []
    k = 0
    while len(names) > 0:            
        k += 1
        
        st = ""
        curReq = []
        while len(st) <= 1900:
            if(len(names) == 0):
                break
            st += names[0][0]
            st += "\n"
            curReq.append(names[0])
            names = names[1:]
            x+=1
            
        req = requests.post("https://api2.unalengua.com/ipav3", json={"text": st, "lang":"en-GB-WLS", "mode": "true"})
        reqIpa = json.loads(req.text)['ipa'].split("\n")
        for i in range(len(curReq)):
            c2.writerow([curReq[i][0], curReq[i][1], reqIpa[i]])
        print(k, x)
    return
      

# OLD CODE: Go through the file every time you want to check
def findNearbyHashes(name):
    f = open("IndianNamesIPA.csv", "r")
    c = csv.reader(f)
    nameHashed = [row for row in c]

    mainHash = soundex(name)
    l = []

    for i in nameHashed:    
        if i[0][0] != mainHash[0]:
            continue
        p = levenshteinRecursive(i[1], mainHash, len(i[1]), len(mainHash))
        # if(p >= 0.7):
        if p < 1:
            l.append(i)


    lSorted = sorted(l, key=lambda x: x[1])
    return lSorted
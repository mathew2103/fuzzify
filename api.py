from fastapi import FastAPI
# from app import findNear, loadHashIPA
# loadHashIPA()
from match import loadHashDict, fasterChecker, newChecker
from search import search
from json import dumps
app = FastAPI()
from pydantic import BaseModel

loadHashDict()
class Item(BaseModel):
    name: str
    
@app.get("/")
async def rootRead():
    return {"Message": "helo codialo"}

toFindName = ""

@app.post("/newfind")
async def find(item: Item):
    r = newChecker(item.name)
    l = []
    for i in r:
        l.append({"name": i[0], "age": 69, "ipa": i[2]*100})
    return l


@app.post("/find")
async def find(item: Item):
    # print(item.name)
    # global toFindName
    # toFindName = 
    r = search(item.name)
    l = []
    # print(fasterChecker(item.name))
    for i in range(len(r["documents"][0])):
        
        l.append({"name": r["documents"][0][i], "age": r["metadatas"][0][i]['age'], "ipa": r["metadatas"][0][i]['ipa']})
    # print(l)
    return l
    # return {"documents": r["documents"][0], "metadatas": r["metadatas"], "distances": r["distances"]}

# while True:
#     pass
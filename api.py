from fastapi import FastAPI
from querry import search
from querry import english_to_ipa
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from querry import add
from querry import edit
from querry import delete
import requests
from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import Annotated
import re
import random
from alt_name import alt_name
import random
from trans import *

def detect_language(text):
    """Detects if the input text is Hindi or English."""
    if any('\u0900' <= char <= '\u097F' for char in text):
        return 'hindi'
    else:
        return 'english'

app = FastAPI()

origins = ["https://fuzzify-codialo.flutterflow.app"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name: str
    
class test(BaseModel):
    rec: str     
    
@app.get("/")
async def rootRead():
    return {"Message": "hello!!, this is team codialo,please send a post request to /find"}

def towhisperb(bdata):
    headers = {
        "Authorization": "Bearer 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",
        "Accept-Language": "en"
    }
    # API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
    response = requests.post(API_URL, headers=headers, data=bdata)
    print(response)
    # return response.json()
    if response.json():
        print(response.json()["text"])
        
        # return english_to_ipa(response.json()   ["text"])
        match = re.search(r'[A-z|\s]+', response.json()["text"])
        if match:
            "".join(match.group(0))
            print(match.group(0))
            return response.json()["text"]
            return {"name":match.group(0)}
    else:
        return "NOICE"
  
@app.post("/voice")
async def receive_audio(rec: Annotated[bytes, File()]):
    try:
        print(rec)
        n = towhisperb(rec)
        print(n)
        if n:
            return {"name": n}
    except Exception as e:
        print(f"Error: {e}")
        return {"name": ""}
 
    
@app.post("/find")
async def find(item: Item):
    print(item.name)
    r = search(item.name)
    l = []
    for i in range(len(r["documents"])):
        l.append({
            "name": r["documents"][i],
            "hindi_name": epitran_ipa_to_hindi(r["metadatas"][i]['ipa']) if is_english(r["documents"][i]) else r["documents"][i],
            "age": r["metadatas"][i]['age'],
            "ipa": r["metadatas"][i]['ipa'],
            "address": r["metadatas"][i]['address'],
            "dob": r["metadatas"][i]['dob'],
            "doc": r["metadatas"][i]['doc'],
            "crime": r["metadatas"][i]['crime'],
            "gender": "",
            "trans_name": r["metadatas"][i]['trans_name'],
            # "gender": "Male",
            "aadhar": r["metadatas"][i]['aadhaar'],
            "station": r["metadatas"][i]['station'],
            "id": r["ids"][i]
            # "id": '1'
        })
    print(l)
    return l
@app.post("/find2")
async def find(item: Item):
    print(item.name)
    
    r = search(item.name)
    l = []
    exact_matches = []
    other_matches = []
    for i in range(len(r["documents"])):
        L = ["Criminal", "Suspect", "Victim", "Witness"]
        Lr = random.choice(L)
        entry = {
            "name": r["documents"][i],
            "age": r["metadatas"][i]['age'],
            "ipa": r["metadatas"][i]['ipa'],
            "address": r["metadatas"][i]['address'],
            "dob": r["metadatas"][i]['dob'], 
            "doc": r["metadatas"][i]['doc'],
            "crime": f"{Lr} in {r['metadatas'][i]['crime']}",
            "gender": "",
            "aadhaar": r["metadatas"][i]['aadhaar'],
            "station": r["metadatas"][i]['station'],
            "trans_name": r["metadatas"][i]['trans_name'],
            "id": r["ids"][i],
            "type": Lr
        }

        if (r["documents"][i].split()[0]).lower() == (item.name.split()[0]).lower():
            exact_matches.append(entry)
        else:
            other_matches.append(entry)
    l = exact_matches + other_matches
    print(l)
    exact_match = 1 if any((r["documents"][i].split()[0]).lower() ==  (item.name.split()[0]).lower() for i in range(len(r["documents"]))) else 0
    return {"result": l, "exact": exact_match}

class AdddItem(BaseModel):
    name: str
    metadata: dict
@app.post("/add")
async def add2(item: AdddItem):
    if detect_language(item.name) == 'hindi':
        item.metadata["trans_name"] = trans_hindi_to_english(item.name)
    else:
        item.metadata["trans_name"] = trans_english_to_hindi(item.name)
    print(add(item.name, item.metadata))
    return {"message": "name added successfully"}

class EditItem(BaseModel):
    id: str
    updated_name: str
    updated_metadata: dict
@app.post("/edit")
async def edit2(item: EditItem):
    edit(item.id, item.updated_name, item.updated_metadata)
    return {"message": "item updated successfully"}

class DeleteItem(BaseModel):
    id: str
@app.post("/delete")
async def delete_item(item: DeleteItem):
    delete(item.id)
    return {"message": "item deleted successfully"}

@app.post("/suggest")
async def suggest(item: Item):
    suggestions = search(item.name)['documents']
    aisuggestions = []
    suggestions = [s for s in suggestions if s.lower() != item.name.lower()]
    if len(suggestions) < 3:
        aisuggestions = alt_name(item.name)[0].split(',')
        aisuggestions = aisuggestions[0:(3 - len(suggestions))]
    else:
        suggestions=suggestions[0:3]
    return {"suggestions": suggestions,"aisuggestions": aisuggestions}



#voice to ipa:-

# def towhisper(filename):
#     headers = {"Authorization": "Bearer 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"}
#     # API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
#     API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
#     with open(filename, "rb") as f:
#         data = f.read()
#     response = requests.post(API_URL, headers=headers, data=data)
#     return english_to_ipa(response.json()["text"])



if __name__ == "__main__":
   uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
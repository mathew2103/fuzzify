# Fuzzify backend

Project for the SIH Grand Finale 2024: Fuzzify addresses challenges faced by police officers and others managing large public databases, where variations in names—such as Laxmi being written as Lakshmi, Lakxmy, or Lackshmy—create inconsistencies. Fuzzify leverages a fine-tuned Lama 3.2 1B model, optimized for lightweight performance, to predict all possible pronunciations of a given name in English Latin script. It outputs these variations in IPA (International Phonetic Alphabet) notation, effectively capturing the full range of pronunciations. A custom embedder then converts the IPA representations into vectors, which are stored in a vector database. Searches are efficiently performed using the cosine similarity algorithm to match and retrieve relevant results

## To start the api to the backend:

### Running the App Locally
To start the application on localhost, use the following command:
```sh
uvicorn api:app --reload
```

#### To tunnel the local host to global static ip that the app sends request to 
To connect using a static IP, run:
```sh
ngrok tunnel --label edge=edghts_2pPvGTg0WJve7kKBZfqbMRpjOuP http://localhost:8000
```

## The LLMs: 
the fine tuned llms are structured to be hosted locally on lm studio or other such llm running tools, the files alt_ipa.py and alt_name.py describes the way to request to this hosted lmstudio server, currently the code base is set to work even if  the llms are offline but suggestions when adding names may not work 

## The database:
due to upload size limitations, the vector database(vdb) is not uploaded in this repo and thus starting the code directly would need to download the entire folder vdb(epi) from https://drive.google.com/drive/folders/13dtmtGPrh93L6Qbn04mb1B6XUrK7C967?usp=sharing 
if u want to instead create your own database follow the chromadb.ipynb, it is well documented and contains code to control the entire backend

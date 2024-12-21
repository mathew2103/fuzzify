# To start the api to the backend

## Initialization

### Running the App Locally
To start the application on localhost, use the following command:
```sh
uvicorn api:app --reload
```

#### to tunnel the local host to global static ip that the app sends request to 
To connect using a static IP, run:
```sh
ngrok tunnel --label edge=edghts_2pPvGTg0WJve7kKBZfqbMRpjOuP http://localhost:8000
```

## The LLMs: 
the fine tuned llms are structured to be hosted locally on lm studio or other such llm running tools, the files alt_ipa.py and alt_name.py describes the way to request to this hosted lmstudio server, currently the code base is set to work even if  the llms are offline but suggestions when adding names may not work 

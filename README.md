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


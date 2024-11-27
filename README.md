# Fuzzify API

## Initialization

### Running the App Locally
To start the application on localhost, use the following command:
```sh
uvicorn api:app --reload
```

### Connecting to Ngrok
#### Dynamic IP (No Tokens Required)
To connect using a dynamic IP, run:
```sh
ngrok http http://127.0.0.1:8000
```

#### Static IP
To connect using a static IP, run:
```sh
ngrok tunnel --label edge=<token> http://localhost:8000/
```

## API Endpoints

1. **`/`**: 
    - **Method**: GET
    - **Description**: Test endpoint to check if the API is running.

2. **`/find`**: 
    - **Method**: POST
    - **Parameters**: 
      - `name` (string): The name to search for.
    - **Description**: Returns an array of similar names using complex algorithms such as cosine similarity.

3. **`/newfind`**: 
    - **Method**: POST
    - **Description**: A new checker that uses the Levenshtein distance algorithm to find similar names.

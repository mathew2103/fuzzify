# Backend:-
to run backend,
1) start the fastapi server:
   uvicorn api:app --reload
2) tunnel the local host to global via ngrok, u can use my credentials to get the static ip that the app sends request to:
   ngrok tunnel --label edge=edghts_2pPvGTg0WJve7kKBZfqbMRpjOuP http://localhost:8000

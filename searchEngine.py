from epitran import Epitran
import panphon
import panphon.distance
import numpy as np
from chromadb.config import Settings
from chromadb import Client
import chromadb
import os
# Initialize PanPhon
ft = panphon.FeatureTable()


# Initialize Epitran for English
english_epi = Epitran('eng-Latn')

def english_to_ipa(text):
    """Converts English text to IPA using Epitran."""
    try:
        return english_epi.transliterate(text)
    except Exception as e:
        return f"Error: {e}"

# Initialize Epitran for Hindi
hindi_epi = Epitran('hin-Deva')

def hindi_to_ipa(text):
    """Converts Hindi text to IPA using Epitran."""
    try:
        return hindi_epi.transliterate(text)
    except Exception as e:
        return f"Error: {e}"
    

    # Specify the persistence directory
persist_directory = "Vdb1(60k)"
os.makedirs(persist_directory, exist_ok=True)
client = chromadb.PersistentClient(path=persist_directory)

collection = client.get_collection("vdb_l2")

# Function to compute the average feature vector (same as before)
def ipa2vec(ipa):
    vectors = ft.word_to_vector_list(ipa, numeric=True)
    if not vectors:
        return np.ones(ft.num_features) * 0.1  # Handle empty vectors
    processed_vectors = np.array(vectors)
    avg_vector = np.mean(processed_vectors, axis=0)
    return avg_vector.tolist()  # ChromaDB needs lists


def embedder(names, pronunciations):
    """Adds pronunciations to the ChromaDB collection."""

    if len(names) != len(pronunciations):
        raise ValueError("Names and pronunciations lists must have the same length.")

    embeddings = [ipa2vec(ipa) for ipa in pronunciations]
    collection.add(
        documents=names,
        embeddings=embeddings,
        metadatas=[{"ipa": ipa} for ipa in pronunciations],  # Store IPA for reference
        ids=[str(i) for i in range(len(names))] # provide IDs to avoid issues
    )


def querrier(query_ipa, n_results=5):
    """Retrieves similar names from the ChromaDB vdb."""
    query_embedding = ipa2vec(query_ipa)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["distances", "metadatas", "documents"] #include additional data
    )
    return results
dst = panphon.distance.Distance()

def searchEngine(name):
    # prompt: so write code to input a name in english from the user, use the espeak -ng to convert it to ipa and then querry it

    # Get user input
    # name = input("Enter a name in English: ")

    # Convert the name to IPA
    ipa = english_to_ipa(name)

    print(f"The IPA representation of '{name}' is: {ipa}")

    # Query the ChromaDB collection
    results = querrier(ipa)
    print(results['documents'])
    print(results['metadatas'])
    print(results['distances'])
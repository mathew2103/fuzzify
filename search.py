from epitran import Epitran
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
    
    
import panphon
import panphon.distance
import numpy as np
from chromadb.config import Settings
from chromadb import Client
import chromadb
import os
ft = panphon.FeatureTable()

persist_directory = "Vdb(60k)epi"
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

def querrier(query_ipa, n_results=30, weight_chromadb=0.7, weight_edit_distance=0.3,cuttoff=0.7):
    """Retrieves similar names with combined ChromaDB and edit distance scoring."""
    query_embedding = ipa2vec(query_ipa)
    results = collection.query(
        query_embeddings=[query_embedding],
        include=["distances", "metadatas", "documents"]
    )
    dst = panphon.distance.Distance()
    # Calculate combined scores
    scores = []
    for i in range(len(results["documents"][0])):
        chromadb_distance = results["distances"][0][i]
        metadata = results["metadatas"][0][i]

        if metadata and "ipa" in metadata:
            edit_distance = dst.weighted_feature_edit_distance(query_ipa, metadata["ipa"])
            combined_score = weight_chromadb * chromadb_distance + weight_edit_distance * edit_distance
            if collection.name == "vdb_l2" and combined_score > cuttoff:
                continue  # Skip results with a combined score greater than cuttoff
            scores.append((i, combined_score))  # Store index and score

    # Sort by combined scores and select top results
    scores.sort(key=lambda item: item[1])  # Sort by score
    top_indices = [item[0] for item in scores[:n_results]]

    # Extract top results
    filtered_results = {
        "documents": [results["documents"][0][i] for i in top_indices],
        "metadatas": [results["metadatas"][0][i] for i in top_indices],
        "distances": [results["distances"][0][i] for i in top_indices],
    }
    return filtered_results
def detect_language(text):
    """Detects if the input text is Hindi or English."""
    if any('\u0900' <= char <= '\u097F' for char in text):
        return 'hindi'
    else:
        return 'english'

def search(name):
    # Detect the language of the input name
    language = detect_language(name)

    # Convert the name to IPA based on the detected language
    if language == 'hindi':
        ipa = hindi_to_ipa(name)
        cutoff = 1
    else:
        ipa = english_to_ipa(name)
        cutoff = 0.7

    print(f"The IPA representation of '{name}' is: {ipa}")

    # Query the ChromaDB collection
    results = querrier(ipa, cuttoff=cutoff)
    return results
#test:-

# namein=input()
# print(detect_language(namein))
# print(search(namein))
    # print(results['documents'])
    # print(results['metadatas'])
    # print(results['distances']) 
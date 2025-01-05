from epitran import Epitran
english_epi = Epitran('eng-Latn')
def english_to_ipa(text):
    try:
        return english_epi.transliterate(text)
    except Exception as e:
        return f"Error: {e}"
hindi_epi = Epitran('hin-Deva')
def hindi_to_ipa(text):
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
from panphon import distance
dst = distance.Distance()

from trans import *
# from alt_ipa import alt_ipa
import uuid


persist_directory = "Vdb(epi)"
os.makedirs(persist_directory, exist_ok=True)
client = chromadb.PersistentClient(path=persist_directory)


collection = client.get_collection("200k_single_hindi_cosine_today")
# collection = client.get_collection("vdb_277k_fullname_cosine")
# Get the total number of documents in the collection
total_documents = collection.count()
print(f"Total number of documents in the collection: {total_documents}")

def ipa2vec(ipa):
    vectors = ft.word_to_vector_list(ipa, numeric=True)
    if not vectors:
        return np.ones(ft.num_features) * 0.1  # Handle empty vectors
    processed_vectors = np.array(vectors)
    avg_vector = np.mean(processed_vectors, axis=0)
    return avg_vector.tolist()  # ChromaDB needs lists


def detect_language(text):
    """Detects if the input text is Hindi or English."""
    if any('\u0900' <= char <= '\u097F' for char in text):
        return 'hindi'
    else:
        return 'english'
 
    
def querrier(name, n_results=50, weight_chromadb=0.7, weight_edit_distance=0.3, cutoff=0.6):
    """Retrieves similar names with combined ChromaDB and edit distance scoring."""
    language = detect_language(name)
    if language == 'hindi':
        query_ipa = hindi_to_ipa(name)
        query_ipa = english_to_ipa(trans_hindi_to_english(name))
        # alt_ipa_list = alt_ipa(query_ipa)
    else:
        query_ipa = english_to_ipa(name)
        # alt_ipa_list = alt_ipa(name)
    # print(f"alt_ipa_list: {alt_ipa_list}")
    all_scores = []

    # Process the main query IPA first:-
    main_query_embedding = ipa2vec(query_ipa)
    main_results = collection.query(
        query_embeddings=[main_query_embedding],
        n_results=n_results,
        include=["distances", "metadatas", "documents"]
    )
    for i in range(len(main_results["documents"][0])):
        chromadb_distance = main_results["distances"][0][i]
        metadata = main_results["metadatas"][0][i]
        doc_id = main_results["ids"][0][i]
        edit_distance = dst.weighted_feature_edit_distance(query_ipa, metadata["ipa"])
        combined_score = weight_chromadb * chromadb_distance + weight_edit_distance * edit_distance
        if combined_score > cutoff:
            continue  # Skip results with a combined score greater than cutoff
        all_scores.append((main_results["documents"][0][i], metadata, chromadb_distance, combined_score, doc_id))
        print(f"Document: {main_results['documents'][0][i]}, ChromaDB Distance: {chromadb_distance}, Combined Score: {combined_score}, Weighted Edit Distance: {edit_distance}, ID: {doc_id}")
    # Process alternate IPAs:-
    # weight_edit_distance=0
    # weight_chromadb=1
    # cutoff=0.003
    # for alt_ipa_item in alt_ipa_list:
    #     alt_query_embedding = ipa2vec(alt_ipa_item)
    #     alt_results = collection.query(
    #         query_embeddings=[alt_query_embedding],
    #         n_results=n_results,
    #         include=["distances", "metadatas", "documents"]
    # #     )
    #     for i in range(len(alt_results["documents"][0])):
    #         chromadb_distance = alt_results["distances"][0][i]
    #         metadata = alt_results["metadatas"][0][i]
    #         edit_distance = dst.weighted_feature_edit_distance(alt_ipa_item, metadata["ipa"])
    #         combined_score = weight_chromadb * chromadb_distance + weight_edit_distance * edit_distance
    #         # if combined_score > cutoff:
    #         #     continue  # Skip results with a combined score greater than cutoff
    #         all_scores.append((alt_results["documents"][0][i], metadata, chromadb_distance, combined_score))
    #         print(f"altDocument: {alt_results['documents'][0][i]}, ChromaDB Distance: {chromadb_distance}, Combined Score: {combined_score}, Weighted Edit Distance: {edit_distance}")
    # Sort all combined results by chromadb_distance (ascending order)
    all_scores.sort(key=lambda item: item[2])  # Sort by chromadb_distance

    # Extract top results
    filtered_results = {
        "documents": [item[0] for item in all_scores],
        "metadatas": [item[1] for item in all_scores],
        "distances": [item[2] for item in all_scores],
        "ids": [item[4] for item in all_scores],
    }
    # Remove duplicate elements in filtered_results:-
    unique_documents = []
    unique_metadatas = []
    unique_distances = []
    unique_ids = []

    for doc, meta, dist, doc_id in zip(filtered_results["documents"], filtered_results["metadatas"], filtered_results["distances"], filtered_results["ids"]):
        if doc not in unique_documents:
            unique_documents.append(doc)
            unique_metadatas.append(meta)
            unique_distances.append(dist)
            unique_ids.append(doc_id)

    filtered_results["documents"] = unique_documents
    filtered_results["metadatas"] = unique_metadatas
    filtered_results["distances"] = unique_distances
    filtered_results["ids"] = unique_ids
    return filtered_results


def search(name):
    results = querrier(name)
    return results

def add(document,metadata):
    language = detect_language(document)
    name_parts = document.split()
    for part in name_parts:
        if len(part) > 2:
            if language == 'hindi':
                part_ipa = hindi_to_ipa(part)
            else:
                part_ipa = english_to_ipa(part)
            
            part_embedding = ipa2vec(part_ipa)
            part_id = str(uuid.uuid4())
            
            part_metadata = metadata.copy()
            part_metadata["ipa"] = part_ipa  # Add IPA to metadata
            part_metadata["part"] = part  # Add part to metadata
            
            collection.add(
                documents=[document],
                metadatas=[part_metadata],
                ids=[part_id],
                embeddings=[part_embedding]
            )
            return part_id
def edit(doc_id, updated_document, updated_metadata):
    language = detect_language(updated_document)
    name_parts = updated_document.split()
    for part in name_parts:
        if len(part) > 2:
            if language == 'hindi':
                part_ipa = hindi_to_ipa(part)
            else:
                part_ipa = english_to_ipa(part)
            
            part_embedding = ipa2vec(part_ipa)
            
            updated_metadata["ipa"] = part_ipa  # Add IPA to metadata
            updated_metadata["part"] = part  # Add part to metadata
            
            collection.update(
                ids=[doc_id],
                documents=[updated_document],
                metadatas=[updated_metadata],
                embeddings=[part_embedding]
            )
def delete(doc_id):
    collection.delete(ids=[doc_id])
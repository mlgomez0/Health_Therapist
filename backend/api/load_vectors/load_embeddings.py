import os
import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModel
import chromadb
import sys

def create_chroma_db(embedding_name, dataset_path, persist_directory, collection_name):
    print("Loading model and tokenizer...")
    # Load the model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(embedding_name)
    model = AutoModel.from_pretrained(embedding_name)

    # Function to get embeddings in batches
    def get_embeddings(texts, batch_size=32):
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            inputs = tokenizer(batch_texts, padding=True, truncation=True, return_tensors="pt")
            with torch.no_grad():
                outputs = model(**inputs)
            batch_embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
            embeddings.append(batch_embeddings)
            print(f"Processed batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size}")
        return np.vstack(embeddings)

    print("Loading dataset...")

    # Load dataset from CSV
    df = pd.read_csv(dataset_path)

    # Check if 'Context' and 'Response' columns exist
    if 'Context' not in df.columns or 'Response' not in df.columns:
        raise ValueError("CSV file must contain 'Context' and 'Response' columns.")

    # Extract 'context' and 'response' columns
    contexts = df['Context'].tolist()
    responses = df['Response'].tolist()

    print("Getting embeddings for the contexts...")
    # Get embeddings for the contexts
    context_embeddings = get_embeddings(contexts, batch_size=32)

    print(f"Context embeddings shape: {context_embeddings.shape}")

    # Initialize ChromaDB client with SQLite persistence

    client = chromadb.PersistentClient(path=persist_directory)

    try:
        print(f"Creating collection {collection_name}...")
        collection = client.create_collection(collection_name)
        print(f"Collection {collection_name} created.")
    except ValueError:
        print(f"Collection {collection_name} already exists, fetching the collection...")
        collection = client.get_collection(collection_name)
        print(f"Fetched existing collection {collection_name}.")

    print("Saving data into ChromaDB...")
    # Prepare data to add to ChromaDB
    ids = [str(i) for i in range(len(contexts))]
    embeddings = [embedding.tolist() for embedding in context_embeddings]

    # Add data to ChromaDB collection
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=[{"context": context, "response": response} for context, response in zip(contexts, responses)]
    )

    print("Vector store created successfully.")

    # Verify persistence by listing all collections
    print("Listing all collections...")
    collections = client.list_collections()
    print("Available collections:", collections)

if __name__ == "__main__":
    embedding_name = os.getenv('EMBEDDING_NAME')
    dataset_path = os.getenv('DATASET_PATH')
    persist_directory = os.getenv('PERSIST_DIRECTORY')
    collection_name = os.getenv('COLLECTION_NAME')

    if not all([embedding_name, dataset_path, persist_directory, collection_name]):
        print("Error: Please set the EMBEDDING_NAME, DATASET_PATH, PERSIST_DIRECTORY, and COLLECTION_NAME environment variables.")
        sys.exit(1)

    create_chroma_db(embedding_name, dataset_path, persist_directory, collection_name)
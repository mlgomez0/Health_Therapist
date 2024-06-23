import os
import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch
import chromadb
from chromadb.config import Settings

class CreateVectorStore:
    """
    A class for creating and managing a vector store using ChromaDB and a transformer model.

    Attributes:
        tokenizer (AutoTokenizer): The tokenizer for the transformer model.
        model (AutoModel): The transformer model for generating embeddings.
        settings (Settings): The settings for ChromaDB client.
        client (chromadb.Client): The ChromaDB client.
        collection_name (str): The name of the collection in ChromaDB.
        collection (chromadb.Collection): The collection object in ChromaDB.
    """

    def __init__(self, model_name, persist_directory, collection_name):
        """
        Initializes the CreateVectorStore with the specified model and ChromaDB settings.

        Args:
            model_name (str): The name of the transformer model to use.
            persist_directory (str): The directory for ChromaDB persistence.
            collection_name (str): The name of the collection in ChromaDB.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.settings = Settings(persist_directory=persist_directory)
        self.client = chromadb.Client(settings=self.settings)
        self.collection_name = collection_name
        self.collection = self._create_or_get_collection()

    def _create_or_get_collection(self):
        """
        Creates a new collection or retrieves an existing collection from ChromaDB.

        Returns:
            chromadb.Collection: The collection object.

        Raises:
            ValueError: If the collection cannot be created or retrieved.
        """
        if not os.path.exists(self.settings.persist_directory):
            os.makedirs(self.settings.persist_directory)
            print(f"Created {self.settings.persist_directory} directory.")

        try:
            print(f"Creating collection '{self.collection_name}'...")
            collection = self.client.create_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' created.")
        except ValueError:
            print(f"Collection '{self.collection_name}' already exists, fetching the collection...")
            collection = self.client.get_collection(self.collection_name)
            print(f"Fetched existing collection '{self.collection_name}'.")
        return collection

    def get_embeddings(self, texts, batch_size=32):
        """
        Generates embeddings for a list of texts using the transformer model in batches.

        Args:
            texts (list of str): The list of texts to generate embeddings for.
            batch_size (int): The batch size for processing texts.

        Returns:
            np.ndarray: The generated embeddings.
        """
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            inputs = self.tokenizer(batch_texts, padding=True, truncation=True, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model(**inputs)
            batch_embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
            embeddings.append(batch_embeddings)
            print(f"Processed batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size}")
        return np.vstack(embeddings)

    def load_dataset(self, csv_path):
        """
        Loads the dataset from a CSV file.

        Args:
            csv_path (str): The path to the CSV file.

        Returns:
            tuple: A tuple containing lists of contexts and responses.

        Raises:
            ValueError: If the CSV file does not contain 'Context' and 'Response' columns.
        """
        df = pd.read_csv(csv_path)
        if 'Context' not in df.columns or 'Response' not in df.columns:
            raise ValueError("CSV file must contain 'Context' and 'Response' columns.")
        contexts = df['Context'].tolist()
        responses = df['Response'].tolist()
        return contexts, responses

    def add_data_to_collection(self, contexts, responses):
        """
        Adds context-response pairs to the collection with their embeddings.

        Args:
            contexts (list of str): The list of context texts.
            responses (list of str): The list of response texts.
        """
        context_embeddings = self.get_embeddings(contexts, batch_size=32)
        ids = [str(i) for i in range(len(contexts))]
        embeddings = [embedding.tolist() for embedding in context_embeddings]
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=[{"context": context, "response": response} for context, response in zip(contexts, responses)]
        )
        print("Data added to the collection successfully.")

    def list_collections(self):
        """
        Lists all collections in ChromaDB.

        Returns:
            list: A list of collection names.
        """
        collections = self.client.list_collections()
        return collections

if __name__ == "__main__":
    handler = CreateVectorStore(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        persist_directory="./chromadb_store",
        collection_name="context_response_store"
    )
    # Load dataset
    contexts, responses = handler.load_dataset(r"C:\Users\ashp2\Health_Therapist\backend\ml_models\datasets\dataset.csv")
    # Add data to collection
    handler.add_data_to_collection(contexts, responses)
    # List all collections
    collections = handler.list_collections()
    print("Available collections:", collections)
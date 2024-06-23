import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
import chromadb
from chromadb.config import Settings

class SimilaritySearch:
    """
    A class for performing similarity searches using embeddings and ChromaDB.

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
        Initializes the SimilaritySearch with the specified model and ChromaDB settings.

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
        self.collection = self._get_collection()

    def _get_collection(self):
        """
        Retrieves the specified collection from ChromaDB.

        Returns:
            chromadb.Collection: The collection object.

        Raises:
            ValueError: If the collection does not exist.
        """
        try:
            print(f"Fetching collection '{self.collection_name}'...")
            collection = self.client.get_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' retrieved successfully.")
            return collection
        except ValueError:
            raise ValueError(f"Collection '{self.collection_name}' does not exist. Make sure to run create_vector_store.py first.")

    def get_embeddings(self, texts):
        """
        Generates embeddings for a list of texts using the transformer model.

        Args:
            texts (list of str): The list of texts to generate embeddings for.

        Returns:
            np.ndarray: The generated embeddings.
        """
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
        return embeddings

    def retrieve_responses(self, query, k=3):
        """
        Retrieves the top k responses based on the similarity of the query to the stored contexts.

        Args:
            query (str): The query text.
            k (int): The number of top responses to retrieve.

        Returns:
            list of str: The list of top k responses.
        """
        query_embedding = self.get_embeddings([query])[0]
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=k
        )
        print("Query results:", results)  # Debugging line
        similar_responses = [metadata['response'] for metadata_list in results["metadatas"] for metadata in metadata_list]
        return similar_responses

    def interactive_query(self):
        """
        Starts an interactive query session where the user can input queries and retrieve responses.
        """
        while True:
            query = input("Please enter your search query (type 'exit' to quit): ")
            if query.lower() == "exit":
                break
            top_responses = self.retrieve_responses(query)
            print(f"\nTop {len(top_responses)} responses for '{query}':")
            for i, response in enumerate(top_responses, start=1):
                print(f"{i}. {response}")

if __name__ == "__main__":
    handler = SimilaritySearch(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        persist_directory="./chromadb_store",
        collection_name="context_response_store"
    )
    handler.interactive_query()
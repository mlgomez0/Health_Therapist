from transformers import AutoTokenizer, AutoModel
import torch
import chromadb
import os

class SimilaritySearcher:
    """
    A class to perform similarity search using embeddings from a pre-trained model and ChromaDB.

    Methods
    -------
    get_embeddings(texts, tokenizer, model):
        Generates embeddings for a list of texts using the provided tokenizer and model.

    do_similarity_search_chroma(query, collection_name, embedding_name, chroma_db_path, k=3):
        Performs a similarity search on a specified ChromaDB collection using the provided query.
    """

    def get_embeddings(self, texts, tokenizer, model):
        """
        Generates embeddings for a list of texts using the provided tokenizer and model.

        Parameters
        ----------
        texts : list of str
            The list of texts to be embedded.
        tokenizer : transformers.AutoTokenizer
            The tokenizer to preprocess the texts.
        model : transformers.AutoModel
            The model to generate the embeddings.

        Returns
        -------
        np.ndarray
            An array of embeddings for the provided texts.
        """
        inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
        return embeddings

    def do_similarity_search_chroma(self, query, collection_name, embedding_name, chroma_db_path, k=3):
        """
        Performs a similarity search on a specified ChromaDB collection using the provided query.

        Parameters
        ----------
        query : str
            The query text to search for similar responses.
        collection_name : str
            The name of the ChromaDB collection to search in.
        embedding_name : str
            The name of the pre-trained embedding model to use.
        chroma_db_path : str
            The path to the ChromaDB database.
        k : int, optional
            The number of similar responses to return (default is 3).

        Returns
        -------
        list of dict
            A list of dictionaries containing similar contexts and responses.
        
        Raises
        ------
        FileNotFoundError
            If the specified ChromaDB path does not exist.
        ValueError
            If the specified collection does not exist in ChromaDB.
        """
        # Load the model and tokenizer
        print("Loading model and tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(embedding_name)
        model = AutoModel.from_pretrained(embedding_name)

        # Initialize ChromaDB client with SQLite persistence
        if not os.path.exists(chroma_db_path):
            raise FileNotFoundError(f"Database path does not exist: {chroma_db_path}")

        client = chromadb.PersistentClient(path=chroma_db_path)

        # Ensure the collection exists
        try:
            print(f"Fetching collection {collection_name}...")
            collection = client.get_collection(collection_name)
            print(f"Collection {collection_name} retrieved successfully.")
        except ValueError as e:
            raise ValueError(f"{collection_name} does not exist: {e}")

        # Get the embedding for the query
        query_embedding = self.get_embeddings([query], tokenizer, model)[0]

        # Perform the query on the collection
        results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=k
        )
        print("Query results:", results)  # Debugging line

        # Extract the similar contexts and responses
        similar_responses = [
            {"Context": metadata['context'], "Response": metadata['response']}
            for metadata_list in results["metadatas"] for metadata in metadata_list
        ]
        return similar_responses

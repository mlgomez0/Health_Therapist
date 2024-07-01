import os
import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch
import chromadb
from chromadb.config import Settings

class PromptTemplate:
    def __init__(self, similarity_search):
        self.similarity_search = similarity_search

    def one_shot(self, query):
        examples = self.similarity_search(query, num_examples=1)
        return self._format_prompt(query, examples)

    def two_shot(self, query):
        examples = self.similarity_search(query, num_examples=2)
        return self._format_prompt(query, examples)

    def few_shot(self, query):
        examples = self.similarity_search(query, num_examples=3)
        return self._format_prompt(query, examples)
    
    def _format_prompt(self, query, examples):
        formatted_examples = "\n".join(
            [f"Example {i+1}:\nContext: {ex['Context']}\nResponse: {ex['Response']}\n" for i, ex in enumerate(examples)]
        )
        response = "\n".join(
            [f"{ex['Response']}\n" for i, ex in enumerate(examples)]
        )
        #return f"Query: {query}\n\n{formatted_examples}"
        return response

class Rag():

    def __init__(self) -> None:

        print("Loading model and tokenizer...")
        # Load the model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

        # Function to get embeddings in batches
        def get_embeddings(texts, batch_size=10):
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

        # Upload dataset to Colab
        #from google.colab import files
        #uploaded = files.upload()

        # Load dataset from CSV
        #df = pd.read_csv(next(iter("combined_data.csv")))
        parent_dir1 = os.path.abspath(os.path.join(os.path.dirname(__file__), './'))
        df = pd.read_csv(r"%s\combined_data.csv"%parent_dir1)

        # Check if 'Context' and 'Response' columns exist
        if 'Context' not in df.columns or 'Response' not in df.columns:
            raise ValueError("CSV file must contain 'Context' and 'Response' columns.")

        # Extract 'context' and 'response' columns
        contexts = df['Context'].tolist()[:166]
        responses = df['Response'].tolist()[:166]

        print("Getting embeddings for the contexts...")
        # Get embeddings for the contexts
        context_embeddings = get_embeddings(contexts, batch_size=10)

        print(f"Context embeddings shape: {context_embeddings.shape}")

        # Initialize ChromaDB client with SQLite persistence
        settings = Settings(persist_directory="./chromadb_store")
        client = chromadb.Client(settings=settings)

        try:
            print("Creating collection 'context_response_store'...")
            collection = client.create_collection("context_response_store")
            print("Collection 'context_response_store' created.")
        except ValueError:
            print("Collection 'context_response_store' already exists, fetching the collection...")
            collection = client.get_collection("context_response_store")
            print("Fetched existing collection 'context_response_store'.")

        print("Saving contexts, responses, and embeddings to ChromaDB...")
        # Prepare data to add to ChromaDB
        ids = [str(i) for i in range(len(contexts))]
        #ids = [str(i) for i in range(160)]
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

        # Load the model and tokenizer
        print("Loading model and tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

        # Initialize ChromaDB client with SQLite persistence
        settings = Settings(persist_directory="./chromadb_store")
        client = chromadb.Client(settings=settings)

        # Ensure the collection exists
        try:
            print("Fetching collection 'context_response_store'...")
            collection = client.get_collection("context_response_store")
            print("Collection 'context_response_store' retrieved successfully.")
        except ValueError:
            raise ValueError("Collection 'context_response_store' does not exist. Make sure to run create_vector_store.py first.")



        # Function to get embeddings for a list of texts
        def get_embeddings(texts):
            inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
            with torch.no_grad():
                outputs = model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
            return embeddings

        # Function to retrieve top k responses based on similar context
        def retrieve_responses(query, collection, k=3):
            query_embedding = get_embeddings([query])[0]
            results = collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=k
            )
            #print("Query results:", results)  # Debugging line
            similar_responses = [
                {"Context": metadata['context'], "Response": metadata['response']}
                for metadata_list in results["metadatas"] for metadata in metadata_list
            ]
            return similar_responses
        
        self.prompt_template = PromptTemplate(lambda query, num_examples: retrieve_responses(query, collection, k=num_examples))

    def predict(self, conversation_id: str, user_input: str) -> str:

        # Create an instance of the PromptTemplate class with the retrieve_responses function
        
        # Test the one_shot, two_shot, and few_shot methods
        query = user_input
        one_shot_result = self.prompt_template.one_shot(query)

        print("\n\n\n",one_shot_result)
        return one_shot_result

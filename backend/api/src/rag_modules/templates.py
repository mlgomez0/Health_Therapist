from .similarity_search import SimilaritySearcher
import os

class PromptTemplate:
    """
    A class to generate prompt templates for a mental health therapy application.

    Attributes:
    -----------
    embedding_name : str
        The name of the embedding model.
    chromadb_path : str
        The path to the Chroma database directory.
    collection_name : str
        The name of the collection in the Chroma database.
    similarity_searcher : SimilaritySearcher
        An instance of the SimilaritySearcher class used for performing similarity searches.

    Methods:
    --------
    one_shot(query: str) -> str
        Generates a one-shot prompt based on the provided query.
    two_shot(query: str) -> str
        Generates a two-shot prompt based on the provided query.
    few_shot(query: str) -> str
        Generates a few-shot prompt based on the provided query.
    _format_prompt(query: str, examples: list) -> str
        Formats the final prompt by combining the query with retrieved examples.
    """
    def __init__(self):
        """
        Initializes the PromptTemplate class by loading environment variables and 
        setting up the attributes for embedding name, Chroma database path, 
        collection name, and similarity searcher.
        """
        self.embedding_name = os.getenv('EMBEDDING_NAME')
        self.chromadb_path = os.getenv('CHROMA_DB_DIR')
        self.collection_name = os.getenv('COLLECTION_NAME')
        self.similarity_searcher = SimilaritySearcher()

    def one_shot(self, query):
        """
        Generates a one-shot prompt based on the provided query.

        Parameters:
        -----------
        query : str
            The input query for which a one-shot prompt is to be generated.

        Returns:
        --------
        str
            The formatted one-shot prompt.
        """
        examples = self.similarity_searcher.do_similarity_search_chroma(
                query, self.collection_name, self.embedding_name, self.chromadb_path, k=1)
        return self._format_prompt(examples)

    def two_shot(self, query):
        """
        Generates a two-shot prompt based on the provided query.

        Parameters:
        -----------
        query : str
            The input query for which a two-shot prompt is to be generated.

        Returns:
        --------
        str
            The formatted two-shot prompt.
        """
        examples = self.similarity_searcher.do_similarity_search_chroma(
                query, self.collection_name, self.embedding_name, self.chromadb_path, k=2)
        return self._format_prompt(examples)

    def few_shot(self, query):
        """
        Generates a few-shot prompt based on the provided query.

        Parameters:
        -----------
        query : str
            The input query for which a few-shot prompt is to be generated.

        Returns:
        --------
        str
            The formatted few-shot prompt.
        """
        examples = self.similarity_searcher.do_similarity_search_chroma(
                query, self.collection_name, self.embedding_name, self.chromadb_path, k=3)
        return self._format_prompt(examples)
    
    def _format_prompt(self, examples):
        """
        Formats the final prompt by combining the query with retrieved examples.

        Parameters:
        -----------
        query : str
            The input query to be included in the final prompt.
        examples : list
            A list of examples retrieved from the similarity search.

        Returns:
        --------
        str
            The final formatted prompt ready for use.
        """

        formatted_examples = "You are a mental health therapist. Please use the following examples to provide a thoughtful and supportive response\n" + "\n".join(
            [f"<|user|>\n{ex['Context']}<|end|>\n<|assistant|>\n{ex['Response']}<|end|>\n" for ex in examples]
        )
        return formatted_examples
    
    def zero_shot(self, query):
        """
        Generates a one-shot prompt based on the provided query.

        Parameters:
        -----------
        query : str
            The input query for which a one-shot prompt is to be generated.

        Returns:
        --------
        str
            The formatted one-shot prompt.
        """
        
        return self._format_prompt(query, [])
    


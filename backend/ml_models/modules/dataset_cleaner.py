import re
import contractions

class DatasetCleaner:
    """
    A class used to clean text data within a dataset.

    Attributes
    ----------
    dataset : pandas.DataFrame
        The dataset containing the text data to be cleaned.
    columns : list of str
        The list of column names in the dataset that need to be cleaned.

    Methods
    -------
    clean_text(text)
        Cleans a single text entry by fixing contractions, removing special characters and digits, removing extra whitespace, and converting to lowercase.
    clean_dataset()
        Cleans the specified columns of the dataset in place using the clean_text method.
    """

    def __init__(self, dataset, columns):
        """
        Parameters
        ----------
        dataset : pandas.DataFrame
            The dataset containing the text data to be cleaned.
        columns : list of str
            The list of column names in the dataset that need to be cleaned.
        """
        self.dataset = dataset
        self.columns = columns

    def clean_text(self, text):
        """
        Cleans a single text entry.

        This function performs the following operations on the input text:
        1. Fixes contractions (e.g., "can't" -> "cannot").
        2. Removes special characters and digits, leaving only alphabetic characters and spaces.
        3. Removes extra whitespace.
        4. Converts the text to lowercase.

        Parameters
        ----------
        text : str
            The text to be cleaned.

        Returns
        -------
        str
            The cleaned text.
        """
        # Fix contractions
        text = contractions.fix(text)
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Convert to lowercase
        text = text.lower()
        return text

    def clean_dataset(self):
        """
        Cleans the specified columns of the dataset.

        This method applies the clean_text method to each entry in the specified columns of the dataset.
        The cleaning is performed in place, modifying the original dataset.

        Returns
        -------
        None
        """
        for col in self.columns:
            self.dataset[col] = self.dataset[col].apply(self.clean_text)
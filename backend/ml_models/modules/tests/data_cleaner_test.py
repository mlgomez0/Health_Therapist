import unittest
import pandas as pd
from backend.ml_models.modules.dataset_cleaner import DatasetCleaner

class TestDatasetCleaner(unittest.TestCase):

    def setUp(self):
        # Sample dataset for testing
        self.data = {
            'Context': [
                "I'm going through some things with my feelings and myself. I barely sleep and I do nothing but think about how I'm worthless and how I shouldn't be here.",
                "This is another context. It has some numbers 123 and symbols #@$!"
            ],
            'Response': [
                "If everyone thinks you're worthless, then maybe you need to find new people to hang out with.",
                "This is another response! It's simple but effective."
            ]
        }
        self.df = pd.DataFrame(self.data)
        self.columns_to_clean = ['Context', 'Response']
        self.cleaner = DatasetCleaner(self.df, self.columns_to_clean)

    def test_clean_text(self):
        text = "I'm so happy! Can't wait to see you. #excited"
        expected_output = "i am so happy cannot wait to see you excited"
        self.assertEqual(self.cleaner.clean_text(text), expected_output)

    def test_clean_dataset(self):
        self.cleaner.clean_dataset()
        cleaned_data = {
            'Context': [
                "i am going through some things with my feelings and myself i barely sleep and i do nothing but think about how i am worthless and how i should not be here",
                "this is another context it has some numbers and symbols"
            ],
            'Response': [
                "if everyone thinks you are worthless then maybe you need to find new people to hang out with",
                "this is another response it is simple but effective"
            ]
        }
        expected_df = pd.DataFrame(cleaned_data)
        pd.testing.assert_frame_equal(self.df, expected_df)

if __name__ == '__main__':
    unittest.main()
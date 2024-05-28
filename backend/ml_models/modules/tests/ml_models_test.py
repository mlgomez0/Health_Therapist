import unittest
from collections import defaultdict
from backend.ml_models.modules.model_tester import ModelTester

class TestModelTester(unittest.TestCase):
    def setUp(self):

        self.test_texts = [
            "The quick brown fox jumps over the lazy dog.",
        ]
        self.gen_texts = [
            "The quick brown fox jumps over a lazy dog.",
        ]

        # Instantiate ModelTester with dummy data
        self.model_tester = ModelTester(self.test_texts, self.gen_texts)

    def test_calculate_rouge_score(self):
        # Calculate ROUGE scores
        self.model_tester.calculate_rouge_score()

        # Expected results
        expected_results = {
            'rouge1': defaultdict(int, {'precision': 0.8888888888888888, 'recall': 0.8888888888888888, 'fmeasure': 0.8888888888888888}),
            'rouge2': defaultdict(int, {'precision': 0.75, 'recall': 0.75, 'fmeasure': 0.75}),
            'rougeL': defaultdict(int, {'precision': 0.8888888888888888, 'recall': 0.8888888888888888, 'fmeasure': 0.8888888888888888}),
        }

        # Compare the results
        for metric, scores in expected_results.items():
            for score_type, expected_value in scores.items():
                actual_value = self.model_tester.test_results[metric][score_type]
                self.assertAlmostEqual(actual_value, expected_value, places=4, msg=f"{metric} {score_type} not as expected")

if __name__ == '__main__':
    unittest.main()

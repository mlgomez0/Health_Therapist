from rouge_score import rouge_scorer
from collections import defaultdict

class ModelTester:
    def __init__(self, test_texts, gen_texts):
        self.test_texts = test_texts
        self.gen_texts = gen_texts
        self.test_results = defaultdict(lambda: defaultdict(int))
        self.length = len(test_texts)

    def calculate_rouge_score(self):
        for test_text, gen_text in zip(self.test_texts, self.gen_texts):
            scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
            scores = scorer.score(test_text, gen_text)
            for metric, score in scores.items():
              precision, recall, fmeasure = score
              self.test_results[metric]['precision'] += precision
              self.test_results[metric]['recall'] += recall
              self.test_results[metric]['fmeasure'] += fmeasure
            
        for metric, value in self.test_results.items():
          for k, v in value.items():
            self.test_results[metric][k] = v  / self.length




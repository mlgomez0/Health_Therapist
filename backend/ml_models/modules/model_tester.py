from rouge_score import rouge_scorer
from collections import defaultdict

class ModelTester:
    """
    A class used to calculate ROUGE scores for evaluating the quality of generated texts.

    Attributes
    ----------
    test_texts : list of str
        A list of reference texts to compare against.
    gen_texts : list of str
        A list of generated texts to be evaluated.
    test_results : defaultdict
        A nested dictionary storing accumulated ROUGE scores for precision, recall, and f-measure.
    length : int
        The number of texts being evaluated.

    Methods
    -------
    calculate_rouge_score():
        Calculates the ROUGE scores (precision, recall, and f-measure) for the generated texts
        against the reference texts and stores the average results in `test_results`.
    """

    def __init__(self, test_texts, gen_texts):
        """
        Parameters
        ----------
        test_texts : list of str
            A list of reference texts to compare against.
        gen_texts : list of str
            A list of generated texts to be evaluated.
        """
        self.test_texts = test_texts
        self.gen_texts = gen_texts
        self.test_results = defaultdict(lambda: defaultdict(int))
        self.length = len(test_texts)

    def calculate_rouge_score(self):
        """
        Calculates the ROUGE scores for the generated texts compared to the reference texts.

        This method calculates the ROUGE-1, ROUGE-2, and ROUGE-L scores for each pair of
        test_text and gen_text, accumulating the scores for precision, recall, and f-measure.
        It then averages the accumulated scores across all texts and stores them in `test_results`.

        Returns
        -------
        None
        """
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
                self.test_results[metric][k] = v / self.length

    def calculate_rouge_score_by_item(self):
        """
        Calculates the ROUGE scores for the generated texts compared to the reference texts.

        This method calculates the ROUGE-1, ROUGE-2, and ROUGE-L scores for each pair of
        test_text and gen_text, accumulating the scores for precision, recall, and f-measure.
        It then averages the accumulated scores across all texts and stores them in `test_results`.

        Returns
        -------
        dictionary
        """
        result = defaultdict(lambda: defaultdict(list))
   
        for test_text, gen_text in zip(self.test_texts, self.gen_texts):
            scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
            scores = scorer.score(test_text, gen_text)
            for metric, score in scores.items():
                precision, recall, fmeasure = score
                result[metric]['precision'].append(precision)
                result[metric]['recall'].append(recall)
                result[metric]['fmeasure'].append(fmeasure)
        return result
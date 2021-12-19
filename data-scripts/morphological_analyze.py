import json

from feature_extraction.morphological_analysis import Analyzer

if __name__ == "__main__":
    with open("data/normalized_books.json", 'r', encoding='utf-8') as f:
        books_data = json.load(f)["books"]

    analyzer = Analyzer(use_transformer=False)
    analyzer.analyze(books_data, "data")
import json

from feature_extraction.vectorize import make_pos_featured_data, tf_idf_vectorize

if __name__ == "__main__":
    with open("data/analyzed_data.json", 'r', encoding='utf-8') as f:
        books_data = json.load(f)

    make_pos_featured_data(books_data, "data")
    tf_idf_vectorize(books_data, "data")
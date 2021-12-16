"""
books.json からテキストデータを以下のように配置しなおす
    output_root
        author1
            novel1.txt
            novel2.txt
        author2
            novel1.txt
"""

import json
import os

def books_json_to_each_novels(books_json_path: str, output_root: str) -> None:
    with open(books_json_path, 'r', encoding='utf-8') as f:
        books_data = json.load(f)["books"]

    for book_info in books_data:
        author_name = book_info["authors"][0]["full_name"]
        output_dir = os.path.join(output_root, author_name)
        os.makedirs(output_dir, exist_ok=True)

        novel_name = book_info["title"]
        output_file_path = os.path.join(output_dir, novel_name+".txt")
        with open(output_file_path, "w", encoding='utf-8') as f:
            f.write(book_info["content"])

if __name__ == "__main__":
    books_json_to_each_novels("data/books.json", "data/plain_novels")
"""
books.json からテキストデータを以下のように配置しなおす
    output_root
        author1
            novel1.txt
            novel2.txt
        author2
            novel1.txt
"""

import random
import re
import json
import os

from shaping.cleaners import normalize_text

def _write_json(path, data:dict) -> None:
    with open(path, 'w', encoding='utf-8', errors='ignore') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def normalized_novels(books_json_path: str, output_root: str, min_text: int = 1000,  min_sent: int = 10, part_size: int = 5000, each_class_size: int = 150) -> None:
    space_pattern = re.compile(r"\s+")
    sent_pattern = re.compile(r"(?<=。)")
    author_dict = {}

    output_novel_root = os.path.join(output_root, "normalized_novels")
    normalized_books_json = []
    with open(books_json_path, 'r', encoding='utf-8') as f:
        books_data = json.load(f)["books"]

    for book_info in books_data:
        author_name = book_info["authors"][0]["full_name"]
        output_dir = os.path.join(output_novel_root, author_name)
        os.makedirs(output_dir, exist_ok=True)

        book_text = normalize_text(book_info["content"])

        # 文字数が少ないものを除外
        if len(book_text) < min_text:
            continue

        # 一定数、句読点がないものを除外
        book_sents = sent_pattern.split(book_text)
        if len(book_sents) < min_sent:
            continue

        # save text
        novel_name = book_info["title"]
        output_file_path = os.path.join(output_dir, novel_name+".txt")
        with open(output_file_path, "w", encoding='utf-8') as f:
            f.write(book_text)

        if author_name not in author_dict:
            author_dict[author_name] = len(author_dict)

        # いくつかに分割して格納
        part_n = 0
        part_content = ""
        for sent in book_sents:
            part_content += sent

            if len(part_content) >= part_size:
                normalized_books_json.append({
                    "id": book_info["id"],
                    "title": novel_name,
                    "author": author_name,
                    "author_id": author_dict[author_name],
                    "part_n": part_n,
                    "content": space_pattern.sub("", part_content)
                })
                part_content = ""
                part_n += 1

    # 各著者のデータの数を整える
    author_books = {}
    for book_info in normalized_books_json:
        if book_info["author_id"] not in author_books:
            author_books[book_info["author_id"]] = [book_info, ]
        else:
            author_books[book_info["author_id"]].append(book_info)

    for author_key in author_books.keys():
        random.shuffle(author_books[author_key])
        author_books[author_key] = author_books[author_key][:each_class_size]

    normalized_books_json = sum(author_books.values(), [])

    # save json
    output_json_path = os.path.join(output_root, "normalized_books.json")
    _write_json(output_json_path, {"books": normalized_books_json})

if __name__ == "__main__":
    normalized_novels("data/books.json", "data", 2000, 10, 5000, 150)
import json
import re
import os
from typing import List

import spacy

def _write_json(path, data:dict) -> None:
    with open(path, 'w', encoding='utf-8', errors='ignore') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


class Analyzer:
    def __init__(self, use_transformer: bool = True) -> None:
        if use_transformer:
            self.nlp = spacy.load("ja_ginza_electra")
        else:
            self.nlp = spacy.load("ja_ginza")
        self.books_data = []

    def analyze(self, books_data: List[dict], output_root: str) -> None:
        print("start analyzer")
        self.books_data = books_data
        contents_list: List[str] = list(map(lambda x: x["content"], self.books_data))

        tags_json = []

        not_hiragana = re.compile(r"[^ぁ-ゟ]+")
        not_katakana = re.compile(r"[^゠-ヿ]+")

        output_json_path = os.path.join(output_root, "analyzed_data.json")

        i = 0
        parallel_n = 50
        content_i = parallel_n
        save_n = 100
        while content_i <= len(contents_list):
            print(f"process... [{content_i-parallel_n}:{content_i}]")
            docs = self.nlp.pipe(contents_list[content_i-parallel_n: content_i])
            for book_info, doc in zip(self.books_data[content_i-parallel_n:content_i], docs):
                doc_text = str(doc)

                hiragana_n = len(not_hiragana.sub("", doc_text))
                katakana_n = len(not_katakana.sub("", doc_text))

                words = [str(token) for sent in doc.sents for token in sent]
                tags = [str(token.tag_) for sent in doc.sents for token in sent]
                lemmas = [str(token.lemma_) for sent in doc.sents for token in sent]

                tags_json.append({
                    "id": book_info["id"],
                    "title": book_info["title"],
                    "author": book_info["author"],
                    "author_id": book_info["author_id"],
                    "part_n": book_info["part_n"],
                    "hiragana_n": hiragana_n,
                    "katakana_n": katakana_n,
                    "words": ' '.join(words),
                    "tags": ' '.join(tags),
                    "lemmas": ' '.join(lemmas),
                })
                i += 1

                if i % save_n == 0:
                    print(f"save: i={i}")
                    _write_json(output_json_path, tags_json)
            content_i += parallel_n

        print(f"save: i={i}")
        _write_json(output_json_path, tags_json)

        print("done")


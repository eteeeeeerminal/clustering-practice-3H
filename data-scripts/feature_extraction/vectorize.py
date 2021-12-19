import re
import os
from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def count_pos(tokens: List[str]) -> List[int]:
    pos_dict = {
        "名詞": 0,
        "動詞": 0,
        "助詞": 0,
        "助動詞": 0,
        "補助記号": 0,
        "総単語数": len(tokens),
    }
    for token in tokens:
        if token in pos_dict:
            pos_dict[token] += 1

    return list(pos_dict.values())

def make_pos_featured_data(books_data: List[dict], output_dir: str):
    header = [
        "作品名", "作品番号", "part_id", "作家名", "作家番号",
        "ひらがなの数", "カタカナの数", "総文字数",
        "名詞", "動詞", "助詞", "助動詞", "補助記号", "総単語数",
    ]
    ratio_header = [
        "作品名", "作品番号", "part_id", "作家名", "作家番号",
        "総文字数", "総単語数",
        "ひらがな率", "カタカナ率",
        "名詞率", "動詞率", "助詞率", "助動詞率", "補助記号率",
    ]

    first_tag_pattern = re.compile(r"-.+")
    data_rows: List[str] = []
    ratio_data_rows: List[str] = []
    for book in books_data:
        tags = book["tags"].split()
        tags = list(map(lambda x: first_tag_pattern.sub("", x), tags))

        pos_count_list = count_pos(tags)
        char_n = len(book["words"].replace(" ", ""))
        data_row = [
            book["title"], book["id"], book["part_n"], book["author"], book["author_id"],
            book["hiragana_n"], book["katakana_n"], char_n,
        ] + pos_count_list
        data_row = map(str, data_row)
        data_row = '\t'.join(data_row)

        data_rows.append(data_row)

        # 比率版
        word_n = pos_count_list[-1]
        pos_count_ratios = [pc / word_n for pc in pos_count_list]
        ratio_data_row = [
            book["title"], book["id"], book["part_n"], book["author"], book["author_id"],
            char_n, word_n,
            book["hiragana_n"]/char_n, book["katakana_n"]/char_n,
        ] + pos_count_ratios[:-1]
        ratio_data_row = map(str, ratio_data_row)
        ratio_data_row = '\t'.join(ratio_data_row)

        ratio_data_rows.append(ratio_data_row)

    output_tsv_path = os.path.join(output_dir, "pos_featured.tsv")
    with open(output_tsv_path, 'w', encoding="utf-8") as f:
        f.write('\t'.join(header) + '\n')
        f.write('\n'.join(data_rows) + '\n')

    output_tsv_path = os.path.join(output_dir, "pos_ratio_featured.tsv")
    with open(output_tsv_path, 'w', encoding="utf-8") as f:
        f.write('\t'.join(ratio_header) + '\n')
        f.write('\n'.join(ratio_data_rows) + '\n')


def normalize_lemmas(tags: str, lemmas: str) -> str:
    tags = tags.split()
    lemmas = lemmas.split()

    normalized_lemmas = []
    for tag, lemma in zip(tags, lemmas):
        # 短すぎるものと長過ぎるものを削除
        if len(lemma) <= 1 or len(lemma) >= 15:
            continue
        if re.sub(r"-.+", "", tag) in ("補助記号", "助詞", "助動詞"):
            continue
        # 英数字を含む
        if len(re.sub(r"[^0-9a-zA-Z]+", "", lemma)) > 0:
            continue
        normalized_lemmas.append(lemma)

    return " ".join(normalized_lemmas)

def tf_idf_vectorize(books_data: List[dict], output_dir: str):
    all_lemmas = list(map(lambda x: normalize_lemmas(x["tags"], x["lemmas"]), books_data))
    author_ids = np.array([list(map(lambda x: x["author_id"], books_data)), ])

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(all_lemmas)
    tf_idf_array = X.toarray()

    output_tsv_path = os.path.join(output_dir, "tf_idf_featured.tsv")
    print(vectorizer.get_feature_names_out())
    print(len(vectorizer.get_feature_names_out()))

    tf_idf_array = np.hstack((author_ids.T, tf_idf_array))
    np.savetxt(output_tsv_path, tf_idf_array, delimiter='\t', header= "author_id\t" + '\t'.join(vectorizer.get_feature_names_out()), encoding='utf-8')
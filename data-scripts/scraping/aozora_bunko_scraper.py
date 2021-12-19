import os
import time
import json

from .aozora_bunko_api import AozoraBunkoAPI

def _write_json(path, data:dict) -> None:
    with open(path, 'w', encoding='utf-8', errors='ignore') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

class AozoraBunkoScraper:

    SLEEP_TIME = 5

    def __init__(self, save_dir) -> None:
        self.aozorapi = AozoraBunkoAPI()
        self.save_dir = save_dir
        self.gotton_books = []

    def get_theauthor_books(self,
        author_name:str, maximum:int = 100, save_n:int = 10
        ) -> None:
        book_list = self.aozorapi.get_booklist(author=author_name, limit=maximum).json()
        print(f"found {len(book_list)} {author_name}'s books (max: {maximum})")
        book_list = book_list[:maximum]
        self.get_books(book_list, save_n=save_n)

    def get_books(self, book_list, save_n:int=50) -> None:
        books = []
        for i, book_info in enumerate(book_list):
            book_data = {
                'id': book_info["book_id"],
                'title': book_info["title"],
                'authors': book_info["authors"],
                'content': self.aozorapi.get_booktxt(book_info["book_id"]).text
            }
            books.append(book_data)

            if i % save_n == 0:
                print(f"got {len(books)} books")
                self.gotton_books.extend(books)
                self.save()
                books = []

            time.sleep(self.SLEEP_TIME)

        self.gotton_books.extend(books)
        print(f"got {len(books)} books")

    def save(self):
        os.makedirs(self.save_dir, exist_ok=True)

        save_path = os.path.join(self.save_dir, "books.json")
        _write_json(save_path, {"books": self.gotton_books})
        print(f"saved {len(self.gotton_books)} books to {save_path}")
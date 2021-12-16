"""the wrapper of Aozora Bunko API

Aozora Bunko (https://www.aozora.gr.jp/)

See below links about Aozora Bunko API.
    * https://github.com/aozorahack/pubserver2
    * https://github.com/aozorahack/aozora-cli
"""

import requests
import os
from typing import Union

def _shape_params(params:dict) -> dict:
    """
    remove None item
    """
    return {
        key:value for (key, value) in params.items()
        if value is not None
    }

# TODO: response 用のデータクラス作りたい
class AozoraBunkoAPI:
    """the wrapper class of Aozora Bunko API

    Attributes:
        AOZORAPI_HOST (str): To get api host address.
        AOZORAPI_URL (str): This is API URL.

    Example::
        >>> from scrapers import AozoraBunkoAPI
        >>> aozora = AozoraBunkoAPI()
        >>> aozora.get_bookinfo(2093).json()
    """

    AOZORAPI_HOST = os.environ.get("AOZORAPI_HOST", "www.aozorahack.net")
    AOZORAPI_URL = f"http://{AOZORAPI_HOST}/api/v0.1"

    def __init__(self):
        self.session = requests.Session()

    def get_booklist(self,
        title:str=None, author:str=None, fields:str=None,
        limit:int=None, skip:int=None,   after:str=None
    ) -> requests.Response:
        params = {
            'title' : title, 'author' : author,
            'fields' : fields, 'limit' : limit,
            'skip' : skip, 'after' : after
        }
        params = _shape_params(params)
        return self._aozora_get("books", params=params)

    def get_bookinfo(self, book_id:int) -> requests.Response:
        return self._aozora_get(f"books/{book_id}")

    def get_bookcard(self, book_id:int) -> requests.Response:
        return self._aozora_get(f"books/{book_id}/card")

    def get_booktxt(self, book_id:int) -> requests.Response:
        return self._aozora_get(f"books/{book_id}/content?format=txt")

    def get_bookhtml(self, book_id:int) -> requests.Response:
        return self._aozora_get(f"books/{book_id}/content?format=html")

    def get_personlist(self, name:str=None) -> requests.Response:
        params = _shape_params({'name' : name})
        return self._aozora_get("persons", params=params)

    def get_personinfo(self, person_id:int) -> requests.Response:
        return self._aozora_get(f"persons/{person_id}")

    def get_workerlist(self, name:str=None) -> requests.Response:
        params = _shape_params({'name' : name})
        return self._aozora_get("workers", params=params)

    def get_workerinfo(self, worker_id:int) -> requests.Response:
        return self._aozora_get(f"workers/{worker_id}")

    def get_ranking(self,
        year:Union[str,int], month:Union[str,int], data_type:str="txt"
    ) -> requests.Response:
        return self._aozora_get(f"ranking/{data_type}/{year}/{month:0>2d}")

    def _aozora_get(self, path:str, params={}) -> requests.Response:
        return self.session.get(f"{self.AOZORAPI_URL}/{path}", params=params)
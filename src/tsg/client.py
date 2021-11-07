from typing import Union

import attr
import requests
from aiohttp import ClientSession
from yarl import URL

from tsg.models import Book
from tsg.handlers.browse import BrowseHandler
from tsg.handlers.book import BookHandler


BASE_URL = 'https://app.thestorygraph.com'


@attr.s
class TSGClientBase:
    _base_url: URL = attr.ib(default=URL(BASE_URL))
    # Internal
    _browse_handler: BrowseHandler = attr.ib(init=False)
    _book_handler: BookHandler = attr.ib(init=False)

    def __attrs_post_init__(self):
        self._browse_handler = BrowseHandler(base_url=self._base_url)
        self._book_handler = BookHandler(base_url=self._base_url)


@attr.s
class SyncTSGClient(TSGClientBase):
    def _get(self, url: Union[str, URL]) -> str:
        return requests.get(str(url)).text

    def get_browse(self, text: str) -> list[Book]:
        return self._browse_handler.parse_body(
            self._get(self._browse_handler.make_url(text=text))
        )

    def get_book(self, id: str) -> Book:
        return self._book_handler.parse_body(
            self._get(self._book_handler.make_url(id=id))
        )


@attr.s
class AsyncTSGClient(TSGClientBase):
    async def _get(self, url: Union[str, URL]) -> str:
        async with ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    async def get_browse(self, text: str) -> list[Book]:
        return self._browse_handler.parse_body(
            await self._get(self._browse_handler.make_url(text=text))
        )

    async def get_book(self, id: str) -> Book:
        return self._book_handler.parse_body(
            await self._get(self._book_handler.make_url(id=id))
        )

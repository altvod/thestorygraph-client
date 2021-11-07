from __future__ import annotations

from typing import Any

import attr
from bs4 import BeautifulSoup
from yarl import URL

from tsg.handlers.base import BaseHandler
from tsg.models import Book
from tsg.handlers.book_common import BookPageParser


@attr.s
class BrowseHandler(BaseHandler[list[Book]]):
    _book_page_parser: BookPageParser = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        self._book_page_parser = BookPageParser(base_url=self._base_url)

    def make_url(self, text: str = '', **kwargs: Any) -> URL:
        return (self._base_url / 'browse').with_query(search_term=text)

    def parse_body(self, body: str) -> list[Book]:
        soup = BeautifulSoup(body, 'html.parser')
        raw_items = soup.find_all('div', 'book-pane')
        result: list[Book] = []
        for book_pane in raw_items:
            book = self._book_page_parser.parse_book_pane(book_pane)
            result.append(book)

        return result

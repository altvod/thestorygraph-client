from __future__ import annotations

from typing import Any

import attr
from bs4 import BeautifulSoup
from yarl import URL

from tsg import exc
from tsg.handlers.base import BaseHandler
from tsg.models import Book
from tsg.handlers.book_common import BookPageParser


@attr.s
class BookHandler(BaseHandler[Book]):
    _book_page_parser: BookPageParser = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        self._book_page_parser = BookPageParser(base_url=self._base_url)

    def make_url(self, id: str = '', **kwargs: Any) -> URL:
        assert id
        return self._base_url / 'books' / id

    def parse_body(self, body: str) -> Book:
        soup = BeautifulSoup(body, 'html.parser')
        book_panes = soup.find_all('div', 'book-pane')
        i = 0
        while i < len(book_panes) - 1:
            book_pane = book_panes[i]
            title_author_series = book_pane.find('div', 'book-title-author-and-series')
            if title_author_series is not None:
                break
            i += 1
        else:
            raise exc.FailedToParse('Failed to parse book')
        main_book_pane, descr_book_pane = book_panes[i:i+2]
        book = self._book_page_parser.parse_book_pane(main_book_pane)
        description = self._book_page_parser.parse_descr_book_pane(descr_book_pane)
        book_cover_div = soup.find('div', 'book-cover')
        cover_url = self._book_page_parser.parse_cover_url(book_cover_div)
        book = book.clone(description=description, cover_url=cover_url)
        return book

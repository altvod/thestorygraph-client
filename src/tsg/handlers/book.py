from __future__ import annotations

from typing import Any, Optional

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
        book: Optional[Book] = None
        description = ''
        for book_pane in book_panes:
            title_author_series = book_pane.find('div', 'book-title-author-and-series')
            if title_author_series is not None:
                book = self._book_page_parser.parse_book_pane(book_pane)
            elif book is not None:
                # Main book pane has already been found
                text = book_pane.get_text().strip()
                if text.startswith('Description'):
                    description = text.split('\n', 1)[1].strip()

            if description:
                # Everything has been found
                break

        if book is None:
            raise exc.FailedToParse('Failed to parse book')

        book_cover_div = soup.find('div', 'book-cover')
        cover_url = self._book_page_parser.parse_cover_url(book_cover_div)
        book = book.clone(description=description, cover_url=cover_url)
        return book

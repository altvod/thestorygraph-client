from __future__ import annotations

import re
from typing import Any, ClassVar, Optional, TYPE_CHECKING

from bs4 import BeautifulSoup
from yarl import URL

from tsg.handlers.base import BaseHandler
from tsg.models import AuthorRef, SeriesRef, Book

if TYPE_CHECKING:
    import bs4.element


class BrowseHandler(BaseHandler[list[Book]]):
    _HREF_RE_TITLE: ClassVar[re.Pattern] = re.compile(r'/books/(?P<book_id>[\w\d\-]+$)')
    _HREF_RE_SERIES: ClassVar[re.Pattern] = re.compile(r'/series/(?P<series_id>[\w\d\-]+$)')
    _HREF_RE_AUTHOR: ClassVar[re.Pattern] = re.compile(r'/authors/(?P<author_id>[\w\d\-]+$)')

    def make_url(self, text: str = '', **kwargs: Any) -> URL:
        return (self._base_url / 'browse').with_query(search_term=text)

    def _parse_book_pane(self, book_pane: bs4.element.Tag) -> Book:
        title_author_series = book_pane.find('div', 'book-title-author-and-series')
        # Title and ID
        title_node = title_author_series.find('a', href=self._HREF_RE_TITLE)
        book_id = self._HREF_RE_TITLE.match(title_node.get('href')).group('book_id')  # type: ignore
        book_title = title_node.get_text()

        # Series
        series_node = title_author_series.find('a', href=self._HREF_RE_SERIES)
        series: Optional[SeriesRef] = None
        if series_node is not None:
            series_id = self._HREF_RE_SERIES.match(series_node.get('href')).group('series_id')  # type: ignore
            series_name = series_node.get_text()
            series = SeriesRef(id=series_id, name=series_name)

        # Authors
        authors: list[AuthorRef] = []
        author_node_list = title_author_series.find_all('a', href=self._HREF_RE_AUTHOR)
        for author_node in author_node_list:
            author_id = self._HREF_RE_AUTHOR.match(author_node.get('href')).group('author_id')  # type: ignore
            author_name = author_node.get_text()
            authors.append(AuthorRef(id=author_id, name=author_name))

        book = Book(
            id=book_id,
            title=book_title,
            series=series,
            authors=authors,
        )
        return book

    def parse_body(self, body: str) -> list[Book]:
        soup = BeautifulSoup(body, 'html.parser')
        raw_items = soup.find_all('div', 'book-pane')
        result: list[Book] = []
        for book_pane in raw_items:
            book = self._parse_book_pane(book_pane)
            result.append(book)

        return result

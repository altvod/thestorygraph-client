from __future__ import annotations

import re
from typing import ClassVar, Optional, TYPE_CHECKING

import attr

from tsg.models import AuthorRef, SeriesRef, Book

if TYPE_CHECKING:
    from yarl import URL
    import bs4.element


@attr.s
class BookPageParser:
    _HREF_RE_TITLE: ClassVar[re.Pattern] = re.compile(r'/books/(?P<book_id>[\w\d\-]+$)')
    _HREF_RE_SERIES: ClassVar[re.Pattern] = re.compile(r'/series/(?P<series_id>[\w\d\-]+$)')
    _HREF_RE_AUTHOR: ClassVar[re.Pattern] = re.compile(r'/authors/(?P<author_id>[\w\d\-]+$)')

    _base_url: URL = attr.ib(kw_only=True)

    def parse_cover_url(self, book_cover_div: Optional[bs4.element.Tag]) -> Optional[str]:
        cover_url: Optional[str] = None
        if book_cover_div is not None:
            cover_url = book_cover_div.find('img').attrs['src']
        return cover_url

    def parse_book_pane(self, book_pane: bs4.element.Tag) -> Book:
        book_cover_div = book_pane.find('div', 'book-cover')
        cover_url = self.parse_cover_url(book_cover_div)

        title_author_series = book_pane.find('div', 'book-title-author-and-series')
        # Title and ID
        title_node = title_author_series.find('a', href=self._HREF_RE_TITLE)
        book_rel_url = title_node.get('href')
        book_id = self._HREF_RE_TITLE.match(book_rel_url).group('book_id')  # type: ignore
        book_title = title_node.get_text()
        book_full_url = str(self._base_url / book_rel_url.strip('/'))

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
            url=book_full_url,
            cover_url=cover_url,
        )
        return book

    def parse_descr_book_pane(self, descr_book_pane: bs4.element.Tag) -> str:
        h4 = descr_book_pane.find('h4')
        return h4.get_text().strip()

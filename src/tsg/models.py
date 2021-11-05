from typing import Optional

import attr


@attr.s(frozen=True)
class AuthorRef:
    id: str = attr.ib(kw_only=True)
    name: str = attr.ib(kw_only=True)


@attr.s(frozen=True)
class SeriesRef:
    id: str = attr.ib(kw_only=True)
    name: str = attr.ib(kw_only=True)


@attr.s(frozen=True)
class Book:
    id: str = attr.ib(kw_only=True)
    title: str = attr.ib(kw_only=True)
    series: Optional[SeriesRef] = attr.ib(kw_only=True)
    authors: list[AuthorRef] = attr.ib(kw_only=True)

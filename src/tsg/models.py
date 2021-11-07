from __future__ import annotations

from typing import Any, Optional

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
    url: str = attr.ib(kw_only=True)
    cover_url: Optional[str] = attr.ib(kw_only=True, default=None)
    description: str = attr.ib(kw_only=True, default='')

    @property
    def author_names(self) -> list[str]:
        return [author.name for author in self.authors]

    def clone(self, **kwargs: Any) -> Book:
        return attr.evolve(self, **kwargs)

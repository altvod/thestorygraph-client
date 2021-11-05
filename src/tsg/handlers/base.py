from __future__ import annotations

import abc
from typing import Any, Generic, TypeVar, TYPE_CHECKING

import attr

if TYPE_CHECKING:
    from yarl import URL


_HANDLER_RES_TV = TypeVar('_HANDLER_RES_TV')


@attr.s
class BaseHandler(abc.ABC, Generic[_HANDLER_RES_TV]):
    _base_url: URL = attr.ib(kw_only=True)

    @abc.abstractmethod
    def make_url(self, **kwargs: Any) -> URL:
        raise NotImplementedError

    @abc.abstractmethod
    def parse_body(self, body: str) -> _HANDLER_RES_TV:
        raise NotImplementedError

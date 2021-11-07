import pytest

from tsg.client import SyncTSGClient


@pytest.fixture(scope='session')
def sync_client() -> SyncTSGClient:
    return SyncTSGClient()


@pytest.fixture(scope='session')
def one_book_id(sync_client) -> str:
    book_list = sync_client.get_browse(text='SPQR')
    book = book_list[0]
    assert book.id
    return book.id

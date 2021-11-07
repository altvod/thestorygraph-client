def test_get_browse(sync_client):
    book_list = sync_client.get_browse(text='SPQR')
    assert len(book_list) > 5
    book = book_list[0]
    assert book.id
    assert book.title
    assert book.authors
    assert book.url
    assert book.cover_url


def test_get_book(sync_client, one_book_id):
    book = sync_client.get_book(id=one_book_id)
    assert book.id
    assert book.title
    assert book.authors
    assert book.url
    assert book.cover_url
    assert book.description

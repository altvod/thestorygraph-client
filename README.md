# thestorygraph-client

A Simple Python Client for TheStoryGraph.com

Sync and async clients as well as a model abstraction layer for the website.

Since no public API is available, this library parses HTML via `BeautifulSoup4`
and loads the data into model objects.


## Installation

```bash
pip install thestorygraph-client
```

## Examples

### Search for books (sync)

Find and print books related to `'SPQR'`:

```python
from tsg.client import SyncTSGClient

def print_search_result(search_text: str) -> None:
    client = SyncTSGClient()
    book_list = client.search(text=search_text)
    for book in book_list:
        print(f'{book.authors[0].name} - {book.title}')

print_search_result('SPQR')
```

### Search for books (async)

Same as above, but using the asynchronous client:

```python
import asyncio
from tsg.client import AsyncTSGClient

async def print_search_result(search_text: str) -> None:
    client = AsyncTSGClient()
    book_list = await client.get_browse(text=search_text)
    for book in book_list:
        print(f'{", ".join(book.author_names)} - {book.title}')

asyncio.run(print_search_result('SPQR'))
```

The two clients have identical APIs (beside the fact that the latter is async).

### Get a book by ID

```python
import asyncio
from tsg.client import AsyncTSGClient

async def print_book_by_id(book_id: str) -> None:
    client = AsyncTSGClient()
    book = await client.get_book(id=book_id)
    print(f'{book.title} by {", ".join(book.author_names)}')

asyncio.run(print_book_by_id('79b894b0-df12-4bb6-89d7-40288f28acc1'))
```

## Development and Testing

### Configuring the test environment

Install

```bash
pip install -Ue .[testing]
```

### Testing

Run the tests:

```bash
pytest tests
```

And always validate typing:

```bash
mypy src/tsg
```

Or simply

```bash
make test
```

(it will run all test commands)

## Links

Homepage on GitHub: https://github.com/altvod/thestorygraph-client

Project's page on PyPi: https://pypi.org/project/thestorygraph-client/

TheStoryGraph: https://thestorygraph.com/

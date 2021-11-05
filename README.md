# thestorygraph-py
A Simple Python Client for TheStoryGraph

Sync and async clients as well as a model abstraction layer for the website.


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
    book_list = await client.search(text=search_text)
    for book in book_list:
        print(f'{book.authors[0].name} - {book.title}')

asyncio.run(print_search_result('SPQR'))
```

The two clients have identical APIs (beside the fact that the latter is async).

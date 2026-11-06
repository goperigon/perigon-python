<!-- ----------  Header  ---------- -->
<p align="center">
  <img src="https://goperigon.com/favicon.ico" width="120" alt="Perigon logo" />
</p>

<h1 align="center">Perigon&nbsp;Python&nbsp;SDK</h1>
<p align="center">Python client for the <strong>Perigon&nbsp;API</strong></p>

<!-- ----------  Badges  ---------- -->
<p align="center">
  <!-- PyPI -->
  <a href="https://pypi.org/project/perigon">
    <img src="https://img.shields.io/pypi/v/perigon?style=for-the-badge" alt="pypi version">
  </a>
  <!-- Python versions -->
  <img src="https://img.shields.io/pypi/pyversions/perigon?style=for-the-badge" alt="python versions">
  <!-- downloads -->
  <img src="https://img.shields.io/pypi/dm/perigon?style=for-the-badge" alt="pypi downloads">
  <!-- tests -->
  <a href="https://github.com/goperigon/perigon-python/actions/workflows/test.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/goperigon/perigon-python/test.yml?label=test%20%E2%9C%85&style=for-the-badge" alt="tests status">
  </a>
  <!-- docs -->
  <a href="https://perigon.io/docs/api/intro">
    <img src="https://img.shields.io/badge/docs-perigon.io-informational?style=for-the-badge&logo=readthedocs" alt="documentation">
  </a>
  <!-- license -->
  <a href="LICENSE">
    <img src="https://img.shields.io/github/license/goperigon/perigon-python?style=for-the-badge" alt="license">
  </a>
</p>

A modern, fully‑typed Python SDK for the Perigon API, generated from the official OpenAPI specification.  
Works in **CPython 3.11+**, **PyPy**, serverless runtimes, notebooks, and async frameworks.

## Table&nbsp;of&nbsp;Contents

<!-- START doctoc -->
<!-- END doctoc -->

---

## ✨ Features

- **Type‑hinted** request/response models powered by Pydantic
- **Async and sync support** - choose the right approach for your application
- Ships with **PEP 561 type hints** for excellent IDE integration
- Generated directly from <https://perigon.io/docs/api/intro>, so it's always in sync

---

## 📦 Installation

```bash
pip install perigon
# poetry add perigon
# pipx install perigon
# uv add perigon
```

---

## 🚀 Quick start

### 1. Instantiate the client and make calls

```python
from perigon import V1Api, ApiClient

# One API class owns its HTTP client and closes it on the way out.
with V1Api(api_key="YOUR_API_KEY") as api:
    # 🔍 Search recent news articles (sync)
    articles = api.search_articles(q="artificial intelligence", size=5)
    print(articles.num_results, articles.articles[0].title)

    # 👤 Look up a journalist by ID (sync)
    journalist = api.get_journalist_by_id(id="123456")
    print(journalist.name)

# Share one pool across API classes.
with ApiClient(api_key="YOUR_API_KEY") as client:
    news = V1Api(client)

# Alternative: environment variable
# import os
# with V1Api(api_key=os.environ["PERIGON_API_KEY"]) as api:
#     ...
```

### 2. Make async calls

```python
import asyncio
from perigon import AsyncV1Api, AsyncApiClient


async def fetch_data():
    async with AsyncV1Api(api_key="YOUR_API_KEY") as api:
        # Search articles asynchronously
        articles = await api.search_articles(q="technology", size=5)

        # Look up journalist asynchronously
        journalist = await api.get_journalist_by_id(id="123456")

        return articles, journalist


# Run in async context
articles, journalist = asyncio.run(fetch_data())

# Share one async pool across API classes.
# async with AsyncApiClient(api_key="YOUR_API_KEY") as client:
#     news = AsyncV1Api(client)
```

> All methods return **typed objects** with full IDE autocompletion support.

---

## 🧑‍💻 Endpoint examples

### Articles – search and filter news (`/v1/articles/all`)<br>

**Docs →** [https://perigon.io/docs/api/intro](https://perigon.io/docs/api/intro)

```python
from datetime import datetime

# Simple query
articles = api.search_articles(q="technology", size=5)

# With date range. 'from' is a reserved keyword in Python, so the parameter is var_from.
articles = api.search_articles(
    q="business",
    var_from=datetime(2025, 4, 1),
    to=datetime(2025, 4, 8),
)

# Restrict to specific sources
articles = api.search_articles(source=["nytimes.com"])
```

### Companies – fetch structured company data (`/v1/companies/all`)<br>

**Docs →** [https://perigon.io/docs/api/data-model#companies](https://perigon.io/docs/api/data-model#companies)

```python
results = api.search_companies(name="Apple", size=5)
```

### Journalists – search (`/v1/journalists/all`) and detail look‑up (`/v1/journalists/{id}`)<br>

**Docs →** [https://perigon.io/docs/api/data-model#journalists--authors](https://perigon.io/docs/api/data-model#journalists--authors)

```python
# Search for journalists
results = api.search_journalists(name="Kevin", size=1)

# Get detailed information
journalist = api.get_journalist_by_id(id=results.results[0].id)
```

### Stories – discover related article clusters (`/v1/stories/all`)<br>

**Docs →** [https://perigon.io/docs/api/data-model#stories](https://perigon.io/docs/api/data-model#stories)

```python
stories = api.search_stories(q="climate change", size=5)
```

### Vector search – semantic retrieval (`/v1/vector/news/all`)<br>

**Docs →** [https://perigon.io/docs/api/vector-search](https://perigon.io/docs/api/vector-search)

```python
from perigon.models import ArticleSearchParams

results = api.vector_search_articles(
    article_search_params=ArticleSearchParams(
        prompt="Latest advancements in artificial intelligence", size=5
    )
)
```

### Summarizer – generate an instant summary (`/v1/summarize`)<br>

**Docs →** [https://perigon.io/docs/api/summarizer](https://perigon.io/docs/api/summarizer)

```python
from perigon.models import SummaryBody

summary = api.search_summarizer(
    summary_body=SummaryBody(
        prompt="Key developments",
        max_article_count=10,
        returned_article_count=10,
    ),
    q="renewable energy",
).summary

print(summary)
```

### Topics – explore taxonomy (`/v1/topics/all`)<br>

**Docs →** [https://perigon.io/docs/api/topics-types](https://perigon.io/docs/api/topics-types)

```python
topics = api.search_topics(size=10)
```

### Wikipedia – search and filter pages (`/v1/wikipedia/all`)<br>

**Docs →** [https://perigon.io/docs/api/wikipedia](https://perigon.io/docs/api/wikipedia)

```python
# Search Wikipedia pages
wikipedia_result = api.search_wikipedia(
    q="machine learning", size=3, sort_by="relevance"
)

# Filter by specific criteria
wikipedia_result = api.search_wikipedia(
    q="artificial intelligence",
    pageviews_from=100,  # Only popular pages
)
```

### Wikipedia vector search – semantic retrieval (`/v1/vector/wikipedia/all`)<br>

**Docs →** [https://perigon.io/docs/api/wikipedia](https://perigon.io/docs/api/wikipedia)

```python
from perigon.models import WikipediaSearchParams

results = api.vector_search_wikipedia(
    wikipedia_search_params=WikipediaSearchParams(
        prompt="artificial intelligence and neural networks in computing",
        size=3,
        pageviews_from=100,
    )
)
```

| Action                              | Code Example                                                                                                                                  |
|-------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| Filter by source                    | `api.search_articles(source=["nytimes.com"])`                                                                                                 |
| Limit by date range                 | `api.search_articles(q="business", var_from=datetime(2025, 4, 1), to=datetime(2025, 4, 8))`                                                   |
| Company lookup                      | `api.search_companies(name="Apple", size=5)`                                                                                                  |
| Summarize any query                 | `api.search_summarizer(summary_body=SummaryBody(prompt="Key points", max_article_count=20, returned_article_count=20), q="renewable energy")` |
| Semantic / vector search            | `api.vector_search_articles(article_search_params=ArticleSearchParams(prompt="advancements in AI", size=5))`                                  |
| Retrieve available taxonomic topics | `api.search_topics(size=10)`                                                                                                                  |
| Search Wikipedia pages              | `api.search_wikipedia(q="machine learning", size=3, sort_by="relevance")`                                                                     |
| Wikipedia semantic search           | `api.vector_search_wikipedia(wikipedia_search_params=WikipediaSearchParams(prompt="artificial intelligence", size=3))`                        |

---

## Webhooks

Verify a delivery before reading the body. Pass the raw request bytes and the
`perigon-signature` header. The default tolerance is 5 minutes.

```python
import os

from perigon import WEBHOOK_HEADER, SignatureVerificationError, Webhooks

webhooks = Webhooks()
secret = os.environ["PERIGON_WEBHOOK_SECRET"]


def handle(raw_body: bytes, signature: str | None):
    try:
        event = webhooks.construct_event(raw_body, signature, secret)
    except SignatureVerificationError:
        return None
    return event
```

`signature` is the `perigon-signature` header (`WEBHOOK_HEADER`). A full
listener is in `examples/webhooks.py`.

---

## 🔄 Async Support

`AsyncV1Api` has the same method names. Each one is a coroutine:

```python
import asyncio
from perigon import AsyncV1Api


async def main():
    async with AsyncV1Api(api_key="YOUR_API_KEY") as api:
        # Concurrent API calls
        articles_task = api.search_articles(q="technology", size=5)
        journalist_task = api.get_journalist_by_id(id="123456")

        # Gather results
        articles, journalist = await asyncio.gather(articles_task, journalist_task)

        return articles, journalist


# Run the async function
articles, journalist = asyncio.run(main())
```

---

## 🧪 Development

The default test suite checks the client and every API method against a fake HTTP transport. It does not call the
Perigon API and does not need `PERIGON_API_KEY`.

```bash
uv sync --group dev
uv run pytest
```

Before publishing, run the live API checks. These call `https://api.perigon.io` and use your quota. Add `--unit` to run
the offline tests in the same command.

```bash
export PERIGON_API_KEY="your-api-key"
uv run pytest --integration
uv run pytest --integration --unit
```

### Regenerate the SDK

Update the version in both places before generating. They must match. `uv version` updates `pyproject.toml` and
`uv.lock`. `packageVersion` in `openapi-config.yaml` is what the generator writes into `perigon.__version__`.

```bash
uv version 1.0.0
```

Set `packageVersion` in `openapi-config.yaml` to that same version, then regenerate:

```bash
./scripts/generate.sh
```

The script downloads the OpenAPI spec, regenerates `src/perigon`, then lints and runs the offline tests. Commit the
result.

### Publish

Merge to `main` and run the Publish workflow. It reads the version from the project, tags `v{version}`, smoke-tests the
built wheel and sdist, and publishes to PyPI. It does not change the version.

---

## 🪪 License

MIT © Perigon

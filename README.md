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
  <a href="https://docs.perigon.io">
    <img src="https://img.shields.io/badge/docs-perigon.io-informational?style=for-the-badge&logo=readthedocs" alt="documentation">
  </a>
  <!-- license -->
  <a href="LICENSE">
    <img src="https://img.shields.io/github/license/goperigon/perigon-python?style=for-the-badge" alt="license">
  </a>
</p>

A modern, fully‑typed Python SDK for the Perigon API, generated from the official OpenAPI specification.  
Works in **CPython 3.8+**, **PyPy**, serverless runtimes, notebooks, and async frameworks.

## Table&nbsp;of&nbsp;Contents
<!-- START doctoc -->
<!-- END doctoc -->

---

## ✨ Features

- **Type‑hinted** request/response models powered by Pydantic
- **Async and sync support** - choose the right approach for your application
- Ships with **PEP 561 type hints** for excellent IDE integration
- Generated directly from <https://docs.perigon.io>, so it's always in sync

---

## 📦 Installation

```bash
pip install perigon
# poetry add perigon
# pipx install perigon
```

---

## 🚀 Quick start

### 1. Instantiate the client

```python
from perigon import V1Api, ApiClient

# Create client with API key
api = V1Api(ApiClient(api_key="YOUR_API_KEY"))

# Alternative: environment variable or callable
# api = V1Api(ApiClient(api_key=os.environ["PERIGON_API_KEY"]))
# api = V1Api(ApiClient(api_key=lambda: get_api_key_from_vault()))
```

### 2. Make calls

```python
# 🔍 Search recent news articles (sync)
articles = api.search_articles(q="artificial intelligence", size=5)
print(articles.num_results, articles.articles[0].title)

# 👤 Look up a journalist by ID (sync)
journalist = api.get_journalist_by_id(id="123456")
print(journalist.name)

# 🔄 Use async variant for async applications
import asyncio

async def fetch_data():
    # Search articles asynchronously 
    articles = await api.search_articles_async(q="technology", size=5)
    
    # Look up journalist asynchronously
    journalist = await api.get_journalist_by_id_async(id="123456")
    
    return articles, journalist

# Run in async context
articles, journalist = asyncio.run(fetch_data())
```

> All methods return **typed objects** with full IDE autocompletion support.

---

## 🧑‍💻 Endpoint examples

### Articles – search and filter news (`/v1/all`)<br>

**Docs →** [https://docs.perigon.io/docs/overview](https://docs.perigon.io/docs/overview)

```python
# Simple query
articles = api.search_articles(q="technology", size=5)

# With date range
articles = api.search_articles(
    q="business", 
    var_from="2025-04-01",  # Note: 'from' is a reserved keyword in Python
    to="2025-04-08"
)

# Restrict to specific sources
articles = api.search_articles(source=["nytimes.com"])
```

### Companies – fetch structured company data (`/v1/companies`)<br>

**Docs →** [https://docs.perigon.io/docs/company-data](https://docs.perigon.io/docs/company-data)

```python
results = api.search_companies(name="Apple", size=5)
```

### Journalists – search and detail look‑up (`/v1/journalists`)<br>

**Docs →** [https://docs.perigon.io/docs/journalist-data](https://docs.perigon.io/docs/journalist-data)

```python
# Search for journalists
results = api.search_journalists1(name="Kevin", size=1)

# Get detailed information
journalist = api.get_journalist_by_id(id=results.journalists[0].id)
```

### Stories – discover related article clusters (`/v1/stories`)<br>

**Docs →** [https://docs.perigon.io/docs/stories-overview](https://docs.perigon.io/docs/stories-overview)

```python
stories = api.search_stories(q="climate change", size=5)
```

### Vector search – semantic retrieval (`/v1/vector`)<br>

**Docs →** [https://docs.perigon.io/docs/vector-endpoint](https://docs.perigon.io/docs/vector-endpoint)

```python
from perigon.models.article_search_params import ArticleSearchParams

results = api.vector_search_articles(
    article_search_params=ArticleSearchParams(
        prompt="Latest advancements in artificial intelligence",
        size=5
    )
)
```

### Summarizer – generate an instant summary (`/v1/summarizer`)<br>

**Docs →** [https://docs.perigon.io/docs/search-summarizer](https://docs.perigon.io/docs/search-summarizer)

```python
from perigon.models.summary_body import SummaryBody

summary = api.search_summarizer(
    summary_body=SummaryBody(prompt="Key developments"),
    q="renewable energy", 
    size=10
).summary

print(summary)
```

### Topics – explore taxonomy (`/v1/topics`)<br>

**Docs →** [https://docs.perigon.io/docs/topics](https://docs.perigon.io/docs/topics)

```python
topics = api.search_topics(size=10)
```

| Action | Code Example |
| --- | --- |
| Filter by source | `api.search_articles(source=["nytimes.com"])` |
| Limit by date range | `api.search_articles(q="business", var_from="2025-04-01", to="2025-04-08")` |
| Company lookup | `api.search_companies(name="Apple", size=5)` |
| Summarize any query | `api.search_summarizer(summary_body=SummaryBody(prompt="Key points"), q="renewable energy", size=20)` |
| Semantic / vector search | `api.vector_search_articles(article_search_params=ArticleSearchParams(prompt="advancements in AI", size=5))` |
| Retrieve available taxonomic topics | `api.search_topics(size=10)` |

---

## 🔄 Async Support

All methods have async counterparts with the `_async` suffix:

```python
import asyncio
from perigon import V1Api, ApiClient

async def main():
    api = V1Api(ApiClient(api_key="YOUR_API_KEY"))
    
    # Concurrent API calls
    articles_task = api.search_articles_async(q="technology", size=5)
    journalist_task = api.get_journalist_by_id_async(id="123456")
    
    # Gather results
    articles, journalist = await asyncio.gather(articles_task, journalist_task)
    
    return articles, journalist

# Run the async function
articles, journalist = asyncio.run(main())
```

---

## 🪪 License

MIT © Perigon
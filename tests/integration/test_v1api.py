import os
from datetime import datetime, timedelta, timezone

import pytest

# ---- Perigon SDK imports ---- #
from perigon import ApiClient, V1Api
from perigon.models import ArticleSearchParams, SummaryBody

# ----------------------------------------------------------------------------
#  Configuration & shared fixtures
# ----------------------------------------------------------------------------

API_KEY = os.getenv("PERIGON_API_KEY")

pytestmark = pytest.mark.skipif(
    API_KEY is None,
    reason="Environment variable PERIGON_API_KEY must be set to run integration tests.",
)


@pytest.fixture(scope="session")
def api() -> V1Api:
    """Create a single V1Api client for the entire test session."""
    client = ApiClient(api_key=API_KEY)
    return V1Api(client)


# ----------------------------------------------------------------------------
#  Helper utilities
# ----------------------------------------------------------------------------


def _to_utc(dt: datetime) -> datetime:
    """Ensure the datetime is timezone‑aware and UTC‑normalised."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


# ----------------------------------------------------------------------------
#  Article Search tests
# ----------------------------------------------------------------------------


def test_article_search_basic(api: V1Api):
    """`search_articles` should return a non‑empty set for a simple query."""
    result = api.search_articles(q="technology", size=5)
    assert result.articles
    assert result.num_results > 0
    article = result.articles[0]
    assert article.title


def test_article_search_date_filter(api: V1Api):
    """Articles returned with a date filter should respect the range."""
    to_date = _to_utc(datetime.now(timezone.utc))
    from_date = to_date - timedelta(days=7)

    result = api.search_articles(q="business", var_from=from_date, to=to_date, size=5)
    articles = result.articles
    assert len(articles) > 0
    for article in articles:
        pub = article.pub_date
        if not pub:
            continue
        # Perigon returns ISO‐8601 strings (e.g. "2025-04-28T12:34:56Z")
        pub_dt = _to_utc(datetime.fromisoformat(pub.replace("Z", "+00:00")))
        assert from_date <= pub_dt <= to_date


def test_article_search_source_filter(api: V1Api):
    """Filtering by `source` should limit results to that domain."""
    domain = "nytimes.com"
    result = api.search_articles(source=[domain], size=5)
    articles = result.articles

    assert len(articles) > 0
    for article in articles:
        assert article.source and article.source.domain == domain


# ----------------------------------------------------------------------------
#  Company Search
# ----------------------------------------------------------------------------


def test_company_search(api: V1Api):
    result = api.search_companies(name="Apple", size=5)
    results = result.results
    assert results
    company = results[0]
    assert company.id and company.name


# ----------------------------------------------------------------------------
#  Journalist API
# ----------------------------------------------------------------------------


def test_get_journalist_by_id(api: V1Api):
    search = api.search_journalists(name="Kevin", size=1)
    results = search.results

    if not results:
        pytest.skip("No journalists found for the name 'Kevin'.")

    jrn_id = results[0].id
    print(jrn_id)
    journalist = api.get_journalist_by_id(id=jrn_id)

    assert journalist.id == jrn_id


# ----------------------------------------------------------------------------
#  Stories API
# ----------------------------------------------------------------------------


def test_story_search(api: V1Api):
    result = api.search_stories(q="climate change", size=5)
    data = result.results

    assert len(data) > 0
    story = data[0]
    assert story.id


# ----------------------------------------------------------------------------
#  Vector Search
# ----------------------------------------------------------------------------


def test_vector_search(api: V1Api):
    params = ArticleSearchParams(
        prompt="Latest advancements in artificial intelligence", size=5
    )
    result = api.vector_search_articles(article_search_params=params).results
    assert len(result) > 0


# ----------------------------------------------------------------------------
#  Summarizer API
# ----------------------------------------------------------------------------


def test_summarizer(api: V1Api):
    # Use gpt-4o-mini which is more stable and widely supported
    summary_body = SummaryBody(prompt="Key developments", model="gpt-4o-mini")
    result = api.search_summarizer(
        summary_body=summary_body, q="renewable energy", size=10
    )
    assert result.summary and len(result.results) > 0


# ----------------------------------------------------------------------------
#  Topics API
# ----------------------------------------------------------------------------


def test_topics(api: V1Api):
    result = api.search_topics(size=10)
    assert len(result.data) > 0

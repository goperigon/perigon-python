import json
from datetime import datetime, timedelta, timezone
from uuid import UUID

import httpx
import pytest
import respx

from perigon import V1Api
from perigon.models import Journalist, MonitorResult, QuerySearchResult, SummaryBody
from perigon.models.summary_search_result import SummarySearchResult
from tests.samples import sample_json


def test_search_articles_encodes_query_and_auth() -> None:
    route = respx.get("https://api.perigon.io/v1/articles/all").mock(
        return_value=httpx.Response(200, json=sample_json(QuerySearchResult))
    )
    published_from = datetime(2024, 6, 1, 12, 0, tzinfo=timezone(timedelta(hours=2)))

    with V1Api(api_key="test-key") as api:
        result = api.search_articles(
            q="technology",
            size=5,
            source=["nytimes.com", "wsj.com"],
            var_from=published_from,
            paywall=True,
            title=None,
        )

    request = route.calls.last.request
    assert request.method == "GET"
    assert request.url.path == "/v1/articles/all"
    assert request.headers["authorization"] == "Bearer test-key"
    assert request.url.params["q"] == "technology"
    assert request.url.params["size"] == "5"
    assert request.url.params.get_list("source") == ["nytimes.com", "wsj.com"]
    assert request.url.params["from"] == "2024-06-01T10:00:00"
    assert request.url.params["paywall"] == "true"
    assert "title" not in request.url.params
    assert isinstance(result, QuerySearchResult)


def test_search_summarizer_sends_only_set_body_fields() -> None:
    route = respx.post("https://api.perigon.io/v1/summarize").mock(
        return_value=httpx.Response(200, json=sample_json(SummarySearchResult))
    )
    body = SummaryBody(model="gpt-6-luna", max_article_count=3)

    with V1Api(api_key="test-key") as api:
        result = api.search_summarizer(summary_body=body)

    request = route.calls.last.request
    assert json.loads(request.content) == {"model": "gpt-6-luna", "maxArticleCount": 3}
    assert isinstance(result, SummarySearchResult)


def test_path_parameters_are_substituted() -> None:
    journalist = respx.get("https://api.perigon.io/v1/journalists/jrn-1").mock(
        return_value=httpx.Response(200, json=sample_json(Journalist))
    )
    monitor_id = UUID("00000000-0000-0000-0000-000000000001")
    monitor = respx.post(
        f"https://api.perigon.io/v1/api/monitors/{monitor_id}/activate"
    ).mock(return_value=httpx.Response(200, json=sample_json(MonitorResult)))

    with V1Api(api_key="test-key") as api:
        found = api.get_journalist_by_id(id="jrn-1")
        activated = api.activate_monitor_api(uuid=monitor_id)

    assert journalist.calls.last.request.url.path == "/v1/journalists/jrn-1"
    assert isinstance(found, Journalist)
    assert monitor.calls.last.request.method == "POST"
    assert monitor.calls.last.request.url.path == (
        f"/v1/api/monitors/{monitor_id}/activate"
    )
    assert isinstance(activated, MonitorResult)


def test_http_error_raises() -> None:
    respx.get("https://api.perigon.io/v1/articles/all").mock(
        return_value=httpx.Response(401, json={"message": "nope"})
    )
    with V1Api(api_key="test-key") as api, pytest.raises(httpx.HTTPStatusError):
        api.search_articles(q="technology")


def test_missing_api_key_omits_authorization() -> None:
    route = respx.get("https://api.perigon.io/v1/articles/all").mock(
        return_value=httpx.Response(200, json=sample_json(QuerySearchResult))
    )
    with V1Api() as api:
        api.search_articles(q="technology")

    assert "authorization" not in route.calls.last.request.headers

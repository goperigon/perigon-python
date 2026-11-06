import inspect
import re
from typing import Any, get_type_hints

import httpx
import pytest
import respx

import perigon.api.v1_api as v1_module
from perigon import AsyncV1Api, V1Api
from tests.samples import sample_argument, sample_json

_VERB = re.compile(r"""request\(\s*["']([A-Z]+)["']""")


def _cases() -> list[tuple[type[V1Api] | type[AsyncV1Api], str]]:
    cases: list[tuple[type[V1Api] | type[AsyncV1Api], str]] = []
    for api_cls in (V1Api, AsyncV1Api):
        for name, member in inspect.getmembers(api_cls, inspect.isfunction):
            if name.startswith("_") or name == "close":
                continue
            cases.append((api_cls, name))
    return cases


def _case_id(api_cls: type[V1Api] | type[AsyncV1Api], name: str) -> str:
    return f"{api_cls.__name__}.{name}"


_ENDPOINT_CASES = _cases()


@pytest.mark.parametrize(
    ("api_cls", "method_name"),
    _ENDPOINT_CASES,
    ids=[_case_id(api_cls, name) for api_cls, name in _ENDPOINT_CASES],
)
async def test_method_sends_request_and_parses_response(
    api_cls: type[V1Api] | type[AsyncV1Api], method_name: str
) -> None:
    method = getattr(api_cls, method_name)
    hints = get_type_hints(method)
    return_type = hints["return"]
    payload = sample_json(return_type)
    kwargs: dict[str, Any] = {}
    for name, param in inspect.signature(method).parameters.items():
        if name == "self" or param.default is not inspect.Parameter.empty:
            continue
        kwargs[name] = sample_argument(hints[name])

    route = respx.route(host="api.perigon.io").mock(
        return_value=httpx.Response(200, json=payload)
    )
    api = api_cls(api_key="test-key")
    try:
        result = getattr(api, method_name)(**kwargs)
        if inspect.isawaitable(result):
            result = await result
    finally:
        closed = api.close()
        if inspect.isawaitable(closed):
            await closed

    request = route.calls.last.request
    verb = _VERB.search(inspect.getsource(method))
    assert verb is not None
    assert request.method == verb.group(1)
    assert request.url.path == _expected_path(method_name, kwargs)
    assert request.headers["authorization"] == "Bearer test-key"
    assert isinstance(result, return_type)


def _expected_path(method_name: str, kwargs: dict[str, Any]) -> str:
    path = getattr(v1_module, f"PATH_{method_name.upper()}")
    for key, value in kwargs.items():
        token = "{" + key + "}"
        if token in path:
            path = path.replace(token, str(value))
    return path

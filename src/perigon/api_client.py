# Package: perigon
from __future__ import annotations

from typing import Any, TypeVar

import httpx

from perigon.configuration import DEFAULT_BASE_URL, Configuration

# The generator REST client uses this timeout when the caller does not set one.
DEFAULT_ASYNC_TIMEOUT = 5 * 60

ClientT = TypeVar("ClientT", bound="ApiClient | AsyncApiClient")


def _auth_headers(api_key: str | None) -> dict[str, str]:
    headers: dict[str, str] = {}
    if not api_key:
        return headers
    headers["Authorization"] = f"Bearer {api_key}"
    return headers


def _resolve_configuration(
    api_key: str | None,
    base_url: str | None,
    configuration: Configuration | None,
) -> Configuration:
    if configuration is not None and (api_key is not None or base_url is not None):
        raise ValueError("Pass either configuration or api_key and base_url, not both.")
    if configuration is not None:
        return configuration
    return Configuration(api_key=api_key, base_url=base_url or DEFAULT_BASE_URL)


class ApiClient:
    """Sync HTTP client. Owns one ``httpx.Client`` and one connection pool."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
        configuration: Configuration | None = None,
    ) -> None:
        self.configuration = _resolve_configuration(api_key, base_url, configuration)
        self.timeout = timeout
        # The pool is created here. __enter__ does not enter the httpx client,
        # because httpx only allows that before the first request.
        self._client = httpx.Client(
            base_url=self.configuration.base_url, timeout=self.timeout
        )

    def request(
        self,
        method: str,
        path: str,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        all_headers = _auth_headers(self.configuration.api_key)
        if headers:
            all_headers.update(headers)
        url = f"{self.configuration.base_url}{path}"
        return self._client.request(method, url, headers=all_headers, **kwargs)

    def __enter__(self) -> ApiClient:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def close(self) -> None:
        self._client.close()


class _AsyncRESTClient:
    """Lazy async pool, following the generator REST client.

    ``pool_manager`` stays ``None`` until the first request, which creates the
    ``httpx.AsyncClient`` on the running loop.
    """

    def __init__(self, timeout: float) -> None:
        self.timeout = timeout
        self.pool_manager: httpx.AsyncClient | None = None

    async def close(self) -> None:
        if self.pool_manager is not None:
            await self.pool_manager.aclose()

    async def request(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        if self.pool_manager is None:
            self.pool_manager = httpx.AsyncClient()
        kwargs.setdefault("timeout", self.timeout)
        return await self.pool_manager.request(method, url, headers=headers, **kwargs)


class AsyncApiClient:
    """Async HTTP client. The pool is created on the first request."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
        configuration: Configuration | None = None,
    ) -> None:
        self.configuration = _resolve_configuration(api_key, base_url, configuration)
        self.timeout = DEFAULT_ASYNC_TIMEOUT if timeout is None else timeout
        self.rest_client = _AsyncRESTClient(self.timeout)

    async def request(
        self,
        method: str,
        path: str,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        all_headers = _auth_headers(self.configuration.api_key)
        if headers:
            all_headers.update(headers)
        url = f"{self.configuration.base_url}{path}"
        return await self.rest_client.request(
            method, url, headers=all_headers, **kwargs
        )

    async def __aenter__(self) -> AsyncApiClient:
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.close()

    async def close(self) -> None:
        await self.rest_client.close()


def bind_client(
    api_client: ClientT | None,
    client_cls: type[ClientT],
    *,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout: float | None = None,
    configuration: Configuration | None = None,
) -> tuple[ClientT, bool]:
    """Return a client and whether the caller owns it.

    A passed client is borrowed. Keyword arguments create a client that the
    caller must close. Passing both is rejected.
    """
    if api_client is not None and (
        api_key is not None
        or base_url is not None
        or timeout is not None
        or configuration is not None
    ):
        raise ValueError(
            "Pass either an API client or api_key, base_url, timeout, "
            "and configuration, not both."
        )
    if api_client is not None:
        return api_client, False
    return (
        client_cls(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            configuration=configuration,
        ),
        True,
    )

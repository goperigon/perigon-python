# Package : perigon
from __future__ import annotations

from typing import Any, Dict, Optional

import httpx


class ApiClient:
    """
    Single entry‑point that wraps an httpx.Client *and* httpx.AsyncClient.
    Accepts api_key & base_url directly instead of a separate Configuration.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.perigon.io",
        timeout: Optional[float] = None,
    ):
        self.api_key = api_key
        self.base_url = base_url or "https://api.perigon.io"
        self.timeout = timeout

        # Persistent sessions for connection‑pool reuse (HTTP/1.1 or HTTP/2)
        self._sync = httpx.Client(base_url=self.base_url, timeout=self.timeout)
        self._async = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #
    def _auth_headers(self) -> Dict[str, str]:
        hdrs: Dict[str, str] = {}

        if self.api_key:
            hdrs["Authorization"] = f"Bearer {self.api_key}"

        return hdrs

    def _prepare_url(self, path: str) -> str:
        url = f"{self.base_url}{path}"
        return url

    # ------------------------------------------------------------------ #
    # Public request wrappers
    # ------------------------------------------------------------------ #
    def request(
        self,
        method: str,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> httpx.Response:
        all_headers = self._auth_headers()
        if headers:  # merge user‑provided headers
            all_headers.update(headers)
        url = self._prepare_url(path)
        return self._sync.request(method, url, headers=all_headers, **kwargs)

    async def request_async(
        self,
        method: str,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> httpx.Response:
        all_headers = self._auth_headers()
        if headers:
            all_headers.update(headers)
        url = self._prepare_url(path)
        return await self._async.request(method, url, headers=all_headers, **kwargs)

    # ------------------------------------------------------------------ #
    # Clean‑up helpers
    # ------------------------------------------------------------------ #
    def close(self) -> None:
        self._sync.close()

    async def aclose(self) -> None:
        await self._async.aclose()

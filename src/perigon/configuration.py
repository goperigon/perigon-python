# Package: perigon
"""Settings shared by the sync and async API clients."""

DEFAULT_BASE_URL = "https://api.perigon.io"


class Configuration:
    """API key and host used to build a client.

    :param api_key: Perigon API key. Sent as ``Authorization: Bearer``.
    :param base_url: API host. Defaults to ``https://api.perigon.io``.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url or DEFAULT_BASE_URL

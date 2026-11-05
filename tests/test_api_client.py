import httpx
import pytest
import respx

from perigon import (
    ApiClient,
    AsyncApiClient,
    AsyncV1Api,
    Configuration,
    V1Api,
)


def test_sync_context_manager_closes_client() -> None:
    client = ApiClient()
    with client:
        assert not client._client.is_closed
    assert client._client.is_closed
    client.close()


def test_owned_v1api_closes_client() -> None:
    with V1Api(api_key="test") as api:
        client = api.api_client
        assert api._owns_client
        assert not client._client.is_closed
    assert client._client.is_closed


def test_borrowed_v1api_leaves_client_open() -> None:
    client = ApiClient(api_key="test")
    with V1Api(client) as api:
        assert api.api_client is client
        assert not api._owns_client
    assert not client._client.is_closed
    client.close()


def test_conflicting_api_arguments_raise() -> None:
    client = ApiClient()
    with pytest.raises(ValueError):
        V1Api(client, api_key="test")
    client.close()


def test_conflicting_configuration_arguments_raise() -> None:
    config = Configuration(api_key="test", base_url="https://example.com")
    with pytest.raises(ValueError):
        ApiClient(api_key="other", configuration=config)
    client = ApiClient(configuration=config)
    assert client.configuration is config
    assert client.timeout is None
    client.close()


async def test_async_pool_is_created_on_first_request() -> None:
    client = AsyncApiClient(timeout=1)
    assert client.rest_client.pool_manager is None
    await client.close()
    respx.get("https://api.perigon.io/").mock(return_value=httpx.Response(200))
    response = await client.request("GET", "/")
    assert response.status_code == 200
    pool = client.rest_client.pool_manager
    assert pool is not None
    assert not pool.is_closed
    await client.close()
    assert pool.is_closed


async def test_async_context_manager_closes_pool() -> None:
    respx.get("https://api.perigon.io/").mock(return_value=httpx.Response(200))
    async with AsyncApiClient(timeout=1) as client:
        response = await client.request("GET", "/")
        assert response.status_code == 200
        pool = client.rest_client.pool_manager
        assert pool is not None
    assert pool is not None
    assert pool.is_closed


async def test_owned_async_v1api_closes_pool() -> None:
    respx.get("https://api.perigon.io/").mock(return_value=httpx.Response(200))
    async with AsyncV1Api(api_key="test", timeout=1) as api:
        assert api._owns_client
        response = await api.api_client.request("GET", "/")
        assert response.status_code == 200
        pool = api.api_client.rest_client.pool_manager
        assert pool is not None
        assert not pool.is_closed
    assert pool is not None
    assert pool.is_closed


async def test_borrowed_async_v1api_leaves_client_open() -> None:
    client = AsyncApiClient(timeout=1)
    async with AsyncV1Api(client) as api:
        assert api.api_client is client
        assert not api._owns_client
        assert client.rest_client.pool_manager is None
    await client.close()
    assert client.rest_client.pool_manager is None


def test_async_client_default_timeout() -> None:
    client = AsyncApiClient()
    assert client.timeout == 300

from enum import Enum
from typing import Any, Dict, Iterable, List, Mapping, Optional

from pydantic import Field, StrictInt, StrictStr
from typing_extensions import Annotated

from perigon.api_client import ApiClient
from perigon.models.create_watchlist_params import CreateWatchlistParams
from perigon.models.update_watchlist_params import UpdateWatchlistParams

# Define API paths
PATH_CREATE_WATCHLIST = "/v1/api/watchlists"
PATH_DELETE_WATCHLIST = "/v1/api/watchlists/{id}"
PATH_GET_WATCHLIST = "/v1/api/watchlists/{id}"
PATH_LIST_WATCHLISTS = "/v1/api/watchlists"
PATH_RESOLVE_WATCHLISTS = "/v1/api/watchlists/resolve"
PATH_UPDATE_WATCHLIST = "/v1/api/watchlists/{id}"


def _normalise_query(params: Mapping[str, Any]) -> Dict[str, Any]:
    """
    • Convert Enum → Enum.value
    • Convert list/tuple/set → CSV string (after Enum handling)
    • Skip None values
    """
    out: Dict[str, Any] = {}
    for key, value in params.items():
        if value is None:  # ignore "unset"
            continue

        # Unwrap single Enum
        if isinstance(value, Enum):  # Enum → str
            value = value.value

        # Handle datetime objects properly
        from datetime import datetime

        if isinstance(value, datetime):
            value = value.isoformat().split("+")[0]

        # Handle collection (after possible Enum unwrap)
        elif isinstance(value, (list, tuple, set)):
            # unwrap Enum members inside the collection
            items: Iterable[str] = (
                (
                    item.isoformat().replace(" ", "+")
                    if isinstance(item, datetime)
                    else str(item.value if isinstance(item, Enum) else item)
                )
                for item in value
            )
            value = ",".join(items)  # CSV join
        else:
            value = str(value)

        out[key] = value

    return out


class WatchlistsApi:
    """"""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()

    # ----------------- create_watchlist (sync) ----------------- #
    def create_watchlist(self, create_watchlist_params: CreateWatchlistParams):
        """
        Create a new watchlist under the organization associated with the API key. A watchlist can contain up to 100 combined people and companies.

        Args:
            create_watchlist_params (CreateWatchlistParams): Parameter create_watchlist_params (required)

        """
        # Get path template from class attribute
        path = PATH_CREATE_WATCHLIST

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = self.api_client.request(
            "POST",
            path,
            params=params,
            json=create_watchlist_params.model_dump(by_alias=True, exclude_none=True),
        )
        resp.raise_for_status()
        return resp.json()

    # ----------------- create_watchlist (async) ----------------- #
    async def create_watchlist_async(
        self, create_watchlist_params: CreateWatchlistParams
    ):
        """
        Async variant of create_watchlist. Create a new watchlist under the organization associated with the API key. A watchlist can contain up to 100 combined people and companies.

        Args:
            create_watchlist_params (CreateWatchlistParams): Parameter create_watchlist_params (required)

        """
        # Get path template from class attribute
        path = PATH_CREATE_WATCHLIST

        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = await self.api_client.request_async(
            "POST",
            path,
            params=params,
            json=create_watchlist_params.model_dump(by_alias=True, exclude_none=True),
        )
        resp.raise_for_status()
        return resp.json()

    # ----------------- delete_watchlist (sync) ----------------- #
    def delete_watchlist(self, id: int):
        """
        Delete a watchlist owned by the organization associated with the API key. A watchlist cannot be deleted if it is attached to active signals.

        Args:
            id (int): Parameter id (required)

        """
        # Get path template from class attribute
        path = PATH_DELETE_WATCHLIST

        # Replace path parameters
        path = path.format(id=str(id))

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = self.api_client.request("DELETE", path, params=params)
        resp.raise_for_status()
        return resp.json()

    # ----------------- delete_watchlist (async) ----------------- #
    async def delete_watchlist_async(self, id: int):
        """
        Async variant of delete_watchlist. Delete a watchlist owned by the organization associated with the API key. A watchlist cannot be deleted if it is attached to active signals.

        Args:
            id (int): Parameter id (required)

        """
        # Get path template from class attribute
        path = PATH_DELETE_WATCHLIST

        # Replace path parameters
        path = path.format(id=str(id))

        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = await self.api_client.request_async("DELETE", path, params=params)
        resp.raise_for_status()
        return resp.json()

    # ----------------- get_watchlist (sync) ----------------- #
    def get_watchlist(self, id: int):
        """
        Retrieve a watchlist by ID. Only returns watchlists owned by the organization associated with the API key.

        Args:
            id (int): Parameter id (required)

        """
        # Get path template from class attribute
        path = PATH_GET_WATCHLIST

        # Replace path parameters
        path = path.format(id=str(id))

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()
        return resp.json()

    # ----------------- get_watchlist (async) ----------------- #
    async def get_watchlist_async(self, id: int):
        """
        Async variant of get_watchlist. Retrieve a watchlist by ID. Only returns watchlists owned by the organization associated with the API key.

        Args:
            id (int): Parameter id (required)

        """
        # Get path template from class attribute
        path = PATH_GET_WATCHLIST

        # Replace path parameters
        path = path.format(id=str(id))

        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()
        return resp.json()

    # ----------------- list_watchlists (sync) ----------------- #
    def list_watchlists(
        self,
        sort_by: str,
        sort_order: str,
        name: Optional[str] = None,
        page: Optional[str] = None,
        size: Optional[str] = None,
    ):
        """
        List watchlists owned by the organization associated with the API key, as well as publicly visible watchlists. Supports filtering by name.

        Args:
            sort_by (str): Field to sort by. (required)
            sort_order (str): The sort order for the results.   _Available values: 'asc' or 'desc'_. (required)
            name (Optional[str]): Filter watchlists by name (case-insensitive, partial match)
            page (Optional[str]): The page number to retrieve.   _Starting from 0_.   _Default value 0_.
            size (Optional[str]): The number of items per page.   _Must be at least 1_.   _Default value 10_.

        """
        # Get path template from class attribute
        path = PATH_LIST_WATCHLISTS

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if sort_by is not None:
            params["sortBy"] = sort_by
        if sort_order is not None:
            params["sortOrder"] = sort_order
        params = _normalise_query(params)

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()
        return resp.json()

    # ----------------- list_watchlists (async) ----------------- #
    async def list_watchlists_async(
        self,
        sort_by: str,
        sort_order: str,
        name: Optional[str] = None,
        page: Optional[str] = None,
        size: Optional[str] = None,
    ):
        """
        Async variant of list_watchlists. List watchlists owned by the organization associated with the API key, as well as publicly visible watchlists. Supports filtering by name.

        Args:
            sort_by (str): Field to sort by. (required)
            sort_order (str): The sort order for the results.   _Available values: 'asc' or 'desc'_. (required)
            name (Optional[str]): Filter watchlists by name (case-insensitive, partial match)
            page (Optional[str]): The page number to retrieve.   _Starting from 0_.   _Default value 0_.
            size (Optional[str]): The number of items per page.   _Must be at least 1_.   _Default value 10_.

        """
        # Get path template from class attribute
        path = PATH_LIST_WATCHLISTS

        params: Dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if sort_by is not None:
            params["sortBy"] = sort_by
        if sort_order is not None:
            params["sortOrder"] = sort_order
        params = _normalise_query(params)

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()
        return resp.json()

    # ----------------- resolve_watchlists (sync) ----------------- #
    def resolve_watchlists(self, name: Optional[List[str]] = None):
        """
        Resolve watchlists by name. For each name, returns the organization&#39;s private watchlist if one exists, otherwise falls back to the matching public watchlist.

        Args:
            name (Optional[List[str]]): Watchlist names to resolve (max 100)

        """
        # Get path template from class attribute
        path = PATH_RESOLVE_WATCHLISTS

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        params = _normalise_query(params)

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()
        return resp.json()

    # ----------------- resolve_watchlists (async) ----------------- #
    async def resolve_watchlists_async(self, name: Optional[List[str]] = None):
        """
        Async variant of resolve_watchlists. Resolve watchlists by name. For each name, returns the organization&#39;s private watchlist if one exists, otherwise falls back to the matching public watchlist.

        Args:
            name (Optional[List[str]]): Watchlist names to resolve (max 100)

        """
        # Get path template from class attribute
        path = PATH_RESOLVE_WATCHLISTS

        params: Dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        params = _normalise_query(params)

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()
        return resp.json()

    # ----------------- update_watchlist (sync) ----------------- #
    def update_watchlist(self, id: int, update_watchlist_params: UpdateWatchlistParams):
        """
        Partially update a watchlist owned by the organization associated with the API key. Only provided fields will be updated.

        Args:
            id (int): Parameter id (required)
            update_watchlist_params (UpdateWatchlistParams): Parameter update_watchlist_params (required)

        """
        # Get path template from class attribute
        path = PATH_UPDATE_WATCHLIST

        # Replace path parameters
        path = path.format(id=str(id))

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = self.api_client.request(
            "PATCH",
            path,
            params=params,
            json=update_watchlist_params.model_dump(by_alias=True, exclude_none=True),
        )
        resp.raise_for_status()
        return resp.json()

    # ----------------- update_watchlist (async) ----------------- #
    async def update_watchlist_async(
        self, id: int, update_watchlist_params: UpdateWatchlistParams
    ):
        """
        Async variant of update_watchlist. Partially update a watchlist owned by the organization associated with the API key. Only provided fields will be updated.

        Args:
            id (int): Parameter id (required)
            update_watchlist_params (UpdateWatchlistParams): Parameter update_watchlist_params (required)

        """
        # Get path template from class attribute
        path = PATH_UPDATE_WATCHLIST

        # Replace path parameters
        path = path.format(id=str(id))

        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = await self.api_client.request_async(
            "PATCH",
            path,
            params=params,
            json=update_watchlist_params.model_dump(by_alias=True, exclude_none=True),
        )
        resp.raise_for_status()
        return resp.json()

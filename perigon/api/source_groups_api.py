from enum import Enum
from typing import Any, Dict, Iterable, List, Mapping, Optional

from pydantic import Field, StrictInt, StrictStr
from typing_extensions import Annotated

from perigon.api_client import ApiClient
from perigon.models.create_source_group_params import CreateSourceGroupParams
from perigon.models.patch_source_group_params import PatchSourceGroupParams

# Define API paths
PATH_CREATE_SOURCE_GROUP = "/v1/api/sourceGroups"
PATH_DELETE_SOURCE_GROUP = "/v1/api/sourceGroups/{id}"
PATH_GET_SOURCE_GROUP = "/v1/api/sourceGroups/{id}"
PATH_LIST_SOURCE_GROUPS = "/v1/api/sourceGroups"
PATH_RESOLVE_SOURCE_GROUPS = "/v1/api/sourceGroups/resolve"
PATH_UPDATE_SOURCE_GROUP = "/v1/api/sourceGroups/{id}"


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


class SourceGroupsApi:
    """"""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()

    # ----------------- create_source_group (sync) ----------------- #
    def create_source_group(self, create_source_group_params: CreateSourceGroupParams):
        """
        Create a new source group under the organization associated with the API key.

        Args:
            create_source_group_params (CreateSourceGroupParams): Parameter create_source_group_params (required)

        """
        # Get path template from class attribute
        path = PATH_CREATE_SOURCE_GROUP

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = self.api_client.request(
            "POST",
            path,
            params=params,
            json=create_source_group_params.model_dump(
                by_alias=True, exclude_none=True
            ),
        )
        resp.raise_for_status()
        return resp.json()

    # ----------------- create_source_group (async) ----------------- #
    async def create_source_group_async(
        self, create_source_group_params: CreateSourceGroupParams
    ):
        """
        Async variant of create_source_group. Create a new source group under the organization associated with the API key.

        Args:
            create_source_group_params (CreateSourceGroupParams): Parameter create_source_group_params (required)

        """
        # Get path template from class attribute
        path = PATH_CREATE_SOURCE_GROUP

        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = await self.api_client.request_async(
            "POST",
            path,
            params=params,
            json=create_source_group_params.model_dump(
                by_alias=True, exclude_none=True
            ),
        )
        resp.raise_for_status()
        return resp.json()

    # ----------------- delete_source_group (sync) ----------------- #
    def delete_source_group(self, id: int):
        """
        Delete a source group owned by the organization associated with the API key.

        Args:
            id (int): Parameter id (required)

        """
        # Get path template from class attribute
        path = PATH_DELETE_SOURCE_GROUP

        # Replace path parameters
        path = path.format(id=str(id))

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = self.api_client.request("DELETE", path, params=params)
        resp.raise_for_status()
        return resp.json()

    # ----------------- delete_source_group (async) ----------------- #
    async def delete_source_group_async(self, id: int):
        """
        Async variant of delete_source_group. Delete a source group owned by the organization associated with the API key.

        Args:
            id (int): Parameter id (required)

        """
        # Get path template from class attribute
        path = PATH_DELETE_SOURCE_GROUP

        # Replace path parameters
        path = path.format(id=str(id))

        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = await self.api_client.request_async("DELETE", path, params=params)
        resp.raise_for_status()
        return resp.json()

    # ----------------- get_source_group (sync) ----------------- #
    def get_source_group(self, id: int):
        """
        Retrieve a source group by ID. Only returns source groups owned by the organization associated with the API key.

        Args:
            id (int): Parameter id (required)

        """
        # Get path template from class attribute
        path = PATH_GET_SOURCE_GROUP

        # Replace path parameters
        path = path.format(id=str(id))

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()
        return resp.json()

    # ----------------- get_source_group (async) ----------------- #
    async def get_source_group_async(self, id: int):
        """
        Async variant of get_source_group. Retrieve a source group by ID. Only returns source groups owned by the organization associated with the API key.

        Args:
            id (int): Parameter id (required)

        """
        # Get path template from class attribute
        path = PATH_GET_SOURCE_GROUP

        # Replace path parameters
        path = path.format(id=str(id))

        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()
        return resp.json()

    # ----------------- list_source_groups (sync) ----------------- #
    def list_source_groups(
        self,
        sort_by: str,
        sort_order: str,
        name: Optional[str] = None,
        domain: Optional[str] = None,
        page: Optional[str] = None,
        size: Optional[str] = None,
    ):
        """
        List source groups owned by the organization associated with the API key, as well as publicly visible source groups. Supports filtering by name and domain.

        Args:
            sort_by (str): Field to sort by. (required)
            sort_order (str): The sort order for the results.   _Available values: 'asc' or 'desc'_. (required)
            name (Optional[str]): Parameter name
            domain (Optional[str]): Parameter domain
            page (Optional[str]): The page number to retrieve.   _Starting from 0_.   _Default value 0_.
            size (Optional[str]): The number of items per page.   _Must be at least 1_.   _Default value 10_.

        """
        # Get path template from class attribute
        path = PATH_LIST_SOURCE_GROUPS

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if domain is not None:
            params["domain"] = domain
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

    # ----------------- list_source_groups (async) ----------------- #
    async def list_source_groups_async(
        self,
        sort_by: str,
        sort_order: str,
        name: Optional[str] = None,
        domain: Optional[str] = None,
        page: Optional[str] = None,
        size: Optional[str] = None,
    ):
        """
        Async variant of list_source_groups. List source groups owned by the organization associated with the API key, as well as publicly visible source groups. Supports filtering by name and domain.

        Args:
            sort_by (str): Field to sort by. (required)
            sort_order (str): The sort order for the results.   _Available values: 'asc' or 'desc'_. (required)
            name (Optional[str]): Parameter name
            domain (Optional[str]): Parameter domain
            page (Optional[str]): The page number to retrieve.   _Starting from 0_.   _Default value 0_.
            size (Optional[str]): The number of items per page.   _Must be at least 1_.   _Default value 10_.

        """
        # Get path template from class attribute
        path = PATH_LIST_SOURCE_GROUPS

        params: Dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if domain is not None:
            params["domain"] = domain
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

    # ----------------- resolve_source_groups (sync) ----------------- #
    def resolve_source_groups(self, name: Optional[List[str]] = None):
        """
        Resolve source groups by name. For each name, returns the organization&#39;s private source group if one exists, otherwise falls back to the matching public source group.

        Args:
            name (Optional[List[str]]): Source group names to resolve (max 100)

        """
        # Get path template from class attribute
        path = PATH_RESOLVE_SOURCE_GROUPS

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        params = _normalise_query(params)

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()
        return resp.json()

    # ----------------- resolve_source_groups (async) ----------------- #
    async def resolve_source_groups_async(self, name: Optional[List[str]] = None):
        """
        Async variant of resolve_source_groups. Resolve source groups by name. For each name, returns the organization&#39;s private source group if one exists, otherwise falls back to the matching public source group.

        Args:
            name (Optional[List[str]]): Source group names to resolve (max 100)

        """
        # Get path template from class attribute
        path = PATH_RESOLVE_SOURCE_GROUPS

        params: Dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        params = _normalise_query(params)

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()
        return resp.json()

    # ----------------- update_source_group (sync) ----------------- #
    def update_source_group(
        self, id: int, patch_source_group_params: PatchSourceGroupParams
    ):
        """
        Partially update a source group owned by the organization associated with the API key. Only provided fields will be updated.

        Args:
            id (int): Parameter id (required)
            patch_source_group_params (PatchSourceGroupParams): Parameter patch_source_group_params (required)

        """
        # Get path template from class attribute
        path = PATH_UPDATE_SOURCE_GROUP

        # Replace path parameters
        path = path.format(id=str(id))

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = self.api_client.request(
            "PATCH",
            path,
            params=params,
            json=patch_source_group_params.model_dump(by_alias=True, exclude_none=True),
        )
        resp.raise_for_status()
        return resp.json()

    # ----------------- update_source_group (async) ----------------- #
    async def update_source_group_async(
        self, id: int, patch_source_group_params: PatchSourceGroupParams
    ):
        """
        Async variant of update_source_group. Partially update a source group owned by the organization associated with the API key. Only provided fields will be updated.

        Args:
            id (int): Parameter id (required)
            patch_source_group_params (PatchSourceGroupParams): Parameter patch_source_group_params (required)

        """
        # Get path template from class attribute
        path = PATH_UPDATE_SOURCE_GROUP

        # Replace path parameters
        path = path.format(id=str(id))

        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = await self.api_client.request_async(
            "PATCH",
            path,
            params=params,
            json=patch_source_group_params.model_dump(by_alias=True, exclude_none=True),
        )
        resp.raise_for_status()
        return resp.json()

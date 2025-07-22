from datetime import datetime
from enum import Enum
from typing import Any, Dict, Iterable, List, Mapping, Optional, Union

from pydantic import Field, StrictBool, StrictInt, StrictStr
from typing_extensions import Annotated

from perigon.api_client import ApiClient
from perigon.models.company_search_result import CompanySearchResult
from perigon.models.journalist import Journalist
from perigon.models.journalist_search_result import JournalistSearchResult
from perigon.models.people_search_result import PeopleSearchResult
from perigon.models.sort_by import SortBy
from perigon.models.source_search_result import SourceSearchResult
from perigon.models.topic_search_result import TopicSearchResult

# Define API paths
PATH_GET_JOURNALIST_BY_ID = "/v1/journalists/{id}"
PATH_SEARCH_COMPANIES = "/v1/companies/all"
PATH_SEARCH_JOURNALISTS = "/v1/journalists/all"
PATH_SEARCH_PEOPLE = "/v1/people/all"
PATH_SEARCH_SOURCES = "/v1/sources/all"
PATH_SEARCH_TOPICS = "/v1/topics/all"


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


class SupplementalEndpointsApi:
    """"""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()

    # ----------------- get_journalist_by_id (sync) ----------------- #
    def get_journalist_by_id(self, id: str) -> Journalist:
        """
        Find additional details on a journalist by using the journalist ID found in an article response object.

        Args:
            id (str): Parameter id (required)

        Returns:
            Journalist: The response
        """
        # Get path template from class attribute
        path = PATH_GET_JOURNALIST_BY_ID

        # Replace path parameters
        path = path.format(id=str(id))

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()
        return Journalist.model_validate(resp.json())

    # ----------------- get_journalist_by_id (async) ----------------- #
    async def get_journalist_by_id_async(self, id: str) -> Journalist:
        """
        Async variant of get_journalist_by_id. Find additional details on a journalist by using the journalist ID found in an article response object.

        Args:
            id (str): Parameter id (required)

        Returns:
            Journalist: The response
        """
        # Get path template from class attribute
        path = PATH_GET_JOURNALIST_BY_ID

        # Replace path parameters
        path = path.format(id=str(id))

        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()
        return Journalist.model_validate(resp.json())

    # ----------------- search_companies (sync) ----------------- #
    def search_companies(
        self,
        id: Optional[List[str]] = None,
        symbol: Optional[List[str]] = None,
        domain: Optional[List[str]] = None,
        country: Optional[List[str]] = None,
        exchange: Optional[List[str]] = None,
        num_employees_from: Optional[int] = None,
        num_employees_to: Optional[int] = None,
        ipo_from: Optional[datetime] = None,
        ipo_to: Optional[datetime] = None,
        q: Optional[str] = None,
        name: Optional[str] = None,
        industry: Optional[str] = None,
        sector: Optional[str] = None,
        size: Optional[int] = None,
        page: Optional[int] = None,
    ) -> CompanySearchResult:
        """
        Browse or search for companies Perigon tracks using name, domain, ticker symbol, industry, and more. Supports Boolean search logic and filtering by metadata such as country, exchange, employee count, and IPO date.

        Args:
            id (Optional[List[str]]): Filter by unique company identifiers. Multiple values create an OR filter.
            symbol (Optional[List[str]]): Filter by company stock ticker symbols (e.g., AAPL, MSFT, GOOGL). Multiple values create an OR filter.
            domain (Optional[List[str]]): Filter by company domains or websites (e.g., apple.com, microsoft.com). Multiple values create an OR filter.
            country (Optional[List[str]]): Filter by company headquarters country. Multiple values create an OR filter.
            exchange (Optional[List[str]]): Filter by stock exchange where companies are listed (e.g., NASDAQ, NYSE). Multiple values create an OR filter.
            num_employees_from (Optional[int]): Filter for companies with at least this many employees.
            num_employees_to (Optional[int]): Filter for companies with no more than this many employees.
            ipo_from (Optional[datetime]): Filter for companies that went public on or after this date. Accepts ISO 8601 format (e.g., 2023-01-01T00:00:00) or yyyy-mm-dd format.
            ipo_to (Optional[datetime]): Filter for companies that went public on or before this date. Accepts ISO 8601 format (e.g., 2023-12-31T23:59:59) or yyyy-mm-dd format.
            q (Optional[str]): Primary search query for filtering companies across name, alternative names, domains, and ticker symbols. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            name (Optional[str]): Search within company names. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            industry (Optional[str]): Filter by company industry classifications. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            sector (Optional[str]): Filter by company sector classifications. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            size (Optional[int]): The number of companies to return per page in the paginated response.
            page (Optional[int]): The specific page of results to retrieve in the paginated response. Starts at 0.

        Returns:
            CompanySearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_COMPANIES

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if id is not None:
            params["id"] = id
        if symbol is not None:
            params["symbol"] = symbol
        if domain is not None:
            params["domain"] = domain
        if country is not None:
            params["country"] = country
        if exchange is not None:
            params["exchange"] = exchange
        if num_employees_from is not None:
            params["numEmployeesFrom"] = num_employees_from
        if num_employees_to is not None:
            params["numEmployeesTo"] = num_employees_to
        if ipo_from is not None:
            params["ipoFrom"] = ipo_from
        if ipo_to is not None:
            params["ipoTo"] = ipo_to
        if q is not None:
            params["q"] = q
        if name is not None:
            params["name"] = name
        if industry is not None:
            params["industry"] = industry
        if sector is not None:
            params["sector"] = sector
        if size is not None:
            params["size"] = size
        if page is not None:
            params["page"] = page
        params = _normalise_query(params)

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()
        return CompanySearchResult.model_validate(resp.json())

    # ----------------- search_companies (async) ----------------- #
    async def search_companies_async(
        self,
        id: Optional[List[str]] = None,
        symbol: Optional[List[str]] = None,
        domain: Optional[List[str]] = None,
        country: Optional[List[str]] = None,
        exchange: Optional[List[str]] = None,
        num_employees_from: Optional[int] = None,
        num_employees_to: Optional[int] = None,
        ipo_from: Optional[datetime] = None,
        ipo_to: Optional[datetime] = None,
        q: Optional[str] = None,
        name: Optional[str] = None,
        industry: Optional[str] = None,
        sector: Optional[str] = None,
        size: Optional[int] = None,
        page: Optional[int] = None,
    ) -> CompanySearchResult:
        """
        Async variant of search_companies. Browse or search for companies Perigon tracks using name, domain, ticker symbol, industry, and more. Supports Boolean search logic and filtering by metadata such as country, exchange, employee count, and IPO date.

        Args:
            id (Optional[List[str]]): Filter by unique company identifiers. Multiple values create an OR filter.
            symbol (Optional[List[str]]): Filter by company stock ticker symbols (e.g., AAPL, MSFT, GOOGL). Multiple values create an OR filter.
            domain (Optional[List[str]]): Filter by company domains or websites (e.g., apple.com, microsoft.com). Multiple values create an OR filter.
            country (Optional[List[str]]): Filter by company headquarters country. Multiple values create an OR filter.
            exchange (Optional[List[str]]): Filter by stock exchange where companies are listed (e.g., NASDAQ, NYSE). Multiple values create an OR filter.
            num_employees_from (Optional[int]): Filter for companies with at least this many employees.
            num_employees_to (Optional[int]): Filter for companies with no more than this many employees.
            ipo_from (Optional[datetime]): Filter for companies that went public on or after this date. Accepts ISO 8601 format (e.g., 2023-01-01T00:00:00) or yyyy-mm-dd format.
            ipo_to (Optional[datetime]): Filter for companies that went public on or before this date. Accepts ISO 8601 format (e.g., 2023-12-31T23:59:59) or yyyy-mm-dd format.
            q (Optional[str]): Primary search query for filtering companies across name, alternative names, domains, and ticker symbols. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            name (Optional[str]): Search within company names. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            industry (Optional[str]): Filter by company industry classifications. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            sector (Optional[str]): Filter by company sector classifications. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            size (Optional[int]): The number of companies to return per page in the paginated response.
            page (Optional[int]): The specific page of results to retrieve in the paginated response. Starts at 0.

        Returns:
            CompanySearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_COMPANIES

        params: Dict[str, Any] = {}
        if id is not None:
            params["id"] = id
        if symbol is not None:
            params["symbol"] = symbol
        if domain is not None:
            params["domain"] = domain
        if country is not None:
            params["country"] = country
        if exchange is not None:
            params["exchange"] = exchange
        if num_employees_from is not None:
            params["numEmployeesFrom"] = num_employees_from
        if num_employees_to is not None:
            params["numEmployeesTo"] = num_employees_to
        if ipo_from is not None:
            params["ipoFrom"] = ipo_from
        if ipo_to is not None:
            params["ipoTo"] = ipo_to
        if q is not None:
            params["q"] = q
        if name is not None:
            params["name"] = name
        if industry is not None:
            params["industry"] = industry
        if sector is not None:
            params["sector"] = sector
        if size is not None:
            params["size"] = size
        if page is not None:
            params["page"] = page
        params = _normalise_query(params)

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()
        return CompanySearchResult.model_validate(resp.json())

    # ----------------- search_journalists (sync) ----------------- #
    def search_journalists(
        self,
        id: Optional[List[str]] = None,
        q: Optional[str] = None,
        name: Optional[str] = None,
        twitter: Optional[str] = None,
        size: Optional[int] = None,
        page: Optional[int] = None,
        source: Optional[List[str]] = None,
        topic: Optional[List[str]] = None,
        category: Optional[List[str]] = None,
        label: Optional[List[str]] = None,
        min_monthly_posts: Optional[int] = None,
        max_monthly_posts: Optional[int] = None,
        country: Optional[List[str]] = None,
        updated_at_from: Optional[datetime] = None,
        updated_at_to: Optional[datetime] = None,
        show_num_results: Optional[bool] = None,
    ) -> JournalistSearchResult:
        """
        Search journalists using broad search attributes. Our database contains over 230,000 journalists from around the world and is refreshed frequently.

        Args:
            id (Optional[List[str]]): Filter by unique journalist identifiers. Multiple values create an OR filter to find journalists matching any of the specified IDs.
            q (Optional[str]): Primary search query for filtering journalists based on their name, title, and Twitter bio. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            name (Optional[str]): Search specifically within journalist names. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            twitter (Optional[str]): Filter journalists by their exact Twitter handle, without the @ symbol.
            size (Optional[int]): The number of journalists to return per page in the paginated response.
            page (Optional[int]): The specific page of results to retrieve in the paginated response. Starts at 0.
            source (Optional[List[str]]): Filter journalists by the publisher domains they write for. Supports wildcards (* and ?) for pattern matching (e.g., *.cnn.com). Multiple values create an OR filter.
            topic (Optional[List[str]]): Filter journalists by the topics they frequently cover. Multiple values create an OR filter to find journalists covering any of the specified topics.
            category (Optional[List[str]]): Filter journalists by the content categories they typically write about (e.g., Politics, Tech, Sports, Business). Multiple values create an OR filter.
            label (Optional[List[str]]): Filter journalists by the type of content they typically produce (e.g., Opinion, Paid-news, Non-news). Multiple values create an OR filter.
            min_monthly_posts (Optional[int]): Filter for journalists who publish at least this many articles per month. Used to identify more active journalists.
            max_monthly_posts (Optional[int]): Filter for journalists who publish no more than this many articles per month.
            country (Optional[List[str]]): Filter journalists by countries they commonly cover in their reporting. Uses ISO 3166-1 alpha-2 two-letter country codes in lowercase (e.g., us, gb, jp). Multiple values create an OR filter.
            updated_at_from (Optional[datetime]): Filter for journalist profiles updated on or after this date. Accepts ISO 8601 format (e.g., 2023-03-01T00:00:00) or yyyy-mm-dd format.
            updated_at_to (Optional[datetime]): Filter for journalist profiles updated on or before this date. Accepts ISO 8601 format (e.g., 2023-03-01T23:59:59) or yyyy-mm-dd format.
            show_num_results (Optional[bool]): Controls whether to return the exact result count. When false (default), counts are capped at 10,000 for performance reasons. Set to true for precise counts in smaller result sets.

        Returns:
            JournalistSearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_JOURNALISTS

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if id is not None:
            params["id"] = id
        if q is not None:
            params["q"] = q
        if name is not None:
            params["name"] = name
        if twitter is not None:
            params["twitter"] = twitter
        if size is not None:
            params["size"] = size
        if page is not None:
            params["page"] = page
        if source is not None:
            params["source"] = source
        if topic is not None:
            params["topic"] = topic
        if category is not None:
            params["category"] = category
        if label is not None:
            params["label"] = label
        if min_monthly_posts is not None:
            params["minMonthlyPosts"] = min_monthly_posts
        if max_monthly_posts is not None:
            params["maxMonthlyPosts"] = max_monthly_posts
        if country is not None:
            params["country"] = country
        if updated_at_from is not None:
            params["updatedAtFrom"] = updated_at_from
        if updated_at_to is not None:
            params["updatedAtTo"] = updated_at_to
        if show_num_results is not None:
            params["showNumResults"] = show_num_results
        params = _normalise_query(params)

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()
        return JournalistSearchResult.model_validate(resp.json())

    # ----------------- search_journalists (async) ----------------- #
    async def search_journalists_async(
        self,
        id: Optional[List[str]] = None,
        q: Optional[str] = None,
        name: Optional[str] = None,
        twitter: Optional[str] = None,
        size: Optional[int] = None,
        page: Optional[int] = None,
        source: Optional[List[str]] = None,
        topic: Optional[List[str]] = None,
        category: Optional[List[str]] = None,
        label: Optional[List[str]] = None,
        min_monthly_posts: Optional[int] = None,
        max_monthly_posts: Optional[int] = None,
        country: Optional[List[str]] = None,
        updated_at_from: Optional[datetime] = None,
        updated_at_to: Optional[datetime] = None,
        show_num_results: Optional[bool] = None,
    ) -> JournalistSearchResult:
        """
        Async variant of search_journalists. Search journalists using broad search attributes. Our database contains over 230,000 journalists from around the world and is refreshed frequently.

        Args:
            id (Optional[List[str]]): Filter by unique journalist identifiers. Multiple values create an OR filter to find journalists matching any of the specified IDs.
            q (Optional[str]): Primary search query for filtering journalists based on their name, title, and Twitter bio. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            name (Optional[str]): Search specifically within journalist names. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            twitter (Optional[str]): Filter journalists by their exact Twitter handle, without the @ symbol.
            size (Optional[int]): The number of journalists to return per page in the paginated response.
            page (Optional[int]): The specific page of results to retrieve in the paginated response. Starts at 0.
            source (Optional[List[str]]): Filter journalists by the publisher domains they write for. Supports wildcards (* and ?) for pattern matching (e.g., *.cnn.com). Multiple values create an OR filter.
            topic (Optional[List[str]]): Filter journalists by the topics they frequently cover. Multiple values create an OR filter to find journalists covering any of the specified topics.
            category (Optional[List[str]]): Filter journalists by the content categories they typically write about (e.g., Politics, Tech, Sports, Business). Multiple values create an OR filter.
            label (Optional[List[str]]): Filter journalists by the type of content they typically produce (e.g., Opinion, Paid-news, Non-news). Multiple values create an OR filter.
            min_monthly_posts (Optional[int]): Filter for journalists who publish at least this many articles per month. Used to identify more active journalists.
            max_monthly_posts (Optional[int]): Filter for journalists who publish no more than this many articles per month.
            country (Optional[List[str]]): Filter journalists by countries they commonly cover in their reporting. Uses ISO 3166-1 alpha-2 two-letter country codes in lowercase (e.g., us, gb, jp). Multiple values create an OR filter.
            updated_at_from (Optional[datetime]): Filter for journalist profiles updated on or after this date. Accepts ISO 8601 format (e.g., 2023-03-01T00:00:00) or yyyy-mm-dd format.
            updated_at_to (Optional[datetime]): Filter for journalist profiles updated on or before this date. Accepts ISO 8601 format (e.g., 2023-03-01T23:59:59) or yyyy-mm-dd format.
            show_num_results (Optional[bool]): Controls whether to return the exact result count. When false (default), counts are capped at 10,000 for performance reasons. Set to true for precise counts in smaller result sets.

        Returns:
            JournalistSearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_JOURNALISTS

        params: Dict[str, Any] = {}
        if id is not None:
            params["id"] = id
        if q is not None:
            params["q"] = q
        if name is not None:
            params["name"] = name
        if twitter is not None:
            params["twitter"] = twitter
        if size is not None:
            params["size"] = size
        if page is not None:
            params["page"] = page
        if source is not None:
            params["source"] = source
        if topic is not None:
            params["topic"] = topic
        if category is not None:
            params["category"] = category
        if label is not None:
            params["label"] = label
        if min_monthly_posts is not None:
            params["minMonthlyPosts"] = min_monthly_posts
        if max_monthly_posts is not None:
            params["maxMonthlyPosts"] = max_monthly_posts
        if country is not None:
            params["country"] = country
        if updated_at_from is not None:
            params["updatedAtFrom"] = updated_at_from
        if updated_at_to is not None:
            params["updatedAtTo"] = updated_at_to
        if show_num_results is not None:
            params["showNumResults"] = show_num_results
        params = _normalise_query(params)

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()
        return JournalistSearchResult.model_validate(resp.json())

    # ----------------- search_people (sync) ----------------- #
    def search_people(
        self,
        name: Optional[str] = None,
        wikidata_id: Optional[List[str]] = None,
        occupation_id: Optional[List[str]] = None,
        occupation_label: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
    ) -> PeopleSearchResult:
        """
        Search and retrieve additional information on known persons that exist within Perigon&#39;s entity database and as referenced in any article response object. Our database contains over 650,000 people from around the world and is refreshed frequently. People data is derived from Wikidata and includes a wikidataId field that can be used to lookup even more information on Wikidata&#39;s website.

        Args:
            name (Optional[str]): Search by person's name. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            wikidata_id (Optional[List[str]]): Filter by Wikidata entity IDs (e.g., Q7747, Q937). These are unique identifiers from Wikidata.org that precisely identify public figures and eliminate name ambiguity. Multiple values create an OR filter.
            occupation_id (Optional[List[str]]): Filter by Wikidata occupation IDs (e.g., Q82955 for politician, Q33999 for actor, Q19546 for businessman). Finds people with specific professions. Multiple values create an OR filter.
            occupation_label (Optional[str]): Search by occupation name (e.g., politician, actor, CEO, athlete). Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            page (Optional[int]): The specific page of results to retrieve in the paginated response. Starts at 0.
            size (Optional[int]): The number of people to return per page in the paginated response.

        Returns:
            PeopleSearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_PEOPLE

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if wikidata_id is not None:
            params["wikidataId"] = wikidata_id
        if occupation_id is not None:
            params["occupationId"] = occupation_id
        if occupation_label is not None:
            params["occupationLabel"] = occupation_label
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        params = _normalise_query(params)

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()
        return PeopleSearchResult.model_validate(resp.json())

    # ----------------- search_people (async) ----------------- #
    async def search_people_async(
        self,
        name: Optional[str] = None,
        wikidata_id: Optional[List[str]] = None,
        occupation_id: Optional[List[str]] = None,
        occupation_label: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
    ) -> PeopleSearchResult:
        """
        Async variant of search_people. Search and retrieve additional information on known persons that exist within Perigon&#39;s entity database and as referenced in any article response object. Our database contains over 650,000 people from around the world and is refreshed frequently. People data is derived from Wikidata and includes a wikidataId field that can be used to lookup even more information on Wikidata&#39;s website.

        Args:
            name (Optional[str]): Search by person's name. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            wikidata_id (Optional[List[str]]): Filter by Wikidata entity IDs (e.g., Q7747, Q937). These are unique identifiers from Wikidata.org that precisely identify public figures and eliminate name ambiguity. Multiple values create an OR filter.
            occupation_id (Optional[List[str]]): Filter by Wikidata occupation IDs (e.g., Q82955 for politician, Q33999 for actor, Q19546 for businessman). Finds people with specific professions. Multiple values create an OR filter.
            occupation_label (Optional[str]): Search by occupation name (e.g., politician, actor, CEO, athlete). Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            page (Optional[int]): The specific page of results to retrieve in the paginated response. Starts at 0.
            size (Optional[int]): The number of people to return per page in the paginated response.

        Returns:
            PeopleSearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_PEOPLE

        params: Dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if wikidata_id is not None:
            params["wikidataId"] = wikidata_id
        if occupation_id is not None:
            params["occupationId"] = occupation_id
        if occupation_label is not None:
            params["occupationLabel"] = occupation_label
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        params = _normalise_query(params)

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()
        return PeopleSearchResult.model_validate(resp.json())

    # ----------------- search_sources (sync) ----------------- #
    def search_sources(
        self,
        domain: Optional[List[str]] = None,
        name: Optional[str] = None,
        source_group: Optional[str] = None,
        sort_by: Optional[SortBy] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        min_monthly_visits: Optional[int] = None,
        max_monthly_visits: Optional[int] = None,
        min_monthly_posts: Optional[int] = None,
        max_monthly_posts: Optional[int] = None,
        country: Optional[List[str]] = None,
        source_country: Optional[List[str]] = None,
        source_state: Optional[List[str]] = None,
        source_county: Optional[List[str]] = None,
        source_city: Optional[List[str]] = None,
        source_lat: Optional[float] = None,
        source_lon: Optional[float] = None,
        source_max_distance: Optional[float] = None,
        category: Optional[List[str]] = None,
        topic: Optional[List[str]] = None,
        label: Optional[List[str]] = None,
        paywall: Optional[bool] = None,
        show_subdomains: Optional[bool] = None,
        show_num_results: Optional[bool] = None,
    ) -> SourceSearchResult:
        """
        Search and filter the 142,000+ media sources available via the Perigon API. The result includes a list of individual media sources that were matched to your specific criteria.

        Args:
            domain (Optional[List[str]]): Filter by specific publisher domains or subdomains. Supports wildcards (* and ?) for pattern matching (e.g., *.cnn.com, us?.nytimes.com). Multiple values create an OR filter.
            name (Optional[str]): Search by source name or alternative names. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            source_group (Optional[str]): Filter by predefined publisher bundles (e.g., top100, top50tech). Returns all sources within the specified group. See documentation for available source groups.
            sort_by (Optional[SortBy]): Determines the source sorting order. Options include relevance (default, best match to query), globalRank (by overall traffic and popularity), monthlyVisits (by total monthly visitor count), and avgMonthlyPosts (by number of articles published monthly).
            page (Optional[int]): The specific page of results to retrieve in the paginated response. Starts at 0.
            size (Optional[int]): The number of sources to return per page in the paginated response.
            min_monthly_visits (Optional[int]): Filter for sources with at least this many monthly visitors. Used to target publishers by audience size.
            max_monthly_visits (Optional[int]): Filter for sources with no more than this many monthly visitors. Used to target publishers by audience size.
            min_monthly_posts (Optional[int]): Filter for sources that publish at least this many articles per month. Used to target publishers by content volume.
            max_monthly_posts (Optional[int]): Filter for sources that publish no more than this many articles per month. Used to target publishers by content volume.
            country (Optional[List[str]]): Filter sources by countries they commonly cover in their reporting. Uses ISO 3166-1 alpha-2 two-letter country codes in lowercase (e.g., us, gb, jp). See documentation for supported country codes. Multiple values create an OR filter.
            source_country (Optional[List[str]]): Filter for local publications based in specific countries. Uses ISO 3166-1 alpha-2 two-letter country codes in lowercase (e.g., us, gb, jp). See documentation for supported country codes. Multiple values create an OR filter.
            source_state (Optional[List[str]]): Filter for local publications based in specific states or regions. Uses standard two-letter state codes in lowercase (e.g., ca, ny, tx). See documentation for supported state codes. Multiple values create an OR filter.
            source_county (Optional[List[str]]): Filter for local publications based in specific counties. Multiple values create an OR filter.
            source_city (Optional[List[str]]): Filter for local publications based in specific cities. Multiple values create an OR filter.
            source_lat (Optional[float]): Latitude coordinate for filtering local publications by geographic proximity. Used with sourceLon and sourceMaxDistance for radius search.
            source_lon (Optional[float]): Longitude coordinate for filtering local publications by geographic proximity. Used with sourceLat and sourceMaxDistance for radius search.
            source_max_distance (Optional[float]): Maximum distance in kilometers from the coordinates defined by sourceLat and sourceLon. Defines the radius for local publication searches.
            category (Optional[List[str]]): Filter sources by their primary content categories such as Politics, Tech, Sports, Business, or Finance. Returns sources that frequently cover these topics. Multiple values create an OR filter.
            topic (Optional[List[str]]): Filter sources by their frequently covered topics (e.g., Markets, Cryptocurrency, Climate Change). Returns sources where the specified topic is among their top 10 covered areas. Multiple values create an OR filter.
            label (Optional[List[str]]): Filter sources by their content label patterns (e.g., Opinion, Paid-news, Non-news). Returns sources where the specified label is common in their published content. See documentation for all available labels. Multiple values create an OR filter.
            paywall (Optional[bool]): Filter by paywall status. Set to true to find sources with paywalls, or false to find sources without paywalls.
            show_subdomains (Optional[bool]): Controls whether subdomains are included as separate results. When true (default), subdomains appear as distinct sources. When false, results are consolidated to parent domains only.
            show_num_results (Optional[bool]): Controls whether to return the exact result count. When false (default), counts are capped at 10,000 for performance reasons. Set to true for precise counts in smaller result sets.

        Returns:
            SourceSearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_SOURCES

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if domain is not None:
            params["domain"] = domain
        if name is not None:
            params["name"] = name
        if source_group is not None:
            params["sourceGroup"] = source_group
        if sort_by is not None:
            params["sortBy"] = sort_by
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if min_monthly_visits is not None:
            params["minMonthlyVisits"] = min_monthly_visits
        if max_monthly_visits is not None:
            params["maxMonthlyVisits"] = max_monthly_visits
        if min_monthly_posts is not None:
            params["minMonthlyPosts"] = min_monthly_posts
        if max_monthly_posts is not None:
            params["maxMonthlyPosts"] = max_monthly_posts
        if country is not None:
            params["country"] = country
        if source_country is not None:
            params["sourceCountry"] = source_country
        if source_state is not None:
            params["sourceState"] = source_state
        if source_county is not None:
            params["sourceCounty"] = source_county
        if source_city is not None:
            params["sourceCity"] = source_city
        if source_lat is not None:
            params["sourceLat"] = source_lat
        if source_lon is not None:
            params["sourceLon"] = source_lon
        if source_max_distance is not None:
            params["sourceMaxDistance"] = source_max_distance
        if category is not None:
            params["category"] = category
        if topic is not None:
            params["topic"] = topic
        if label is not None:
            params["label"] = label
        if paywall is not None:
            params["paywall"] = paywall
        if show_subdomains is not None:
            params["showSubdomains"] = show_subdomains
        if show_num_results is not None:
            params["showNumResults"] = show_num_results
        params = _normalise_query(params)

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()
        return SourceSearchResult.model_validate(resp.json())

    # ----------------- search_sources (async) ----------------- #
    async def search_sources_async(
        self,
        domain: Optional[List[str]] = None,
        name: Optional[str] = None,
        source_group: Optional[str] = None,
        sort_by: Optional[SortBy] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        min_monthly_visits: Optional[int] = None,
        max_monthly_visits: Optional[int] = None,
        min_monthly_posts: Optional[int] = None,
        max_monthly_posts: Optional[int] = None,
        country: Optional[List[str]] = None,
        source_country: Optional[List[str]] = None,
        source_state: Optional[List[str]] = None,
        source_county: Optional[List[str]] = None,
        source_city: Optional[List[str]] = None,
        source_lat: Optional[float] = None,
        source_lon: Optional[float] = None,
        source_max_distance: Optional[float] = None,
        category: Optional[List[str]] = None,
        topic: Optional[List[str]] = None,
        label: Optional[List[str]] = None,
        paywall: Optional[bool] = None,
        show_subdomains: Optional[bool] = None,
        show_num_results: Optional[bool] = None,
    ) -> SourceSearchResult:
        """
        Async variant of search_sources. Search and filter the 142,000+ media sources available via the Perigon API. The result includes a list of individual media sources that were matched to your specific criteria.

        Args:
            domain (Optional[List[str]]): Filter by specific publisher domains or subdomains. Supports wildcards (* and ?) for pattern matching (e.g., *.cnn.com, us?.nytimes.com). Multiple values create an OR filter.
            name (Optional[str]): Search by source name or alternative names. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            source_group (Optional[str]): Filter by predefined publisher bundles (e.g., top100, top50tech). Returns all sources within the specified group. See documentation for available source groups.
            sort_by (Optional[SortBy]): Determines the source sorting order. Options include relevance (default, best match to query), globalRank (by overall traffic and popularity), monthlyVisits (by total monthly visitor count), and avgMonthlyPosts (by number of articles published monthly).
            page (Optional[int]): The specific page of results to retrieve in the paginated response. Starts at 0.
            size (Optional[int]): The number of sources to return per page in the paginated response.
            min_monthly_visits (Optional[int]): Filter for sources with at least this many monthly visitors. Used to target publishers by audience size.
            max_monthly_visits (Optional[int]): Filter for sources with no more than this many monthly visitors. Used to target publishers by audience size.
            min_monthly_posts (Optional[int]): Filter for sources that publish at least this many articles per month. Used to target publishers by content volume.
            max_monthly_posts (Optional[int]): Filter for sources that publish no more than this many articles per month. Used to target publishers by content volume.
            country (Optional[List[str]]): Filter sources by countries they commonly cover in their reporting. Uses ISO 3166-1 alpha-2 two-letter country codes in lowercase (e.g., us, gb, jp). See documentation for supported country codes. Multiple values create an OR filter.
            source_country (Optional[List[str]]): Filter for local publications based in specific countries. Uses ISO 3166-1 alpha-2 two-letter country codes in lowercase (e.g., us, gb, jp). See documentation for supported country codes. Multiple values create an OR filter.
            source_state (Optional[List[str]]): Filter for local publications based in specific states or regions. Uses standard two-letter state codes in lowercase (e.g., ca, ny, tx). See documentation for supported state codes. Multiple values create an OR filter.
            source_county (Optional[List[str]]): Filter for local publications based in specific counties. Multiple values create an OR filter.
            source_city (Optional[List[str]]): Filter for local publications based in specific cities. Multiple values create an OR filter.
            source_lat (Optional[float]): Latitude coordinate for filtering local publications by geographic proximity. Used with sourceLon and sourceMaxDistance for radius search.
            source_lon (Optional[float]): Longitude coordinate for filtering local publications by geographic proximity. Used with sourceLat and sourceMaxDistance for radius search.
            source_max_distance (Optional[float]): Maximum distance in kilometers from the coordinates defined by sourceLat and sourceLon. Defines the radius for local publication searches.
            category (Optional[List[str]]): Filter sources by their primary content categories such as Politics, Tech, Sports, Business, or Finance. Returns sources that frequently cover these topics. Multiple values create an OR filter.
            topic (Optional[List[str]]): Filter sources by their frequently covered topics (e.g., Markets, Cryptocurrency, Climate Change). Returns sources where the specified topic is among their top 10 covered areas. Multiple values create an OR filter.
            label (Optional[List[str]]): Filter sources by their content label patterns (e.g., Opinion, Paid-news, Non-news). Returns sources where the specified label is common in their published content. See documentation for all available labels. Multiple values create an OR filter.
            paywall (Optional[bool]): Filter by paywall status. Set to true to find sources with paywalls, or false to find sources without paywalls.
            show_subdomains (Optional[bool]): Controls whether subdomains are included as separate results. When true (default), subdomains appear as distinct sources. When false, results are consolidated to parent domains only.
            show_num_results (Optional[bool]): Controls whether to return the exact result count. When false (default), counts are capped at 10,000 for performance reasons. Set to true for precise counts in smaller result sets.

        Returns:
            SourceSearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_SOURCES

        params: Dict[str, Any] = {}
        if domain is not None:
            params["domain"] = domain
        if name is not None:
            params["name"] = name
        if source_group is not None:
            params["sourceGroup"] = source_group
        if sort_by is not None:
            params["sortBy"] = sort_by
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if min_monthly_visits is not None:
            params["minMonthlyVisits"] = min_monthly_visits
        if max_monthly_visits is not None:
            params["maxMonthlyVisits"] = max_monthly_visits
        if min_monthly_posts is not None:
            params["minMonthlyPosts"] = min_monthly_posts
        if max_monthly_posts is not None:
            params["maxMonthlyPosts"] = max_monthly_posts
        if country is not None:
            params["country"] = country
        if source_country is not None:
            params["sourceCountry"] = source_country
        if source_state is not None:
            params["sourceState"] = source_state
        if source_county is not None:
            params["sourceCounty"] = source_county
        if source_city is not None:
            params["sourceCity"] = source_city
        if source_lat is not None:
            params["sourceLat"] = source_lat
        if source_lon is not None:
            params["sourceLon"] = source_lon
        if source_max_distance is not None:
            params["sourceMaxDistance"] = source_max_distance
        if category is not None:
            params["category"] = category
        if topic is not None:
            params["topic"] = topic
        if label is not None:
            params["label"] = label
        if paywall is not None:
            params["paywall"] = paywall
        if show_subdomains is not None:
            params["showSubdomains"] = show_subdomains
        if show_num_results is not None:
            params["showNumResults"] = show_num_results
        params = _normalise_query(params)

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()
        return SourceSearchResult.model_validate(resp.json())

    # ----------------- search_topics (sync) ----------------- #
    def search_topics(
        self,
        name: Optional[str] = None,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
    ) -> TopicSearchResult:
        """
        Search through all available Topics that exist within the Perigon Database.

        Args:
            name (Optional[str]): Search for topics by exact name or partial text match. Does not support wildcards. Examples include Markets, Cryptocurrency, Climate Change, etc.
            category (Optional[str]): Filter topics by broad article categories such as Politics, Tech, Sports, Business, Finance, Entertainment, etc.
            subcategory (Optional[str]): Filter topics by their specific subcategory. Subcategories provide more granular classification beyond the main category, such as TV or Event.
            page (Optional[int]): The specific page of results to retrieve in the paginated response. Starts at 0.
            size (Optional[int]): The number of topics to return per page in the paginated response.

        Returns:
            TopicSearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_TOPICS

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if category is not None:
            params["category"] = category
        if subcategory is not None:
            params["subcategory"] = subcategory
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        params = _normalise_query(params)

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()
        return TopicSearchResult.model_validate(resp.json())

    # ----------------- search_topics (async) ----------------- #
    async def search_topics_async(
        self,
        name: Optional[str] = None,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
    ) -> TopicSearchResult:
        """
        Async variant of search_topics. Search through all available Topics that exist within the Perigon Database.

        Args:
            name (Optional[str]): Search for topics by exact name or partial text match. Does not support wildcards. Examples include Markets, Cryptocurrency, Climate Change, etc.
            category (Optional[str]): Filter topics by broad article categories such as Politics, Tech, Sports, Business, Finance, Entertainment, etc.
            subcategory (Optional[str]): Filter topics by their specific subcategory. Subcategories provide more granular classification beyond the main category, such as TV or Event.
            page (Optional[int]): The specific page of results to retrieve in the paginated response. Starts at 0.
            size (Optional[int]): The number of topics to return per page in the paginated response.

        Returns:
            TopicSearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_TOPICS

        params: Dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if category is not None:
            params["category"] = category
        if subcategory is not None:
            params["subcategory"] = subcategory
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        params = _normalise_query(params)

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()
        return TopicSearchResult.model_validate(resp.json())

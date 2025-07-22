from datetime import datetime
from enum import Enum
from typing import Any, Dict, Iterable, List, Mapping, Optional, Union

from pydantic import Field, StrictBool, StrictFloat, StrictInt, StrictStr
from typing_extensions import Annotated

from perigon.api_client import ApiClient
from perigon.models.all_endpoint_sort_by import AllEndpointSortBy
from perigon.models.article_search_params import ArticleSearchParams
from perigon.models.articles_vector_search_result import ArticlesVectorSearchResult
from perigon.models.company_search_result import CompanySearchResult
from perigon.models.journalist import Journalist
from perigon.models.journalist_search_result import JournalistSearchResult
from perigon.models.people_search_result import PeopleSearchResult
from perigon.models.query_search_result import QuerySearchResult
from perigon.models.sort_by import SortBy
from perigon.models.source_search_result import SourceSearchResult
from perigon.models.story_search_result import StorySearchResult
from perigon.models.summary_body import SummaryBody
from perigon.models.summary_search_result import SummarySearchResult
from perigon.models.topic_search_result import TopicSearchResult
from perigon.models.wikipedia_search_params import WikipediaSearchParams
from perigon.models.wikipedia_search_result import WikipediaSearchResult
from perigon.models.wikipedia_vector_search_result import WikipediaVectorSearchResult

# Define API paths
PATH_GET_JOURNALIST_BY_ID = "/v1/journalists/{id}"
PATH_SEARCH_ARTICLES = "/v1/articles/all"
PATH_SEARCH_COMPANIES = "/v1/companies/all"
PATH_SEARCH_JOURNALISTS = "/v1/journalists/all"
PATH_SEARCH_PEOPLE = "/v1/people/all"
PATH_SEARCH_SOURCES = "/v1/sources/all"
PATH_SEARCH_STORIES = "/v1/stories/all"
PATH_SEARCH_SUMMARIZER = "/v1/summarize"
PATH_SEARCH_TOPICS = "/v1/topics/all"
PATH_SEARCH_WIKIPEDIA = "/v1/wikipedia/all"
PATH_VECTOR_SEARCH_ARTICLES = "/v1/vector/news/all"
PATH_VECTOR_SEARCH_WIKIPEDIA = "/v1/vector/wikipedia/all"


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


class V1Api:
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

    # ----------------- search_articles (sync) ----------------- #
    def search_articles(
        self,
        q: Optional[str] = None,
        title: Optional[str] = None,
        desc: Optional[str] = None,
        content: Optional[str] = None,
        url: Optional[str] = None,
        article_id: Optional[List[str]] = None,
        cluster_id: Optional[List[str]] = None,
        sort_by: Optional[AllEndpointSortBy] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        var_from: Optional[datetime] = None,
        to: Optional[datetime] = None,
        add_date_from: Optional[datetime] = None,
        add_date_to: Optional[datetime] = None,
        refresh_date_from: Optional[datetime] = None,
        refresh_date_to: Optional[datetime] = None,
        medium: Optional[List[str]] = None,
        source: Optional[List[str]] = None,
        source_group: Optional[List[str]] = None,
        exclude_source_group: Optional[List[str]] = None,
        exclude_source: Optional[List[str]] = None,
        paywall: Optional[bool] = None,
        byline: Optional[List[str]] = None,
        author: Optional[List[str]] = None,
        exclude_author: Optional[List[str]] = None,
        journalist_id: Optional[List[str]] = None,
        exclude_journalist_id: Optional[List[str]] = None,
        language: Optional[List[str]] = None,
        exclude_language: Optional[List[str]] = None,
        search_translation: Optional[bool] = None,
        label: Optional[List[str]] = None,
        exclude_label: Optional[List[str]] = None,
        category: Optional[List[str]] = None,
        exclude_category: Optional[List[str]] = None,
        topic: Optional[List[str]] = None,
        exclude_topic: Optional[List[str]] = None,
        link_to: Optional[str] = None,
        show_reprints: Optional[bool] = None,
        reprint_group_id: Optional[str] = None,
        city: Optional[List[str]] = None,
        exclude_city: Optional[List[str]] = None,
        area: Optional[List[str]] = None,
        state: Optional[List[str]] = None,
        exclude_state: Optional[List[str]] = None,
        county: Optional[List[str]] = None,
        exclude_county: Optional[List[str]] = None,
        locations_country: Optional[List[str]] = None,
        country: Optional[List[str]] = None,
        exclude_locations_country: Optional[List[str]] = None,
        location: Optional[List[str]] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        max_distance: Optional[float] = None,
        source_city: Optional[List[str]] = None,
        source_county: Optional[List[str]] = None,
        source_country: Optional[List[str]] = None,
        source_state: Optional[List[str]] = None,
        source_lat: Optional[float] = None,
        source_lon: Optional[float] = None,
        source_max_distance: Optional[float] = None,
        person_wikidata_id: Optional[List[str]] = None,
        exclude_person_wikidata_id: Optional[List[str]] = None,
        person_name: Optional[List[str]] = None,
        exclude_person_name: Optional[List[str]] = None,
        company_id: Optional[List[str]] = None,
        exclude_company_id: Optional[List[str]] = None,
        company_name: Optional[str] = None,
        company_domain: Optional[List[str]] = None,
        exclude_company_domain: Optional[List[str]] = None,
        company_symbol: Optional[List[str]] = None,
        exclude_company_symbol: Optional[List[str]] = None,
        show_num_results: Optional[bool] = None,
        positive_sentiment_from: Optional[float] = None,
        positive_sentiment_to: Optional[float] = None,
        neutral_sentiment_from: Optional[float] = None,
        neutral_sentiment_to: Optional[float] = None,
        negative_sentiment_from: Optional[float] = None,
        negative_sentiment_to: Optional[float] = None,
        taxonomy: Optional[List[str]] = None,
        prefix_taxonomy: Optional[str] = None,
        show_highlighting: Optional[bool] = None,
        highlight_fragment_size: Optional[int] = None,
        highlight_num_fragments: Optional[int] = None,
        highlight_pre_tag: Optional[str] = None,
        highlight_post_tag: Optional[str] = None,
        highlight_q: Optional[str] = None,
    ) -> QuerySearchResult:
        """
        Search and filter all news articles available via the Perigon API. The result includes a list of individual articles that were matched to your specific criteria.

        Args:
            q (Optional[str]): Primary search query for filtering articles based on their title, description, and content. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            title (Optional[str]): Search specifically within article headlines/titles. Supports Boolean operators, exact phrases with quotes, and wildcards for matching title variations.
            desc (Optional[str]): Search within article description fields. Supports Boolean expressions, exact phrase matching with quotes, and wildcards for flexible pattern matching.
            content (Optional[str]): Search within the full article body content. Supports Boolean logic, exact phrase matching with quotes, and wildcards for comprehensive content searching.
            url (Optional[str]): Search within article URLs to find content from specific website sections or domains. Supports wildcards (* and ?) for partial URL matching.
            article_id (Optional[List[str]]): Retrieve specific news articles by their unique article identifiers. Multiple IDs can be provided to return a collection of specific articles.
            cluster_id (Optional[List[str]]): Filter results to only show content within a specific related content cluster. Returns articles grouped together as part of Perigon Stories based on topic relevance.
            sort_by (Optional[AllEndpointSortBy]): Determines the article sorting order. Options include relevance (default), date/pubDate (newest publication date first), reverseDate (oldest publication date first), addDate (newest ingestion date first), reverseAddDate (oldest ingestion date first), and refreshDate (most recently updated in system first, often identical to addDate).
            page (Optional[int]): The specific page of results to retrieve in the paginated response. Starts at 0.
            size (Optional[int]): The number of articles to return per page in the paginated response.
            var_from (Optional[datetime]): Filter for articles published after this date. Accepts ISO 8601 format (e.g., 2023-03-01T00:00:00) or yyyy-mm-dd format.
            to (Optional[datetime]): Filter for articles published before this date. Accepts ISO 8601 format (e.g., 2022-02-01T23:59:59) or yyyy-mm-dd format.
            add_date_from (Optional[datetime]): Filter for articles added to Perigon's system after this date. Accepts ISO 8601 format (e.g., 2022-02-01T00:00:00) or yyyy-mm-dd format.
            add_date_to (Optional[datetime]): Filter for articles added to Perigon's system before this date. Accepts ISO 8601 format (e.g., 2022-02-01T23:59:59) or yyyy-mm-dd format.
            refresh_date_from (Optional[datetime]): Filter for articles refreshed/updated in Perigon's system after this date. In most cases yields similar results to addDateFrom but can differ for updated content. Accepts ISO 8601 format (e.g., 2022-02-01T00:00:00) or yyyy-mm-dd format.
            refresh_date_to (Optional[datetime]): Filter for articles refreshed/updated in Perigon's system before this date. In most cases yields similar results to addDateTo but can differ for updated content. Accepts ISO 8601 format (e.g., 2022-02-01T23:59:59) or yyyy-mm-dd format.
            medium (Optional[List[str]]): Filter articles by their primary medium type. Accepts Article for written content or Video for video-based stories. Multiple values create an OR filter.
            source (Optional[List[str]]): Filter articles by specific publisher domains or subdomains. Supports wildcards (* and ?) for pattern matching (e.g., *.cnn.com). Multiple values create an OR filter.
            source_group (Optional[List[str]]): Filter articles using Perigon's curated publisher bundles (e.g., top100, top25crypto). Multiple values create an OR filter to include articles from any of the specified bundles.
            exclude_source_group (Optional[List[str]]): Exclude articles from specified Perigon source groups. Multiple values create an AND-exclude filter, removing content from publishers in any of the specified bundles (e.g., top10, top100).
            exclude_source (Optional[List[str]]): Exclude articles from specific publisher domains or subdomains. Supports wildcards (* and ?) for pattern matching (e.g., *.cnn.com). Multiple values create an AND-exclude filter.
            paywall (Optional[bool]): Filter to show only results where the source has a paywall (true) or does not have a paywall (false).
            byline (Optional[List[str]]): Filter articles by author bylines. Works as an exact match for each author name provided. Multiple values create an OR filter to find articles by any of the specified authors.
            author (Optional[List[str]]): Filter articles by specific author names. Works as an exact match for each name. Multiple values create an OR filter to find articles by any of the specified authors.
            exclude_author (Optional[List[str]]): Exclude articles written by specific authors. Any article with an author name matching an entry in this list will be omitted from results. Multiple values create an AND-exclude filter.
            journalist_id (Optional[List[str]]): Filter by unique journalist identifiers which can be found through the Journalist API or in the matchedAuthors field. Multiple values create an OR filter.
            exclude_journalist_id (Optional[List[str]]): Exclude articles written by specific journalists identified by their unique IDs. Multiple values create an AND-exclude filter.
            language (Optional[List[str]]): Filter articles by their language using ISO-639 two-letter codes (e.g., en, es, fr). Multiple values create an OR filter.
            exclude_language (Optional[List[str]]): Exclude articles in specific languages using ISO-639 two-letter codes. Multiple values create an AND-exclude filter.
            search_translation (Optional[bool]): Expand search to include translated content fields for non-English articles. When true, searches translated title, description, and content fields.
            label (Optional[List[str]]): Filter articles by editorial labels such as Opinion, Paid-news, Non-news, Fact Check, or Press Release. Multiple values create an OR filter.
            exclude_label (Optional[List[str]]): Exclude articles with specific editorial labels. Multiple values create an AND-exclude filter, removing all content with any of these labels.
            category (Optional[List[str]]): Filter by broad content categories such as Politics, Tech, Sports, Business, or Finance. Use 'none' to find uncategorized articles. Multiple values create an OR filter.
            exclude_category (Optional[List[str]]): Exclude articles with specific categories. Multiple values create an AND-exclude filter, removing all content with any of these categories.
            topic (Optional[List[str]]): Filter by specific topics such as Markets, Crime, Cryptocurrency, or College Sports. Topics are more granular than categories, and articles can have multiple topics. Use the /topics endpoint for a complete list of available topics. Multiple values create an OR filter.
            exclude_topic (Optional[List[str]]): Exclude articles with specific topics. Multiple values create an AND-exclude filter, removing all content with any of these topics.
            link_to (Optional[str]): Returns only articles that contain links to the specified URL pattern. Matches against the 'links' field in article responses.
            show_reprints (Optional[bool]): Controls whether to include reprinted content in results. When true (default), shows syndicated articles from wire services like AP or Reuters that appear on multiple sites.
            reprint_group_id (Optional[str]): Returns all articles in a specific reprint group, including the original article and all its known reprints. Use when you want to see all versions of the same content.
            city (Optional[List[str]]): Filters articles where a specified city plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the urban area in question. If multiple parameters are passed, they will be applied as OR operations.
            exclude_city (Optional[List[str]]): A list of cities to exclude from the results. Articles that are associated with any of the specified cities will be filtered out.
            area (Optional[List[str]]): Filters articles where a specified area, such as a neighborhood, borough, or district, plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the area in question. If multiple parameters are passed, they will be applied as OR operations.
            state (Optional[List[str]]): Filters articles where a specified state plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the state in question. If multiple parameters are passed, they will be applied as OR operations.
            exclude_state (Optional[List[str]]): A list of states to exclude. Articles that include, or are associated with, any of the states provided here will be filtered out. This is especially useful if you want to ignore news tied to certain geographical areas (e.g., US states).
            county (Optional[List[str]]): A list of counties to include (or specify) in the search results. This field filters the returned articles based on the county associated with the event or news. Only articles tagged with one of these counties will be included.
            exclude_county (Optional[List[str]]): Excludes articles from specific counties or administrative divisions in the search results. Accepts either a single county name or a list of county names. County names should match the format used in article metadata (e.g., 'Los Angeles County', 'Cook County'). This parameter allows for more granular geographic filter
            locations_country (Optional[List[str]]): Filters articles where a specified country plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the country in question. If multiple parameters are passed, they will be applied as OR operations.
            country (Optional[List[str]]): Country code to filter by country. If multiple parameters are passed, they will be applied as OR operations.
            exclude_locations_country (Optional[List[str]]): Excludes articles where a specified country plays a central role in the content, ensuring results are not deeply relevant to the country in question. If multiple parameters are passed, they will be applied as AND operations, excluding articles relevant to any of the specified countries.
            location (Optional[List[str]]): Return all articles that have the specified location. Location attributes are delimited by ':' between key and value, and '::' between attributes. Example: 'city:New York::state:NY'.
            lat (Optional[float]): Latitude of the center point to search places
            lon (Optional[float]): Longitude of the center point to search places
            max_distance (Optional[float]): Maximum distance (in km) from starting point to search articles by tagged places
            source_city (Optional[List[str]]): Find articles published by sources that are located within a given city.
            source_county (Optional[List[str]]): Find articles published by sources that are located within a given county.
            source_country (Optional[List[str]]): Find articles published by sources that are located within a given country. Must be 2 character country code (i.e. us, gb, etc).
            source_state (Optional[List[str]]): Find articles published by sources that are located within a given state.
            source_lat (Optional[float]): Latitude of the center point to search articles created by local publications.
            source_lon (Optional[float]): Latitude of the center point to search articles created by local publications.
            source_max_distance (Optional[float]): Maximum distance from starting point to search articles created by local publications.
            person_wikidata_id (Optional[List[str]]): Filter articles by Wikidata IDs of mentioned people. Refer to the /people endpoint for a complete list of tracked individuals.
            exclude_person_wikidata_id (Optional[List[str]]): Exclude articles mentioning people with specific Wikidata IDs. Creates an AND-exclude filter to remove content about these individuals. Uses precise identifiers to avoid name ambiguity.
            person_name (Optional[List[str]]): Filter articles by exact person name matches. Does not support Boolean or complex logic. For available person entities, consult the /people endpoint.
            exclude_person_name (Optional[List[str]]): Exclude articles mentioning specific people by name. Creates an AND-exclude filter to remove content about these individuals.
            company_id (Optional[List[str]]): Filter articles by company identifiers. For a complete list of tracked companies, refer to the /companies endpoint.
            exclude_company_id (Optional[List[str]]): Exclude articles mentioning companies with specific identifiers. Creates an AND-exclude filter to remove content about these corporate entities.
            company_name (Optional[str]): Filter articles by company name mentions. Performs an exact match on company names.
            company_domain (Optional[List[str]]): Filter articles by company domains (e.g., apple.com). For available company entities, consult the /companies endpoint.
            exclude_company_domain (Optional[List[str]]): Exclude articles related to companies with specific domains. Creates an AND-exclude filter to remove content about these companies.
            company_symbol (Optional[List[str]]): Filter articles by company stock symbols. For available company entities and their symbols, consult the /companies endpoint.
            exclude_company_symbol (Optional[List[str]]): A list of stock symbols (ticker symbols) that identify companies to be excluded. Articles related to companies using any of these symbols will be omitted, which is useful for targeting or avoiding specific public companies.
            show_num_results (Optional[bool]): Whether to show the total number of all matched articles. Default value is false which makes queries a bit more efficient but also counts up to 10000 articles.
            positive_sentiment_from (Optional[float]): Filter articles with a positive sentiment score greater than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger positive tone.
            positive_sentiment_to (Optional[float]): Filter articles with a positive sentiment score less than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger positive tone.
            neutral_sentiment_from (Optional[float]): Filter articles with a neutral sentiment score greater than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger neutral tone.
            neutral_sentiment_to (Optional[float]): Filter articles with a neutral sentiment score less than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger neutral tone.
            negative_sentiment_from (Optional[float]): Filter articles with a negative sentiment score greater than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger negative tone.
            negative_sentiment_to (Optional[float]): Filter articles with a negative sentiment score less than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger negative tone.
            taxonomy (Optional[List[str]]): Filters by Google Content Categories. This field will accept 1 or more categories, must pass the full name of the category. Example: taxonomy=/Finance/Banking/Other, /Finance/Investing/Funds. [Full list](https://cloud.google.com/natural-language/docs/categories)
            prefix_taxonomy (Optional[str]): Filters by Google Content Categories. This field will filter by the category prefix only. Example: prefixTaxonomy=/Finance
            show_highlighting (Optional[bool]): When set to true, enables text highlighting in search results.
            highlight_fragment_size (Optional[int]): Specifies the size in characters of each highlighted text fragment. Defaults to 100 if not specified.
            highlight_num_fragments (Optional[int]): Controls the maximum number of highlighted fragments to return per field.
            highlight_pre_tag (Optional[str]): Defines the HTML tag that appears before highlighted text. Defaults to '<em>' if not specified.
            highlight_post_tag (Optional[str]): Defines the HTML tag that appears after highlighted text. Defaults to '</em>' if not specified.
            highlight_q (Optional[str]): Specifies a separate query for highlighting, allowing highlights based on terms different from the main search query. Example: main query 'q=climate change' with 'highlightQ=renewable OR solar' will highlight terms 'renewable' and 'solar' in results about climate change.

        Returns:
            QuerySearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_ARTICLES

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if q is not None:
            params["q"] = q
        if title is not None:
            params["title"] = title
        if desc is not None:
            params["desc"] = desc
        if content is not None:
            params["content"] = content
        if url is not None:
            params["url"] = url
        if article_id is not None:
            params["articleId"] = article_id
        if cluster_id is not None:
            params["clusterId"] = cluster_id
        if sort_by is not None:
            params["sortBy"] = sort_by
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if var_from is not None:
            params["from"] = var_from
        if to is not None:
            params["to"] = to
        if add_date_from is not None:
            params["addDateFrom"] = add_date_from
        if add_date_to is not None:
            params["addDateTo"] = add_date_to
        if refresh_date_from is not None:
            params["refreshDateFrom"] = refresh_date_from
        if refresh_date_to is not None:
            params["refreshDateTo"] = refresh_date_to
        if medium is not None:
            params["medium"] = medium
        if source is not None:
            params["source"] = source
        if source_group is not None:
            params["sourceGroup"] = source_group
        if exclude_source_group is not None:
            params["excludeSourceGroup"] = exclude_source_group
        if exclude_source is not None:
            params["excludeSource"] = exclude_source
        if paywall is not None:
            params["paywall"] = paywall
        if byline is not None:
            params["byline"] = byline
        if author is not None:
            params["author"] = author
        if exclude_author is not None:
            params["excludeAuthor"] = exclude_author
        if journalist_id is not None:
            params["journalistId"] = journalist_id
        if exclude_journalist_id is not None:
            params["excludeJournalistId"] = exclude_journalist_id
        if language is not None:
            params["language"] = language
        if exclude_language is not None:
            params["excludeLanguage"] = exclude_language
        if search_translation is not None:
            params["searchTranslation"] = search_translation
        if label is not None:
            params["label"] = label
        if exclude_label is not None:
            params["excludeLabel"] = exclude_label
        if category is not None:
            params["category"] = category
        if exclude_category is not None:
            params["excludeCategory"] = exclude_category
        if topic is not None:
            params["topic"] = topic
        if exclude_topic is not None:
            params["excludeTopic"] = exclude_topic
        if link_to is not None:
            params["linkTo"] = link_to
        if show_reprints is not None:
            params["showReprints"] = show_reprints
        if reprint_group_id is not None:
            params["reprintGroupId"] = reprint_group_id
        if city is not None:
            params["city"] = city
        if exclude_city is not None:
            params["excludeCity"] = exclude_city
        if area is not None:
            params["area"] = area
        if state is not None:
            params["state"] = state
        if exclude_state is not None:
            params["excludeState"] = exclude_state
        if county is not None:
            params["county"] = county
        if exclude_county is not None:
            params["excludeCounty"] = exclude_county
        if locations_country is not None:
            params["locationsCountry"] = locations_country
        if country is not None:
            params["country"] = country
        if exclude_locations_country is not None:
            params["excludeLocationsCountry"] = exclude_locations_country
        if location is not None:
            params["location"] = location
        if lat is not None:
            params["lat"] = lat
        if lon is not None:
            params["lon"] = lon
        if max_distance is not None:
            params["maxDistance"] = max_distance
        if source_city is not None:
            params["sourceCity"] = source_city
        if source_county is not None:
            params["sourceCounty"] = source_county
        if source_country is not None:
            params["sourceCountry"] = source_country
        if source_state is not None:
            params["sourceState"] = source_state
        if source_lat is not None:
            params["sourceLat"] = source_lat
        if source_lon is not None:
            params["sourceLon"] = source_lon
        if source_max_distance is not None:
            params["sourceMaxDistance"] = source_max_distance
        if person_wikidata_id is not None:
            params["personWikidataId"] = person_wikidata_id
        if exclude_person_wikidata_id is not None:
            params["excludePersonWikidataId"] = exclude_person_wikidata_id
        if person_name is not None:
            params["personName"] = person_name
        if exclude_person_name is not None:
            params["excludePersonName"] = exclude_person_name
        if company_id is not None:
            params["companyId"] = company_id
        if exclude_company_id is not None:
            params["excludeCompanyId"] = exclude_company_id
        if company_name is not None:
            params["companyName"] = company_name
        if company_domain is not None:
            params["companyDomain"] = company_domain
        if exclude_company_domain is not None:
            params["excludeCompanyDomain"] = exclude_company_domain
        if company_symbol is not None:
            params["companySymbol"] = company_symbol
        if exclude_company_symbol is not None:
            params["excludeCompanySymbol"] = exclude_company_symbol
        if show_num_results is not None:
            params["showNumResults"] = show_num_results
        if positive_sentiment_from is not None:
            params["positiveSentimentFrom"] = positive_sentiment_from
        if positive_sentiment_to is not None:
            params["positiveSentimentTo"] = positive_sentiment_to
        if neutral_sentiment_from is not None:
            params["neutralSentimentFrom"] = neutral_sentiment_from
        if neutral_sentiment_to is not None:
            params["neutralSentimentTo"] = neutral_sentiment_to
        if negative_sentiment_from is not None:
            params["negativeSentimentFrom"] = negative_sentiment_from
        if negative_sentiment_to is not None:
            params["negativeSentimentTo"] = negative_sentiment_to
        if taxonomy is not None:
            params["taxonomy"] = taxonomy
        if prefix_taxonomy is not None:
            params["prefixTaxonomy"] = prefix_taxonomy
        if show_highlighting is not None:
            params["showHighlighting"] = show_highlighting
        if highlight_fragment_size is not None:
            params["highlightFragmentSize"] = highlight_fragment_size
        if highlight_num_fragments is not None:
            params["highlightNumFragments"] = highlight_num_fragments
        if highlight_pre_tag is not None:
            params["highlightPreTag"] = highlight_pre_tag
        if highlight_post_tag is not None:
            params["highlightPostTag"] = highlight_post_tag
        if highlight_q is not None:
            params["highlightQ"] = highlight_q
        params = _normalise_query(params)

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()
        return QuerySearchResult.model_validate(resp.json())

    # ----------------- search_articles (async) ----------------- #
    async def search_articles_async(
        self,
        q: Optional[str] = None,
        title: Optional[str] = None,
        desc: Optional[str] = None,
        content: Optional[str] = None,
        url: Optional[str] = None,
        article_id: Optional[List[str]] = None,
        cluster_id: Optional[List[str]] = None,
        sort_by: Optional[AllEndpointSortBy] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        var_from: Optional[datetime] = None,
        to: Optional[datetime] = None,
        add_date_from: Optional[datetime] = None,
        add_date_to: Optional[datetime] = None,
        refresh_date_from: Optional[datetime] = None,
        refresh_date_to: Optional[datetime] = None,
        medium: Optional[List[str]] = None,
        source: Optional[List[str]] = None,
        source_group: Optional[List[str]] = None,
        exclude_source_group: Optional[List[str]] = None,
        exclude_source: Optional[List[str]] = None,
        paywall: Optional[bool] = None,
        byline: Optional[List[str]] = None,
        author: Optional[List[str]] = None,
        exclude_author: Optional[List[str]] = None,
        journalist_id: Optional[List[str]] = None,
        exclude_journalist_id: Optional[List[str]] = None,
        language: Optional[List[str]] = None,
        exclude_language: Optional[List[str]] = None,
        search_translation: Optional[bool] = None,
        label: Optional[List[str]] = None,
        exclude_label: Optional[List[str]] = None,
        category: Optional[List[str]] = None,
        exclude_category: Optional[List[str]] = None,
        topic: Optional[List[str]] = None,
        exclude_topic: Optional[List[str]] = None,
        link_to: Optional[str] = None,
        show_reprints: Optional[bool] = None,
        reprint_group_id: Optional[str] = None,
        city: Optional[List[str]] = None,
        exclude_city: Optional[List[str]] = None,
        area: Optional[List[str]] = None,
        state: Optional[List[str]] = None,
        exclude_state: Optional[List[str]] = None,
        county: Optional[List[str]] = None,
        exclude_county: Optional[List[str]] = None,
        locations_country: Optional[List[str]] = None,
        country: Optional[List[str]] = None,
        exclude_locations_country: Optional[List[str]] = None,
        location: Optional[List[str]] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        max_distance: Optional[float] = None,
        source_city: Optional[List[str]] = None,
        source_county: Optional[List[str]] = None,
        source_country: Optional[List[str]] = None,
        source_state: Optional[List[str]] = None,
        source_lat: Optional[float] = None,
        source_lon: Optional[float] = None,
        source_max_distance: Optional[float] = None,
        person_wikidata_id: Optional[List[str]] = None,
        exclude_person_wikidata_id: Optional[List[str]] = None,
        person_name: Optional[List[str]] = None,
        exclude_person_name: Optional[List[str]] = None,
        company_id: Optional[List[str]] = None,
        exclude_company_id: Optional[List[str]] = None,
        company_name: Optional[str] = None,
        company_domain: Optional[List[str]] = None,
        exclude_company_domain: Optional[List[str]] = None,
        company_symbol: Optional[List[str]] = None,
        exclude_company_symbol: Optional[List[str]] = None,
        show_num_results: Optional[bool] = None,
        positive_sentiment_from: Optional[float] = None,
        positive_sentiment_to: Optional[float] = None,
        neutral_sentiment_from: Optional[float] = None,
        neutral_sentiment_to: Optional[float] = None,
        negative_sentiment_from: Optional[float] = None,
        negative_sentiment_to: Optional[float] = None,
        taxonomy: Optional[List[str]] = None,
        prefix_taxonomy: Optional[str] = None,
        show_highlighting: Optional[bool] = None,
        highlight_fragment_size: Optional[int] = None,
        highlight_num_fragments: Optional[int] = None,
        highlight_pre_tag: Optional[str] = None,
        highlight_post_tag: Optional[str] = None,
        highlight_q: Optional[str] = None,
    ) -> QuerySearchResult:
        """
        Async variant of search_articles. Search and filter all news articles available via the Perigon API. The result includes a list of individual articles that were matched to your specific criteria.

        Args:
            q (Optional[str]): Primary search query for filtering articles based on their title, description, and content. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            title (Optional[str]): Search specifically within article headlines/titles. Supports Boolean operators, exact phrases with quotes, and wildcards for matching title variations.
            desc (Optional[str]): Search within article description fields. Supports Boolean expressions, exact phrase matching with quotes, and wildcards for flexible pattern matching.
            content (Optional[str]): Search within the full article body content. Supports Boolean logic, exact phrase matching with quotes, and wildcards for comprehensive content searching.
            url (Optional[str]): Search within article URLs to find content from specific website sections or domains. Supports wildcards (* and ?) for partial URL matching.
            article_id (Optional[List[str]]): Retrieve specific news articles by their unique article identifiers. Multiple IDs can be provided to return a collection of specific articles.
            cluster_id (Optional[List[str]]): Filter results to only show content within a specific related content cluster. Returns articles grouped together as part of Perigon Stories based on topic relevance.
            sort_by (Optional[AllEndpointSortBy]): Determines the article sorting order. Options include relevance (default), date/pubDate (newest publication date first), reverseDate (oldest publication date first), addDate (newest ingestion date first), reverseAddDate (oldest ingestion date first), and refreshDate (most recently updated in system first, often identical to addDate).
            page (Optional[int]): The specific page of results to retrieve in the paginated response. Starts at 0.
            size (Optional[int]): The number of articles to return per page in the paginated response.
            var_from (Optional[datetime]): Filter for articles published after this date. Accepts ISO 8601 format (e.g., 2023-03-01T00:00:00) or yyyy-mm-dd format.
            to (Optional[datetime]): Filter for articles published before this date. Accepts ISO 8601 format (e.g., 2022-02-01T23:59:59) or yyyy-mm-dd format.
            add_date_from (Optional[datetime]): Filter for articles added to Perigon's system after this date. Accepts ISO 8601 format (e.g., 2022-02-01T00:00:00) or yyyy-mm-dd format.
            add_date_to (Optional[datetime]): Filter for articles added to Perigon's system before this date. Accepts ISO 8601 format (e.g., 2022-02-01T23:59:59) or yyyy-mm-dd format.
            refresh_date_from (Optional[datetime]): Filter for articles refreshed/updated in Perigon's system after this date. In most cases yields similar results to addDateFrom but can differ for updated content. Accepts ISO 8601 format (e.g., 2022-02-01T00:00:00) or yyyy-mm-dd format.
            refresh_date_to (Optional[datetime]): Filter for articles refreshed/updated in Perigon's system before this date. In most cases yields similar results to addDateTo but can differ for updated content. Accepts ISO 8601 format (e.g., 2022-02-01T23:59:59) or yyyy-mm-dd format.
            medium (Optional[List[str]]): Filter articles by their primary medium type. Accepts Article for written content or Video for video-based stories. Multiple values create an OR filter.
            source (Optional[List[str]]): Filter articles by specific publisher domains or subdomains. Supports wildcards (* and ?) for pattern matching (e.g., *.cnn.com). Multiple values create an OR filter.
            source_group (Optional[List[str]]): Filter articles using Perigon's curated publisher bundles (e.g., top100, top25crypto). Multiple values create an OR filter to include articles from any of the specified bundles.
            exclude_source_group (Optional[List[str]]): Exclude articles from specified Perigon source groups. Multiple values create an AND-exclude filter, removing content from publishers in any of the specified bundles (e.g., top10, top100).
            exclude_source (Optional[List[str]]): Exclude articles from specific publisher domains or subdomains. Supports wildcards (* and ?) for pattern matching (e.g., *.cnn.com). Multiple values create an AND-exclude filter.
            paywall (Optional[bool]): Filter to show only results where the source has a paywall (true) or does not have a paywall (false).
            byline (Optional[List[str]]): Filter articles by author bylines. Works as an exact match for each author name provided. Multiple values create an OR filter to find articles by any of the specified authors.
            author (Optional[List[str]]): Filter articles by specific author names. Works as an exact match for each name. Multiple values create an OR filter to find articles by any of the specified authors.
            exclude_author (Optional[List[str]]): Exclude articles written by specific authors. Any article with an author name matching an entry in this list will be omitted from results. Multiple values create an AND-exclude filter.
            journalist_id (Optional[List[str]]): Filter by unique journalist identifiers which can be found through the Journalist API or in the matchedAuthors field. Multiple values create an OR filter.
            exclude_journalist_id (Optional[List[str]]): Exclude articles written by specific journalists identified by their unique IDs. Multiple values create an AND-exclude filter.
            language (Optional[List[str]]): Filter articles by their language using ISO-639 two-letter codes (e.g., en, es, fr). Multiple values create an OR filter.
            exclude_language (Optional[List[str]]): Exclude articles in specific languages using ISO-639 two-letter codes. Multiple values create an AND-exclude filter.
            search_translation (Optional[bool]): Expand search to include translated content fields for non-English articles. When true, searches translated title, description, and content fields.
            label (Optional[List[str]]): Filter articles by editorial labels such as Opinion, Paid-news, Non-news, Fact Check, or Press Release. Multiple values create an OR filter.
            exclude_label (Optional[List[str]]): Exclude articles with specific editorial labels. Multiple values create an AND-exclude filter, removing all content with any of these labels.
            category (Optional[List[str]]): Filter by broad content categories such as Politics, Tech, Sports, Business, or Finance. Use 'none' to find uncategorized articles. Multiple values create an OR filter.
            exclude_category (Optional[List[str]]): Exclude articles with specific categories. Multiple values create an AND-exclude filter, removing all content with any of these categories.
            topic (Optional[List[str]]): Filter by specific topics such as Markets, Crime, Cryptocurrency, or College Sports. Topics are more granular than categories, and articles can have multiple topics. Use the /topics endpoint for a complete list of available topics. Multiple values create an OR filter.
            exclude_topic (Optional[List[str]]): Exclude articles with specific topics. Multiple values create an AND-exclude filter, removing all content with any of these topics.
            link_to (Optional[str]): Returns only articles that contain links to the specified URL pattern. Matches against the 'links' field in article responses.
            show_reprints (Optional[bool]): Controls whether to include reprinted content in results. When true (default), shows syndicated articles from wire services like AP or Reuters that appear on multiple sites.
            reprint_group_id (Optional[str]): Returns all articles in a specific reprint group, including the original article and all its known reprints. Use when you want to see all versions of the same content.
            city (Optional[List[str]]): Filters articles where a specified city plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the urban area in question. If multiple parameters are passed, they will be applied as OR operations.
            exclude_city (Optional[List[str]]): A list of cities to exclude from the results. Articles that are associated with any of the specified cities will be filtered out.
            area (Optional[List[str]]): Filters articles where a specified area, such as a neighborhood, borough, or district, plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the area in question. If multiple parameters are passed, they will be applied as OR operations.
            state (Optional[List[str]]): Filters articles where a specified state plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the state in question. If multiple parameters are passed, they will be applied as OR operations.
            exclude_state (Optional[List[str]]): A list of states to exclude. Articles that include, or are associated with, any of the states provided here will be filtered out. This is especially useful if you want to ignore news tied to certain geographical areas (e.g., US states).
            county (Optional[List[str]]): A list of counties to include (or specify) in the search results. This field filters the returned articles based on the county associated with the event or news. Only articles tagged with one of these counties will be included.
            exclude_county (Optional[List[str]]): Excludes articles from specific counties or administrative divisions in the search results. Accepts either a single county name or a list of county names. County names should match the format used in article metadata (e.g., 'Los Angeles County', 'Cook County'). This parameter allows for more granular geographic filter
            locations_country (Optional[List[str]]): Filters articles where a specified country plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the country in question. If multiple parameters are passed, they will be applied as OR operations.
            country (Optional[List[str]]): Country code to filter by country. If multiple parameters are passed, they will be applied as OR operations.
            exclude_locations_country (Optional[List[str]]): Excludes articles where a specified country plays a central role in the content, ensuring results are not deeply relevant to the country in question. If multiple parameters are passed, they will be applied as AND operations, excluding articles relevant to any of the specified countries.
            location (Optional[List[str]]): Return all articles that have the specified location. Location attributes are delimited by ':' between key and value, and '::' between attributes. Example: 'city:New York::state:NY'.
            lat (Optional[float]): Latitude of the center point to search places
            lon (Optional[float]): Longitude of the center point to search places
            max_distance (Optional[float]): Maximum distance (in km) from starting point to search articles by tagged places
            source_city (Optional[List[str]]): Find articles published by sources that are located within a given city.
            source_county (Optional[List[str]]): Find articles published by sources that are located within a given county.
            source_country (Optional[List[str]]): Find articles published by sources that are located within a given country. Must be 2 character country code (i.e. us, gb, etc).
            source_state (Optional[List[str]]): Find articles published by sources that are located within a given state.
            source_lat (Optional[float]): Latitude of the center point to search articles created by local publications.
            source_lon (Optional[float]): Latitude of the center point to search articles created by local publications.
            source_max_distance (Optional[float]): Maximum distance from starting point to search articles created by local publications.
            person_wikidata_id (Optional[List[str]]): Filter articles by Wikidata IDs of mentioned people. Refer to the /people endpoint for a complete list of tracked individuals.
            exclude_person_wikidata_id (Optional[List[str]]): Exclude articles mentioning people with specific Wikidata IDs. Creates an AND-exclude filter to remove content about these individuals. Uses precise identifiers to avoid name ambiguity.
            person_name (Optional[List[str]]): Filter articles by exact person name matches. Does not support Boolean or complex logic. For available person entities, consult the /people endpoint.
            exclude_person_name (Optional[List[str]]): Exclude articles mentioning specific people by name. Creates an AND-exclude filter to remove content about these individuals.
            company_id (Optional[List[str]]): Filter articles by company identifiers. For a complete list of tracked companies, refer to the /companies endpoint.
            exclude_company_id (Optional[List[str]]): Exclude articles mentioning companies with specific identifiers. Creates an AND-exclude filter to remove content about these corporate entities.
            company_name (Optional[str]): Filter articles by company name mentions. Performs an exact match on company names.
            company_domain (Optional[List[str]]): Filter articles by company domains (e.g., apple.com). For available company entities, consult the /companies endpoint.
            exclude_company_domain (Optional[List[str]]): Exclude articles related to companies with specific domains. Creates an AND-exclude filter to remove content about these companies.
            company_symbol (Optional[List[str]]): Filter articles by company stock symbols. For available company entities and their symbols, consult the /companies endpoint.
            exclude_company_symbol (Optional[List[str]]): A list of stock symbols (ticker symbols) that identify companies to be excluded. Articles related to companies using any of these symbols will be omitted, which is useful for targeting or avoiding specific public companies.
            show_num_results (Optional[bool]): Whether to show the total number of all matched articles. Default value is false which makes queries a bit more efficient but also counts up to 10000 articles.
            positive_sentiment_from (Optional[float]): Filter articles with a positive sentiment score greater than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger positive tone.
            positive_sentiment_to (Optional[float]): Filter articles with a positive sentiment score less than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger positive tone.
            neutral_sentiment_from (Optional[float]): Filter articles with a neutral sentiment score greater than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger neutral tone.
            neutral_sentiment_to (Optional[float]): Filter articles with a neutral sentiment score less than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger neutral tone.
            negative_sentiment_from (Optional[float]): Filter articles with a negative sentiment score greater than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger negative tone.
            negative_sentiment_to (Optional[float]): Filter articles with a negative sentiment score less than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger negative tone.
            taxonomy (Optional[List[str]]): Filters by Google Content Categories. This field will accept 1 or more categories, must pass the full name of the category. Example: taxonomy=/Finance/Banking/Other, /Finance/Investing/Funds. [Full list](https://cloud.google.com/natural-language/docs/categories)
            prefix_taxonomy (Optional[str]): Filters by Google Content Categories. This field will filter by the category prefix only. Example: prefixTaxonomy=/Finance
            show_highlighting (Optional[bool]): When set to true, enables text highlighting in search results.
            highlight_fragment_size (Optional[int]): Specifies the size in characters of each highlighted text fragment. Defaults to 100 if not specified.
            highlight_num_fragments (Optional[int]): Controls the maximum number of highlighted fragments to return per field.
            highlight_pre_tag (Optional[str]): Defines the HTML tag that appears before highlighted text. Defaults to '<em>' if not specified.
            highlight_post_tag (Optional[str]): Defines the HTML tag that appears after highlighted text. Defaults to '</em>' if not specified.
            highlight_q (Optional[str]): Specifies a separate query for highlighting, allowing highlights based on terms different from the main search query. Example: main query 'q=climate change' with 'highlightQ=renewable OR solar' will highlight terms 'renewable' and 'solar' in results about climate change.

        Returns:
            QuerySearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_ARTICLES

        params: Dict[str, Any] = {}
        if q is not None:
            params["q"] = q
        if title is not None:
            params["title"] = title
        if desc is not None:
            params["desc"] = desc
        if content is not None:
            params["content"] = content
        if url is not None:
            params["url"] = url
        if article_id is not None:
            params["articleId"] = article_id
        if cluster_id is not None:
            params["clusterId"] = cluster_id
        if sort_by is not None:
            params["sortBy"] = sort_by
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if var_from is not None:
            params["from"] = var_from
        if to is not None:
            params["to"] = to
        if add_date_from is not None:
            params["addDateFrom"] = add_date_from
        if add_date_to is not None:
            params["addDateTo"] = add_date_to
        if refresh_date_from is not None:
            params["refreshDateFrom"] = refresh_date_from
        if refresh_date_to is not None:
            params["refreshDateTo"] = refresh_date_to
        if medium is not None:
            params["medium"] = medium
        if source is not None:
            params["source"] = source
        if source_group is not None:
            params["sourceGroup"] = source_group
        if exclude_source_group is not None:
            params["excludeSourceGroup"] = exclude_source_group
        if exclude_source is not None:
            params["excludeSource"] = exclude_source
        if paywall is not None:
            params["paywall"] = paywall
        if byline is not None:
            params["byline"] = byline
        if author is not None:
            params["author"] = author
        if exclude_author is not None:
            params["excludeAuthor"] = exclude_author
        if journalist_id is not None:
            params["journalistId"] = journalist_id
        if exclude_journalist_id is not None:
            params["excludeJournalistId"] = exclude_journalist_id
        if language is not None:
            params["language"] = language
        if exclude_language is not None:
            params["excludeLanguage"] = exclude_language
        if search_translation is not None:
            params["searchTranslation"] = search_translation
        if label is not None:
            params["label"] = label
        if exclude_label is not None:
            params["excludeLabel"] = exclude_label
        if category is not None:
            params["category"] = category
        if exclude_category is not None:
            params["excludeCategory"] = exclude_category
        if topic is not None:
            params["topic"] = topic
        if exclude_topic is not None:
            params["excludeTopic"] = exclude_topic
        if link_to is not None:
            params["linkTo"] = link_to
        if show_reprints is not None:
            params["showReprints"] = show_reprints
        if reprint_group_id is not None:
            params["reprintGroupId"] = reprint_group_id
        if city is not None:
            params["city"] = city
        if exclude_city is not None:
            params["excludeCity"] = exclude_city
        if area is not None:
            params["area"] = area
        if state is not None:
            params["state"] = state
        if exclude_state is not None:
            params["excludeState"] = exclude_state
        if county is not None:
            params["county"] = county
        if exclude_county is not None:
            params["excludeCounty"] = exclude_county
        if locations_country is not None:
            params["locationsCountry"] = locations_country
        if country is not None:
            params["country"] = country
        if exclude_locations_country is not None:
            params["excludeLocationsCountry"] = exclude_locations_country
        if location is not None:
            params["location"] = location
        if lat is not None:
            params["lat"] = lat
        if lon is not None:
            params["lon"] = lon
        if max_distance is not None:
            params["maxDistance"] = max_distance
        if source_city is not None:
            params["sourceCity"] = source_city
        if source_county is not None:
            params["sourceCounty"] = source_county
        if source_country is not None:
            params["sourceCountry"] = source_country
        if source_state is not None:
            params["sourceState"] = source_state
        if source_lat is not None:
            params["sourceLat"] = source_lat
        if source_lon is not None:
            params["sourceLon"] = source_lon
        if source_max_distance is not None:
            params["sourceMaxDistance"] = source_max_distance
        if person_wikidata_id is not None:
            params["personWikidataId"] = person_wikidata_id
        if exclude_person_wikidata_id is not None:
            params["excludePersonWikidataId"] = exclude_person_wikidata_id
        if person_name is not None:
            params["personName"] = person_name
        if exclude_person_name is not None:
            params["excludePersonName"] = exclude_person_name
        if company_id is not None:
            params["companyId"] = company_id
        if exclude_company_id is not None:
            params["excludeCompanyId"] = exclude_company_id
        if company_name is not None:
            params["companyName"] = company_name
        if company_domain is not None:
            params["companyDomain"] = company_domain
        if exclude_company_domain is not None:
            params["excludeCompanyDomain"] = exclude_company_domain
        if company_symbol is not None:
            params["companySymbol"] = company_symbol
        if exclude_company_symbol is not None:
            params["excludeCompanySymbol"] = exclude_company_symbol
        if show_num_results is not None:
            params["showNumResults"] = show_num_results
        if positive_sentiment_from is not None:
            params["positiveSentimentFrom"] = positive_sentiment_from
        if positive_sentiment_to is not None:
            params["positiveSentimentTo"] = positive_sentiment_to
        if neutral_sentiment_from is not None:
            params["neutralSentimentFrom"] = neutral_sentiment_from
        if neutral_sentiment_to is not None:
            params["neutralSentimentTo"] = neutral_sentiment_to
        if negative_sentiment_from is not None:
            params["negativeSentimentFrom"] = negative_sentiment_from
        if negative_sentiment_to is not None:
            params["negativeSentimentTo"] = negative_sentiment_to
        if taxonomy is not None:
            params["taxonomy"] = taxonomy
        if prefix_taxonomy is not None:
            params["prefixTaxonomy"] = prefix_taxonomy
        if show_highlighting is not None:
            params["showHighlighting"] = show_highlighting
        if highlight_fragment_size is not None:
            params["highlightFragmentSize"] = highlight_fragment_size
        if highlight_num_fragments is not None:
            params["highlightNumFragments"] = highlight_num_fragments
        if highlight_pre_tag is not None:
            params["highlightPreTag"] = highlight_pre_tag
        if highlight_post_tag is not None:
            params["highlightPostTag"] = highlight_post_tag
        if highlight_q is not None:
            params["highlightQ"] = highlight_q
        params = _normalise_query(params)

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()
        return QuerySearchResult.model_validate(resp.json())

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

    # ----------------- search_stories (sync) ----------------- #
    def search_stories(
        self,
        q: Optional[str] = None,
        name: Optional[str] = None,
        cluster_id: Optional[List[str]] = None,
        exclude_cluster_id: Optional[List[str]] = None,
        sort_by: Optional[SortBy] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        var_from: Optional[datetime] = None,
        to: Optional[datetime] = None,
        initialized_from: Optional[datetime] = None,
        initialized_to: Optional[datetime] = None,
        updated_from: Optional[datetime] = None,
        updated_to: Optional[datetime] = None,
        topic: Optional[List[str]] = None,
        category: Optional[List[str]] = None,
        taxonomy: Optional[List[str]] = None,
        source: Optional[List[str]] = None,
        source_group: Optional[List[str]] = None,
        min_unique_sources: Optional[int] = None,
        person_wikidata_id: Optional[List[str]] = None,
        person_name: Optional[str] = None,
        company_id: Optional[List[str]] = None,
        company_name: Optional[str] = None,
        company_domain: Optional[List[str]] = None,
        company_symbol: Optional[List[str]] = None,
        country: Optional[List[str]] = None,
        state: Optional[List[str]] = None,
        city: Optional[List[str]] = None,
        area: Optional[List[str]] = None,
        min_cluster_size: Optional[int] = None,
        max_cluster_size: Optional[int] = None,
        name_exists: Optional[bool] = None,
        positive_sentiment_from: Optional[float] = None,
        positive_sentiment_to: Optional[float] = None,
        neutral_sentiment_from: Optional[float] = None,
        neutral_sentiment_to: Optional[float] = None,
        negative_sentiment_from: Optional[float] = None,
        negative_sentiment_to: Optional[float] = None,
        show_story_page_info: Optional[bool] = None,
        show_num_results: Optional[bool] = None,
        show_duplicates: Optional[bool] = None,
        show_highlighting: Optional[bool] = None,
        highlight_fragment_size: Optional[int] = None,
        highlight_num_fragments: Optional[int] = None,
        highlight_pre_tag: Optional[str] = None,
        highlight_post_tag: Optional[str] = None,
        highlight_q: Optional[str] = None,
    ) -> StorySearchResult:
        """
        Search and filter all news stories available via the Perigon API. Each story aggregates key information across related articles, including AI-generated names, summaries, and key points.

        Args:
            q (Optional[str]): Primary search query for filtering stories based on their name, summary, and key points. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            name (Optional[str]): Search specifically within story names. Supports Boolean operators, exact phrases with quotes, and wildcards for matching name variations.
            cluster_id (Optional[List[str]]): Filter to specific stories using their unique identifiers. Each clusterId represents a distinct story that groups related articles. Multiple values create an OR filter.
            exclude_cluster_id (Optional[List[str]]): Excludes specific stories from the results by their unique identifiers. Use this parameter to filter out unwanted or previously seen stories.
            sort_by (Optional[SortBy]): Determines the story sorting order. Options include createdAt (default, when stories first emerged), updatedAt (when stories received new articles, best for tracking developing events), relevance (best match to query), count (by unique article count), and totalCount (by total article count including reprints).
            page (Optional[int]): The specific page of results to retrieve in the paginated response. Starts at 0.
            size (Optional[int]): The number of articles to return per page in the paginated response.
            var_from (Optional[datetime]): 'from' filter, will search stories created after the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2023-03-01T00:00:00
            to (Optional[datetime]): 'to' filter, will search stories created before the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2023-03-01T23:59:59
            initialized_from (Optional[datetime]): Filter for stories created after this date. Alternative parameter for filtering by story creation date.
            initialized_to (Optional[datetime]): Filter for stories created before this date. Alternative parameter for filtering by story creation date.
            updated_from (Optional[datetime]): Filter for stories that received new articles after this date. Useful for tracking developing news events or evolving storylines.
            updated_to (Optional[datetime]): Filter for stories that received new articles before this date. Useful for tracking developing news events or evolving storylines.
            topic (Optional[List[str]]): Filter stories by specific topics such as Markets, Crime, Cryptocurrency, or College Sports. Topics are more granular than categories, and stories can include multiple topics based on their constituent articles. Use the /topics endpoint for a complete list of available topics. Multiple values create an OR filter.
            category (Optional[List[str]]): Filter stories by broad content categories such as Politics, Tech, Sports, Business, or Finance. Use 'none' to find uncategorized stories. Categories are derived from the articles within each story. Multiple values create an OR filter.
            taxonomy (Optional[List[str]]): Filter stories by Google Content Categories. Must pass the full hierarchical path of the category. Example: taxonomy=/Finance/Banking/Other,/Finance/Investing/Funds. Stories are categorized based on their constituent articles. Multiple values create an OR filter.
            source (Optional[List[str]]): Filter stories that contain articles from specific publisher domains or subdomains. Supports wildcards (* and ?) for pattern matching (e.g., *.cnn.com). A story will match if it contains at least one article from any of the specified sources. Multiple values create an OR filter.
            source_group (Optional[List[str]]): Filter stories that contain articles from publishers in Perigon's curated bundles (e.g., top100, top25crypto). A story will match if it contains at least one article from any publisher in the specified bundles. Multiple values create an OR filter.
            min_unique_sources (Optional[int]): Specifies the minimum number of unique sources required for a story to appear in results. Higher values return more significant stories covered by multiple publications. Default is 3.
            person_wikidata_id (Optional[List[str]]): Filter stories by Wikidata IDs of top mentioned people. Returns stories where these individuals appear prominently. Refer to the /people endpoint for a complete list of tracked individuals.
            person_name (Optional[str]): Filter stories by exact name matches of top mentioned people. Does not support Boolean or complex logic. For available person entities, consult the /people endpoint.
            company_id (Optional[List[str]]): Filter stories by identifiers of top mentioned companies. Returns stories where these companies appear prominently. For a complete list of tracked companies, refer to the /companies endpoint.
            company_name (Optional[str]): Filter stories by names of top mentioned companies. Performs an exact match on company names in the topCompanies field.
            company_domain (Optional[List[str]]): Filter stories by domains of top mentioned companies (e.g., apple.com). Returns stories where companies with these domains appear prominently. For available company entities, consult the /companies endpoint.
            company_symbol (Optional[List[str]]): Filter stories by stock symbols of top mentioned companies. Returns stories where companies with these symbols appear prominently. For available company entities and their symbols, consult the /companies endpoint.
            country (Optional[List[str]]): Country code to filter by country. If multiple parameters are passed, they will be applied as OR operations.
            state (Optional[List[str]]): Filter local news by state. Applies only to local news, when this param is passed non-local news will not be returned. If multiple parameters are passed, they will be applied as OR operations.
            city (Optional[List[str]]): Filter local news by city. Applies only to local news, when this param is passed non-local news will not be returned. If multiple parameters are passed, they will be applied as OR operations.
            area (Optional[List[str]]): Filter local news by area. Applies only to local news, when this param is passed non-local news will not be returned. If multiple parameters are passed, they will be applied as OR operations.
            min_cluster_size (Optional[int]): Filter by minimum cluster size. Minimum cluster size filter applies to number of unique articles.
            max_cluster_size (Optional[int]): Filter by maximum cluster size. Maximum cluster size filter applies to number of unique articles in the cluster.
            name_exists (Optional[bool]): Filter to only include stories that have been assigned names. Defaults to true. Note that stories only receive names after they contain at least 5 unique articles.
            positive_sentiment_from (Optional[float]): Filter articles with an aggregate positive sentiment score greater than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger positive tone.
            positive_sentiment_to (Optional[float]): Filter articles with an aggregate positive sentiment score less than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger positive tone.
            neutral_sentiment_from (Optional[float]): Filter articles with an aggregate neutral sentiment score greater than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger neutral tone.
            neutral_sentiment_to (Optional[float]): Filter articles with an aggregate neutral sentiment score less than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger neutral tone.
            negative_sentiment_from (Optional[float]): Filter stories with an aggregate negative sentiment score greater than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger negative tone.
            negative_sentiment_to (Optional[float]): Filter articles with an aggregate negative sentiment score less than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger negative tone.
            show_story_page_info (Optional[bool]): Parameter show_story_page_info
            show_num_results (Optional[bool]): Show total number of results. By default set to false, will cap result count at 10000.
            show_duplicates (Optional[bool]): Stories are deduplicated by default. If a story is deduplicated, all future articles are merged into the original story. duplicateOf field contains the original cluster Id. When showDuplicates=true, all stories are shown.
            show_highlighting (Optional[bool]): When set to true, enables text highlighting in search results.
            highlight_fragment_size (Optional[int]): Specifies the size in characters of each highlighted text fragment. Defaults to 100 if not specified.
            highlight_num_fragments (Optional[int]): Controls the maximum number of highlighted fragments to return per field.
            highlight_pre_tag (Optional[str]): Defines the HTML tag that appears before highlighted text. Defaults to '<em>' if not specified.
            highlight_post_tag (Optional[str]): Defines the HTML tag that appears after highlighted text. Defaults to '</em>' if not specified.
            highlight_q (Optional[str]): Specifies a separate query for highlighting, allowing highlights based on terms different from the main search query. Example: main query 'q=climate change' with 'highlightQ=renewable OR solar' will highlight terms 'renewable' and 'solar' in results about climate change.

        Returns:
            StorySearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_STORIES

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if q is not None:
            params["q"] = q
        if name is not None:
            params["name"] = name
        if cluster_id is not None:
            params["clusterId"] = cluster_id
        if exclude_cluster_id is not None:
            params["excludeClusterId"] = exclude_cluster_id
        if sort_by is not None:
            params["sortBy"] = sort_by
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if var_from is not None:
            params["from"] = var_from
        if to is not None:
            params["to"] = to
        if initialized_from is not None:
            params["initializedFrom"] = initialized_from
        if initialized_to is not None:
            params["initializedTo"] = initialized_to
        if updated_from is not None:
            params["updatedFrom"] = updated_from
        if updated_to is not None:
            params["updatedTo"] = updated_to
        if topic is not None:
            params["topic"] = topic
        if category is not None:
            params["category"] = category
        if taxonomy is not None:
            params["taxonomy"] = taxonomy
        if source is not None:
            params["source"] = source
        if source_group is not None:
            params["sourceGroup"] = source_group
        if min_unique_sources is not None:
            params["minUniqueSources"] = min_unique_sources
        if person_wikidata_id is not None:
            params["personWikidataId"] = person_wikidata_id
        if person_name is not None:
            params["personName"] = person_name
        if company_id is not None:
            params["companyId"] = company_id
        if company_name is not None:
            params["companyName"] = company_name
        if company_domain is not None:
            params["companyDomain"] = company_domain
        if company_symbol is not None:
            params["companySymbol"] = company_symbol
        if country is not None:
            params["country"] = country
        if state is not None:
            params["state"] = state
        if city is not None:
            params["city"] = city
        if area is not None:
            params["area"] = area
        if min_cluster_size is not None:
            params["minClusterSize"] = min_cluster_size
        if max_cluster_size is not None:
            params["maxClusterSize"] = max_cluster_size
        if name_exists is not None:
            params["nameExists"] = name_exists
        if positive_sentiment_from is not None:
            params["positiveSentimentFrom"] = positive_sentiment_from
        if positive_sentiment_to is not None:
            params["positiveSentimentTo"] = positive_sentiment_to
        if neutral_sentiment_from is not None:
            params["neutralSentimentFrom"] = neutral_sentiment_from
        if neutral_sentiment_to is not None:
            params["neutralSentimentTo"] = neutral_sentiment_to
        if negative_sentiment_from is not None:
            params["negativeSentimentFrom"] = negative_sentiment_from
        if negative_sentiment_to is not None:
            params["negativeSentimentTo"] = negative_sentiment_to
        if show_story_page_info is not None:
            params["showStoryPageInfo"] = show_story_page_info
        if show_num_results is not None:
            params["showNumResults"] = show_num_results
        if show_duplicates is not None:
            params["showDuplicates"] = show_duplicates
        if show_highlighting is not None:
            params["showHighlighting"] = show_highlighting
        if highlight_fragment_size is not None:
            params["highlightFragmentSize"] = highlight_fragment_size
        if highlight_num_fragments is not None:
            params["highlightNumFragments"] = highlight_num_fragments
        if highlight_pre_tag is not None:
            params["highlightPreTag"] = highlight_pre_tag
        if highlight_post_tag is not None:
            params["highlightPostTag"] = highlight_post_tag
        if highlight_q is not None:
            params["highlightQ"] = highlight_q
        params = _normalise_query(params)

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()
        return StorySearchResult.model_validate(resp.json())

    # ----------------- search_stories (async) ----------------- #
    async def search_stories_async(
        self,
        q: Optional[str] = None,
        name: Optional[str] = None,
        cluster_id: Optional[List[str]] = None,
        exclude_cluster_id: Optional[List[str]] = None,
        sort_by: Optional[SortBy] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        var_from: Optional[datetime] = None,
        to: Optional[datetime] = None,
        initialized_from: Optional[datetime] = None,
        initialized_to: Optional[datetime] = None,
        updated_from: Optional[datetime] = None,
        updated_to: Optional[datetime] = None,
        topic: Optional[List[str]] = None,
        category: Optional[List[str]] = None,
        taxonomy: Optional[List[str]] = None,
        source: Optional[List[str]] = None,
        source_group: Optional[List[str]] = None,
        min_unique_sources: Optional[int] = None,
        person_wikidata_id: Optional[List[str]] = None,
        person_name: Optional[str] = None,
        company_id: Optional[List[str]] = None,
        company_name: Optional[str] = None,
        company_domain: Optional[List[str]] = None,
        company_symbol: Optional[List[str]] = None,
        country: Optional[List[str]] = None,
        state: Optional[List[str]] = None,
        city: Optional[List[str]] = None,
        area: Optional[List[str]] = None,
        min_cluster_size: Optional[int] = None,
        max_cluster_size: Optional[int] = None,
        name_exists: Optional[bool] = None,
        positive_sentiment_from: Optional[float] = None,
        positive_sentiment_to: Optional[float] = None,
        neutral_sentiment_from: Optional[float] = None,
        neutral_sentiment_to: Optional[float] = None,
        negative_sentiment_from: Optional[float] = None,
        negative_sentiment_to: Optional[float] = None,
        show_story_page_info: Optional[bool] = None,
        show_num_results: Optional[bool] = None,
        show_duplicates: Optional[bool] = None,
        show_highlighting: Optional[bool] = None,
        highlight_fragment_size: Optional[int] = None,
        highlight_num_fragments: Optional[int] = None,
        highlight_pre_tag: Optional[str] = None,
        highlight_post_tag: Optional[str] = None,
        highlight_q: Optional[str] = None,
    ) -> StorySearchResult:
        """
        Async variant of search_stories. Search and filter all news stories available via the Perigon API. Each story aggregates key information across related articles, including AI-generated names, summaries, and key points.

        Args:
            q (Optional[str]): Primary search query for filtering stories based on their name, summary, and key points. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            name (Optional[str]): Search specifically within story names. Supports Boolean operators, exact phrases with quotes, and wildcards for matching name variations.
            cluster_id (Optional[List[str]]): Filter to specific stories using their unique identifiers. Each clusterId represents a distinct story that groups related articles. Multiple values create an OR filter.
            exclude_cluster_id (Optional[List[str]]): Excludes specific stories from the results by their unique identifiers. Use this parameter to filter out unwanted or previously seen stories.
            sort_by (Optional[SortBy]): Determines the story sorting order. Options include createdAt (default, when stories first emerged), updatedAt (when stories received new articles, best for tracking developing events), relevance (best match to query), count (by unique article count), and totalCount (by total article count including reprints).
            page (Optional[int]): The specific page of results to retrieve in the paginated response. Starts at 0.
            size (Optional[int]): The number of articles to return per page in the paginated response.
            var_from (Optional[datetime]): 'from' filter, will search stories created after the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2023-03-01T00:00:00
            to (Optional[datetime]): 'to' filter, will search stories created before the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2023-03-01T23:59:59
            initialized_from (Optional[datetime]): Filter for stories created after this date. Alternative parameter for filtering by story creation date.
            initialized_to (Optional[datetime]): Filter for stories created before this date. Alternative parameter for filtering by story creation date.
            updated_from (Optional[datetime]): Filter for stories that received new articles after this date. Useful for tracking developing news events or evolving storylines.
            updated_to (Optional[datetime]): Filter for stories that received new articles before this date. Useful for tracking developing news events or evolving storylines.
            topic (Optional[List[str]]): Filter stories by specific topics such as Markets, Crime, Cryptocurrency, or College Sports. Topics are more granular than categories, and stories can include multiple topics based on their constituent articles. Use the /topics endpoint for a complete list of available topics. Multiple values create an OR filter.
            category (Optional[List[str]]): Filter stories by broad content categories such as Politics, Tech, Sports, Business, or Finance. Use 'none' to find uncategorized stories. Categories are derived from the articles within each story. Multiple values create an OR filter.
            taxonomy (Optional[List[str]]): Filter stories by Google Content Categories. Must pass the full hierarchical path of the category. Example: taxonomy=/Finance/Banking/Other,/Finance/Investing/Funds. Stories are categorized based on their constituent articles. Multiple values create an OR filter.
            source (Optional[List[str]]): Filter stories that contain articles from specific publisher domains or subdomains. Supports wildcards (* and ?) for pattern matching (e.g., *.cnn.com). A story will match if it contains at least one article from any of the specified sources. Multiple values create an OR filter.
            source_group (Optional[List[str]]): Filter stories that contain articles from publishers in Perigon's curated bundles (e.g., top100, top25crypto). A story will match if it contains at least one article from any publisher in the specified bundles. Multiple values create an OR filter.
            min_unique_sources (Optional[int]): Specifies the minimum number of unique sources required for a story to appear in results. Higher values return more significant stories covered by multiple publications. Default is 3.
            person_wikidata_id (Optional[List[str]]): Filter stories by Wikidata IDs of top mentioned people. Returns stories where these individuals appear prominently. Refer to the /people endpoint for a complete list of tracked individuals.
            person_name (Optional[str]): Filter stories by exact name matches of top mentioned people. Does not support Boolean or complex logic. For available person entities, consult the /people endpoint.
            company_id (Optional[List[str]]): Filter stories by identifiers of top mentioned companies. Returns stories where these companies appear prominently. For a complete list of tracked companies, refer to the /companies endpoint.
            company_name (Optional[str]): Filter stories by names of top mentioned companies. Performs an exact match on company names in the topCompanies field.
            company_domain (Optional[List[str]]): Filter stories by domains of top mentioned companies (e.g., apple.com). Returns stories where companies with these domains appear prominently. For available company entities, consult the /companies endpoint.
            company_symbol (Optional[List[str]]): Filter stories by stock symbols of top mentioned companies. Returns stories where companies with these symbols appear prominently. For available company entities and their symbols, consult the /companies endpoint.
            country (Optional[List[str]]): Country code to filter by country. If multiple parameters are passed, they will be applied as OR operations.
            state (Optional[List[str]]): Filter local news by state. Applies only to local news, when this param is passed non-local news will not be returned. If multiple parameters are passed, they will be applied as OR operations.
            city (Optional[List[str]]): Filter local news by city. Applies only to local news, when this param is passed non-local news will not be returned. If multiple parameters are passed, they will be applied as OR operations.
            area (Optional[List[str]]): Filter local news by area. Applies only to local news, when this param is passed non-local news will not be returned. If multiple parameters are passed, they will be applied as OR operations.
            min_cluster_size (Optional[int]): Filter by minimum cluster size. Minimum cluster size filter applies to number of unique articles.
            max_cluster_size (Optional[int]): Filter by maximum cluster size. Maximum cluster size filter applies to number of unique articles in the cluster.
            name_exists (Optional[bool]): Filter to only include stories that have been assigned names. Defaults to true. Note that stories only receive names after they contain at least 5 unique articles.
            positive_sentiment_from (Optional[float]): Filter articles with an aggregate positive sentiment score greater than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger positive tone.
            positive_sentiment_to (Optional[float]): Filter articles with an aggregate positive sentiment score less than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger positive tone.
            neutral_sentiment_from (Optional[float]): Filter articles with an aggregate neutral sentiment score greater than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger neutral tone.
            neutral_sentiment_to (Optional[float]): Filter articles with an aggregate neutral sentiment score less than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger neutral tone.
            negative_sentiment_from (Optional[float]): Filter stories with an aggregate negative sentiment score greater than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger negative tone.
            negative_sentiment_to (Optional[float]): Filter articles with an aggregate negative sentiment score less than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger negative tone.
            show_story_page_info (Optional[bool]): Parameter show_story_page_info
            show_num_results (Optional[bool]): Show total number of results. By default set to false, will cap result count at 10000.
            show_duplicates (Optional[bool]): Stories are deduplicated by default. If a story is deduplicated, all future articles are merged into the original story. duplicateOf field contains the original cluster Id. When showDuplicates=true, all stories are shown.
            show_highlighting (Optional[bool]): When set to true, enables text highlighting in search results.
            highlight_fragment_size (Optional[int]): Specifies the size in characters of each highlighted text fragment. Defaults to 100 if not specified.
            highlight_num_fragments (Optional[int]): Controls the maximum number of highlighted fragments to return per field.
            highlight_pre_tag (Optional[str]): Defines the HTML tag that appears before highlighted text. Defaults to '<em>' if not specified.
            highlight_post_tag (Optional[str]): Defines the HTML tag that appears after highlighted text. Defaults to '</em>' if not specified.
            highlight_q (Optional[str]): Specifies a separate query for highlighting, allowing highlights based on terms different from the main search query. Example: main query 'q=climate change' with 'highlightQ=renewable OR solar' will highlight terms 'renewable' and 'solar' in results about climate change.

        Returns:
            StorySearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_STORIES

        params: Dict[str, Any] = {}
        if q is not None:
            params["q"] = q
        if name is not None:
            params["name"] = name
        if cluster_id is not None:
            params["clusterId"] = cluster_id
        if exclude_cluster_id is not None:
            params["excludeClusterId"] = exclude_cluster_id
        if sort_by is not None:
            params["sortBy"] = sort_by
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if var_from is not None:
            params["from"] = var_from
        if to is not None:
            params["to"] = to
        if initialized_from is not None:
            params["initializedFrom"] = initialized_from
        if initialized_to is not None:
            params["initializedTo"] = initialized_to
        if updated_from is not None:
            params["updatedFrom"] = updated_from
        if updated_to is not None:
            params["updatedTo"] = updated_to
        if topic is not None:
            params["topic"] = topic
        if category is not None:
            params["category"] = category
        if taxonomy is not None:
            params["taxonomy"] = taxonomy
        if source is not None:
            params["source"] = source
        if source_group is not None:
            params["sourceGroup"] = source_group
        if min_unique_sources is not None:
            params["minUniqueSources"] = min_unique_sources
        if person_wikidata_id is not None:
            params["personWikidataId"] = person_wikidata_id
        if person_name is not None:
            params["personName"] = person_name
        if company_id is not None:
            params["companyId"] = company_id
        if company_name is not None:
            params["companyName"] = company_name
        if company_domain is not None:
            params["companyDomain"] = company_domain
        if company_symbol is not None:
            params["companySymbol"] = company_symbol
        if country is not None:
            params["country"] = country
        if state is not None:
            params["state"] = state
        if city is not None:
            params["city"] = city
        if area is not None:
            params["area"] = area
        if min_cluster_size is not None:
            params["minClusterSize"] = min_cluster_size
        if max_cluster_size is not None:
            params["maxClusterSize"] = max_cluster_size
        if name_exists is not None:
            params["nameExists"] = name_exists
        if positive_sentiment_from is not None:
            params["positiveSentimentFrom"] = positive_sentiment_from
        if positive_sentiment_to is not None:
            params["positiveSentimentTo"] = positive_sentiment_to
        if neutral_sentiment_from is not None:
            params["neutralSentimentFrom"] = neutral_sentiment_from
        if neutral_sentiment_to is not None:
            params["neutralSentimentTo"] = neutral_sentiment_to
        if negative_sentiment_from is not None:
            params["negativeSentimentFrom"] = negative_sentiment_from
        if negative_sentiment_to is not None:
            params["negativeSentimentTo"] = negative_sentiment_to
        if show_story_page_info is not None:
            params["showStoryPageInfo"] = show_story_page_info
        if show_num_results is not None:
            params["showNumResults"] = show_num_results
        if show_duplicates is not None:
            params["showDuplicates"] = show_duplicates
        if show_highlighting is not None:
            params["showHighlighting"] = show_highlighting
        if highlight_fragment_size is not None:
            params["highlightFragmentSize"] = highlight_fragment_size
        if highlight_num_fragments is not None:
            params["highlightNumFragments"] = highlight_num_fragments
        if highlight_pre_tag is not None:
            params["highlightPreTag"] = highlight_pre_tag
        if highlight_post_tag is not None:
            params["highlightPostTag"] = highlight_post_tag
        if highlight_q is not None:
            params["highlightQ"] = highlight_q
        params = _normalise_query(params)

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()
        return StorySearchResult.model_validate(resp.json())

    # ----------------- search_summarizer (sync) ----------------- #
    def search_summarizer(
        self,
        summary_body: SummaryBody,
        q: Optional[str] = None,
        title: Optional[str] = None,
        desc: Optional[str] = None,
        content: Optional[str] = None,
        url: Optional[str] = None,
        article_id: Optional[List[str]] = None,
        cluster_id: Optional[List[str]] = None,
        sort_by: Optional[AllEndpointSortBy] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        var_from: Optional[datetime] = None,
        to: Optional[datetime] = None,
        add_date_from: Optional[datetime] = None,
        add_date_to: Optional[datetime] = None,
        refresh_date_from: Optional[datetime] = None,
        refresh_date_to: Optional[datetime] = None,
        medium: Optional[List[str]] = None,
        source: Optional[List[str]] = None,
        source_group: Optional[List[str]] = None,
        exclude_source_group: Optional[List[str]] = None,
        exclude_source: Optional[List[str]] = None,
        paywall: Optional[bool] = None,
        byline: Optional[List[str]] = None,
        author: Optional[List[str]] = None,
        exclude_author: Optional[List[str]] = None,
        journalist_id: Optional[List[str]] = None,
        exclude_journalist_id: Optional[List[str]] = None,
        language: Optional[List[str]] = None,
        exclude_language: Optional[List[str]] = None,
        search_translation: Optional[bool] = None,
        label: Optional[List[str]] = None,
        exclude_label: Optional[List[str]] = None,
        category: Optional[List[str]] = None,
        exclude_category: Optional[List[str]] = None,
        topic: Optional[List[str]] = None,
        exclude_topic: Optional[List[str]] = None,
        link_to: Optional[str] = None,
        show_reprints: Optional[bool] = None,
        reprint_group_id: Optional[str] = None,
        city: Optional[List[str]] = None,
        exclude_city: Optional[List[str]] = None,
        area: Optional[List[str]] = None,
        state: Optional[List[str]] = None,
        exclude_state: Optional[List[str]] = None,
        county: Optional[List[str]] = None,
        exclude_county: Optional[List[str]] = None,
        locations_country: Optional[List[str]] = None,
        country: Optional[List[str]] = None,
        exclude_locations_country: Optional[List[str]] = None,
        location: Optional[List[str]] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        max_distance: Optional[float] = None,
        source_city: Optional[List[str]] = None,
        source_county: Optional[List[str]] = None,
        source_country: Optional[List[str]] = None,
        source_state: Optional[List[str]] = None,
        source_lat: Optional[float] = None,
        source_lon: Optional[float] = None,
        source_max_distance: Optional[float] = None,
        person_wikidata_id: Optional[List[str]] = None,
        exclude_person_wikidata_id: Optional[List[str]] = None,
        person_name: Optional[List[str]] = None,
        exclude_person_name: Optional[List[str]] = None,
        company_id: Optional[List[str]] = None,
        exclude_company_id: Optional[List[str]] = None,
        company_name: Optional[str] = None,
        company_domain: Optional[List[str]] = None,
        exclude_company_domain: Optional[List[str]] = None,
        company_symbol: Optional[List[str]] = None,
        exclude_company_symbol: Optional[List[str]] = None,
        show_num_results: Optional[bool] = None,
        positive_sentiment_from: Optional[float] = None,
        positive_sentiment_to: Optional[float] = None,
        neutral_sentiment_from: Optional[float] = None,
        neutral_sentiment_to: Optional[float] = None,
        negative_sentiment_from: Optional[float] = None,
        negative_sentiment_to: Optional[float] = None,
        taxonomy: Optional[List[str]] = None,
        prefix_taxonomy: Optional[str] = None,
        show_highlighting: Optional[bool] = None,
        highlight_fragment_size: Optional[int] = None,
        highlight_num_fragments: Optional[int] = None,
        highlight_pre_tag: Optional[str] = None,
        highlight_post_tag: Optional[str] = None,
        highlight_q: Optional[str] = None,
    ) -> SummarySearchResult:
        """
        Produce a single, concise summary over the full corpus of articles matching your filters, using your prompt to guide which insights to highlight.

        Args:
            summary_body (SummaryBody): Parameter summary_body (required)
            q (Optional[str]): Primary search query for filtering articles based on their title, description, and content. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            title (Optional[str]): Search specifically within article headlines/titles. Supports Boolean operators, exact phrases with quotes, and wildcards for matching title variations.
            desc (Optional[str]): Search within article description fields. Supports Boolean expressions, exact phrase matching with quotes, and wildcards for flexible pattern matching.
            content (Optional[str]): Search within the full article body content. Supports Boolean logic, exact phrase matching with quotes, and wildcards for comprehensive content searching.
            url (Optional[str]): Search within article URLs to find content from specific website sections or domains. Supports wildcards (* and ?) for partial URL matching.
            article_id (Optional[List[str]]): Retrieve specific news articles by their unique article identifiers. Multiple IDs can be provided to return a collection of specific articles.
            cluster_id (Optional[List[str]]): Filter results to only show content within a specific related content cluster. Returns articles grouped together as part of Perigon Stories based on topic relevance.
            sort_by (Optional[AllEndpointSortBy]): Determines the article sorting order. Options include relevance (default), date/pubDate (newest publication date first), reverseDate (oldest publication date first), addDate (newest ingestion date first), reverseAddDate (oldest ingestion date first), and refreshDate (most recently updated in system first, often identical to addDate).
            page (Optional[int]): The specific page of results to retrieve in the paginated response. Starts at 0.
            size (Optional[int]): The number of articles to return per page in the paginated response.
            var_from (Optional[datetime]): Filter for articles published after this date. Accepts ISO 8601 format (e.g., 2023-03-01T00:00:00) or yyyy-mm-dd format.
            to (Optional[datetime]): Filter for articles published before this date. Accepts ISO 8601 format (e.g., 2022-02-01T23:59:59) or yyyy-mm-dd format.
            add_date_from (Optional[datetime]): Filter for articles added to Perigon's system after this date. Accepts ISO 8601 format (e.g., 2022-02-01T00:00:00) or yyyy-mm-dd format.
            add_date_to (Optional[datetime]): Filter for articles added to Perigon's system before this date. Accepts ISO 8601 format (e.g., 2022-02-01T23:59:59) or yyyy-mm-dd format.
            refresh_date_from (Optional[datetime]): Filter for articles refreshed/updated in Perigon's system after this date. In most cases yields similar results to addDateFrom but can differ for updated content. Accepts ISO 8601 format (e.g., 2022-02-01T00:00:00) or yyyy-mm-dd format.
            refresh_date_to (Optional[datetime]): Filter for articles refreshed/updated in Perigon's system before this date. In most cases yields similar results to addDateTo but can differ for updated content. Accepts ISO 8601 format (e.g., 2022-02-01T23:59:59) or yyyy-mm-dd format.
            medium (Optional[List[str]]): Filter articles by their primary medium type. Accepts Article for written content or Video for video-based stories. Multiple values create an OR filter.
            source (Optional[List[str]]): Filter articles by specific publisher domains or subdomains. Supports wildcards (* and ?) for pattern matching (e.g., *.cnn.com). Multiple values create an OR filter.
            source_group (Optional[List[str]]): Filter articles using Perigon's curated publisher bundles (e.g., top100, top25crypto). Multiple values create an OR filter to include articles from any of the specified bundles.
            exclude_source_group (Optional[List[str]]): Exclude articles from specified Perigon source groups. Multiple values create an AND-exclude filter, removing content from publishers in any of the specified bundles (e.g., top10, top100).
            exclude_source (Optional[List[str]]): Exclude articles from specific publisher domains or subdomains. Supports wildcards (* and ?) for pattern matching (e.g., *.cnn.com). Multiple values create an AND-exclude filter.
            paywall (Optional[bool]): Filter to show only results where the source has a paywall (true) or does not have a paywall (false).
            byline (Optional[List[str]]): Filter articles by author bylines. Works as an exact match for each author name provided. Multiple values create an OR filter to find articles by any of the specified authors.
            author (Optional[List[str]]): Filter articles by specific author names. Works as an exact match for each name. Multiple values create an OR filter to find articles by any of the specified authors.
            exclude_author (Optional[List[str]]): Exclude articles written by specific authors. Any article with an author name matching an entry in this list will be omitted from results. Multiple values create an AND-exclude filter.
            journalist_id (Optional[List[str]]): Filter by unique journalist identifiers which can be found through the Journalist API or in the matchedAuthors field. Multiple values create an OR filter.
            exclude_journalist_id (Optional[List[str]]): Exclude articles written by specific journalists identified by their unique IDs. Multiple values create an AND-exclude filter.
            language (Optional[List[str]]): Filter articles by their language using ISO-639 two-letter codes (e.g., en, es, fr). Multiple values create an OR filter.
            exclude_language (Optional[List[str]]): Exclude articles in specific languages using ISO-639 two-letter codes. Multiple values create an AND-exclude filter.
            search_translation (Optional[bool]): Expand search to include translated content fields for non-English articles. When true, searches translated title, description, and content fields.
            label (Optional[List[str]]): Filter articles by editorial labels such as Opinion, Paid-news, Non-news, Fact Check, or Press Release. Multiple values create an OR filter.
            exclude_label (Optional[List[str]]): Exclude articles with specific editorial labels. Multiple values create an AND-exclude filter, removing all content with any of these labels.
            category (Optional[List[str]]): Filter by broad content categories such as Politics, Tech, Sports, Business, or Finance. Use 'none' to find uncategorized articles. Multiple values create an OR filter.
            exclude_category (Optional[List[str]]): Exclude articles with specific categories. Multiple values create an AND-exclude filter, removing all content with any of these categories.
            topic (Optional[List[str]]): Filter by specific topics such as Markets, Crime, Cryptocurrency, or College Sports. Topics are more granular than categories, and articles can have multiple topics. Use the /topics endpoint for a complete list of available topics. Multiple values create an OR filter.
            exclude_topic (Optional[List[str]]): Exclude articles with specific topics. Multiple values create an AND-exclude filter, removing all content with any of these topics.
            link_to (Optional[str]): Returns only articles that contain links to the specified URL pattern. Matches against the 'links' field in article responses.
            show_reprints (Optional[bool]): Controls whether to include reprinted content in results. When true (default), shows syndicated articles from wire services like AP or Reuters that appear on multiple sites.
            reprint_group_id (Optional[str]): Returns all articles in a specific reprint group, including the original article and all its known reprints. Use when you want to see all versions of the same content.
            city (Optional[List[str]]): Filters articles where a specified city plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the urban area in question. If multiple parameters are passed, they will be applied as OR operations.
            exclude_city (Optional[List[str]]): A list of cities to exclude from the results. Articles that are associated with any of the specified cities will be filtered out.
            area (Optional[List[str]]): Filters articles where a specified area, such as a neighborhood, borough, or district, plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the area in question. If multiple parameters are passed, they will be applied as OR operations.
            state (Optional[List[str]]): Filters articles where a specified state plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the state in question. If multiple parameters are passed, they will be applied as OR operations.
            exclude_state (Optional[List[str]]): A list of states to exclude. Articles that include, or are associated with, any of the states provided here will be filtered out. This is especially useful if you want to ignore news tied to certain geographical areas (e.g., US states).
            county (Optional[List[str]]): A list of counties to include (or specify) in the search results. This field filters the returned articles based on the county associated with the event or news. Only articles tagged with one of these counties will be included.
            exclude_county (Optional[List[str]]): Excludes articles from specific counties or administrative divisions in the search results. Accepts either a single county name or a list of county names. County names should match the format used in article metadata (e.g., 'Los Angeles County', 'Cook County'). This parameter allows for more granular geographic filter
            locations_country (Optional[List[str]]): Filters articles where a specified country plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the country in question. If multiple parameters are passed, they will be applied as OR operations.
            country (Optional[List[str]]): Country code to filter by country. If multiple parameters are passed, they will be applied as OR operations.
            exclude_locations_country (Optional[List[str]]): Excludes articles where a specified country plays a central role in the content, ensuring results are not deeply relevant to the country in question. If multiple parameters are passed, they will be applied as AND operations, excluding articles relevant to any of the specified countries.
            location (Optional[List[str]]): Return all articles that have the specified location. Location attributes are delimited by ':' between key and value, and '::' between attributes. Example: 'city:New York::state:NY'.
            lat (Optional[float]): Latitude of the center point to search places
            lon (Optional[float]): Longitude of the center point to search places
            max_distance (Optional[float]): Maximum distance (in km) from starting point to search articles by tagged places
            source_city (Optional[List[str]]): Find articles published by sources that are located within a given city.
            source_county (Optional[List[str]]): Find articles published by sources that are located within a given county.
            source_country (Optional[List[str]]): Find articles published by sources that are located within a given country. Must be 2 character country code (i.e. us, gb, etc).
            source_state (Optional[List[str]]): Find articles published by sources that are located within a given state.
            source_lat (Optional[float]): Latitude of the center point to search articles created by local publications.
            source_lon (Optional[float]): Latitude of the center point to search articles created by local publications.
            source_max_distance (Optional[float]): Maximum distance from starting point to search articles created by local publications.
            person_wikidata_id (Optional[List[str]]): Filter articles by Wikidata IDs of mentioned people. Refer to the /people endpoint for a complete list of tracked individuals.
            exclude_person_wikidata_id (Optional[List[str]]): Exclude articles mentioning people with specific Wikidata IDs. Creates an AND-exclude filter to remove content about these individuals. Uses precise identifiers to avoid name ambiguity.
            person_name (Optional[List[str]]): Filter articles by exact person name matches. Does not support Boolean or complex logic. For available person entities, consult the /people endpoint.
            exclude_person_name (Optional[List[str]]): Exclude articles mentioning specific people by name. Creates an AND-exclude filter to remove content about these individuals.
            company_id (Optional[List[str]]): Filter articles by company identifiers. For a complete list of tracked companies, refer to the /companies endpoint.
            exclude_company_id (Optional[List[str]]): Exclude articles mentioning companies with specific identifiers. Creates an AND-exclude filter to remove content about these corporate entities.
            company_name (Optional[str]): Filter articles by company name mentions. Performs an exact match on company names.
            company_domain (Optional[List[str]]): Filter articles by company domains (e.g., apple.com). For available company entities, consult the /companies endpoint.
            exclude_company_domain (Optional[List[str]]): Exclude articles related to companies with specific domains. Creates an AND-exclude filter to remove content about these companies.
            company_symbol (Optional[List[str]]): Filter articles by company stock symbols. For available company entities and their symbols, consult the /companies endpoint.
            exclude_company_symbol (Optional[List[str]]): A list of stock symbols (ticker symbols) that identify companies to be excluded. Articles related to companies using any of these symbols will be omitted, which is useful for targeting or avoiding specific public companies.
            show_num_results (Optional[bool]): Whether to show the total number of all matched articles. Default value is false which makes queries a bit more efficient but also counts up to 10000 articles.
            positive_sentiment_from (Optional[float]): Filter articles with a positive sentiment score greater than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger positive tone.
            positive_sentiment_to (Optional[float]): Filter articles with a positive sentiment score less than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger positive tone.
            neutral_sentiment_from (Optional[float]): Filter articles with a neutral sentiment score greater than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger neutral tone.
            neutral_sentiment_to (Optional[float]): Filter articles with a neutral sentiment score less than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger neutral tone.
            negative_sentiment_from (Optional[float]): Filter articles with a negative sentiment score greater than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger negative tone.
            negative_sentiment_to (Optional[float]): Filter articles with a negative sentiment score less than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger negative tone.
            taxonomy (Optional[List[str]]): Filters by Google Content Categories. This field will accept 1 or more categories, must pass the full name of the category. Example: taxonomy=/Finance/Banking/Other, /Finance/Investing/Funds. [Full list](https://cloud.google.com/natural-language/docs/categories)
            prefix_taxonomy (Optional[str]): Filters by Google Content Categories. This field will filter by the category prefix only. Example: prefixTaxonomy=/Finance
            show_highlighting (Optional[bool]): When set to true, enables text highlighting in search results.
            highlight_fragment_size (Optional[int]): Specifies the size in characters of each highlighted text fragment. Defaults to 100 if not specified.
            highlight_num_fragments (Optional[int]): Controls the maximum number of highlighted fragments to return per field.
            highlight_pre_tag (Optional[str]): Defines the HTML tag that appears before highlighted text. Defaults to '<em>' if not specified.
            highlight_post_tag (Optional[str]): Defines the HTML tag that appears after highlighted text. Defaults to '</em>' if not specified.
            highlight_q (Optional[str]): Specifies a separate query for highlighting, allowing highlights based on terms different from the main search query. Example: main query 'q=climate change' with 'highlightQ=renewable OR solar' will highlight terms 'renewable' and 'solar' in results about climate change.

        Returns:
            SummarySearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_SUMMARIZER

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if q is not None:
            params["q"] = q
        if title is not None:
            params["title"] = title
        if desc is not None:
            params["desc"] = desc
        if content is not None:
            params["content"] = content
        if url is not None:
            params["url"] = url
        if article_id is not None:
            params["articleId"] = article_id
        if cluster_id is not None:
            params["clusterId"] = cluster_id
        if sort_by is not None:
            params["sortBy"] = sort_by
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if var_from is not None:
            params["from"] = var_from
        if to is not None:
            params["to"] = to
        if add_date_from is not None:
            params["addDateFrom"] = add_date_from
        if add_date_to is not None:
            params["addDateTo"] = add_date_to
        if refresh_date_from is not None:
            params["refreshDateFrom"] = refresh_date_from
        if refresh_date_to is not None:
            params["refreshDateTo"] = refresh_date_to
        if medium is not None:
            params["medium"] = medium
        if source is not None:
            params["source"] = source
        if source_group is not None:
            params["sourceGroup"] = source_group
        if exclude_source_group is not None:
            params["excludeSourceGroup"] = exclude_source_group
        if exclude_source is not None:
            params["excludeSource"] = exclude_source
        if paywall is not None:
            params["paywall"] = paywall
        if byline is not None:
            params["byline"] = byline
        if author is not None:
            params["author"] = author
        if exclude_author is not None:
            params["excludeAuthor"] = exclude_author
        if journalist_id is not None:
            params["journalistId"] = journalist_id
        if exclude_journalist_id is not None:
            params["excludeJournalistId"] = exclude_journalist_id
        if language is not None:
            params["language"] = language
        if exclude_language is not None:
            params["excludeLanguage"] = exclude_language
        if search_translation is not None:
            params["searchTranslation"] = search_translation
        if label is not None:
            params["label"] = label
        if exclude_label is not None:
            params["excludeLabel"] = exclude_label
        if category is not None:
            params["category"] = category
        if exclude_category is not None:
            params["excludeCategory"] = exclude_category
        if topic is not None:
            params["topic"] = topic
        if exclude_topic is not None:
            params["excludeTopic"] = exclude_topic
        if link_to is not None:
            params["linkTo"] = link_to
        if show_reprints is not None:
            params["showReprints"] = show_reprints
        if reprint_group_id is not None:
            params["reprintGroupId"] = reprint_group_id
        if city is not None:
            params["city"] = city
        if exclude_city is not None:
            params["excludeCity"] = exclude_city
        if area is not None:
            params["area"] = area
        if state is not None:
            params["state"] = state
        if exclude_state is not None:
            params["excludeState"] = exclude_state
        if county is not None:
            params["county"] = county
        if exclude_county is not None:
            params["excludeCounty"] = exclude_county
        if locations_country is not None:
            params["locationsCountry"] = locations_country
        if country is not None:
            params["country"] = country
        if exclude_locations_country is not None:
            params["excludeLocationsCountry"] = exclude_locations_country
        if location is not None:
            params["location"] = location
        if lat is not None:
            params["lat"] = lat
        if lon is not None:
            params["lon"] = lon
        if max_distance is not None:
            params["maxDistance"] = max_distance
        if source_city is not None:
            params["sourceCity"] = source_city
        if source_county is not None:
            params["sourceCounty"] = source_county
        if source_country is not None:
            params["sourceCountry"] = source_country
        if source_state is not None:
            params["sourceState"] = source_state
        if source_lat is not None:
            params["sourceLat"] = source_lat
        if source_lon is not None:
            params["sourceLon"] = source_lon
        if source_max_distance is not None:
            params["sourceMaxDistance"] = source_max_distance
        if person_wikidata_id is not None:
            params["personWikidataId"] = person_wikidata_id
        if exclude_person_wikidata_id is not None:
            params["excludePersonWikidataId"] = exclude_person_wikidata_id
        if person_name is not None:
            params["personName"] = person_name
        if exclude_person_name is not None:
            params["excludePersonName"] = exclude_person_name
        if company_id is not None:
            params["companyId"] = company_id
        if exclude_company_id is not None:
            params["excludeCompanyId"] = exclude_company_id
        if company_name is not None:
            params["companyName"] = company_name
        if company_domain is not None:
            params["companyDomain"] = company_domain
        if exclude_company_domain is not None:
            params["excludeCompanyDomain"] = exclude_company_domain
        if company_symbol is not None:
            params["companySymbol"] = company_symbol
        if exclude_company_symbol is not None:
            params["excludeCompanySymbol"] = exclude_company_symbol
        if show_num_results is not None:
            params["showNumResults"] = show_num_results
        if positive_sentiment_from is not None:
            params["positiveSentimentFrom"] = positive_sentiment_from
        if positive_sentiment_to is not None:
            params["positiveSentimentTo"] = positive_sentiment_to
        if neutral_sentiment_from is not None:
            params["neutralSentimentFrom"] = neutral_sentiment_from
        if neutral_sentiment_to is not None:
            params["neutralSentimentTo"] = neutral_sentiment_to
        if negative_sentiment_from is not None:
            params["negativeSentimentFrom"] = negative_sentiment_from
        if negative_sentiment_to is not None:
            params["negativeSentimentTo"] = negative_sentiment_to
        if taxonomy is not None:
            params["taxonomy"] = taxonomy
        if prefix_taxonomy is not None:
            params["prefixTaxonomy"] = prefix_taxonomy
        if show_highlighting is not None:
            params["showHighlighting"] = show_highlighting
        if highlight_fragment_size is not None:
            params["highlightFragmentSize"] = highlight_fragment_size
        if highlight_num_fragments is not None:
            params["highlightNumFragments"] = highlight_num_fragments
        if highlight_pre_tag is not None:
            params["highlightPreTag"] = highlight_pre_tag
        if highlight_post_tag is not None:
            params["highlightPostTag"] = highlight_post_tag
        if highlight_q is not None:
            params["highlightQ"] = highlight_q
        params = _normalise_query(params)

        resp = self.api_client.request(
            "POST", path, params=params, json=summary_body.model_dump(by_alias=True)
        )
        resp.raise_for_status()
        return SummarySearchResult.model_validate(resp.json())

    # ----------------- search_summarizer (async) ----------------- #
    async def search_summarizer_async(
        self,
        summary_body: SummaryBody,
        q: Optional[str] = None,
        title: Optional[str] = None,
        desc: Optional[str] = None,
        content: Optional[str] = None,
        url: Optional[str] = None,
        article_id: Optional[List[str]] = None,
        cluster_id: Optional[List[str]] = None,
        sort_by: Optional[AllEndpointSortBy] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        var_from: Optional[datetime] = None,
        to: Optional[datetime] = None,
        add_date_from: Optional[datetime] = None,
        add_date_to: Optional[datetime] = None,
        refresh_date_from: Optional[datetime] = None,
        refresh_date_to: Optional[datetime] = None,
        medium: Optional[List[str]] = None,
        source: Optional[List[str]] = None,
        source_group: Optional[List[str]] = None,
        exclude_source_group: Optional[List[str]] = None,
        exclude_source: Optional[List[str]] = None,
        paywall: Optional[bool] = None,
        byline: Optional[List[str]] = None,
        author: Optional[List[str]] = None,
        exclude_author: Optional[List[str]] = None,
        journalist_id: Optional[List[str]] = None,
        exclude_journalist_id: Optional[List[str]] = None,
        language: Optional[List[str]] = None,
        exclude_language: Optional[List[str]] = None,
        search_translation: Optional[bool] = None,
        label: Optional[List[str]] = None,
        exclude_label: Optional[List[str]] = None,
        category: Optional[List[str]] = None,
        exclude_category: Optional[List[str]] = None,
        topic: Optional[List[str]] = None,
        exclude_topic: Optional[List[str]] = None,
        link_to: Optional[str] = None,
        show_reprints: Optional[bool] = None,
        reprint_group_id: Optional[str] = None,
        city: Optional[List[str]] = None,
        exclude_city: Optional[List[str]] = None,
        area: Optional[List[str]] = None,
        state: Optional[List[str]] = None,
        exclude_state: Optional[List[str]] = None,
        county: Optional[List[str]] = None,
        exclude_county: Optional[List[str]] = None,
        locations_country: Optional[List[str]] = None,
        country: Optional[List[str]] = None,
        exclude_locations_country: Optional[List[str]] = None,
        location: Optional[List[str]] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        max_distance: Optional[float] = None,
        source_city: Optional[List[str]] = None,
        source_county: Optional[List[str]] = None,
        source_country: Optional[List[str]] = None,
        source_state: Optional[List[str]] = None,
        source_lat: Optional[float] = None,
        source_lon: Optional[float] = None,
        source_max_distance: Optional[float] = None,
        person_wikidata_id: Optional[List[str]] = None,
        exclude_person_wikidata_id: Optional[List[str]] = None,
        person_name: Optional[List[str]] = None,
        exclude_person_name: Optional[List[str]] = None,
        company_id: Optional[List[str]] = None,
        exclude_company_id: Optional[List[str]] = None,
        company_name: Optional[str] = None,
        company_domain: Optional[List[str]] = None,
        exclude_company_domain: Optional[List[str]] = None,
        company_symbol: Optional[List[str]] = None,
        exclude_company_symbol: Optional[List[str]] = None,
        show_num_results: Optional[bool] = None,
        positive_sentiment_from: Optional[float] = None,
        positive_sentiment_to: Optional[float] = None,
        neutral_sentiment_from: Optional[float] = None,
        neutral_sentiment_to: Optional[float] = None,
        negative_sentiment_from: Optional[float] = None,
        negative_sentiment_to: Optional[float] = None,
        taxonomy: Optional[List[str]] = None,
        prefix_taxonomy: Optional[str] = None,
        show_highlighting: Optional[bool] = None,
        highlight_fragment_size: Optional[int] = None,
        highlight_num_fragments: Optional[int] = None,
        highlight_pre_tag: Optional[str] = None,
        highlight_post_tag: Optional[str] = None,
        highlight_q: Optional[str] = None,
    ) -> SummarySearchResult:
        """
        Async variant of search_summarizer. Produce a single, concise summary over the full corpus of articles matching your filters, using your prompt to guide which insights to highlight.

        Args:
            summary_body (SummaryBody): Parameter summary_body (required)
            q (Optional[str]): Primary search query for filtering articles based on their title, description, and content. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            title (Optional[str]): Search specifically within article headlines/titles. Supports Boolean operators, exact phrases with quotes, and wildcards for matching title variations.
            desc (Optional[str]): Search within article description fields. Supports Boolean expressions, exact phrase matching with quotes, and wildcards for flexible pattern matching.
            content (Optional[str]): Search within the full article body content. Supports Boolean logic, exact phrase matching with quotes, and wildcards for comprehensive content searching.
            url (Optional[str]): Search within article URLs to find content from specific website sections or domains. Supports wildcards (* and ?) for partial URL matching.
            article_id (Optional[List[str]]): Retrieve specific news articles by their unique article identifiers. Multiple IDs can be provided to return a collection of specific articles.
            cluster_id (Optional[List[str]]): Filter results to only show content within a specific related content cluster. Returns articles grouped together as part of Perigon Stories based on topic relevance.
            sort_by (Optional[AllEndpointSortBy]): Determines the article sorting order. Options include relevance (default), date/pubDate (newest publication date first), reverseDate (oldest publication date first), addDate (newest ingestion date first), reverseAddDate (oldest ingestion date first), and refreshDate (most recently updated in system first, often identical to addDate).
            page (Optional[int]): The specific page of results to retrieve in the paginated response. Starts at 0.
            size (Optional[int]): The number of articles to return per page in the paginated response.
            var_from (Optional[datetime]): Filter for articles published after this date. Accepts ISO 8601 format (e.g., 2023-03-01T00:00:00) or yyyy-mm-dd format.
            to (Optional[datetime]): Filter for articles published before this date. Accepts ISO 8601 format (e.g., 2022-02-01T23:59:59) or yyyy-mm-dd format.
            add_date_from (Optional[datetime]): Filter for articles added to Perigon's system after this date. Accepts ISO 8601 format (e.g., 2022-02-01T00:00:00) or yyyy-mm-dd format.
            add_date_to (Optional[datetime]): Filter for articles added to Perigon's system before this date. Accepts ISO 8601 format (e.g., 2022-02-01T23:59:59) or yyyy-mm-dd format.
            refresh_date_from (Optional[datetime]): Filter for articles refreshed/updated in Perigon's system after this date. In most cases yields similar results to addDateFrom but can differ for updated content. Accepts ISO 8601 format (e.g., 2022-02-01T00:00:00) or yyyy-mm-dd format.
            refresh_date_to (Optional[datetime]): Filter for articles refreshed/updated in Perigon's system before this date. In most cases yields similar results to addDateTo but can differ for updated content. Accepts ISO 8601 format (e.g., 2022-02-01T23:59:59) or yyyy-mm-dd format.
            medium (Optional[List[str]]): Filter articles by their primary medium type. Accepts Article for written content or Video for video-based stories. Multiple values create an OR filter.
            source (Optional[List[str]]): Filter articles by specific publisher domains or subdomains. Supports wildcards (* and ?) for pattern matching (e.g., *.cnn.com). Multiple values create an OR filter.
            source_group (Optional[List[str]]): Filter articles using Perigon's curated publisher bundles (e.g., top100, top25crypto). Multiple values create an OR filter to include articles from any of the specified bundles.
            exclude_source_group (Optional[List[str]]): Exclude articles from specified Perigon source groups. Multiple values create an AND-exclude filter, removing content from publishers in any of the specified bundles (e.g., top10, top100).
            exclude_source (Optional[List[str]]): Exclude articles from specific publisher domains or subdomains. Supports wildcards (* and ?) for pattern matching (e.g., *.cnn.com). Multiple values create an AND-exclude filter.
            paywall (Optional[bool]): Filter to show only results where the source has a paywall (true) or does not have a paywall (false).
            byline (Optional[List[str]]): Filter articles by author bylines. Works as an exact match for each author name provided. Multiple values create an OR filter to find articles by any of the specified authors.
            author (Optional[List[str]]): Filter articles by specific author names. Works as an exact match for each name. Multiple values create an OR filter to find articles by any of the specified authors.
            exclude_author (Optional[List[str]]): Exclude articles written by specific authors. Any article with an author name matching an entry in this list will be omitted from results. Multiple values create an AND-exclude filter.
            journalist_id (Optional[List[str]]): Filter by unique journalist identifiers which can be found through the Journalist API or in the matchedAuthors field. Multiple values create an OR filter.
            exclude_journalist_id (Optional[List[str]]): Exclude articles written by specific journalists identified by their unique IDs. Multiple values create an AND-exclude filter.
            language (Optional[List[str]]): Filter articles by their language using ISO-639 two-letter codes (e.g., en, es, fr). Multiple values create an OR filter.
            exclude_language (Optional[List[str]]): Exclude articles in specific languages using ISO-639 two-letter codes. Multiple values create an AND-exclude filter.
            search_translation (Optional[bool]): Expand search to include translated content fields for non-English articles. When true, searches translated title, description, and content fields.
            label (Optional[List[str]]): Filter articles by editorial labels such as Opinion, Paid-news, Non-news, Fact Check, or Press Release. Multiple values create an OR filter.
            exclude_label (Optional[List[str]]): Exclude articles with specific editorial labels. Multiple values create an AND-exclude filter, removing all content with any of these labels.
            category (Optional[List[str]]): Filter by broad content categories such as Politics, Tech, Sports, Business, or Finance. Use 'none' to find uncategorized articles. Multiple values create an OR filter.
            exclude_category (Optional[List[str]]): Exclude articles with specific categories. Multiple values create an AND-exclude filter, removing all content with any of these categories.
            topic (Optional[List[str]]): Filter by specific topics such as Markets, Crime, Cryptocurrency, or College Sports. Topics are more granular than categories, and articles can have multiple topics. Use the /topics endpoint for a complete list of available topics. Multiple values create an OR filter.
            exclude_topic (Optional[List[str]]): Exclude articles with specific topics. Multiple values create an AND-exclude filter, removing all content with any of these topics.
            link_to (Optional[str]): Returns only articles that contain links to the specified URL pattern. Matches against the 'links' field in article responses.
            show_reprints (Optional[bool]): Controls whether to include reprinted content in results. When true (default), shows syndicated articles from wire services like AP or Reuters that appear on multiple sites.
            reprint_group_id (Optional[str]): Returns all articles in a specific reprint group, including the original article and all its known reprints. Use when you want to see all versions of the same content.
            city (Optional[List[str]]): Filters articles where a specified city plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the urban area in question. If multiple parameters are passed, they will be applied as OR operations.
            exclude_city (Optional[List[str]]): A list of cities to exclude from the results. Articles that are associated with any of the specified cities will be filtered out.
            area (Optional[List[str]]): Filters articles where a specified area, such as a neighborhood, borough, or district, plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the area in question. If multiple parameters are passed, they will be applied as OR operations.
            state (Optional[List[str]]): Filters articles where a specified state plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the state in question. If multiple parameters are passed, they will be applied as OR operations.
            exclude_state (Optional[List[str]]): A list of states to exclude. Articles that include, or are associated with, any of the states provided here will be filtered out. This is especially useful if you want to ignore news tied to certain geographical areas (e.g., US states).
            county (Optional[List[str]]): A list of counties to include (or specify) in the search results. This field filters the returned articles based on the county associated with the event or news. Only articles tagged with one of these counties will be included.
            exclude_county (Optional[List[str]]): Excludes articles from specific counties or administrative divisions in the search results. Accepts either a single county name or a list of county names. County names should match the format used in article metadata (e.g., 'Los Angeles County', 'Cook County'). This parameter allows for more granular geographic filter
            locations_country (Optional[List[str]]): Filters articles where a specified country plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the country in question. If multiple parameters are passed, they will be applied as OR operations.
            country (Optional[List[str]]): Country code to filter by country. If multiple parameters are passed, they will be applied as OR operations.
            exclude_locations_country (Optional[List[str]]): Excludes articles where a specified country plays a central role in the content, ensuring results are not deeply relevant to the country in question. If multiple parameters are passed, they will be applied as AND operations, excluding articles relevant to any of the specified countries.
            location (Optional[List[str]]): Return all articles that have the specified location. Location attributes are delimited by ':' between key and value, and '::' between attributes. Example: 'city:New York::state:NY'.
            lat (Optional[float]): Latitude of the center point to search places
            lon (Optional[float]): Longitude of the center point to search places
            max_distance (Optional[float]): Maximum distance (in km) from starting point to search articles by tagged places
            source_city (Optional[List[str]]): Find articles published by sources that are located within a given city.
            source_county (Optional[List[str]]): Find articles published by sources that are located within a given county.
            source_country (Optional[List[str]]): Find articles published by sources that are located within a given country. Must be 2 character country code (i.e. us, gb, etc).
            source_state (Optional[List[str]]): Find articles published by sources that are located within a given state.
            source_lat (Optional[float]): Latitude of the center point to search articles created by local publications.
            source_lon (Optional[float]): Latitude of the center point to search articles created by local publications.
            source_max_distance (Optional[float]): Maximum distance from starting point to search articles created by local publications.
            person_wikidata_id (Optional[List[str]]): Filter articles by Wikidata IDs of mentioned people. Refer to the /people endpoint for a complete list of tracked individuals.
            exclude_person_wikidata_id (Optional[List[str]]): Exclude articles mentioning people with specific Wikidata IDs. Creates an AND-exclude filter to remove content about these individuals. Uses precise identifiers to avoid name ambiguity.
            person_name (Optional[List[str]]): Filter articles by exact person name matches. Does not support Boolean or complex logic. For available person entities, consult the /people endpoint.
            exclude_person_name (Optional[List[str]]): Exclude articles mentioning specific people by name. Creates an AND-exclude filter to remove content about these individuals.
            company_id (Optional[List[str]]): Filter articles by company identifiers. For a complete list of tracked companies, refer to the /companies endpoint.
            exclude_company_id (Optional[List[str]]): Exclude articles mentioning companies with specific identifiers. Creates an AND-exclude filter to remove content about these corporate entities.
            company_name (Optional[str]): Filter articles by company name mentions. Performs an exact match on company names.
            company_domain (Optional[List[str]]): Filter articles by company domains (e.g., apple.com). For available company entities, consult the /companies endpoint.
            exclude_company_domain (Optional[List[str]]): Exclude articles related to companies with specific domains. Creates an AND-exclude filter to remove content about these companies.
            company_symbol (Optional[List[str]]): Filter articles by company stock symbols. For available company entities and their symbols, consult the /companies endpoint.
            exclude_company_symbol (Optional[List[str]]): A list of stock symbols (ticker symbols) that identify companies to be excluded. Articles related to companies using any of these symbols will be omitted, which is useful for targeting or avoiding specific public companies.
            show_num_results (Optional[bool]): Whether to show the total number of all matched articles. Default value is false which makes queries a bit more efficient but also counts up to 10000 articles.
            positive_sentiment_from (Optional[float]): Filter articles with a positive sentiment score greater than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger positive tone.
            positive_sentiment_to (Optional[float]): Filter articles with a positive sentiment score less than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger positive tone.
            neutral_sentiment_from (Optional[float]): Filter articles with a neutral sentiment score greater than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger neutral tone.
            neutral_sentiment_to (Optional[float]): Filter articles with a neutral sentiment score less than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger neutral tone.
            negative_sentiment_from (Optional[float]): Filter articles with a negative sentiment score greater than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger negative tone.
            negative_sentiment_to (Optional[float]): Filter articles with a negative sentiment score less than or equal to the specified value. Scores range from 0 to 1, with higher values indicating stronger negative tone.
            taxonomy (Optional[List[str]]): Filters by Google Content Categories. This field will accept 1 or more categories, must pass the full name of the category. Example: taxonomy=/Finance/Banking/Other, /Finance/Investing/Funds. [Full list](https://cloud.google.com/natural-language/docs/categories)
            prefix_taxonomy (Optional[str]): Filters by Google Content Categories. This field will filter by the category prefix only. Example: prefixTaxonomy=/Finance
            show_highlighting (Optional[bool]): When set to true, enables text highlighting in search results.
            highlight_fragment_size (Optional[int]): Specifies the size in characters of each highlighted text fragment. Defaults to 100 if not specified.
            highlight_num_fragments (Optional[int]): Controls the maximum number of highlighted fragments to return per field.
            highlight_pre_tag (Optional[str]): Defines the HTML tag that appears before highlighted text. Defaults to '<em>' if not specified.
            highlight_post_tag (Optional[str]): Defines the HTML tag that appears after highlighted text. Defaults to '</em>' if not specified.
            highlight_q (Optional[str]): Specifies a separate query for highlighting, allowing highlights based on terms different from the main search query. Example: main query 'q=climate change' with 'highlightQ=renewable OR solar' will highlight terms 'renewable' and 'solar' in results about climate change.

        Returns:
            SummarySearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_SUMMARIZER

        params: Dict[str, Any] = {}
        if q is not None:
            params["q"] = q
        if title is not None:
            params["title"] = title
        if desc is not None:
            params["desc"] = desc
        if content is not None:
            params["content"] = content
        if url is not None:
            params["url"] = url
        if article_id is not None:
            params["articleId"] = article_id
        if cluster_id is not None:
            params["clusterId"] = cluster_id
        if sort_by is not None:
            params["sortBy"] = sort_by
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if var_from is not None:
            params["from"] = var_from
        if to is not None:
            params["to"] = to
        if add_date_from is not None:
            params["addDateFrom"] = add_date_from
        if add_date_to is not None:
            params["addDateTo"] = add_date_to
        if refresh_date_from is not None:
            params["refreshDateFrom"] = refresh_date_from
        if refresh_date_to is not None:
            params["refreshDateTo"] = refresh_date_to
        if medium is not None:
            params["medium"] = medium
        if source is not None:
            params["source"] = source
        if source_group is not None:
            params["sourceGroup"] = source_group
        if exclude_source_group is not None:
            params["excludeSourceGroup"] = exclude_source_group
        if exclude_source is not None:
            params["excludeSource"] = exclude_source
        if paywall is not None:
            params["paywall"] = paywall
        if byline is not None:
            params["byline"] = byline
        if author is not None:
            params["author"] = author
        if exclude_author is not None:
            params["excludeAuthor"] = exclude_author
        if journalist_id is not None:
            params["journalistId"] = journalist_id
        if exclude_journalist_id is not None:
            params["excludeJournalistId"] = exclude_journalist_id
        if language is not None:
            params["language"] = language
        if exclude_language is not None:
            params["excludeLanguage"] = exclude_language
        if search_translation is not None:
            params["searchTranslation"] = search_translation
        if label is not None:
            params["label"] = label
        if exclude_label is not None:
            params["excludeLabel"] = exclude_label
        if category is not None:
            params["category"] = category
        if exclude_category is not None:
            params["excludeCategory"] = exclude_category
        if topic is not None:
            params["topic"] = topic
        if exclude_topic is not None:
            params["excludeTopic"] = exclude_topic
        if link_to is not None:
            params["linkTo"] = link_to
        if show_reprints is not None:
            params["showReprints"] = show_reprints
        if reprint_group_id is not None:
            params["reprintGroupId"] = reprint_group_id
        if city is not None:
            params["city"] = city
        if exclude_city is not None:
            params["excludeCity"] = exclude_city
        if area is not None:
            params["area"] = area
        if state is not None:
            params["state"] = state
        if exclude_state is not None:
            params["excludeState"] = exclude_state
        if county is not None:
            params["county"] = county
        if exclude_county is not None:
            params["excludeCounty"] = exclude_county
        if locations_country is not None:
            params["locationsCountry"] = locations_country
        if country is not None:
            params["country"] = country
        if exclude_locations_country is not None:
            params["excludeLocationsCountry"] = exclude_locations_country
        if location is not None:
            params["location"] = location
        if lat is not None:
            params["lat"] = lat
        if lon is not None:
            params["lon"] = lon
        if max_distance is not None:
            params["maxDistance"] = max_distance
        if source_city is not None:
            params["sourceCity"] = source_city
        if source_county is not None:
            params["sourceCounty"] = source_county
        if source_country is not None:
            params["sourceCountry"] = source_country
        if source_state is not None:
            params["sourceState"] = source_state
        if source_lat is not None:
            params["sourceLat"] = source_lat
        if source_lon is not None:
            params["sourceLon"] = source_lon
        if source_max_distance is not None:
            params["sourceMaxDistance"] = source_max_distance
        if person_wikidata_id is not None:
            params["personWikidataId"] = person_wikidata_id
        if exclude_person_wikidata_id is not None:
            params["excludePersonWikidataId"] = exclude_person_wikidata_id
        if person_name is not None:
            params["personName"] = person_name
        if exclude_person_name is not None:
            params["excludePersonName"] = exclude_person_name
        if company_id is not None:
            params["companyId"] = company_id
        if exclude_company_id is not None:
            params["excludeCompanyId"] = exclude_company_id
        if company_name is not None:
            params["companyName"] = company_name
        if company_domain is not None:
            params["companyDomain"] = company_domain
        if exclude_company_domain is not None:
            params["excludeCompanyDomain"] = exclude_company_domain
        if company_symbol is not None:
            params["companySymbol"] = company_symbol
        if exclude_company_symbol is not None:
            params["excludeCompanySymbol"] = exclude_company_symbol
        if show_num_results is not None:
            params["showNumResults"] = show_num_results
        if positive_sentiment_from is not None:
            params["positiveSentimentFrom"] = positive_sentiment_from
        if positive_sentiment_to is not None:
            params["positiveSentimentTo"] = positive_sentiment_to
        if neutral_sentiment_from is not None:
            params["neutralSentimentFrom"] = neutral_sentiment_from
        if neutral_sentiment_to is not None:
            params["neutralSentimentTo"] = neutral_sentiment_to
        if negative_sentiment_from is not None:
            params["negativeSentimentFrom"] = negative_sentiment_from
        if negative_sentiment_to is not None:
            params["negativeSentimentTo"] = negative_sentiment_to
        if taxonomy is not None:
            params["taxonomy"] = taxonomy
        if prefix_taxonomy is not None:
            params["prefixTaxonomy"] = prefix_taxonomy
        if show_highlighting is not None:
            params["showHighlighting"] = show_highlighting
        if highlight_fragment_size is not None:
            params["highlightFragmentSize"] = highlight_fragment_size
        if highlight_num_fragments is not None:
            params["highlightNumFragments"] = highlight_num_fragments
        if highlight_pre_tag is not None:
            params["highlightPreTag"] = highlight_pre_tag
        if highlight_post_tag is not None:
            params["highlightPostTag"] = highlight_post_tag
        if highlight_q is not None:
            params["highlightQ"] = highlight_q
        params = _normalise_query(params)

        resp = await self.api_client.request_async(
            "POST", path, params=params, json=summary_body.model_dump(by_alias=True)
        )
        resp.raise_for_status()
        return SummarySearchResult.model_validate(resp.json())

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

    # ----------------- search_wikipedia (sync) ----------------- #
    def search_wikipedia(
        self,
        q: Optional[str] = None,
        title: Optional[str] = None,
        summary: Optional[str] = None,
        text: Optional[str] = None,
        reference: Optional[str] = None,
        id: Optional[List[str]] = None,
        wiki_page_id: Optional[List[int]] = None,
        wiki_revision_id: Optional[List[int]] = None,
        wiki_code: Optional[List[str]] = None,
        wiki_namespace: Optional[List[int]] = None,
        wikidata_id: Optional[List[str]] = None,
        wikidata_instance_of_id: Optional[List[str]] = None,
        wikidata_instance_of_label: Optional[List[str]] = None,
        category: Optional[List[str]] = None,
        section_id: Optional[List[str]] = None,
        wiki_revision_from: Optional[datetime] = None,
        wiki_revision_to: Optional[datetime] = None,
        scraped_at_from: Optional[datetime] = None,
        scraped_at_to: Optional[datetime] = None,
        pageviews_from: Optional[int] = None,
        pageviews_to: Optional[int] = None,
        with_pageviews: Optional[bool] = None,
        show_num_results: Optional[bool] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        sort_by: Optional[SortBy] = None,
    ) -> WikipediaSearchResult:
        """
        Search and filter all Wikipedia pages available via the Perigon API. The result includes a list of individual pages that were matched to your specific criteria.

        Args:
            q (Optional[str]): Primary search query for filtering pages based on their title, summary, and content. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            title (Optional[str]): Search specifically within page titles. Supports Boolean operators, exact phrases with quotes, and wildcards for matching title variations.
            summary (Optional[str]): Search specifically within page summary. Supports Boolean operators, exact phrases with quotes, and wildcards for matching title variations.
            text (Optional[str]): Search specifically within the page's content (across all sections). Supports Boolean operators, exact phrases with quotes, and wildcards for matching title variations.
            reference (Optional[str]): Search specifically across page's references. Supports Boolean operators, exact phrases with quotes, and wildcards for matching title variations.
            id (Optional[List[str]]): Retrieve specific pages by their unique Perigon identifiers. Multiple IDs can be provided to return a collection of specific pages.
            wiki_page_id (Optional[List[int]]): Retrieve specific pages by their Wikipedia identifiers. These are unique only in a combination with `wikiCode` parameter. Multiple IDs can be provided to return a collection of specific pages.
            wiki_revision_id (Optional[List[int]]): Retrieve specific pages by their Wikipedia revision identifiers. These are unique only in a combination with `wikiCode` parameter. Multiple IDs can be provided to return a collection of specific pages. This ID changes each time a page is edited.
            wiki_code (Optional[List[str]]): Retrieve pages only from specified wiki projects. Currently, the only accepted value is `enwiki`.
            wiki_namespace (Optional[List[int]]): Retrieve pages only from specified wiki namespace. Currently, only the main namespace (0) is available.
            wikidata_id (Optional[List[str]]): Retrieve pages by the ids corresponding to their Wikidata entities.
            wikidata_instance_of_id (Optional[List[str]]): Retrieve all pages whose Wikidata entities are instances of these provided ids.
            wikidata_instance_of_label (Optional[List[str]]): Retrieve all pages whose Wikidata entities are instances of these ids (provided as labels).
            category (Optional[List[str]]): Retrieve all pages for specified categories.
            section_id (Optional[List[str]]): Retrieve pages containing provided section ids. Each section ID is unique.
            wiki_revision_from (Optional[datetime]): Retrieve pages modified after this date. Accepts ISO 8601 format (e.g., 2023-03-01T00:00:00) or yyyy-mm-dd format.
            wiki_revision_to (Optional[datetime]): Retrieve pages modified before this date. Accepts ISO 8601 format (e.g., 2023-03-01T00:00:00) or yyyy-mm-dd format.
            scraped_at_from (Optional[datetime]): Retrieve pages scraped after this date. Accepts ISO 8601 format (e.g., 2023-03-01T00:00:00) or yyyy-mm-dd format.
            scraped_at_to (Optional[datetime]): Retrieve pages scraped before this date. Accepts ISO 8601 format (e.g., 2023-03-01T00:00:00) or yyyy-mm-dd format.
            pageviews_from (Optional[int]): Retrieve pages with the average number of views per day higher than the provided value.
            pageviews_to (Optional[int]): Retrieve pages with the average number of views per day lower than the provided value.
            with_pageviews (Optional[bool]): Retrieve pages that have any viewership statistics available for them. If `false` (the default) - return all pages.
            show_num_results (Optional[bool]): Whether to show the total number of all matched pages. Default value is false which makes queries a bit more efficient but also counts up to 10000 pages.
            page (Optional[int]): The specific page of results to retrieve in the paginated response. Starts at 0.
            size (Optional[int]): The number of articles to return per page in the paginated response.
            sort_by (Optional[SortBy]): Determines the Wikipedia page sorting order. Options include relevance (default), revisionTsDesc (recently edited first), revisionTsAsc (recently edited last), pageViewsDesc (highest viewership first), pageViewsAsc (highest viewership last), scrapedAtDesc (recently scraped first), scrapedAtAsc (recently scraped last).

        Returns:
            WikipediaSearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_WIKIPEDIA

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if q is not None:
            params["q"] = q
        if title is not None:
            params["title"] = title
        if summary is not None:
            params["summary"] = summary
        if text is not None:
            params["text"] = text
        if reference is not None:
            params["reference"] = reference
        if id is not None:
            params["id"] = id
        if wiki_page_id is not None:
            params["wikiPageId"] = wiki_page_id
        if wiki_revision_id is not None:
            params["wikiRevisionId"] = wiki_revision_id
        if wiki_code is not None:
            params["wikiCode"] = wiki_code
        if wiki_namespace is not None:
            params["wikiNamespace"] = wiki_namespace
        if wikidata_id is not None:
            params["wikidataId"] = wikidata_id
        if wikidata_instance_of_id is not None:
            params["wikidataInstanceOfId"] = wikidata_instance_of_id
        if wikidata_instance_of_label is not None:
            params["wikidataInstanceOfLabel"] = wikidata_instance_of_label
        if category is not None:
            params["category"] = category
        if section_id is not None:
            params["sectionId"] = section_id
        if wiki_revision_from is not None:
            params["wikiRevisionFrom"] = wiki_revision_from
        if wiki_revision_to is not None:
            params["wikiRevisionTo"] = wiki_revision_to
        if scraped_at_from is not None:
            params["scrapedAtFrom"] = scraped_at_from
        if scraped_at_to is not None:
            params["scrapedAtTo"] = scraped_at_to
        if pageviews_from is not None:
            params["pageviewsFrom"] = pageviews_from
        if pageviews_to is not None:
            params["pageviewsTo"] = pageviews_to
        if with_pageviews is not None:
            params["withPageviews"] = with_pageviews
        if show_num_results is not None:
            params["showNumResults"] = show_num_results
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if sort_by is not None:
            params["sortBy"] = sort_by
        params = _normalise_query(params)

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()
        return WikipediaSearchResult.model_validate(resp.json())

    # ----------------- search_wikipedia (async) ----------------- #
    async def search_wikipedia_async(
        self,
        q: Optional[str] = None,
        title: Optional[str] = None,
        summary: Optional[str] = None,
        text: Optional[str] = None,
        reference: Optional[str] = None,
        id: Optional[List[str]] = None,
        wiki_page_id: Optional[List[int]] = None,
        wiki_revision_id: Optional[List[int]] = None,
        wiki_code: Optional[List[str]] = None,
        wiki_namespace: Optional[List[int]] = None,
        wikidata_id: Optional[List[str]] = None,
        wikidata_instance_of_id: Optional[List[str]] = None,
        wikidata_instance_of_label: Optional[List[str]] = None,
        category: Optional[List[str]] = None,
        section_id: Optional[List[str]] = None,
        wiki_revision_from: Optional[datetime] = None,
        wiki_revision_to: Optional[datetime] = None,
        scraped_at_from: Optional[datetime] = None,
        scraped_at_to: Optional[datetime] = None,
        pageviews_from: Optional[int] = None,
        pageviews_to: Optional[int] = None,
        with_pageviews: Optional[bool] = None,
        show_num_results: Optional[bool] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        sort_by: Optional[SortBy] = None,
    ) -> WikipediaSearchResult:
        """
        Async variant of search_wikipedia. Search and filter all Wikipedia pages available via the Perigon API. The result includes a list of individual pages that were matched to your specific criteria.

        Args:
            q (Optional[str]): Primary search query for filtering pages based on their title, summary, and content. Supports Boolean operators (AND, OR, NOT), exact phrases with quotes, and wildcards (* and ?) for flexible searching.
            title (Optional[str]): Search specifically within page titles. Supports Boolean operators, exact phrases with quotes, and wildcards for matching title variations.
            summary (Optional[str]): Search specifically within page summary. Supports Boolean operators, exact phrases with quotes, and wildcards for matching title variations.
            text (Optional[str]): Search specifically within the page's content (across all sections). Supports Boolean operators, exact phrases with quotes, and wildcards for matching title variations.
            reference (Optional[str]): Search specifically across page's references. Supports Boolean operators, exact phrases with quotes, and wildcards for matching title variations.
            id (Optional[List[str]]): Retrieve specific pages by their unique Perigon identifiers. Multiple IDs can be provided to return a collection of specific pages.
            wiki_page_id (Optional[List[int]]): Retrieve specific pages by their Wikipedia identifiers. These are unique only in a combination with `wikiCode` parameter. Multiple IDs can be provided to return a collection of specific pages.
            wiki_revision_id (Optional[List[int]]): Retrieve specific pages by their Wikipedia revision identifiers. These are unique only in a combination with `wikiCode` parameter. Multiple IDs can be provided to return a collection of specific pages. This ID changes each time a page is edited.
            wiki_code (Optional[List[str]]): Retrieve pages only from specified wiki projects. Currently, the only accepted value is `enwiki`.
            wiki_namespace (Optional[List[int]]): Retrieve pages only from specified wiki namespace. Currently, only the main namespace (0) is available.
            wikidata_id (Optional[List[str]]): Retrieve pages by the ids corresponding to their Wikidata entities.
            wikidata_instance_of_id (Optional[List[str]]): Retrieve all pages whose Wikidata entities are instances of these provided ids.
            wikidata_instance_of_label (Optional[List[str]]): Retrieve all pages whose Wikidata entities are instances of these ids (provided as labels).
            category (Optional[List[str]]): Retrieve all pages for specified categories.
            section_id (Optional[List[str]]): Retrieve pages containing provided section ids. Each section ID is unique.
            wiki_revision_from (Optional[datetime]): Retrieve pages modified after this date. Accepts ISO 8601 format (e.g., 2023-03-01T00:00:00) or yyyy-mm-dd format.
            wiki_revision_to (Optional[datetime]): Retrieve pages modified before this date. Accepts ISO 8601 format (e.g., 2023-03-01T00:00:00) or yyyy-mm-dd format.
            scraped_at_from (Optional[datetime]): Retrieve pages scraped after this date. Accepts ISO 8601 format (e.g., 2023-03-01T00:00:00) or yyyy-mm-dd format.
            scraped_at_to (Optional[datetime]): Retrieve pages scraped before this date. Accepts ISO 8601 format (e.g., 2023-03-01T00:00:00) or yyyy-mm-dd format.
            pageviews_from (Optional[int]): Retrieve pages with the average number of views per day higher than the provided value.
            pageviews_to (Optional[int]): Retrieve pages with the average number of views per day lower than the provided value.
            with_pageviews (Optional[bool]): Retrieve pages that have any viewership statistics available for them. If `false` (the default) - return all pages.
            show_num_results (Optional[bool]): Whether to show the total number of all matched pages. Default value is false which makes queries a bit more efficient but also counts up to 10000 pages.
            page (Optional[int]): The specific page of results to retrieve in the paginated response. Starts at 0.
            size (Optional[int]): The number of articles to return per page in the paginated response.
            sort_by (Optional[SortBy]): Determines the Wikipedia page sorting order. Options include relevance (default), revisionTsDesc (recently edited first), revisionTsAsc (recently edited last), pageViewsDesc (highest viewership first), pageViewsAsc (highest viewership last), scrapedAtDesc (recently scraped first), scrapedAtAsc (recently scraped last).

        Returns:
            WikipediaSearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_WIKIPEDIA

        params: Dict[str, Any] = {}
        if q is not None:
            params["q"] = q
        if title is not None:
            params["title"] = title
        if summary is not None:
            params["summary"] = summary
        if text is not None:
            params["text"] = text
        if reference is not None:
            params["reference"] = reference
        if id is not None:
            params["id"] = id
        if wiki_page_id is not None:
            params["wikiPageId"] = wiki_page_id
        if wiki_revision_id is not None:
            params["wikiRevisionId"] = wiki_revision_id
        if wiki_code is not None:
            params["wikiCode"] = wiki_code
        if wiki_namespace is not None:
            params["wikiNamespace"] = wiki_namespace
        if wikidata_id is not None:
            params["wikidataId"] = wikidata_id
        if wikidata_instance_of_id is not None:
            params["wikidataInstanceOfId"] = wikidata_instance_of_id
        if wikidata_instance_of_label is not None:
            params["wikidataInstanceOfLabel"] = wikidata_instance_of_label
        if category is not None:
            params["category"] = category
        if section_id is not None:
            params["sectionId"] = section_id
        if wiki_revision_from is not None:
            params["wikiRevisionFrom"] = wiki_revision_from
        if wiki_revision_to is not None:
            params["wikiRevisionTo"] = wiki_revision_to
        if scraped_at_from is not None:
            params["scrapedAtFrom"] = scraped_at_from
        if scraped_at_to is not None:
            params["scrapedAtTo"] = scraped_at_to
        if pageviews_from is not None:
            params["pageviewsFrom"] = pageviews_from
        if pageviews_to is not None:
            params["pageviewsTo"] = pageviews_to
        if with_pageviews is not None:
            params["withPageviews"] = with_pageviews
        if show_num_results is not None:
            params["showNumResults"] = show_num_results
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if sort_by is not None:
            params["sortBy"] = sort_by
        params = _normalise_query(params)

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()
        return WikipediaSearchResult.model_validate(resp.json())

    # ----------------- vector_search_articles (sync) ----------------- #
    def vector_search_articles(
        self, article_search_params: ArticleSearchParams
    ) -> ArticlesVectorSearchResult:
        """
        Perform a natural language search over news articles from the past 6 months using semantic relevance. The result includes a list of articles most closely matched to your query intent.

        Args:
            article_search_params (ArticleSearchParams): Parameter article_search_params (required)

        Returns:
            ArticlesVectorSearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_VECTOR_SEARCH_ARTICLES

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = self.api_client.request(
            "POST",
            path,
            params=params,
            json=article_search_params.model_dump(by_alias=True),
        )
        resp.raise_for_status()
        return ArticlesVectorSearchResult.model_validate(resp.json())

    # ----------------- vector_search_articles (async) ----------------- #
    async def vector_search_articles_async(
        self, article_search_params: ArticleSearchParams
    ) -> ArticlesVectorSearchResult:
        """
        Async variant of vector_search_articles. Perform a natural language search over news articles from the past 6 months using semantic relevance. The result includes a list of articles most closely matched to your query intent.

        Args:
            article_search_params (ArticleSearchParams): Parameter article_search_params (required)

        Returns:
            ArticlesVectorSearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_VECTOR_SEARCH_ARTICLES

        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = await self.api_client.request_async(
            "POST",
            path,
            params=params,
            json=article_search_params.model_dump(by_alias=True),
        )
        resp.raise_for_status()
        return ArticlesVectorSearchResult.model_validate(resp.json())

    # ----------------- vector_search_wikipedia (sync) ----------------- #
    def vector_search_wikipedia(
        self, wikipedia_search_params: WikipediaSearchParams
    ) -> WikipediaVectorSearchResult:
        """
        Perform a natural language search over Wikipedia pages using semantic relevance. The result includes a list of page sections most closely matched to your query intent.

        Args:
            wikipedia_search_params (WikipediaSearchParams): Parameter wikipedia_search_params (required)

        Returns:
            WikipediaVectorSearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_VECTOR_SEARCH_WIKIPEDIA

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = self.api_client.request(
            "POST",
            path,
            params=params,
            json=wikipedia_search_params.model_dump(by_alias=True),
        )
        resp.raise_for_status()
        return WikipediaVectorSearchResult.model_validate(resp.json())

    # ----------------- vector_search_wikipedia (async) ----------------- #
    async def vector_search_wikipedia_async(
        self, wikipedia_search_params: WikipediaSearchParams
    ) -> WikipediaVectorSearchResult:
        """
        Async variant of vector_search_wikipedia. Perform a natural language search over Wikipedia pages using semantic relevance. The result includes a list of page sections most closely matched to your query intent.

        Args:
            wikipedia_search_params (WikipediaSearchParams): Parameter wikipedia_search_params (required)

        Returns:
            WikipediaVectorSearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_VECTOR_SEARCH_WIKIPEDIA

        params: Dict[str, Any] = {}
        params = _normalise_query(params)

        resp = await self.api_client.request_async(
            "POST",
            path,
            params=params,
            json=wikipedia_search_params.model_dump(by_alias=True),
        )
        resp.raise_for_status()
        return WikipediaVectorSearchResult.model_validate(resp.json())

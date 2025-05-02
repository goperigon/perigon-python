from datetime import datetime
from enum import Enum
from typing import Any, Dict, Iterable, List, Mapping, Optional, Union

from pydantic import Field, StrictBool, StrictFloat, StrictInt, StrictStr
from typing_extensions import Annotated

from perigon.api_client import ApiClient
from perigon.models.all_endpoint_sort_by import AllEndpointSortBy
from perigon.models.article_search_params import ArticleSearchParams
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
from perigon.models.vector_search_result import VectorSearchResult

# Define API paths
PATH_GET_JOURNALIST_BY_ID = "/v1/journalists/{id}"
PATH_SEARCH_ARTICLES = "/v1/all"
PATH_SEARCH_COMPANIES = "/v1/companies/all"
PATH_SEARCH_JOURNALISTS1 = "/v1/journalists/all"
PATH_SEARCH_PEOPLE = "/v1/people/all"
PATH_SEARCH_SOURCES = "/v1/sources/all"
PATH_SEARCH_STORIES = "/v1/stories/all"
PATH_SEARCH_SUMMARIZER = "/v1/summarize"
PATH_SEARCH_TOPICS = "/v1/topics/all"
PATH_VECTOR_SEARCH_ARTICLES = "/v1/vector/news/all"


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
    ) -> QuerySearchResult:
        """
        Search and filter all news articles available via the Perigon API. The result includes a list of individual articles that were matched to your specific criteria.

        Args:
            q (Optional[str]): Search query, each article will be scored and ranked against it. Articles are searched on the title, description, and content fields.
            title (Optional[str]): Search article headlines/title field. Semantic similar to q parameter.
            desc (Optional[str]): Search query on the description field. Semantic similar to q parameter.
            content (Optional[str]): Search query on the article's body of content field. Semantic similar to q parameter.
            url (Optional[str]): Search query on the url field. Semantic similar to q parameter. E.g. could be used for querying certain website sections, e.g. source=cnn.com&url=travel.
            article_id (Optional[List[str]]): Article ID will search for a news article by the ID of the article. If several parameters are passed, all matched articles will be returned.
            cluster_id (Optional[List[str]]): Search for related content using a cluster ID. Passing a cluster ID will filter results to only the content found within the cluster.
            sort_by (Optional[AllEndpointSortBy]): 'relevance' to sort by relevance to the query, 'date' to sort by the publication date (desc), 'pubDate' is a synonym to 'date', 'addDate' to sort by 'addDate' field (desc), 'refreshDate' to sort by 'refreshDate' field (desc). Defaults to 'relevance'
            page (Optional[int]): The page number to retrieve.
            size (Optional[int]): The number of items per page.
            var_from (Optional[datetime]): 'from' filter, will search articles published after the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2023-03-01T00:00:00
            to (Optional[datetime]): 'to' filter, will search articles published before the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T23:59:59
            add_date_from (Optional[datetime]): 'addDateFrom' filter, will search articles added after the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T00:00:00
            add_date_to (Optional[datetime]): 'addDateTo' filter, will search articles added before the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T23:59:59
            refresh_date_from (Optional[datetime]): Will search articles that were refreshed after the specified date. The date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T00:00:00
            refresh_date_to (Optional[datetime]): Will search articles that were refreshed before the specified date. The date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T23:59:59
            medium (Optional[List[str]]): Medium will filter out news articles medium, which could be 'Video' or 'Article'. If several parameters are passed, all matched articles will be returned.
            source (Optional[List[str]]): Publisher's domain can include a subdomain. If multiple parameters are passed, they will be applied as OR operations. Wildcards (* and ?) are suported (e.g. *.cnn.com).
            source_group (Optional[List[str]]): One of the supported source groups. Find Source Groups in the guided part of our documentation...
            exclude_source_group (Optional[List[str]]): A list of built-in source group names to exclude from the results. The Perigon API categorizes sources into groups (for example, “top10” or “top100”) based on type or popularity. Using this filter allows you to remove articles coming from any source that belongs to one or more of the specified groups.
            exclude_source (Optional[List[str]]): The domain of the website, which should be excluded from the search. Multiple parameters could be provided. Wildcards (* and ?) are suported (e.g. *.cnn.com).
            paywall (Optional[bool]): Filter to show only results where the source has a paywall (true) or does not have a paywall (false).
            byline (Optional[List[str]]): Author names to filter by. Article author bylines are used as a source field. If multiple parameters are passed, they will be applied as OR operations.
            author (Optional[List[str]]): A list of author names to include. Only articles written by any of the specified authors are returned. This is ideal when you wish to focus on content from particular voices or experts.
            exclude_author (Optional[List[str]]):  A list of author names to exclude from the search results. Any article written by an author whose name matches one in this list will be omitted, which helps to avoid content from certain individuals.
            journalist_id (Optional[List[str]]): Filter by journalist ID. Journalist IDs are unique journalist identifiers which can be found through the Journalist API, or in the matchedAuthors field.
            exclude_journalist_id (Optional[List[str]]): A list of journalist (or reporter) identifiers to exclude. If an article is written by a journalist whose ID matches any in this list, it will not be part of the result set.
            language (Optional[List[str]]): Language code to filter by language. If multiple parameters are passed, they will be applied as OR operations.
            exclude_language (Optional[List[str]]):  A list of languages to be excluded. Any article published in one of the languages provided in this filter will not be returned. This is useful when you are interested only in news published in specific languages.
            search_translation (Optional[bool]): Expand a query to search the translation, translatedTitle, and translatedDescription fields for non-English articles.
            label (Optional[List[str]]): Labels to filter by, could be 'Opinion', 'Paid-news', 'Non-news', etc. If multiple parameters are passed, they will be applied as OR operations.
            exclude_label (Optional[List[str]]): Exclude results that include specific labels (Opinion, Non-news, Paid News, etc.). You can filter multiple by repeating the parameter.
            category (Optional[List[str]]): Filter by categories. Categories are general themes that the article is about. Examples of categories: Tech, Politics, etc. If multiple parameters are passed, they will be applied as OR operations. Use 'none' to search uncategorized articles.
            exclude_category (Optional[List[str]]): A list of article categories to be omitted. If an article is tagged with any category present in this list (such as “Polotics”, “Tech”, “Sports”, etc.), it will not appear in the search results.
            topic (Optional[List[str]]): Filters results to include only articles with the specified topics. Topics are more specific classifications than categories, with an article potentially having multiple topics assigned. Perigon uses both human and machine curation to maintain an evolving list of available topics. Common examples include 'Markets', 'Crime', 'Cryptocurrency', 'Social Issues', 'College Sports', etc. See the Topics page in Docs for a complete list of available topics.
            exclude_topic (Optional[List[str]]): Filter by excluding topics. Each topic is some kind of entity that the article is about. Examples of topics: Markets, Joe Biden, Green Energy, Climate Change, Cryptocurrency, etc. If multiple parameters are passed, they will be applied as OR operations.
            link_to (Optional[str]): Returns only articles that point to specified links (as determined by the 'links' field in the article response).
            show_reprints (Optional[bool]): Whether to return reprints in the response or not. Reprints are usually wired articles from sources like AP or Reuters that are reprinted in multiple sources at the same time. By default, this parameter is 'true'.
            reprint_group_id (Optional[str]): Shows all articles belonging to the same reprint group. A reprint group includes one original article (the first one processed by the API) and all its known reprints.
            city (Optional[List[str]]): Filters articles where a specified city plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the urban area in question. If multiple parameters are passed, they will be applied as OR operations.
            exclude_city (Optional[List[str]]): A list of cities to exclude from the results. Articles that are associated with any of the specified cities will be filtered out.
            area (Optional[List[str]]): Filters articles where a specified area, such as a neighborhood, borough, or district, plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the area in question. If multiple parameters are passed, they will be applied as OR operations.
            state (Optional[List[str]]): Filters articles where a specified state plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the state in question. If multiple parameters are passed, they will be applied as OR operations.
            exclude_state (Optional[List[str]]): A list of states to exclude. Articles that include, or are associated with, any of the states provided here will be filtered out. This is especially useful if you want to ignore news tied to certain geographical areas (e.g., US states).
            county (Optional[List[str]]): A list of counties to include (or specify) in the search results. This field filters the returned articles based on the county associated with the event or news. Only articles tagged with one of these counties will be included.
            exclude_county (Optional[List[str]]): Excludes articles from specific counties or administrative divisions in the vector search results. Accepts either a single county name or a list of county names. County names should match the format used in article metadata (e.g., 'Los Angeles County', 'Cook County'). This parameter allows for more granular geographic filter
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
            person_wikidata_id (Optional[List[str]]): List of person Wikidata IDs for filtering.
            exclude_person_wikidata_id (Optional[List[str]]): A list of Wikidata identifiers for individuals. Articles mentioning persons with any of these Wikidata IDs will be filtered out. This is particularly helpful when using a unique identifier to prevent ambiguity in names.
            person_name (Optional[List[str]]): List of person names for exact matches. Boolean and complex logic is not supported on this paramter.
            exclude_person_name (Optional[List[str]]): A list of person names that, when associated with the content, cause the article to be excluded. This filter removes articles related to any individuals whose names match those on the list.
            company_id (Optional[List[str]]): List of company IDs to filter by.
            exclude_company_id (Optional[List[str]]): A list of company identifiers. Articles associated with companies that have any of these unique IDs will be filtered out from the returned results, ensuring that certain companies or corporate entities are not included.
            company_name (Optional[str]): Search by company name.
            company_domain (Optional[List[str]]): Search by company domains for filtering. E.g. companyDomain=apple.com.
            exclude_company_domain (Optional[List[str]]): A list of company domains to exclude. If an article is related to a company that uses one of the specified domains (for instance, “example.com”), it will not be returned in the results.
            company_symbol (Optional[List[str]]): Search by company symbols.
            exclude_company_symbol (Optional[List[str]]): A list of stock symbols (ticker symbols) that identify companies to be excluded. Articles related to companies using any of these symbols will be omitted, which is useful for targeting or avoiding specific public companies.
            show_num_results (Optional[bool]): Whether to show the total number of all matched articles. Default value is false which makes queries a bit more efficient but also counts up to 10000 articles.
            positive_sentiment_from (Optional[float]): Filters results with a sentiment score greater than or equal to the specified value, indicating positive sentiment. See the Article Data section in Docs for an explanation of scores.
            positive_sentiment_to (Optional[float]): Filters results with a sentiment score less than or equal to the specified value, indicating positive sentiment. See the Article Data section in Docs for an explanation of scores.
            neutral_sentiment_from (Optional[float]): Filters results with a sentiment score greater than or equal to the specified value, indicating neutral sentiment. Explanation of sentimental values can be found in Docs under the Article Data section.
            neutral_sentiment_to (Optional[float]): Filters results with a sentiment score less than or equal to the specified value, indicating neutral sentiment. See the Article Data section in Docs for an explanation of scores.
            negative_sentiment_from (Optional[float]): Filters results with a sentiment score greater than or equal to the specified value, indicating negative sentiment. See the Article Data section in Docs for an explanation of scores.
            negative_sentiment_to (Optional[float]): Filters results with a sentiment score less than or equal to the specified value, indicating negative sentiment. See the Article Data section in Docs for an explanation of scores.
            taxonomy (Optional[List[str]]): Filters by Google Content Categories. This field will accept 1 or more categories, must pass the full name of the category. Example: taxonomy=/Finance/Banking/Other, /Finance/Investing/Funds
            prefix_taxonomy (Optional[str]): Filters by Google Content Categories. This field will filter by the category prefix only. Example: prefixTaxonomy=/Finance

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
    ) -> QuerySearchResult:
        """
        Async variant of search_articles. Search and filter all news articles available via the Perigon API. The result includes a list of individual articles that were matched to your specific criteria.

        Args:
            q (Optional[str]): Search query, each article will be scored and ranked against it. Articles are searched on the title, description, and content fields.
            title (Optional[str]): Search article headlines/title field. Semantic similar to q parameter.
            desc (Optional[str]): Search query on the description field. Semantic similar to q parameter.
            content (Optional[str]): Search query on the article's body of content field. Semantic similar to q parameter.
            url (Optional[str]): Search query on the url field. Semantic similar to q parameter. E.g. could be used for querying certain website sections, e.g. source=cnn.com&url=travel.
            article_id (Optional[List[str]]): Article ID will search for a news article by the ID of the article. If several parameters are passed, all matched articles will be returned.
            cluster_id (Optional[List[str]]): Search for related content using a cluster ID. Passing a cluster ID will filter results to only the content found within the cluster.
            sort_by (Optional[AllEndpointSortBy]): 'relevance' to sort by relevance to the query, 'date' to sort by the publication date (desc), 'pubDate' is a synonym to 'date', 'addDate' to sort by 'addDate' field (desc), 'refreshDate' to sort by 'refreshDate' field (desc). Defaults to 'relevance'
            page (Optional[int]): The page number to retrieve.
            size (Optional[int]): The number of items per page.
            var_from (Optional[datetime]): 'from' filter, will search articles published after the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2023-03-01T00:00:00
            to (Optional[datetime]): 'to' filter, will search articles published before the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T23:59:59
            add_date_from (Optional[datetime]): 'addDateFrom' filter, will search articles added after the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T00:00:00
            add_date_to (Optional[datetime]): 'addDateTo' filter, will search articles added before the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T23:59:59
            refresh_date_from (Optional[datetime]): Will search articles that were refreshed after the specified date. The date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T00:00:00
            refresh_date_to (Optional[datetime]): Will search articles that were refreshed before the specified date. The date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T23:59:59
            medium (Optional[List[str]]): Medium will filter out news articles medium, which could be 'Video' or 'Article'. If several parameters are passed, all matched articles will be returned.
            source (Optional[List[str]]): Publisher's domain can include a subdomain. If multiple parameters are passed, they will be applied as OR operations. Wildcards (* and ?) are suported (e.g. *.cnn.com).
            source_group (Optional[List[str]]): One of the supported source groups. Find Source Groups in the guided part of our documentation...
            exclude_source_group (Optional[List[str]]): A list of built-in source group names to exclude from the results. The Perigon API categorizes sources into groups (for example, “top10” or “top100”) based on type or popularity. Using this filter allows you to remove articles coming from any source that belongs to one or more of the specified groups.
            exclude_source (Optional[List[str]]): The domain of the website, which should be excluded from the search. Multiple parameters could be provided. Wildcards (* and ?) are suported (e.g. *.cnn.com).
            paywall (Optional[bool]): Filter to show only results where the source has a paywall (true) or does not have a paywall (false).
            byline (Optional[List[str]]): Author names to filter by. Article author bylines are used as a source field. If multiple parameters are passed, they will be applied as OR operations.
            author (Optional[List[str]]): A list of author names to include. Only articles written by any of the specified authors are returned. This is ideal when you wish to focus on content from particular voices or experts.
            exclude_author (Optional[List[str]]):  A list of author names to exclude from the search results. Any article written by an author whose name matches one in this list will be omitted, which helps to avoid content from certain individuals.
            journalist_id (Optional[List[str]]): Filter by journalist ID. Journalist IDs are unique journalist identifiers which can be found through the Journalist API, or in the matchedAuthors field.
            exclude_journalist_id (Optional[List[str]]): A list of journalist (or reporter) identifiers to exclude. If an article is written by a journalist whose ID matches any in this list, it will not be part of the result set.
            language (Optional[List[str]]): Language code to filter by language. If multiple parameters are passed, they will be applied as OR operations.
            exclude_language (Optional[List[str]]):  A list of languages to be excluded. Any article published in one of the languages provided in this filter will not be returned. This is useful when you are interested only in news published in specific languages.
            search_translation (Optional[bool]): Expand a query to search the translation, translatedTitle, and translatedDescription fields for non-English articles.
            label (Optional[List[str]]): Labels to filter by, could be 'Opinion', 'Paid-news', 'Non-news', etc. If multiple parameters are passed, they will be applied as OR operations.
            exclude_label (Optional[List[str]]): Exclude results that include specific labels (Opinion, Non-news, Paid News, etc.). You can filter multiple by repeating the parameter.
            category (Optional[List[str]]): Filter by categories. Categories are general themes that the article is about. Examples of categories: Tech, Politics, etc. If multiple parameters are passed, they will be applied as OR operations. Use 'none' to search uncategorized articles.
            exclude_category (Optional[List[str]]): A list of article categories to be omitted. If an article is tagged with any category present in this list (such as “Polotics”, “Tech”, “Sports”, etc.), it will not appear in the search results.
            topic (Optional[List[str]]): Filters results to include only articles with the specified topics. Topics are more specific classifications than categories, with an article potentially having multiple topics assigned. Perigon uses both human and machine curation to maintain an evolving list of available topics. Common examples include 'Markets', 'Crime', 'Cryptocurrency', 'Social Issues', 'College Sports', etc. See the Topics page in Docs for a complete list of available topics.
            exclude_topic (Optional[List[str]]): Filter by excluding topics. Each topic is some kind of entity that the article is about. Examples of topics: Markets, Joe Biden, Green Energy, Climate Change, Cryptocurrency, etc. If multiple parameters are passed, they will be applied as OR operations.
            link_to (Optional[str]): Returns only articles that point to specified links (as determined by the 'links' field in the article response).
            show_reprints (Optional[bool]): Whether to return reprints in the response or not. Reprints are usually wired articles from sources like AP or Reuters that are reprinted in multiple sources at the same time. By default, this parameter is 'true'.
            reprint_group_id (Optional[str]): Shows all articles belonging to the same reprint group. A reprint group includes one original article (the first one processed by the API) and all its known reprints.
            city (Optional[List[str]]): Filters articles where a specified city plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the urban area in question. If multiple parameters are passed, they will be applied as OR operations.
            exclude_city (Optional[List[str]]): A list of cities to exclude from the results. Articles that are associated with any of the specified cities will be filtered out.
            area (Optional[List[str]]): Filters articles where a specified area, such as a neighborhood, borough, or district, plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the area in question. If multiple parameters are passed, they will be applied as OR operations.
            state (Optional[List[str]]): Filters articles where a specified state plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the state in question. If multiple parameters are passed, they will be applied as OR operations.
            exclude_state (Optional[List[str]]): A list of states to exclude. Articles that include, or are associated with, any of the states provided here will be filtered out. This is especially useful if you want to ignore news tied to certain geographical areas (e.g., US states).
            county (Optional[List[str]]): A list of counties to include (or specify) in the search results. This field filters the returned articles based on the county associated with the event or news. Only articles tagged with one of these counties will be included.
            exclude_county (Optional[List[str]]): Excludes articles from specific counties or administrative divisions in the vector search results. Accepts either a single county name or a list of county names. County names should match the format used in article metadata (e.g., 'Los Angeles County', 'Cook County'). This parameter allows for more granular geographic filter
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
            person_wikidata_id (Optional[List[str]]): List of person Wikidata IDs for filtering.
            exclude_person_wikidata_id (Optional[List[str]]): A list of Wikidata identifiers for individuals. Articles mentioning persons with any of these Wikidata IDs will be filtered out. This is particularly helpful when using a unique identifier to prevent ambiguity in names.
            person_name (Optional[List[str]]): List of person names for exact matches. Boolean and complex logic is not supported on this paramter.
            exclude_person_name (Optional[List[str]]): A list of person names that, when associated with the content, cause the article to be excluded. This filter removes articles related to any individuals whose names match those on the list.
            company_id (Optional[List[str]]): List of company IDs to filter by.
            exclude_company_id (Optional[List[str]]): A list of company identifiers. Articles associated with companies that have any of these unique IDs will be filtered out from the returned results, ensuring that certain companies or corporate entities are not included.
            company_name (Optional[str]): Search by company name.
            company_domain (Optional[List[str]]): Search by company domains for filtering. E.g. companyDomain=apple.com.
            exclude_company_domain (Optional[List[str]]): A list of company domains to exclude. If an article is related to a company that uses one of the specified domains (for instance, “example.com”), it will not be returned in the results.
            company_symbol (Optional[List[str]]): Search by company symbols.
            exclude_company_symbol (Optional[List[str]]): A list of stock symbols (ticker symbols) that identify companies to be excluded. Articles related to companies using any of these symbols will be omitted, which is useful for targeting or avoiding specific public companies.
            show_num_results (Optional[bool]): Whether to show the total number of all matched articles. Default value is false which makes queries a bit more efficient but also counts up to 10000 articles.
            positive_sentiment_from (Optional[float]): Filters results with a sentiment score greater than or equal to the specified value, indicating positive sentiment. See the Article Data section in Docs for an explanation of scores.
            positive_sentiment_to (Optional[float]): Filters results with a sentiment score less than or equal to the specified value, indicating positive sentiment. See the Article Data section in Docs for an explanation of scores.
            neutral_sentiment_from (Optional[float]): Filters results with a sentiment score greater than or equal to the specified value, indicating neutral sentiment. Explanation of sentimental values can be found in Docs under the Article Data section.
            neutral_sentiment_to (Optional[float]): Filters results with a sentiment score less than or equal to the specified value, indicating neutral sentiment. See the Article Data section in Docs for an explanation of scores.
            negative_sentiment_from (Optional[float]): Filters results with a sentiment score greater than or equal to the specified value, indicating negative sentiment. See the Article Data section in Docs for an explanation of scores.
            negative_sentiment_to (Optional[float]): Filters results with a sentiment score less than or equal to the specified value, indicating negative sentiment. See the Article Data section in Docs for an explanation of scores.
            taxonomy (Optional[List[str]]): Filters by Google Content Categories. This field will accept 1 or more categories, must pass the full name of the category. Example: taxonomy=/Finance/Banking/Other, /Finance/Investing/Funds
            prefix_taxonomy (Optional[str]): Filters by Google Content Categories. This field will filter by the category prefix only. Example: prefixTaxonomy=/Finance

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
            id (Optional[List[str]]): Search by company id.
            symbol (Optional[List[str]]): Search by ticker symbol.
            domain (Optional[List[str]]): Search by company domain.
            country (Optional[List[str]]): Search by company country.
            exchange (Optional[List[str]]): Search by exchange name.
            num_employees_from (Optional[int]): Minimum number of employees.
            num_employees_to (Optional[int]): Maximum number of employees.
            ipo_from (Optional[datetime]): Starting IPO date.
            ipo_to (Optional[datetime]): Ending IPO date.
            q (Optional[str]): Search companies over 'name', 'altNames', 'domains' and 'symbols.symbol' fields. Boolean operators and logic are supported.
            name (Optional[str]): Search by company name. Boolean operators and logic are supported.
            industry (Optional[str]): Search by industry. Boolean operators and logic are supported.
            sector (Optional[str]): Search by sector. Boolean operators and logic are supported.
            size (Optional[int]): The number of items per page.
            page (Optional[int]): The page number to retrieve.

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
            id (Optional[List[str]]): Search by company id.
            symbol (Optional[List[str]]): Search by ticker symbol.
            domain (Optional[List[str]]): Search by company domain.
            country (Optional[List[str]]): Search by company country.
            exchange (Optional[List[str]]): Search by exchange name.
            num_employees_from (Optional[int]): Minimum number of employees.
            num_employees_to (Optional[int]): Maximum number of employees.
            ipo_from (Optional[datetime]): Starting IPO date.
            ipo_to (Optional[datetime]): Ending IPO date.
            q (Optional[str]): Search companies over 'name', 'altNames', 'domains' and 'symbols.symbol' fields. Boolean operators and logic are supported.
            name (Optional[str]): Search by company name. Boolean operators and logic are supported.
            industry (Optional[str]): Search by industry. Boolean operators and logic are supported.
            sector (Optional[str]): Search by sector. Boolean operators and logic are supported.
            size (Optional[int]): The number of items per page.
            page (Optional[int]): The page number to retrieve.

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

    # ----------------- search_journalists1 (sync) ----------------- #
    def search_journalists1(
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
            id (Optional[List[str]]): Filter by journalist ID. Journalist IDs are unique journalist identifiers which can be found through the Journalist API, or in the matchedAuthors field.
            q (Optional[str]): Searches through name, title, twitterBio fields with priority given to the name, then to the title, then to the twitter bio. Returns results sorted by relevance.
            name (Optional[str]): Searches through journalist names, scores and ranks them, returns results sorted by relevance.
            twitter (Optional[str]): Searches for journalists by (exact match) twitter handle.
            size (Optional[int]): The number of items per page.
            page (Optional[int]): The page number to retrieve.
            source (Optional[List[str]]): Search for journalist by the publisher's domain can include a subdomain. If multiple parameters are passed, they will be applied as OR operations. Wildcards (* and ?) are suported (e.g. *.cnn.com).
            topic (Optional[List[str]]): Searches for journalists by topic.
            category (Optional[List[str]]): Filter by categories. Categories are general themes that the article is about. Examples of categories: Tech, Politics, etc. If multiple parameters are passed, they will be applied as OR operations.
            label (Optional[List[str]]): Filter journalists by label. For example, searching 'Opinion' will return the journalists where 'Opinion'-type articles is one of the top labels for the articles they publish.
            min_monthly_posts (Optional[int]): Returns the journalists with the minimum indicated number of average monthly posts.
            max_monthly_posts (Optional[int]): Returns the journalist with the maximum indicated number of average monthly posts.
            country (Optional[List[str]]): Country code to filter by country. If multiple parameters are passed, they will be applied as OR operations.
            updated_at_from (Optional[datetime]): Starting date when the record was last updated.
            updated_at_to (Optional[datetime]): Ending date when the record was last updated.
            show_num_results (Optional[bool]): If 'true', shows accurate number of results matched by the query. By default, the counter is accurate only up to 10,000 results due performance reasons.

        Returns:
            JournalistSearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_JOURNALISTS1

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

    # ----------------- search_journalists1 (async) ----------------- #
    async def search_journalists1_async(
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
        Async variant of search_journalists1. Search journalists using broad search attributes. Our database contains over 230,000 journalists from around the world and is refreshed frequently.

        Args:
            id (Optional[List[str]]): Filter by journalist ID. Journalist IDs are unique journalist identifiers which can be found through the Journalist API, or in the matchedAuthors field.
            q (Optional[str]): Searches through name, title, twitterBio fields with priority given to the name, then to the title, then to the twitter bio. Returns results sorted by relevance.
            name (Optional[str]): Searches through journalist names, scores and ranks them, returns results sorted by relevance.
            twitter (Optional[str]): Searches for journalists by (exact match) twitter handle.
            size (Optional[int]): The number of items per page.
            page (Optional[int]): The page number to retrieve.
            source (Optional[List[str]]): Search for journalist by the publisher's domain can include a subdomain. If multiple parameters are passed, they will be applied as OR operations. Wildcards (* and ?) are suported (e.g. *.cnn.com).
            topic (Optional[List[str]]): Searches for journalists by topic.
            category (Optional[List[str]]): Filter by categories. Categories are general themes that the article is about. Examples of categories: Tech, Politics, etc. If multiple parameters are passed, they will be applied as OR operations.
            label (Optional[List[str]]): Filter journalists by label. For example, searching 'Opinion' will return the journalists where 'Opinion'-type articles is one of the top labels for the articles they publish.
            min_monthly_posts (Optional[int]): Returns the journalists with the minimum indicated number of average monthly posts.
            max_monthly_posts (Optional[int]): Returns the journalist with the maximum indicated number of average monthly posts.
            country (Optional[List[str]]): Country code to filter by country. If multiple parameters are passed, they will be applied as OR operations.
            updated_at_from (Optional[datetime]): Starting date when the record was last updated.
            updated_at_to (Optional[datetime]): Ending date when the record was last updated.
            show_num_results (Optional[bool]): If 'true', shows accurate number of results matched by the query. By default, the counter is accurate only up to 10,000 results due performance reasons.

        Returns:
            JournalistSearchResult: The response
        """
        # Get path template from class attribute
        path = PATH_SEARCH_JOURNALISTS1

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
            name (Optional[str]): Search by name of the person. Supports exact matching with quotes (\"\") and Boolean operators (AND, OR, NOT).
            wikidata_id (Optional[List[str]]): Filter by Wikidata entity ID(s). Use this to find specific people by their Wikidata identifiers.
            occupation_id (Optional[List[str]]): Filter by Wikidata occupation ID(s). Use this to find people with specific occupations.
            occupation_label (Optional[str]): Search by occupation name. Supports exact matching with quotes (\"\") and Boolean operators (AND, OR, NOT).
            page (Optional[int]): The page number to retrieve.
            size (Optional[int]): The number of items per page.

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
            name (Optional[str]): Search by name of the person. Supports exact matching with quotes (\"\") and Boolean operators (AND, OR, NOT).
            wikidata_id (Optional[List[str]]): Filter by Wikidata entity ID(s). Use this to find specific people by their Wikidata identifiers.
            occupation_id (Optional[List[str]]): Filter by Wikidata occupation ID(s). Use this to find people with specific occupations.
            occupation_label (Optional[str]): Search by occupation name. Supports exact matching with quotes (\"\") and Boolean operators (AND, OR, NOT).
            page (Optional[int]): The page number to retrieve.
            size (Optional[int]): The number of items per page.

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
            domain (Optional[List[str]]): Domain name for the media source to lookup. This parameter supports wildcard queries, ie. \"*.cnn.com\" will match all subdomains for cnn.com.
            name (Optional[str]): Search by name of source. This parameter supports complex boolean search operators, and also searches the altNames field for alternative names of the source.
            source_group (Optional[str]): Find all sources within a sourceGroup. Find Source Groups in the guided part of our documentation...
            sort_by (Optional[SortBy]): Use 'relevance' to sort by relevance to the query, 'globalRank' for top ranked sources based on popularity, 'monthlyVisits' for sources with the largest audience, 'avgMonthlyPosts' for sources with the highest publishing frequency. Defaults to 'relevance'.
            page (Optional[int]): The page number to retrieve.
            size (Optional[int]): The number of items per page.
            min_monthly_visits (Optional[int]): Filter by popularity. Enter a minimum number of monthly visits that the source must have in order to match your query.
            max_monthly_visits (Optional[int]): Enter a maximum number of monthly visits that the source must have in order to match your query.
            min_monthly_posts (Optional[int]): Returns the sources that have at least this number of average monthly posts.
            max_monthly_posts (Optional[int]): Returns the sources that have at most this number of average monthly posts.
            country (Optional[List[str]]): Country code to filter sources by the countries in which they most commonly cover. If multiple parameters are passed, they will be applied as OR operations.
            source_country (Optional[List[str]]): Find all local publications that are located within a given country.
            source_state (Optional[List[str]]): Find all local publications that are located within a given state.
            source_county (Optional[List[str]]): Find all local publications that are located within a given county.
            source_city (Optional[List[str]]): Find all local publications that are located within a given city.
            source_lat (Optional[float]): Latitude of the center point to search local publications.
            source_lon (Optional[float]): Longitude of the center point to search local publications.
            source_max_distance (Optional[float]): Maximum distance from starting point to search local publications.
            category (Optional[List[str]]): Filter by categories. Categories are general themes that the article is about. Examples of categories: Tech, Politics, etc. If multiple parameters are passed, they will be applied as OR operations.
            topic (Optional[List[str]]): Find sources by topic. For example, searching 'Markets' will return the sources where 'Markets' is one of the top 10 topics that they cover.
            label (Optional[List[str]]): Filter sources by label. For example, searching 'Opinion' will return the sources where 'Opinion'-type articles is one of the top labels for the articles they publish.
            paywall (Optional[bool]): Use 'true' to find only sources known to have a paywall, or use 'false' to filter for only sources that do not have a paywall.
            show_subdomains (Optional[bool]): Controls whether subdomains are included in the response. When set to true (default), all relevant subdomains of media sources will be returned as separate results. Set to false to consolidate results to parent domains only.
            show_num_results (Optional[bool]): If 'true', shows accurate number of results matched by the query. By default, the counter is accurate only up to 10,000 results due performance reasons.

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
            domain (Optional[List[str]]): Domain name for the media source to lookup. This parameter supports wildcard queries, ie. \"*.cnn.com\" will match all subdomains for cnn.com.
            name (Optional[str]): Search by name of source. This parameter supports complex boolean search operators, and also searches the altNames field for alternative names of the source.
            source_group (Optional[str]): Find all sources within a sourceGroup. Find Source Groups in the guided part of our documentation...
            sort_by (Optional[SortBy]): Use 'relevance' to sort by relevance to the query, 'globalRank' for top ranked sources based on popularity, 'monthlyVisits' for sources with the largest audience, 'avgMonthlyPosts' for sources with the highest publishing frequency. Defaults to 'relevance'.
            page (Optional[int]): The page number to retrieve.
            size (Optional[int]): The number of items per page.
            min_monthly_visits (Optional[int]): Filter by popularity. Enter a minimum number of monthly visits that the source must have in order to match your query.
            max_monthly_visits (Optional[int]): Enter a maximum number of monthly visits that the source must have in order to match your query.
            min_monthly_posts (Optional[int]): Returns the sources that have at least this number of average monthly posts.
            max_monthly_posts (Optional[int]): Returns the sources that have at most this number of average monthly posts.
            country (Optional[List[str]]): Country code to filter sources by the countries in which they most commonly cover. If multiple parameters are passed, they will be applied as OR operations.
            source_country (Optional[List[str]]): Find all local publications that are located within a given country.
            source_state (Optional[List[str]]): Find all local publications that are located within a given state.
            source_county (Optional[List[str]]): Find all local publications that are located within a given county.
            source_city (Optional[List[str]]): Find all local publications that are located within a given city.
            source_lat (Optional[float]): Latitude of the center point to search local publications.
            source_lon (Optional[float]): Longitude of the center point to search local publications.
            source_max_distance (Optional[float]): Maximum distance from starting point to search local publications.
            category (Optional[List[str]]): Filter by categories. Categories are general themes that the article is about. Examples of categories: Tech, Politics, etc. If multiple parameters are passed, they will be applied as OR operations.
            topic (Optional[List[str]]): Find sources by topic. For example, searching 'Markets' will return the sources where 'Markets' is one of the top 10 topics that they cover.
            label (Optional[List[str]]): Filter sources by label. For example, searching 'Opinion' will return the sources where 'Opinion'-type articles is one of the top labels for the articles they publish.
            paywall (Optional[bool]): Use 'true' to find only sources known to have a paywall, or use 'false' to filter for only sources that do not have a paywall.
            show_subdomains (Optional[bool]): Controls whether subdomains are included in the response. When set to true (default), all relevant subdomains of media sources will be returned as separate results. Set to false to consolidate results to parent domains only.
            show_num_results (Optional[bool]): If 'true', shows accurate number of results matched by the query. By default, the counter is accurate only up to 10,000 results due performance reasons.

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
        sort_by: Optional[SortBy] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        var_from: Optional[datetime] = None,
        to: Optional[datetime] = None,
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
        initialized_from: Optional[datetime] = None,
        initialized_to: Optional[datetime] = None,
        updated_from: Optional[datetime] = None,
        updated_to: Optional[datetime] = None,
        show_story_page_info: Optional[bool] = None,
        show_num_results: Optional[bool] = None,
        show_duplicates: Optional[bool] = None,
        exclude_cluster_id: Optional[List[str]] = None,
    ) -> StorySearchResult:
        """
        Search and filter all news stories available via the Perigon API. Each story aggregates key information across related articles, including AI-generated names, summaries, and key points.

        Args:
            q (Optional[str]): Search story by name, summary and key points. Preference is given to the name field. Supports complex query syntax, same way as q parameter from /all endpoint.
            name (Optional[str]): Search story by name. Supports complex query syntax, same way as q parameter from /all endpoint.
            cluster_id (Optional[List[str]]): Filter to specific story. Passing a cluster ID will filter results to only the content found within the cluster. Multiple params could be passed.
            sort_by (Optional[SortBy]): Sort stories by count ('count'), total count ('totalCount'), creation date ('createdAt'), last updated date ('updatedAt'), or relevance ('relevance'). By default is sorted by 'createdAt'
            page (Optional[int]): The page number to retrieve.
            size (Optional[int]): The number of items per page.
            var_from (Optional[datetime]): 'from' filter, will search stories created after the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2023-03-01T00:00:00
            to (Optional[datetime]): 'to' filter, will search stories created before the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2023-03-01T23:59:59
            topic (Optional[List[str]]): Filter by topics. Each topic is some kind of entity that the article is about. Examples of topics: Markets, Joe Biden, Green Energy, Climate Change, Cryptocurrency, etc. If multiple parameters are passed, they will be applied as OR operations.
            category (Optional[List[str]]): Filter by categories. Categories are general themes that the article is about. Examples of categories: Tech, Politics, etc. If multiple parameters are passed, they will be applied as OR operations. Use 'none' to search uncategorized articles. More ➜
            taxonomy (Optional[List[str]]): Filters by Google Content Categories. This field will accept 1 or more categories, must pass the full name of the category. Example: taxonomy=/Finance/Banking/Other, /Finance/Investing/Funds
            source (Optional[List[str]]): Filter stories by sources that wrote articles belonging to this story. At least 1 article is required for story to match. Multiple parameters could be passed.
            source_group (Optional[List[str]]): Filter stories by sources that wrote articles belonging to this story. Source groups are expanded into a list of sources. At least 1 article by the source is required for story to match. Multiple params could be passed.
            min_unique_sources (Optional[int]): Specifies the minimum number of unique sources required for a story to appear in results. Higher values return more significant stories covered by multiple publications. Default is 3.
            person_wikidata_id (Optional[List[str]]): List of person Wikidata IDs for filtering. Filter is applied on topPeople field.
            person_name (Optional[str]): List of people names. Filtering is applied on topPeople field.
            company_id (Optional[List[str]]): List of company IDs for filtering. Filtering is applied to topCompanies field.
            company_name (Optional[str]): List of company names for filtering. Filtering is applied on topCompanies field.
            company_domain (Optional[List[str]]): List of company domains for filtering. Filtering is applied on topCompanies field.
            company_symbol (Optional[List[str]]): List of company tickers for filtering. Filtering is applied on topCompanies field.
            country (Optional[List[str]]): Country code to filter by country. If multiple parameters are passed, they will be applied as OR operations.
            state (Optional[List[str]]): Filter local news by state. Applies only to local news, when this param is passed non-local news will not be returned. If multiple parameters are passed, they will be applied as OR operations.
            city (Optional[List[str]]): Filter local news by city. Applies only to local news, when this param is passed non-local news will not be returned. If multiple parameters are passed, they will be applied as OR operations.
            area (Optional[List[str]]): Filter local news by area. Applies only to local news, when this param is passed non-local news will not be returned. If multiple parameters are passed, they will be applied as OR operations.
            min_cluster_size (Optional[int]): Filter by minimum cluster size. Minimum cluster size filter applies to number of unique articles.
            max_cluster_size (Optional[int]): Filter by maximum cluster size. Maximum cluster size filter applies to number of unique articles in the cluster.
            name_exists (Optional[bool]): Returns stories with name assigned. Defaults to true.
            positive_sentiment_from (Optional[float]): Filters results with a sentiment score greater than or equal to the specified value, indicating positive sentiment. See the Article Data section in Docs for an explanation of scores.
            positive_sentiment_to (Optional[float]): Filters results with a sentiment score less than or equal to the specified value, indicating positive sentiment. See the Article Data section in Docs for an explanation of scores.
            neutral_sentiment_from (Optional[float]): Filters results with a sentiment score greater than or equal to the specified value, indicating neutral sentiment. Explanation of sentimental values can be found in Docs under the Article Data section.
            neutral_sentiment_to (Optional[float]): Filters results with a sentiment score less than or equal to the specified value, indicating neutral sentiment. See the Article Data section in Docs for an explanation of scores.
            negative_sentiment_from (Optional[float]): Filters results with a sentiment score greater than or equal to the specified value, indicating negative sentiment. See the Article Data section in Docs for an explanation of scores.
            negative_sentiment_to (Optional[float]): Filters results with a sentiment score less than or equal to the specified value, indicating negative sentiment. See the Article Data section in Docs for an explanation of scores.
            initialized_from (Optional[datetime]): 'initializedFrom' filter, will search stories that became available after provided date
            initialized_to (Optional[datetime]): 'initializedTo' filter, will search stories that became available before provided date
            updated_from (Optional[datetime]): Will return stories with 'updatedAt' >= 'updatedFrom'.
            updated_to (Optional[datetime]): Will return stories with 'updatedAt' <= 'updatedTo'.
            show_story_page_info (Optional[bool]): Parameter show_story_page_info
            show_num_results (Optional[bool]): Show total number of results. By default set to false, will cap result count at 10000.
            show_duplicates (Optional[bool]): Stories are deduplicated by default. If a story is deduplicated, all future articles are merged into the original story. duplicateOf field contains the original cluster Id. When showDuplicates=true, all stories are shown.
            exclude_cluster_id (Optional[List[str]]): Excludes specific stories from the results by their unique identifiers. Use this parameter to filter out unwanted or previously seen stories.

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
        if initialized_from is not None:
            params["initializedFrom"] = initialized_from
        if initialized_to is not None:
            params["initializedTo"] = initialized_to
        if updated_from is not None:
            params["updatedFrom"] = updated_from
        if updated_to is not None:
            params["updatedTo"] = updated_to
        if show_story_page_info is not None:
            params["showStoryPageInfo"] = show_story_page_info
        if show_num_results is not None:
            params["showNumResults"] = show_num_results
        if show_duplicates is not None:
            params["showDuplicates"] = show_duplicates
        if exclude_cluster_id is not None:
            params["excludeClusterId"] = exclude_cluster_id
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
        sort_by: Optional[SortBy] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        var_from: Optional[datetime] = None,
        to: Optional[datetime] = None,
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
        initialized_from: Optional[datetime] = None,
        initialized_to: Optional[datetime] = None,
        updated_from: Optional[datetime] = None,
        updated_to: Optional[datetime] = None,
        show_story_page_info: Optional[bool] = None,
        show_num_results: Optional[bool] = None,
        show_duplicates: Optional[bool] = None,
        exclude_cluster_id: Optional[List[str]] = None,
    ) -> StorySearchResult:
        """
        Async variant of search_stories. Search and filter all news stories available via the Perigon API. Each story aggregates key information across related articles, including AI-generated names, summaries, and key points.

        Args:
            q (Optional[str]): Search story by name, summary and key points. Preference is given to the name field. Supports complex query syntax, same way as q parameter from /all endpoint.
            name (Optional[str]): Search story by name. Supports complex query syntax, same way as q parameter from /all endpoint.
            cluster_id (Optional[List[str]]): Filter to specific story. Passing a cluster ID will filter results to only the content found within the cluster. Multiple params could be passed.
            sort_by (Optional[SortBy]): Sort stories by count ('count'), total count ('totalCount'), creation date ('createdAt'), last updated date ('updatedAt'), or relevance ('relevance'). By default is sorted by 'createdAt'
            page (Optional[int]): The page number to retrieve.
            size (Optional[int]): The number of items per page.
            var_from (Optional[datetime]): 'from' filter, will search stories created after the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2023-03-01T00:00:00
            to (Optional[datetime]): 'to' filter, will search stories created before the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2023-03-01T23:59:59
            topic (Optional[List[str]]): Filter by topics. Each topic is some kind of entity that the article is about. Examples of topics: Markets, Joe Biden, Green Energy, Climate Change, Cryptocurrency, etc. If multiple parameters are passed, they will be applied as OR operations.
            category (Optional[List[str]]): Filter by categories. Categories are general themes that the article is about. Examples of categories: Tech, Politics, etc. If multiple parameters are passed, they will be applied as OR operations. Use 'none' to search uncategorized articles. More ➜
            taxonomy (Optional[List[str]]): Filters by Google Content Categories. This field will accept 1 or more categories, must pass the full name of the category. Example: taxonomy=/Finance/Banking/Other, /Finance/Investing/Funds
            source (Optional[List[str]]): Filter stories by sources that wrote articles belonging to this story. At least 1 article is required for story to match. Multiple parameters could be passed.
            source_group (Optional[List[str]]): Filter stories by sources that wrote articles belonging to this story. Source groups are expanded into a list of sources. At least 1 article by the source is required for story to match. Multiple params could be passed.
            min_unique_sources (Optional[int]): Specifies the minimum number of unique sources required for a story to appear in results. Higher values return more significant stories covered by multiple publications. Default is 3.
            person_wikidata_id (Optional[List[str]]): List of person Wikidata IDs for filtering. Filter is applied on topPeople field.
            person_name (Optional[str]): List of people names. Filtering is applied on topPeople field.
            company_id (Optional[List[str]]): List of company IDs for filtering. Filtering is applied to topCompanies field.
            company_name (Optional[str]): List of company names for filtering. Filtering is applied on topCompanies field.
            company_domain (Optional[List[str]]): List of company domains for filtering. Filtering is applied on topCompanies field.
            company_symbol (Optional[List[str]]): List of company tickers for filtering. Filtering is applied on topCompanies field.
            country (Optional[List[str]]): Country code to filter by country. If multiple parameters are passed, they will be applied as OR operations.
            state (Optional[List[str]]): Filter local news by state. Applies only to local news, when this param is passed non-local news will not be returned. If multiple parameters are passed, they will be applied as OR operations.
            city (Optional[List[str]]): Filter local news by city. Applies only to local news, when this param is passed non-local news will not be returned. If multiple parameters are passed, they will be applied as OR operations.
            area (Optional[List[str]]): Filter local news by area. Applies only to local news, when this param is passed non-local news will not be returned. If multiple parameters are passed, they will be applied as OR operations.
            min_cluster_size (Optional[int]): Filter by minimum cluster size. Minimum cluster size filter applies to number of unique articles.
            max_cluster_size (Optional[int]): Filter by maximum cluster size. Maximum cluster size filter applies to number of unique articles in the cluster.
            name_exists (Optional[bool]): Returns stories with name assigned. Defaults to true.
            positive_sentiment_from (Optional[float]): Filters results with a sentiment score greater than or equal to the specified value, indicating positive sentiment. See the Article Data section in Docs for an explanation of scores.
            positive_sentiment_to (Optional[float]): Filters results with a sentiment score less than or equal to the specified value, indicating positive sentiment. See the Article Data section in Docs for an explanation of scores.
            neutral_sentiment_from (Optional[float]): Filters results with a sentiment score greater than or equal to the specified value, indicating neutral sentiment. Explanation of sentimental values can be found in Docs under the Article Data section.
            neutral_sentiment_to (Optional[float]): Filters results with a sentiment score less than or equal to the specified value, indicating neutral sentiment. See the Article Data section in Docs for an explanation of scores.
            negative_sentiment_from (Optional[float]): Filters results with a sentiment score greater than or equal to the specified value, indicating negative sentiment. See the Article Data section in Docs for an explanation of scores.
            negative_sentiment_to (Optional[float]): Filters results with a sentiment score less than or equal to the specified value, indicating negative sentiment. See the Article Data section in Docs for an explanation of scores.
            initialized_from (Optional[datetime]): 'initializedFrom' filter, will search stories that became available after provided date
            initialized_to (Optional[datetime]): 'initializedTo' filter, will search stories that became available before provided date
            updated_from (Optional[datetime]): Will return stories with 'updatedAt' >= 'updatedFrom'.
            updated_to (Optional[datetime]): Will return stories with 'updatedAt' <= 'updatedTo'.
            show_story_page_info (Optional[bool]): Parameter show_story_page_info
            show_num_results (Optional[bool]): Show total number of results. By default set to false, will cap result count at 10000.
            show_duplicates (Optional[bool]): Stories are deduplicated by default. If a story is deduplicated, all future articles are merged into the original story. duplicateOf field contains the original cluster Id. When showDuplicates=true, all stories are shown.
            exclude_cluster_id (Optional[List[str]]): Excludes specific stories from the results by their unique identifiers. Use this parameter to filter out unwanted or previously seen stories.

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
        if initialized_from is not None:
            params["initializedFrom"] = initialized_from
        if initialized_to is not None:
            params["initializedTo"] = initialized_to
        if updated_from is not None:
            params["updatedFrom"] = updated_from
        if updated_to is not None:
            params["updatedTo"] = updated_to
        if show_story_page_info is not None:
            params["showStoryPageInfo"] = show_story_page_info
        if show_num_results is not None:
            params["showNumResults"] = show_num_results
        if show_duplicates is not None:
            params["showDuplicates"] = show_duplicates
        if exclude_cluster_id is not None:
            params["excludeClusterId"] = exclude_cluster_id
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
    ) -> SummarySearchResult:
        """
        Produce a single, concise summary over the full corpus of articles matching your filters, using your prompt to guide which insights to highlight.

        Args:
            summary_body (SummaryBody): Parameter summary_body (required)
            q (Optional[str]): Search query, each article will be scored and ranked against it. Articles are searched on the title, description, and content fields.
            title (Optional[str]): Search article headlines/title field. Semantic similar to q parameter.
            desc (Optional[str]): Search query on the description field. Semantic similar to q parameter.
            content (Optional[str]): Search query on the article's body of content field. Semantic similar to q parameter.
            url (Optional[str]): Search query on the url field. Semantic similar to q parameter. E.g. could be used for querying certain website sections, e.g. source=cnn.com&url=travel.
            article_id (Optional[List[str]]): Article ID will search for a news article by the ID of the article. If several parameters are passed, all matched articles will be returned.
            cluster_id (Optional[List[str]]): Search for related content using a cluster ID. Passing a cluster ID will filter results to only the content found within the cluster.
            sort_by (Optional[AllEndpointSortBy]): 'relevance' to sort by relevance to the query, 'date' to sort by the publication date (desc), 'pubDate' is a synonym to 'date', 'addDate' to sort by 'addDate' field (desc), 'refreshDate' to sort by 'refreshDate' field (desc). Defaults to 'relevance'
            page (Optional[int]): The page number to retrieve.
            size (Optional[int]): The number of items per page.
            var_from (Optional[datetime]): 'from' filter, will search articles published after the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2023-03-01T00:00:00
            to (Optional[datetime]): 'to' filter, will search articles published before the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T23:59:59
            add_date_from (Optional[datetime]): 'addDateFrom' filter, will search articles added after the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T00:00:00
            add_date_to (Optional[datetime]): 'addDateTo' filter, will search articles added before the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T23:59:59
            refresh_date_from (Optional[datetime]): Will search articles that were refreshed after the specified date. The date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T00:00:00
            refresh_date_to (Optional[datetime]): Will search articles that were refreshed before the specified date. The date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T23:59:59
            medium (Optional[List[str]]): Medium will filter out news articles medium, which could be 'Video' or 'Article'. If several parameters are passed, all matched articles will be returned.
            source (Optional[List[str]]): Publisher's domain can include a subdomain. If multiple parameters are passed, they will be applied as OR operations. Wildcards (* and ?) are suported (e.g. *.cnn.com).
            source_group (Optional[List[str]]): One of the supported source groups. Find Source Groups in the guided part of our documentation...
            exclude_source_group (Optional[List[str]]): A list of built-in source group names to exclude from the results. The Perigon API categorizes sources into groups (for example, “top10” or “top100”) based on type or popularity. Using this filter allows you to remove articles coming from any source that belongs to one or more of the specified groups.
            exclude_source (Optional[List[str]]): The domain of the website, which should be excluded from the search. Multiple parameters could be provided. Wildcards (* and ?) are suported (e.g. *.cnn.com).
            paywall (Optional[bool]): Filter to show only results where the source has a paywall (true) or does not have a paywall (false).
            byline (Optional[List[str]]): Author names to filter by. Article author bylines are used as a source field. If multiple parameters are passed, they will be applied as OR operations.
            author (Optional[List[str]]): A list of author names to include. Only articles written by any of the specified authors are returned. This is ideal when you wish to focus on content from particular voices or experts.
            exclude_author (Optional[List[str]]):  A list of author names to exclude from the search results. Any article written by an author whose name matches one in this list will be omitted, which helps to avoid content from certain individuals.
            journalist_id (Optional[List[str]]): Filter by journalist ID. Journalist IDs are unique journalist identifiers which can be found through the Journalist API, or in the matchedAuthors field.
            exclude_journalist_id (Optional[List[str]]): A list of journalist (or reporter) identifiers to exclude. If an article is written by a journalist whose ID matches any in this list, it will not be part of the result set.
            language (Optional[List[str]]): Language code to filter by language. If multiple parameters are passed, they will be applied as OR operations.
            exclude_language (Optional[List[str]]):  A list of languages to be excluded. Any article published in one of the languages provided in this filter will not be returned. This is useful when you are interested only in news published in specific languages.
            search_translation (Optional[bool]): Expand a query to search the translation, translatedTitle, and translatedDescription fields for non-English articles.
            label (Optional[List[str]]): Labels to filter by, could be 'Opinion', 'Paid-news', 'Non-news', etc. If multiple parameters are passed, they will be applied as OR operations.
            exclude_label (Optional[List[str]]): Exclude results that include specific labels (Opinion, Non-news, Paid News, etc.). You can filter multiple by repeating the parameter.
            category (Optional[List[str]]): Filter by categories. Categories are general themes that the article is about. Examples of categories: Tech, Politics, etc. If multiple parameters are passed, they will be applied as OR operations. Use 'none' to search uncategorized articles.
            exclude_category (Optional[List[str]]): A list of article categories to be omitted. If an article is tagged with any category present in this list (such as “Polotics”, “Tech”, “Sports”, etc.), it will not appear in the search results.
            topic (Optional[List[str]]): Filters results to include only articles with the specified topics. Topics are more specific classifications than categories, with an article potentially having multiple topics assigned. Perigon uses both human and machine curation to maintain an evolving list of available topics. Common examples include 'Markets', 'Crime', 'Cryptocurrency', 'Social Issues', 'College Sports', etc. See the Topics page in Docs for a complete list of available topics.
            exclude_topic (Optional[List[str]]): Filter by excluding topics. Each topic is some kind of entity that the article is about. Examples of topics: Markets, Joe Biden, Green Energy, Climate Change, Cryptocurrency, etc. If multiple parameters are passed, they will be applied as OR operations.
            link_to (Optional[str]): Returns only articles that point to specified links (as determined by the 'links' field in the article response).
            show_reprints (Optional[bool]): Whether to return reprints in the response or not. Reprints are usually wired articles from sources like AP or Reuters that are reprinted in multiple sources at the same time. By default, this parameter is 'true'.
            reprint_group_id (Optional[str]): Shows all articles belonging to the same reprint group. A reprint group includes one original article (the first one processed by the API) and all its known reprints.
            city (Optional[List[str]]): Filters articles where a specified city plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the urban area in question. If multiple parameters are passed, they will be applied as OR operations.
            exclude_city (Optional[List[str]]): A list of cities to exclude from the results. Articles that are associated with any of the specified cities will be filtered out.
            area (Optional[List[str]]): Filters articles where a specified area, such as a neighborhood, borough, or district, plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the area in question. If multiple parameters are passed, they will be applied as OR operations.
            state (Optional[List[str]]): Filters articles where a specified state plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the state in question. If multiple parameters are passed, they will be applied as OR operations.
            exclude_state (Optional[List[str]]): A list of states to exclude. Articles that include, or are associated with, any of the states provided here will be filtered out. This is especially useful if you want to ignore news tied to certain geographical areas (e.g., US states).
            county (Optional[List[str]]): A list of counties to include (or specify) in the search results. This field filters the returned articles based on the county associated with the event or news. Only articles tagged with one of these counties will be included.
            exclude_county (Optional[List[str]]): Excludes articles from specific counties or administrative divisions in the vector search results. Accepts either a single county name or a list of county names. County names should match the format used in article metadata (e.g., 'Los Angeles County', 'Cook County'). This parameter allows for more granular geographic filter
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
            person_wikidata_id (Optional[List[str]]): List of person Wikidata IDs for filtering.
            exclude_person_wikidata_id (Optional[List[str]]): A list of Wikidata identifiers for individuals. Articles mentioning persons with any of these Wikidata IDs will be filtered out. This is particularly helpful when using a unique identifier to prevent ambiguity in names.
            person_name (Optional[List[str]]): List of person names for exact matches. Boolean and complex logic is not supported on this paramter.
            exclude_person_name (Optional[List[str]]): A list of person names that, when associated with the content, cause the article to be excluded. This filter removes articles related to any individuals whose names match those on the list.
            company_id (Optional[List[str]]): List of company IDs to filter by.
            exclude_company_id (Optional[List[str]]): A list of company identifiers. Articles associated with companies that have any of these unique IDs will be filtered out from the returned results, ensuring that certain companies or corporate entities are not included.
            company_name (Optional[str]): Search by company name.
            company_domain (Optional[List[str]]): Search by company domains for filtering. E.g. companyDomain=apple.com.
            exclude_company_domain (Optional[List[str]]): A list of company domains to exclude. If an article is related to a company that uses one of the specified domains (for instance, “example.com”), it will not be returned in the results.
            company_symbol (Optional[List[str]]): Search by company symbols.
            exclude_company_symbol (Optional[List[str]]): A list of stock symbols (ticker symbols) that identify companies to be excluded. Articles related to companies using any of these symbols will be omitted, which is useful for targeting or avoiding specific public companies.
            show_num_results (Optional[bool]): Whether to show the total number of all matched articles. Default value is false which makes queries a bit more efficient but also counts up to 10000 articles.
            positive_sentiment_from (Optional[float]): Filters results with a sentiment score greater than or equal to the specified value, indicating positive sentiment. See the Article Data section in Docs for an explanation of scores.
            positive_sentiment_to (Optional[float]): Filters results with a sentiment score less than or equal to the specified value, indicating positive sentiment. See the Article Data section in Docs for an explanation of scores.
            neutral_sentiment_from (Optional[float]): Filters results with a sentiment score greater than or equal to the specified value, indicating neutral sentiment. Explanation of sentimental values can be found in Docs under the Article Data section.
            neutral_sentiment_to (Optional[float]): Filters results with a sentiment score less than or equal to the specified value, indicating neutral sentiment. See the Article Data section in Docs for an explanation of scores.
            negative_sentiment_from (Optional[float]): Filters results with a sentiment score greater than or equal to the specified value, indicating negative sentiment. See the Article Data section in Docs for an explanation of scores.
            negative_sentiment_to (Optional[float]): Filters results with a sentiment score less than or equal to the specified value, indicating negative sentiment. See the Article Data section in Docs for an explanation of scores.
            taxonomy (Optional[List[str]]): Filters by Google Content Categories. This field will accept 1 or more categories, must pass the full name of the category. Example: taxonomy=/Finance/Banking/Other, /Finance/Investing/Funds
            prefix_taxonomy (Optional[str]): Filters by Google Content Categories. This field will filter by the category prefix only. Example: prefixTaxonomy=/Finance

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
    ) -> SummarySearchResult:
        """
        Async variant of search_summarizer. Produce a single, concise summary over the full corpus of articles matching your filters, using your prompt to guide which insights to highlight.

        Args:
            summary_body (SummaryBody): Parameter summary_body (required)
            q (Optional[str]): Search query, each article will be scored and ranked against it. Articles are searched on the title, description, and content fields.
            title (Optional[str]): Search article headlines/title field. Semantic similar to q parameter.
            desc (Optional[str]): Search query on the description field. Semantic similar to q parameter.
            content (Optional[str]): Search query on the article's body of content field. Semantic similar to q parameter.
            url (Optional[str]): Search query on the url field. Semantic similar to q parameter. E.g. could be used for querying certain website sections, e.g. source=cnn.com&url=travel.
            article_id (Optional[List[str]]): Article ID will search for a news article by the ID of the article. If several parameters are passed, all matched articles will be returned.
            cluster_id (Optional[List[str]]): Search for related content using a cluster ID. Passing a cluster ID will filter results to only the content found within the cluster.
            sort_by (Optional[AllEndpointSortBy]): 'relevance' to sort by relevance to the query, 'date' to sort by the publication date (desc), 'pubDate' is a synonym to 'date', 'addDate' to sort by 'addDate' field (desc), 'refreshDate' to sort by 'refreshDate' field (desc). Defaults to 'relevance'
            page (Optional[int]): The page number to retrieve.
            size (Optional[int]): The number of items per page.
            var_from (Optional[datetime]): 'from' filter, will search articles published after the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2023-03-01T00:00:00
            to (Optional[datetime]): 'to' filter, will search articles published before the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T23:59:59
            add_date_from (Optional[datetime]): 'addDateFrom' filter, will search articles added after the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T00:00:00
            add_date_to (Optional[datetime]): 'addDateTo' filter, will search articles added before the specified date, the date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T23:59:59
            refresh_date_from (Optional[datetime]): Will search articles that were refreshed after the specified date. The date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T00:00:00
            refresh_date_to (Optional[datetime]): Will search articles that were refreshed before the specified date. The date could be passed as ISO or 'yyyy-mm-dd'. Add time in ISO format, ie. 2022-02-01T23:59:59
            medium (Optional[List[str]]): Medium will filter out news articles medium, which could be 'Video' or 'Article'. If several parameters are passed, all matched articles will be returned.
            source (Optional[List[str]]): Publisher's domain can include a subdomain. If multiple parameters are passed, they will be applied as OR operations. Wildcards (* and ?) are suported (e.g. *.cnn.com).
            source_group (Optional[List[str]]): One of the supported source groups. Find Source Groups in the guided part of our documentation...
            exclude_source_group (Optional[List[str]]): A list of built-in source group names to exclude from the results. The Perigon API categorizes sources into groups (for example, “top10” or “top100”) based on type or popularity. Using this filter allows you to remove articles coming from any source that belongs to one or more of the specified groups.
            exclude_source (Optional[List[str]]): The domain of the website, which should be excluded from the search. Multiple parameters could be provided. Wildcards (* and ?) are suported (e.g. *.cnn.com).
            paywall (Optional[bool]): Filter to show only results where the source has a paywall (true) or does not have a paywall (false).
            byline (Optional[List[str]]): Author names to filter by. Article author bylines are used as a source field. If multiple parameters are passed, they will be applied as OR operations.
            author (Optional[List[str]]): A list of author names to include. Only articles written by any of the specified authors are returned. This is ideal when you wish to focus on content from particular voices or experts.
            exclude_author (Optional[List[str]]):  A list of author names to exclude from the search results. Any article written by an author whose name matches one in this list will be omitted, which helps to avoid content from certain individuals.
            journalist_id (Optional[List[str]]): Filter by journalist ID. Journalist IDs are unique journalist identifiers which can be found through the Journalist API, or in the matchedAuthors field.
            exclude_journalist_id (Optional[List[str]]): A list of journalist (or reporter) identifiers to exclude. If an article is written by a journalist whose ID matches any in this list, it will not be part of the result set.
            language (Optional[List[str]]): Language code to filter by language. If multiple parameters are passed, they will be applied as OR operations.
            exclude_language (Optional[List[str]]):  A list of languages to be excluded. Any article published in one of the languages provided in this filter will not be returned. This is useful when you are interested only in news published in specific languages.
            search_translation (Optional[bool]): Expand a query to search the translation, translatedTitle, and translatedDescription fields for non-English articles.
            label (Optional[List[str]]): Labels to filter by, could be 'Opinion', 'Paid-news', 'Non-news', etc. If multiple parameters are passed, they will be applied as OR operations.
            exclude_label (Optional[List[str]]): Exclude results that include specific labels (Opinion, Non-news, Paid News, etc.). You can filter multiple by repeating the parameter.
            category (Optional[List[str]]): Filter by categories. Categories are general themes that the article is about. Examples of categories: Tech, Politics, etc. If multiple parameters are passed, they will be applied as OR operations. Use 'none' to search uncategorized articles.
            exclude_category (Optional[List[str]]): A list of article categories to be omitted. If an article is tagged with any category present in this list (such as “Polotics”, “Tech”, “Sports”, etc.), it will not appear in the search results.
            topic (Optional[List[str]]): Filters results to include only articles with the specified topics. Topics are more specific classifications than categories, with an article potentially having multiple topics assigned. Perigon uses both human and machine curation to maintain an evolving list of available topics. Common examples include 'Markets', 'Crime', 'Cryptocurrency', 'Social Issues', 'College Sports', etc. See the Topics page in Docs for a complete list of available topics.
            exclude_topic (Optional[List[str]]): Filter by excluding topics. Each topic is some kind of entity that the article is about. Examples of topics: Markets, Joe Biden, Green Energy, Climate Change, Cryptocurrency, etc. If multiple parameters are passed, they will be applied as OR operations.
            link_to (Optional[str]): Returns only articles that point to specified links (as determined by the 'links' field in the article response).
            show_reprints (Optional[bool]): Whether to return reprints in the response or not. Reprints are usually wired articles from sources like AP or Reuters that are reprinted in multiple sources at the same time. By default, this parameter is 'true'.
            reprint_group_id (Optional[str]): Shows all articles belonging to the same reprint group. A reprint group includes one original article (the first one processed by the API) and all its known reprints.
            city (Optional[List[str]]): Filters articles where a specified city plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the urban area in question. If multiple parameters are passed, they will be applied as OR operations.
            exclude_city (Optional[List[str]]): A list of cities to exclude from the results. Articles that are associated with any of the specified cities will be filtered out.
            area (Optional[List[str]]): Filters articles where a specified area, such as a neighborhood, borough, or district, plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the area in question. If multiple parameters are passed, they will be applied as OR operations.
            state (Optional[List[str]]): Filters articles where a specified state plays a central role in the content, beyond mere mentions, to ensure the results are deeply relevant to the state in question. If multiple parameters are passed, they will be applied as OR operations.
            exclude_state (Optional[List[str]]): A list of states to exclude. Articles that include, or are associated with, any of the states provided here will be filtered out. This is especially useful if you want to ignore news tied to certain geographical areas (e.g., US states).
            county (Optional[List[str]]): A list of counties to include (or specify) in the search results. This field filters the returned articles based on the county associated with the event or news. Only articles tagged with one of these counties will be included.
            exclude_county (Optional[List[str]]): Excludes articles from specific counties or administrative divisions in the vector search results. Accepts either a single county name or a list of county names. County names should match the format used in article metadata (e.g., 'Los Angeles County', 'Cook County'). This parameter allows for more granular geographic filter
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
            person_wikidata_id (Optional[List[str]]): List of person Wikidata IDs for filtering.
            exclude_person_wikidata_id (Optional[List[str]]): A list of Wikidata identifiers for individuals. Articles mentioning persons with any of these Wikidata IDs will be filtered out. This is particularly helpful when using a unique identifier to prevent ambiguity in names.
            person_name (Optional[List[str]]): List of person names for exact matches. Boolean and complex logic is not supported on this paramter.
            exclude_person_name (Optional[List[str]]): A list of person names that, when associated with the content, cause the article to be excluded. This filter removes articles related to any individuals whose names match those on the list.
            company_id (Optional[List[str]]): List of company IDs to filter by.
            exclude_company_id (Optional[List[str]]): A list of company identifiers. Articles associated with companies that have any of these unique IDs will be filtered out from the returned results, ensuring that certain companies or corporate entities are not included.
            company_name (Optional[str]): Search by company name.
            company_domain (Optional[List[str]]): Search by company domains for filtering. E.g. companyDomain=apple.com.
            exclude_company_domain (Optional[List[str]]): A list of company domains to exclude. If an article is related to a company that uses one of the specified domains (for instance, “example.com”), it will not be returned in the results.
            company_symbol (Optional[List[str]]): Search by company symbols.
            exclude_company_symbol (Optional[List[str]]): A list of stock symbols (ticker symbols) that identify companies to be excluded. Articles related to companies using any of these symbols will be omitted, which is useful for targeting or avoiding specific public companies.
            show_num_results (Optional[bool]): Whether to show the total number of all matched articles. Default value is false which makes queries a bit more efficient but also counts up to 10000 articles.
            positive_sentiment_from (Optional[float]): Filters results with a sentiment score greater than or equal to the specified value, indicating positive sentiment. See the Article Data section in Docs for an explanation of scores.
            positive_sentiment_to (Optional[float]): Filters results with a sentiment score less than or equal to the specified value, indicating positive sentiment. See the Article Data section in Docs for an explanation of scores.
            neutral_sentiment_from (Optional[float]): Filters results with a sentiment score greater than or equal to the specified value, indicating neutral sentiment. Explanation of sentimental values can be found in Docs under the Article Data section.
            neutral_sentiment_to (Optional[float]): Filters results with a sentiment score less than or equal to the specified value, indicating neutral sentiment. See the Article Data section in Docs for an explanation of scores.
            negative_sentiment_from (Optional[float]): Filters results with a sentiment score greater than or equal to the specified value, indicating negative sentiment. See the Article Data section in Docs for an explanation of scores.
            negative_sentiment_to (Optional[float]): Filters results with a sentiment score less than or equal to the specified value, indicating negative sentiment. See the Article Data section in Docs for an explanation of scores.
            taxonomy (Optional[List[str]]): Filters by Google Content Categories. This field will accept 1 or more categories, must pass the full name of the category. Example: taxonomy=/Finance/Banking/Other, /Finance/Investing/Funds
            prefix_taxonomy (Optional[str]): Filters by Google Content Categories. This field will filter by the category prefix only. Example: prefixTaxonomy=/Finance

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
            name (Optional[str]): Search by name.
            category (Optional[str]): Search by category.
            subcategory (Optional[str]): Search by subcategory.
            page (Optional[int]): The page number to retrieve.
            size (Optional[int]): The number of items per page.

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
            name (Optional[str]): Search by name.
            category (Optional[str]): Search by category.
            subcategory (Optional[str]): Search by subcategory.
            page (Optional[int]): The page number to retrieve.
            size (Optional[int]): The number of items per page.

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

    # ----------------- vector_search_articles (sync) ----------------- #
    def vector_search_articles(
        self, article_search_params: ArticleSearchParams
    ) -> VectorSearchResult:
        """
        Perform a natural language search over news articles from the past 6 months using semantic relevance. The result includes a list of articles most closely matched to your query intent.

        Args:
            article_search_params (ArticleSearchParams): Parameter article_search_params (required)

        Returns:
            VectorSearchResult: The response
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
        return VectorSearchResult.model_validate(resp.json())

    # ----------------- vector_search_articles (async) ----------------- #
    async def vector_search_articles_async(
        self, article_search_params: ArticleSearchParams
    ) -> VectorSearchResult:
        """
        Async variant of vector_search_articles. Perform a natural language search over news articles from the past 6 months using semantic relevance. The result includes a list of articles most closely matched to your query intent.

        Args:
            article_search_params (ArticleSearchParams): Parameter article_search_params (required)

        Returns:
            VectorSearchResult: The response
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
        return VectorSearchResult.model_validate(resp.json())

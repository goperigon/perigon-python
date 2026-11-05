#!/usr/bin/env python3
"""
Advanced Perigon Python SDK Example

This example demonstrates advanced features of the Perigon Python SDK including:
- Date filtering and complex queries
- Vector search with semantic similarity
- Article summarization
- Story clustering
- Error handling and async operations

Before running this example:
1. Install the SDK: pip install perigon
2. Set your API key: export PERIGON_API_KEY="your-api-key-here"
3. Run: python examples/advanced.py
"""

import asyncio
import os
from datetime import UTC, datetime, timedelta

from perigon import AsyncV1Api, V1Api
from perigon.models import (
    ArticleSearchParams,
    CompanySearchResult,
    JournalistSearchResult,
    QuerySearchResult,
    SummaryBody,
    WikipediaSearchParams,
)


async def main():
    """Advanced example showing sophisticated usage patterns."""

    # Get API key from environment variable
    api_key = os.getenv("PERIGON_API_KEY")
    if not api_key:
        print("❌ Error: Please set the PERIGON_API_KEY environment variable")
        print("   Example: export PERIGON_API_KEY='your-api-key-here'")
        return

    # Each API owns its HTTP client and closes it when the block ends.
    print("🚀 Initializing Perigon API client...")
    with V1Api(api_key=api_key) as api:
        # Example 1: Advanced article search with date filtering
        print("\n📅 Searching articles with date filters...")
        try:
            # Search for business news from the last 7 days
            end_date = datetime.now(UTC)
            start_date = end_date - timedelta(days=7)

            articles_result = api.search_articles(
                q="business technology",
                var_from=start_date,  # 'from' is a reserved keyword, so use 'var_from'
                to=end_date,
                size=5,
                source=["techcrunch.com", "wired.com"],  # Filter by specific sources
            )

            found = articles_result.num_results
            print(f"   Found {found} articles from the last 7 days")
            for i, article in enumerate(articles_result.articles, 1):
                source = article.source.domain if article.source else "Unknown"
                print(f"   {i}. {article.title}")
                print(f"      Source: {source}")
                print(f"      Published: {article.pub_date}")
                if article.summary:
                    print(f"      Summary: {article.summary[:100]}...")
                print()

        except Exception as e:
            print(f"   ❌ Error in advanced article search: {e}")

        # Example 2: Vector search for semantic similarity
        print("🔍 Using vector search for semantic similarity...")
        try:
            search_params = ArticleSearchParams(
                prompt="Climate change impact on renewable energy adoption", size=3
            )

            vector_results = api.vector_search_articles(
                article_search_params=search_params
            )

            if vector_results.results:
                match_count = len(vector_results.results)
                print(f"   Found {match_count} semantically similar articles")
                for i, match in enumerate(vector_results.results, 1):
                    data = match.data
                    title = data.title if data else "Untitled"
                    source = data.source.domain if data and data.source else "Unknown"
                    score = match.score if match.score is not None else "N/A"
                    print(f"   {i}. {title}")
                    print(f"      Relevance Score: {score}")
                    print(f"      Source: {source}")
                    print()
            else:
                print("   No results found for vector search")

        except Exception as e:
            print(f"   ❌ Error in vector search: {e}")

        # Example 3: Article summarization
        print("📝 Generating article summaries...")
        try:
            summary_body = SummaryBody(
                prompt=(
                    "Summarize the key developments and their impact on the industry"
                ),
                max_article_count=10,
                returned_article_count=10,
            )

            summary_result = api.search_summarizer(
                summary_body=summary_body,
                q="artificial intelligence healthcare",
            )

            if summary_result.summary:
                analyzed = len(summary_result.results)
                print(f"   Generated summary ({analyzed} articles analyzed):")
                print(f"   {summary_result.summary}")
                print()
            else:
                print("   No summary generated")

        except Exception as e:
            print(f"   ❌ Error in summarization: {e}")

        # Example 4: Story clustering
        print("📚 Finding related story clusters...")
        try:
            stories_result = api.search_stories(q="cryptocurrency regulation", size=3)

            if stories_result.results:
                print(f"   Found {len(stories_result.results)} story clusters")
                for i, story in enumerate(stories_result.results, 1):
                    print(f"   {i}. Story ID: {story.id}")
                    if story.name:
                        print(f"      Title: {story.name}")
                    article_count = story.unique_count
                    if article_count is None:
                        article_count = story.total_count
                    if article_count is not None:
                        print(f"      Articles in cluster: {article_count}")
                    print()
            else:
                print("   No story clusters found")

        except Exception as e:
            print(f"   ❌ Error in story search: {e}")

        # Example 5: Topics exploration
        print("🏷️  Exploring available topics...")
        try:
            topics_result = api.search_topics(size=5)

            if topics_result.data:
                print(f"   Found {len(topics_result.data)} topics")
                for topic in topics_result.data:
                    print(f"   - {topic.name}")
                    if topic.labels and topic.labels.category:
                        print(f"     Category: {topic.labels.category}")
            else:
                print("   No topics found")

        except Exception as e:
            print(f"   ❌ Error exploring topics: {e}")

        # Example 6: Vector-based Wikipedia Search
        print("\n🧠 Example 6: Vector-based Wikipedia Search")
        print("Using semantic search for pages about artificial intelligence...\n")

        try:
            vector_wikipedia_result = api.vector_search_wikipedia(
                wikipedia_search_params=WikipediaSearchParams(
                    prompt="artificial intelligence and neural networks in computing",
                    size=3,
                    pageviews_from=100,  # Only pages with significant viewership
                )
            )

            match_count = len(vector_wikipedia_result.results)
            print(f"Found {match_count} semantically related Wikipedia pages:")
            for i, result in enumerate(vector_wikipedia_result.results, 1):
                page = result.data
                title = page.wiki_title if page and page.wiki_title else "Untitled"
                if result.score is None:
                    score = "N/A"
                else:
                    score = f"{result.score * 100:.1f}%"
                url = "N/A"
                if page and page.wiki_title and page.wiki_code in (None, "enwiki"):
                    slug = page.wiki_title.replace(" ", "_")
                    url = f"https://en.wikipedia.org/wiki/{slug}"
                summary = (
                    page.content if page and page.content else "No summary available"
                )
                if len(summary) > 200:
                    summary = summary[:200] + "..."
                views = page.pageviews if page and page.pageviews is not None else "N/A"
                wikidata_id = page.wikidata_id if page and page.wikidata_id else "N/A"
                print(f"  {i}. {title}")
                print(f"     Relevance Score: {score}")
                print(f"     URL: {url}")
                print(f"     Summary: {summary}")
                print(f"     Views per day: {views}")
                print(f"     Wikidata ID: {wikidata_id}\n")

        except Exception as e:
            print(f"   ❌ Error in vector Wikipedia search: {e}")

    # Example 7: Demonstrate async usage
    print("\n🔄 Running async operations...")
    async with AsyncV1Api(api_key=api_key) as api:
        try:
            # Run multiple searches concurrently
            print("   Running concurrent async searches...")

            # Execute searches concurrently. return_exceptions keeps one failure
            # from cancelling the others, so each result is checked on its own.
            (
                async_articles,
                async_companies,
                async_journalists,
            ) = await asyncio.gather(
                api.search_articles(q="technology", size=2),
                api.search_companies(name="Google", size=1),
                api.search_journalists(name="Sarah", size=1),
                return_exceptions=True,
            )

            if isinstance(async_articles, QuerySearchResult):
                article_count = len(async_articles.articles)
                print(f"   ✓ Async articles search: {article_count} articles")
            else:
                print(f"   ❌ Async articles search failed: {async_articles}")

            if isinstance(async_companies, CompanySearchResult):
                company_count = len(async_companies.results)
                print(f"   ✓ Async companies search: {company_count} companies")
            else:
                print(f"   ❌ Async companies search failed: {async_companies}")

            if isinstance(async_journalists, JournalistSearchResult):
                journalist_count = len(async_journalists.results)
                print(f"   ✓ Async journalists search: {journalist_count} journalists")
            else:
                print(f"   ❌ Async journalists search failed: {async_journalists}")

        except Exception as e:
            print(f"   ❌ Error in async operations: {e}")

    print("✅ Advanced example completed!")


if __name__ == "__main__":
    asyncio.run(main())

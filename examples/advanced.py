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
from datetime import datetime, timedelta, timezone

from perigon import ApiClient, V1Api
from perigon.models import ArticleSearchParams, SummaryBody


def main():
    """Advanced example showing sophisticated usage patterns."""

    # Get API key from environment variable
    api_key = os.getenv("PERIGON_API_KEY")
    if not api_key:
        print("❌ Error: Please set the PERIGON_API_KEY environment variable")
        print("   Example: export PERIGON_API_KEY='your-api-key-here'")
        return

    # Initialize the API client
    print("🚀 Initializing Perigon API client...")
    api = V1Api(ApiClient(api_key=api_key))

    # Example 1: Advanced article search with date filtering
    print("\n📅 Searching articles with date filters...")
    try:
        # Search for business news from the last 7 days
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=7)

        articles_result = api.search_articles(
            q="business technology",
            var_from=start_date,  # 'from' is a reserved keyword, so use 'var_from'
            to=end_date,
            size=5,
            source=["techcrunch.com", "wired.com"],  # Filter by specific sources
        )

        print(f"   Found {articles_result.num_results} articles from the last 7 days")
        for i, article in enumerate(articles_result.articles, 1):
            print(f"   {i}. {article.title}")
            print(
                f"      Source: {article.source.domain if article.source else 'Unknown'}"
            )
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

        vector_results = api.vector_search_articles(article_search_params=search_params)

        if vector_results.results:
            print(
                f"   Found {len(vector_results.results)} semantically similar articles"
            )
            for i, article in enumerate(vector_results.results, 1):
                print(f"   {i}. {article.data.title}")
                print(f"      Relevance Score: {getattr(article, 'score', 'N/A')}")
                print(
                    f"      Source: {article.data.source.domain if article.data.source else 'Unknown'}"
                )
                print()
        else:
            print("   No results found for vector search")

    except Exception as e:
        print(f"   ❌ Error in vector search: {e}")

    # Example 3: Article summarization
    print("📝 Generating article summaries...")
    try:
        summary_body = SummaryBody(
            prompt="Summarize the key developments and their impact on the industry"
        )

        summary_result = api.search_summarizer(
            summary_body=summary_body, q="artificial intelligence healthcare", size=10
        )

        if summary_result.summary:
            print(
                f"   Generated summary ({len(summary_result.results)} articles analyzed):"
            )
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
                if hasattr(story, "title") and story.title:
                    print(f"      Title: {story.title}")
                if hasattr(story, "article_count"):
                    print(f"      Articles in cluster: {story.article_count}")
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
                if hasattr(topic, "description") and topic.description:
                    print(f"     Description: {topic.description[:80]}...")
        else:
            print("   No topics found")

    except Exception as e:
        print(f"   ❌ Error exploring topics: {e}")

    # Example 6: Demonstrate async usage
    print("\n🔄 Running async operations...")
    asyncio.run(async_example(api))

    print("✅ Advanced example completed!")


async def async_example(api: V1Api):
    """Demonstrate async operations with the Perigon SDK."""
    try:
        # Run multiple searches concurrently
        print("   Running concurrent async searches...")

        # Create multiple async tasks
        tasks = [
            api.search_articles_async(q="technology", size=2),
            api.search_companies_async(name="Google", size=1),
            api.search_journalists_async(name="Sarah", size=1),
        ]

        # Execute tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        articles_result, companies_result, journalists_result = results

        if not isinstance(articles_result, Exception):
            print(
                f"   ✓ Async articles search: {len(articles_result.articles)} articles"
            )
        else:
            print(f"   ❌ Async articles search failed: {articles_result}")

        if not isinstance(companies_result, Exception):
            print(
                f"   ✓ Async companies search: {len(companies_result.results)} companies"
            )
        else:
            print(f"   ❌ Async companies search failed: {companies_result}")

        if not isinstance(journalists_result, Exception):
            print(
                f"   ✓ Async journalists search: {len(journalists_result.results)} journalists"
            )
        else:
            print(f"   ❌ Async journalists search failed: {journalists_result}")

    except Exception as e:
        print(f"   ❌ Error in async operations: {e}")


if __name__ == "__main__":
    main()

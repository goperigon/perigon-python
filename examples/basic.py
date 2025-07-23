#!/usr/bin/env python3
"""
Basic Perigon Python SDK Example

This example demonstrates the fundamental usage of the Perigon Python SDK
for searching news articles, companies, and journalists.

Before running this example:
1. Install the SDK: pip install perigon
2. Set your API key: export PERIGON_API_KEY="your-api-key-here"
3. Run: python examples/basic.py
"""

import os
from datetime import datetime

from perigon import ApiClient, V1Api


def main():
    """Basic example showing core functionality of the Perigon SDK."""

    # Get API key from environment variable
    api_key = os.getenv("PERIGON_API_KEY")
    if not api_key:
        print("❌ Error: Please set the PERIGON_API_KEY environment variable")
        print("   Example: export PERIGON_API_KEY='your-api-key-here'")
        return

    # Initialize the API client
    print("🚀 Initializing Perigon API client...")
    api = V1Api(ApiClient(api_key=api_key))

    # Example 1: Search for news articles
    print("\n📰 Searching for technology news...")
    try:
        articles_result = api.search_articles(q="artificial intelligence", size=3)
        print(f"   Found {articles_result.num_results} articles")

        for i, article in enumerate(articles_result.articles, 1):
            print(f"   {i}. {article.title}")
            print(
                f"      Source: {article.source.domain if article.source else 'Unknown'}"
            )
            print(f"      Published: {article.pub_date}")
            print()

    except Exception as e:
        print(f"   ❌ Error searching articles: {e}")

    # Example 2: Search for companies
    print("🏢 Searching for companies...")
    try:
        companies_result = api.search_companies(name="Apple", size=2)

        if companies_result.results:
            print(f"   Found {len(companies_result.results)} companies")
            for company in companies_result.results:
                print(f"   - {company.name}")
                print(f"     ID: {company.id}")
                if company.description:
                    print(f"     Description: {company.description[:100]}...")
                print()
        else:
            print("   No companies found")

    except Exception as e:
        print(f"   ❌ Error searching companies: {e}")

    # Example 3: Search for journalists
    print("👤 Searching for journalists...")
    try:
        journalists_result = api.search_journalists(name="John", size=2)

        if journalists_result.results:
            print(f"   Found {len(journalists_result.results)} journalists")
            for journalist in journalists_result.results:
                print(f"   - {journalist.name}")
                print(f"     ID: {journalist.id}")
                print()
        else:
            print("   No journalists found")

    except Exception as e:
        print(f"   ❌ Error searching journalists: {e}")

    # Example 4: Wikipedia Search
    print("📚 Example 4: Wikipedia Search")
    print('Searching Wikipedia pages about "machine learning"...\n')

    try:
        wikipedia_result = api.search_wikipedia(
            q="machine learning",
            size=3,
            sort_by="relevance",
        )

        print(f"Found {wikipedia_result.num_results} Wikipedia pages:")
        for i, page in enumerate(wikipedia_result.results, 1):
            print(f"  {i}. {page.wiki_title or 'Untitled'}")
            print(f"     URL: {page.url or 'N/A'}")
            summary = page.summary if page.summary else "No summary available"
            if len(summary) > 150:
                summary = summary[:150] + "..."
            print(f"     Summary: {summary}")
            print(f"     Views per day: {page.pageviews or 'N/A'}")

            # Format the revision timestamp if available
            last_modified = "Unknown"
            if page.wiki_revision_ts:
                try:
                    # Parse ISO timestamp and format as date
                    dt = datetime.fromisoformat(
                        page.wiki_revision_ts.replace("Z", "+00:00")
                    )
                    last_modified = dt.strftime("%m/%d/%Y")
                except:
                    last_modified = page.wiki_revision_ts

            print(f"     Last modified: {last_modified}\n")

    except Exception as e:
        print(f"   ❌ Error searching Wikipedia: {e}")

    print("✅ Basic example completed!")


if __name__ == "__main__":
    main()

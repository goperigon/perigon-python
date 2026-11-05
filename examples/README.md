# Perigon Python SDK Examples

This directory contains practical examples demonstrating how to use the Perigon Python SDK effectively.

## Prerequisites

1. **Install the Perigon SDK:**
   ```bash
   pip install perigon
   ```

2. **Get your API key:**
   - Sign up at [Perigon.io](https://perigon.io)
   - Generate an API key from your dashboard

3. **Set your API key as an environment variable:**
   ```bash
   export PERIGON_API_KEY="your-api-key-here"
   ```

## Examples

### 📚 Basic Example (`basic.py`)

A beginner-friendly introduction to the Perigon SDK showing:
- Simple article search
- Company lookup
- Journalist search
- Wikipedia search
- Basic error handling

**Run it:**
```bash
python examples/basic.py
```

**What you'll learn:**
- How to initialize `V1Api` so it owns its HTTP client
- Basic search operations
- Handling API responses
- Working with article, company, journalist, and Wikipedia data

### 🚀 Advanced Example (`advanced.py`)

A comprehensive example demonstrating sophisticated features:
- Date-filtered article searches
- Vector search for semantic similarity
- Article summarization
- Story clustering
- Topics exploration
- Vector search over Wikipedia
- Asynchronous operations with concurrent requests

**Run it:**
```bash
python examples/advanced.py
```

**What you'll learn:**
- Advanced filtering and querying techniques
- Semantic search capabilities
- AI-powered summarization
- Async/await patterns for concurrent operations
- Error handling for complex workflows

## Example Output

### Basic Example
```
🚀 Initializing Perigon API client...

📰 Searching for technology news...
   Found 1247 articles
   1. OpenAI Announces GPT-5 with Revolutionary Capabilities
      Source: techcrunch.com
      Published: 2024-12-09T14:30:00Z

🏢 Searching for companies...
   Found 2 companies
   - Apple Inc.
     ID: 12345
     Description: Technology company that designs, develops, and sells consumer electronics...

👤 Searching for journalists...
   Found 2 journalists
   - John Smith
     ID: 67890

📚 Example 4: Wikipedia Search
Searching Wikipedia pages about "machine learning"...

Found 3 Wikipedia pages:
  1. Machine learning
     URL: https://en.wikipedia.org/wiki/Machine_learning
     Summary: Machine learning is a field of study in artificial intelligence...
     Views per day: 12000
     Last modified: 12/09/2024

✅ Basic example completed!
```

### Advanced Example
```
🚀 Initializing Perigon API client...

📅 Searching articles with date filters...
   Found 234 articles from the last 7 days
   1. Tech Industry Adapts to New AI Regulations
      Source: techcrunch.com
      Published: 2024-12-08T09:15:00Z
      Summary: New regulations are reshaping how tech companies develop AI...

🔍 Using vector search for semantic similarity...
   Found 3 semantically similar articles
   1. Renewable Energy Revolution Accelerates Climate Goals
      Relevance Score: 0.89
      Source: wired.com

📝 Generating article summaries...
   Generated summary (10 articles analyzed):
   Artificial intelligence is transforming healthcare through diagnostic tools...

📚 Finding related story clusters...
   Found 3 story clusters
   1. Story ID: story-123
      Title: Cryptocurrency regulation
      Articles in cluster: 42

🏷️  Exploring available topics...
   Found 5 topics
   - Technology
     Category: Tech

🧠 Example 6: Vector-based Wikipedia Search
Using semantic search for pages about artificial intelligence...

Found 3 semantically related Wikipedia pages:
  1. Artificial intelligence
     Relevance Score: 92.0%
     URL: https://en.wikipedia.org/wiki/Artificial_intelligence
     Summary: Artificial intelligence (AI) is the capability of computational systems...
     Views per day: 50000
     Wikidata ID: Q11660

🔄 Running async operations...
   Running concurrent async searches...
   ✓ Async articles search: 2 articles
   ✓ Async companies search: 1 companies
   ✓ Async journalists search: 1 journalists

✅ Advanced example completed!
```

## Next Steps

After running these examples:

1. **Explore the [API Documentation](https://perigon.io/docs/api/intro)** for complete endpoint details
2. **Check the test files** in `tests/` for more usage patterns
3. **Build your own application** using these examples as a foundation
4. **Consider rate limiting** and error handling for production use

## Troubleshooting

**"PERIGON_API_KEY not set" error:**
- Make sure you've exported the environment variable in your current shell
- Check that your API key is valid and active

**Import errors:**
- Ensure you've installed the SDK: `pip install perigon`
- Check your Python version (requires Python 3.11+)

**API errors:**
- Verify your API key is correct
- Check your account's API limits
- Review the [API documentation](https://perigon.io/docs/api/intro) for endpoint-specific requirements

## Support

- **Documentation:** [perigon.io](https://perigon.io/docs/api/intro)
- **Issues:** Report bugs or request features on the project repository
- **Questions:** Check the API documentation or contact support 
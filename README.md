## News Scraper and Sentiment Analyzer

This project is a Python-based web scraping tool that extracts news data from multiple URLs, gathers various metadata attributes, and integrates sentiment analysis using Huggingface's transformer models. The scraped data is then saved into a structured JSON file for further analysis.

## Features

- **Web Scraping**: Uses Selenium to scrape news articles from provided URLs.
- **Metadata Extraction**: Extracts important details such as:
  - Title
  - Meta Description
  - Meta Keywords
  - Author
  - News Subcategory
  - Media Type (Online/Newspaper/TV Media, etc.)
  - Published Date
  - Updated Date
  - Article Content
  - Image URL
- **Additional Attributes**: Auto-generates:
  - Sentiment Analysis (positive, negative, or neutral)
  - International Perspective (can be customized via LLM)
  - Importance Score (can be customized via LLM)
  - Age of the article (new or older than 3 days)
  - Views, Rating, and Engagement (default values)

- **Sentiment Analysis**: Uses Huggingface's `distilbert-base-uncased-finetuned-sst-2-english` model to generate sentiment (positive, negative, neutral) from the article content.

- **JSON Output**: All scraped data is saved in a structured JSON file, which includes metadata and analysis results.

## Requirements

Make sure you have the following installed before running the project:

- Python 3.7+
- Selenium
- Huggingface Transformers
- ChromeDriver (for Selenium)
- Google Chrome (latest version)

To install the necessary Python libraries, run:

```bash
pip install -r requirements.txt
```

The `requirements.txt` should contain:

```txt
selenium==<version>
transformers==<version>
torch==<version> # if using a local model for Huggingface
```

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/news-scraper-sentiment.git
   cd news-scraper-sentiment
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup ChromeDriver**:
   Ensure you have [ChromeDriver](https://chromedriver.chromium.org/downloads) installed and accessible in your system path.

4. **Download the Pre-trained Sentiment Model**:
   The sentiment analysis uses Huggingface’s `distilbert-base-uncased-finetuned-sst-2-english`. This is automatically handled when the model is first loaded.

5. **Run the script**:
   You can scrape news articles and analyze sentiment by running the main script:
   ```bash
   python scraper.py
   ```

   The scraped data will be saved as `scraped_metadata_with_sentiment.json`.

## Usage

1. **Initial Scrape**:
   The script first scrapes all relevant links from the target website. The links are filtered based on specific categories and saved in `filtered_links.json`.

2. **Metadata Extraction**:
   After scraping, the script individually visits each article link and extracts the required metadata such as title, description, author, keywords, and content.

3. **Sentiment & International Perspective**:
   The script uses Huggingface to perform sentiment analysis and integrates logic for international perspectives and importance scores (customizable).

4. **Final Output**:
   The results are saved into a JSON file called `scraped_metadata_with_sentiment.json`.

## JSON Structure

The final output file (`scraped_metadata_with_sentiment.json`) will contain the following structure for each news article:

```json
{
    "url": "https://example.com/news/article",
    "title": "Sample News Title",
    "meta_description": "This is a sample meta description.",
    "meta_keywords": "news, sample, example",
    "meta_author": "Author Name",
    "news_subcategory": "Politics",
    "media_type": "Online",
    "image_url": "https://example.com/image.jpg",
    "published_date": "2024-10-19",
    "updated_date": "2024-10-20",
    "last_scraped": "2024-10-19 10:23:00",
    "old": false,
    "sentiment": "positive",
    "views": 0,
    "rating": 0,
    "engagement": 0,
    "author": "Author Name",
    "content": "This is the full content of the article..."
}
```



## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



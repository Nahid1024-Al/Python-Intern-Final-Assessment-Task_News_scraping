from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import json
import time
from transformers import pipeline

# Initialize Huggingface API for sentiment analysis
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Function to analyze sentiment using Huggingface model
def analyze_sentiment_llm(content):
    if len(content) > 0:
        result = sentiment_analyzer(content[:512])  # Analyze the first 512 tokens
        sentiment = result[0]['label'].lower()  # Outputs 'positive', 'negative', or 'neutral'
        return sentiment
    else:
        return "neutral"

# Function to scrape metadata from each link
def scrape_metadata_from_link(link, driver):
    driver.get(link)
    time.sleep(3)  # Wait for the page to load
    
    # Extract the page title
    title = driver.title
    
    # Extract meta tags
    meta_description = ""
    meta_keywords = ""
    meta_tags = driver.find_elements(By.TAG_NAME, 'meta')
    
    for tag in meta_tags:
        name_attr = tag.get_attribute('name')
        if name_attr == 'description':
            meta_description = tag.get_attribute('content')
        elif name_attr == 'keywords':
            meta_keywords = tag.get_attribute('content')
    
# Extract author
    author = ""
    try:
        author_element = driver.find_element(By.XPATH, '//*[@id="inner-wrap"]/div[2]/main/div/div[2]/div[2]/div[1]/div[3]/div/div/div[1]/strong')
        author = author_element.text
    except Exception as e:
        print(f"Author not found for {link}: {e}")
    
    # Extract news subcategory
    news_subcategory = ""
    try:
        subcategory_element = driver.find_element(By.XPATH, '//*[@id="node-267171"]/div[7]/p/a[1]')
        news_subcategory = subcategory_element.text
    except Exception as e:
        print(f"News subcategory not found for {link}: {e}")
    
    # Assume the media_type is 'Online' (adjust logic if needed)
    media_type = "Online"
    
    # Extract image_url
    image_url = ""
    try:
        image_element = driver.find_element(By.XPATH, '//*[@id="node-267171"]/div[3]/span/picture/img')
        image_url = image_element.get_attribute('src')
    except Exception as e:
        print(f"Image URL not found for {link}: {e}")
    
    # Extract published_date
    published_date = ""
    try:
        published_date_element = driver.find_element(By.XPATH, '//*[@id="inner-wrap"]/div[2]/main/div/div[2]/div[2]/div[1]/div[3]/div/div/div[2]')
        published_date = published_date_element.text
    except Exception as e:
        print(f"Published date not found for {link}: {e}")
    
    # Extract updated_date
    updated_date = ""
    try:
        updated_date_element = driver.find_element(By.XPATH, '//*[@id="inner-wrap"]/div[2]/main/div/div[2]/div[2]/div[1]/div[3]/div/div/div[3]')
        updated_date = updated_date_element.text
    except Exception as e:
        print(f"Updated date not found for {link}: {e}")
    
    # Extract full content (assuming content is within the main div)
    content = ""
    try:
        content_element = driver.find_element(By.TAG_NAME, 'article')  # Adjust the tag if needed
        content = content_element.text
    except Exception as e:
        print(f"Content not found for {link}: {e}")
    
    # Generate last_scraped timestamp
    last_scraped = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Determine if the article is old (more than 3 days)
    old = False
    if published_date:
        try:
            # Convert published date to datetime (assuming 'YYYY-MM-DD' format)
            pub_date = datetime.strptime(published_date, '%Y-%m-%d')
            old = (datetime.now() - pub_date).days > 3
        except Exception as e:
            print(f"Error processing published date for {link}: {e}")

    # Use Huggingface models to generate sentiment analysis
    sentiment = analyze_sentiment_llm(content)

    # Set default values for views, rating, and engagement
    views = 0
    rating = 0
    engagement = 0

    # Return the extracted metadata
    return {
        'url': link,
        'title': title,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
        'meta_author': author,
        'news_subcategory': news_subcategory,
        'media_type': media_type,
        'image_url': image_url,
        'published_date': published_date,
        'updated_date': updated_date,
        'last_scraped': last_scraped,
        'old': old,
        'sentiment': sentiment,
        'views': views,
        'rating': rating,
        'engagement': engagement,
        'author': author,
        'content': content
    }

# Main function to scrape data from multiple links
def scrape_news_data(urls):
    # Initialize Chrome with necessary options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    
    # List to store all the metadata
    metadata_list = []

    # Loop through each URL and scrape metadata
    for link in urls:
        try:
            print(f"Scraping {link}...")
            metadata = scrape_metadata_from_link(link, driver)
            metadata_list.append(metadata)
        except Exception as e:
            print(f"Failed to scrape {link}: {e}")
        break
    
    # Close the driver
    driver.quit()

    # Save the metadata to a JSON file
    with open('scraped_metadata_with_sentiment.json', 'w', encoding='utf-8') as f:
        json.dump(metadata_list, f, ensure_ascii=False, indent=4)

    print(f"Metadata for {len(metadata_list)} links saved to 'scraped_metadata_with_sentiment.json'.")

# Load the filtered links from the previous scrape
with open('filtered_links.json', 'r', encoding='utf-8') as f:
    filtered_links = json.load(f)

# Scrape metadata from each link
scrape_news_data(filtered_links)

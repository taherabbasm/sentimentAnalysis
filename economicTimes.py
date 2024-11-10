import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def fetch_news_data(page):
    query = "Nifty-50"
    url = f"https://economictimes.indiatimes.com/topic/{query}/news/{page}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.text

def parse_news_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Debugging: Write HTML content to a file for inspection
    with open('sample_page.html', 'w', encoding='utf-8') as file:
        file.write(soup.prettify())

    articles = soup.find_all('div', class_='slick-slide')
    news_data = []

    if not articles:
        print("No articles found on the page.")

    for article in articles:
        try:
            link_tag = article.find('a', class_='IndicesDetails_newsCard__sq4I7')
            if not link_tag:
                print("No link tag found for an article.")
                continue
            
            # Get the headline
            headline_tag = link_tag.find('p', class_='IndicesDetails_headline__vGhGt')
            if not headline_tag:
                print("No headline tag found for an article.")
                continue
            headline = headline_tag.text.strip()

            # Get the link
            link = link_tag['href']
            if not link.startswith('http'):
                link = "https://economictimes.indiatimes.com" + link

            # Get the date
            date_tag = link_tag.find_next_sibling('span')
            if not date_tag:
                print("No date tag found for an article.")
                continue
            date_str = date_tag.text.strip()
            date = datetime.strptime(date_str, '%d %b, %Y').date()

            news_data.append({
                'Date': date,
                'Headline': headline,
                'Link': link
            })

            # Debugging logs
            print(f"Article found: {headline}, {date}, {link}")

        except Exception as e:
            print(f"Error parsing article: {e}")
            continue

    return news_data

def scrape_nifty50_news(pages=10):
    all_news = []

    for page in range(1, pages + 1):
        print(f"Scraping page {page}")
        html_content = fetch_news_data(page)
        if html_content:
            news_data = parse_news_data(html_content)
            if not news_data:
                print(f"No news data found on page {page}")
            all_news.extend(news_data)
        else:
            print(f"Failed to fetch data for page {page}")

    return all_news

# Define the range of pages you want to scrape
pages = 50  # Adjust as needed

news_data = scrape_nifty50_news(pages)

# Convert to DataFrame
df = pd.DataFrame(news_data)

if not df.empty and 'Date' in df.columns:
    # Convert 'Date' to datetime for filtering
    df['Date'] = pd.to_datetime(df['Date'])

    # Filter for news in the year 2020
    df = df[(df['Date'] >= pd.Timestamp('2020-01-01')) & (df['Date'] <= pd.Timestamp('2020-12-31'))]

    # Save to Excel
    output_file = 'nifty50_news_2020.xlsx'
    df.to_excel(output_file, index=False)

    print(f"Data saved to {output_file}")
else:
    print("No 'Date' column found in the DataFrame or DataFrame is empty. Please check the parsed data.")
    print(df.head())

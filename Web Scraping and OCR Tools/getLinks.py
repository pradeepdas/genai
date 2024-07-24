import requests
from bs4 import BeautifulSoup
import re

def scrape_urls_from_onclick(url):
    # Fetch the content of the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Find all 'li' elements with 'onclick' attribute
    li_elements = soup.find_all('li', onclick=True)

    # Extract URLs from the 'onclick' attributes
    URLs = []
    for li in li_elements:
        onclick_value = li['onclick']
        match = re.search(r"location\.href='(.*?)'", onclick_value)
        if match:
            URLs.append(match.group(1))

    # Save URLs to a text file
    with open('scraped_urls.txt', 'w') as file:
        for url in URLs:
            file.write(url + '\n')

    return URLs

if __name__ == "__main__":
    # Read URLs from a text file
    with open('input_urls.txt', 'r') as file:
        input_urls = [line.strip() for line in file]

    all_scraped_urls = []
    for url in input_urls:
        scraped_urls = scrape_urls_from_onclick(url)
        all_scraped_urls.extend(scraped_urls)
    
    # Save all scraped URLs to a text file
    with open('scraped_urls.txt', 'w') as file:
        for url in all_scraped_urls:
            file.write(url + '\n')

    print("Scraped URLs have been saved to 'scraped_urls.txt'")

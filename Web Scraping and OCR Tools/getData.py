import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_and_store_content(url, article_number):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract main text from <p> and <span> tags
    paragraphs = soup.find_all(['p', 'span'])
    main_text = '\n'.join([element.get_text() for element in paragraphs])

    # Extract images, ignoring those with 'logo' or 'gmail_icon' in the filename
    images = soup.find_all('img')
    image_urls = [
        urljoin(url, img['src']) for img in images
        if 'src' in img.attrs and 'logo' not in img['src'].lower() and 'gmail_icon.ico' not in img['src'].lower()
    ]

    # Create directory for the article
    article_dir = f'article_{article_number}'
    os.makedirs(article_dir, exist_ok=True)

    # Save main text to a file
    with open(os.path.join(article_dir, 'text.txt'), 'w', encoding='utf-8') as text_file:
        text_file.write(main_text)

    # Save images
    for i, img_url in enumerate(image_urls, start=1):
        img_response = requests.get(img_url)
        img_path = os.path.join(article_dir, f'image_{i}.jpg')
        with open(img_path, 'wb') as img_file:
            img_file.write(img_response.content)

def main():
    try:
        with open('scraped_urls.txt', 'r') as file:
            urls = file.readlines()

        article_count = 1
        for url in urls:
            url = url.strip()
            if url:
                try:
                    fetch_and_store_content(url, article_count)
                    print(f'Content saved in article_{article_count} directory.')
                    article_count += 1
                except Exception as e:
                    print(f'Failed to process the URL {url}: {e}')
    except FileNotFoundError:
        print('The file urls.txt was not found.')

if __name__ == '__main__':
    main()

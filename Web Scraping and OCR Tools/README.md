# Web Scraping and OCR Tools

This repository contains several Python scripts for web scraping and image processing. These scripts fetch URLs, extract text and images, and process images to extract text using OCR.

## Project Structure

- **getData.py**: Fetches content from given URLs, extracts main text and images, and stores them in separate directories.
- **getLinks.py**: Scrapes URLs from 'onclick' attributes of `li` elements in the given URLs.
- **imageToText.py**: Processes images in a specified directory to extract text using Tesseract OCR.
- **mergeText.py**: Merges all text files into a single JSON file.
- **text2json.py**: Converts the text from the merged file into JSON format.
- **image_2_text.txt**: Stores the extracted text from the images.
- **merged_text.txt**: Stores the merged text from all extracted texts.
- **input_urls.txt**: A file containing URLs to be scraped.
- **scraped_urls.txt**: A file containing URLs scraped from the input URLs.

## Prerequisites

- Python 3.x
- Required Python packages:
  - requests
  - beautifulsoup4
  - pytesseract
  - Pillow

You can install the required packages using the following command:

```bash
pip install requests beautifulsoup4 pytesseract pillow
```

Additionally, you need to install Tesseract OCR. You can download it from [here](https://github.com/tesseract-ocr/tesseract).

## Usage

### 1. getLinks.py

This script scrapes URLs from 'onclick' attributes of `li` elements in the provided URLs and saves them to a file.

```bash
python getLinks.py
```

- Create a file named `input_urls.txt` and add the URLs you want to scrape, one per line.
- Run the script.

The scraped URLs will be saved in `scraped_urls.txt`.

### 2. getData.py

This script fetches content from URLs, extracts main text and images, and stores them in separate directories.

```bash
python getData.py
```

- Ensure `scraped_urls.txt` (created from the previous step) is in the same directory.
- Run the script.

The content will be saved in directories named `article_1`, `article_2`, etc.

### 3. imageToText.py

This script processes images in a specified directory to extract text using Tesseract OCR.

```bash
python imageToText.py
```

- Update the `article_dir` variable to point to the directory containing your images.
- Run the script.

The extracted text will be saved in text files with the same names as the images, and the original images will be deleted.

### 4. mergeText.py

This script merges text files into a single JSON file.

```bash
python mergeText.py
```

- Ensure `image_2_text.txt` contains the extracted text.
- Run the script.

The merged text will be saved in `merged_text.txt`.

### 5. text2json.py

This script converts the merged text file into a JSON format.

```bash
python text2json.py
```

- Ensure `merged_text.txt` contains the text to be converted.
- Run the script.

The JSON data will be saved in `textData.json`.

## Configuration

- Update the Tesseract executable path in `imageToText.py` to match your Tesseract installation.

```python
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
```

- Update the `article_dir` variable in `imageToText.py` to point to the directory containing your images.

```python
article_dir = 'C:/Users/aiman/Documents/thankful2plants/Articles'
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Tesseract OCR
- BeautifulSoup
- Requests


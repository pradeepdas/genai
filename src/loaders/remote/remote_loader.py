# Required packages
# pip install requests PyPDF2 python-docx pyyaml pandas beautifulsoup4 wikipedia-api

import requests
import PyPDF2
import docx
import json
import yaml
import csv
import pandas as pd
import xml.etree.ElementTree as ET
from io import StringIO, BytesIO
from zipfile import ZipFile
from bs4 import BeautifulSoup
import wikipedia
import datetime

def load_content(url, file_format="auto", is_timeseries=False):
    """
    Load content from a URL and return it in structured JSON format.
    
    Args:
    url (str): The URL to load the content from.
    file_format (str): The format of the file (auto, text/html, application/pdf, application/msword,
                       application/json, application/x-yaml, text/csv, application/zip).
                       Default is "auto" for automatic detection.
    is_timeseries (bool): Whether the CSV content should be treated as timeseries data. Default is False.
    
    Returns:
    str: JSON string with metadata and content.
    
    Metadata format:
    {
        'original_url': str,         # The original URL of the content
        'content_type': str,         # The detected or specified content type
        'date_accessed': str,        # The date and time when the content was accessed
        'error_code': int,           # Error code (0 for success, 1 for unsupported file type, 2 for processing error)
        'treatment_applied': str     # Description of the processing applied
    }
    """
    if file_format == "auto":
        response = requests.head(url, allow_redirects=True)
        content_type = response.headers.get('content-type')
    else:
        content_type = file_format

    try:
        if 'text/html' in content_type:
            content = load_web_page(url)
        elif 'application/pdf' in content_type:
            content = load_online_pdf(url)
        elif 'application/msword' in content_type or 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in content_type:
            content = load_doc_file(url)
        elif 'application/json' in content_type or 'text/json' in content_type:
            content = load_json(url)
        elif 'application/x-yaml' in content_type or 'text/yaml' in content_type:
            content = load_yaml(url)
        elif 'text/csv' in content_type:
            content = load_csv(url, is_timeseries)
        elif 'application/zip' in content_type:
            content = load_apple_health_data(url)
        else:
            content = "Unsupported file type"
            error_code = 1
    except Exception as e:
        content = str(e)
        error_code = 2
    else:
        error_code = 0

    metadata = {
        'original_url': url,
        'content_type': content_type,
        'date_accessed': str(datetime.datetime.now()),
        'error_code': error_code,
        'treatment_applied': 'Loaded and parsed' if error_code == 0 else 'Error in processing'
    }

    result = {
        'metadata': metadata,
        'content': content
    }
    return json.dumps(result, indent=2)

def load_web_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

def load_online_pdf(url):
    response = requests.get(url)
    with open('temp.pdf', 'wb') as f:
        f.write(response.content)
    with open('temp.pdf', 'rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        text = ''
        for page in range(reader.numPages):
            text += reader.getPage(page).extract_text()
    return {'type': 'blob', 'data': text}

def load_doc_file(url):
    response = requests.get(url)
    with open('temp.docx', 'wb') as f:
        f.write(response.content)
    doc = docx.Document('temp.docx')
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return {'type': 'blob', 'data': text}

def load_json(url):
    response = requests.get(url)
    data = response.json()
    return data

def load_yaml(url):
    response = requests.get(url)
    data = yaml.safe_load(response.text)
    return data

def load_csv(url, is_timeseries=False):
    response = requests.get(url)
    csvfile = StringIO(response.text)
    if is_timeseries:
        df = pd.read_csv(csvfile, parse_dates=True, index_col=0)
        return df.to_dict(orient='records')
    else:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]
        return rows

def load_apple_health_data(url):
    response = requests.get(url)
    zipfile = ZipFile(BytesIO(response.content))
    health_data = {}
    for file in zipfile.namelist():
        if file.endswith('.xml'):
            with zipfile.open(file) as xml_file:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                data = []
                for record in root.findall('Record'):
                    data.append(record.attrib)
                health_data[file] = data
    return health_data

def get_wiki_docs(query):
    summary = wikipedia.summary(query)
    return summary

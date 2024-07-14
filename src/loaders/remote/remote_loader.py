# Remote loader 

import requests
import PyPDF2
import docx
import json
import yaml
import csv
from io import StringIO
from bs4 import BeautifulSoup
import wikipedia

def load_content(url):
    response = requests.head(url, allow_redirects=True)
    content_type = response.headers.get('content-type')

    if 'text/html' in content_type:
        return load_web_page(url)
    elif 'application/pdf' in content_type:
        return load_online_pdf(url)
    elif 'application/msword' in content_type or 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in content_type:
        return load_doc_file(url)
    elif 'application/json' in content_type or 'text/json' in content_type:
        return load_json(url)
    elif 'application/x-yaml' in content_type or 'text/yaml' in content_type:
        return load_yaml(url)
    elif 'text/csv' in content_type:
        return load_csv(url)
    else:
        return "Unsupported file type"

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
    return text

def load_doc_file(url):
    response = requests.get(url)
    with open('temp.docx', 'wb') as f:
        f.write(response.content)
    doc = docx.Document('temp.docx')
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return text

def load_json(url):
    response = requests.get(url)
    data = response.json()
    return json.dumps(data, indent=2)

def load_yaml(url):
    response = requests.get(url)
    data = yaml.safe_load(response.text)
    return yaml.dump(data, default_flow_style=False)

def load_csv(url):
    response = requests.get(url)
    csvfile = StringIO(response.text)
    reader = csv.reader(csvfile)
    rows = [row for row in reader]
    return rows

def get_wiki_docs(query):
    summary = wikipedia.summary(query)
    return summary

# Example usage
url = 'https://example.com/somefile.json'
content = load_content(url)
print(content)

# Required packages
#!pip install requests PyPDF2 python-docx pyyaml pandas beautifulsoup4 wikipedia-api

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
from collections import defaultdict
from requests.auth import HTTPBasicAuth

class ContentLoader:
    def __init__(self, url, file_format="auto", auth=None):
        """
        Initialize the ContentLoader.

        Args:
        url (str): The URL to load the content from.
        file_format (str): The format of the file (auto, html, pdf, docx, json, yaml, csv, xml, zip, apple_health).
                           Default is "auto" for automatic detection.
        auth (dict): Dictionary containing authentication method and credentials. Default is None.
                     Example: {'type': 'basic', 'username': 'user', 'password': 'pass'}
        """
        self.url = url
        self.file_format = file_format
        self.auth = self.configure_auth(auth)
        self.content_type = self.detect_content_type() if file_format == "auto" else file_format
        self.metadata = {
            'original_url': url,
            'content_type': self.content_type,
            'date_accessed': str(datetime.datetime.now()),
            'error_code': None,
            'treatment_applied': None
        }

    def configure_auth(self, auth):
        if auth:
            if auth['type'] == 'basic':
                return HTTPBasicAuth(auth['username'], auth['password'])
            elif auth['type'] == 'bearer':
                return {'Authorization': f"Bearer {auth['token']}"}
            elif auth['type'] == 'api_key':
                return {'Authorization': f"Token {auth['token']}"}
        return None

    def detect_content_type(self):
        headers = self.auth if isinstance(self.auth, dict) else None
        auth = None if isinstance(self.auth, dict) else self.auth
        response = requests.head(self.url, allow_redirects=True, headers=headers, auth=auth)
        return response.headers.get('content-type')

    def load_content(self):
        try:
            if 'html' in self.content_type:
                content = self.load_web_page()
            elif 'pdf' in self.content_type:
                content = self.load_online_pdf()
            elif 'msword' in self.content_type or 'officedocument.wordprocessingml.document' in self.content_type:
                content = self.load_doc_file()
            elif 'json' in self.content_type or self.content_type == 'json':
                content = self.load_json()
            elif 'yaml' in self.content_type or self.content_type == 'yaml':
                content = self.load_yaml()
            elif 'csv' in self.content_type:
                content = self.load_csv()
            elif 'xml' in self.content_type or self.content_type == 'xml':
                content = self.load_xml()
            elif 'zip' in self.content_type or self.content_type == 'zip':
                content = self.load_zip_file()
            elif 'apple_health' in self.content_type or self.content_type == 'apple_health':
                content = self.load_zip_file(is_apple_health=True)
            else:
                content = "Unsupported file type"
                self.metadata['error_code'] = 1
        except Exception as e:
            content = str(e)
            self.metadata['error_code'] = 2
        else:
            self.metadata['error_code'] = 0

        self.metadata['treatment_applied'] = 'Loaded and parsed' if self.metadata['error_code'] == 0 else 'Error in processing'
        result = {
            'metadata': self.metadata,
            'content': content
        }
        return json.dumps(result, indent=2)

    def load_web_page(self):
        headers = self.auth if isinstance(self.auth, dict) else None
        auth = None if isinstance(self.auth, dict) else self.auth
        response = requests.get(self.url, headers=headers, auth=auth)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()

    def load_online_pdf(self):
        headers = self.auth if isinstance(self.auth, dict) else None
        auth = None if isinstance(self.auth, dict) else self.auth
        response = requests.get(self.url, headers=headers, auth=auth)
        with open('temp.pdf', 'wb') as f:
            f.write(response.content)
        with open('temp.pdf', 'rb') as f:
            reader = PyPDF2.PdfFileReader(f)
            text = ''
            for page in range(reader.numPages):
                text += reader.getPage(page).extract_text()
        return {'type': 'blob', 'data': text}

    def load_doc_file(self):
        headers = self.auth if isinstance(self.auth, dict) else None
        auth = None if isinstance(self.auth, dict) else self.auth
        response = requests.get(self.url, headers=headers, auth=auth)
        with open('temp.docx', 'wb') as f:
            f.write(response.content)
        doc = docx.Document('temp.docx')
        text = ''
        for paragraph in doc.paragraphs:
            text += paragraph.text
        return {'type': 'blob', 'data': text}

    def load_json(self):
        headers = self.auth if isinstance(self.auth, dict) else None
        auth = None if isinstance(self.auth, dict) else self.auth
        response = requests.get(self.url, headers=headers, auth=auth)
        data = response.json()
        return data

    def load_yaml(self):
        headers = self.auth if isinstance(self.auth, dict) else None
        auth = None if isinstance(self.auth, dict) else self.auth
        response = requests.get(self.url, headers=headers, auth=auth)
        data = yaml.safe_load(response.text)
        return data

    def load_csv(self):
        headers = self.auth if isinstance(self.auth, dict) else None
        auth = None if isinstance(self.auth, dict) else self.auth
        response = requests.get(self.url, headers=headers, auth=auth)
        csvfile = StringIO(response.text)
        df = pd.read_csv(csvfile, parse_dates=True, index_col=0)
        return df.to_dict(orient='records')

    def load_xml(self):
        headers = self.auth if isinstance(self.auth, dict) else None
        auth = None if isinstance(self.auth, dict) else self.auth
        response = requests.get(self.url, headers=headers, auth=auth)
        tree = ET.ElementTree(ET.fromstring(response.content))
        root = tree.getroot()
        return self.parse_xml_element(root)

    def parse_xml_element(self, element):
        data = {element.tag: {} if element.attrib else None}
        children = list(element)
        if children:
            dd = defaultdict(list)
            for dc in map(self.parse_xml_element, children):
                for k, v in dc.items():
                    dd[k].append(v)
            data = {element.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
        if element.attrib:
            data[element.tag].update(('@' + k, v) for k, v in element.attrib.items())
        if element.text:
            text = element.text.strip()
            if children or element.attrib:
                if text:
                    data[element.tag]['#text'] = text
            else:
                data[element.tag] = text
        return data

    def load_zip_file(self, is_apple_health=False):
        headers = self.auth if isinstance(self.auth, dict) else None
        auth = None if isinstance(self.auth, dict) else self.auth
        response = requests.get(self.url, headers=headers, auth=auth)
        zipfile = ZipFile(BytesIO(response.content))
        if is_apple_health:
            return self.load_apple_health_data(zipfile)
        else:
            return self.load_standard_zip(zipfile)

    def load_apple_health_data(self, zipfile):
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

    def load_standard_zip(self, zipfile):
        file_data = {}
        for file in zipfile.namelist():
            with zipfile.open(file) as f:
                file_data[file] = f.read().decode('utf-8')
        return file_data

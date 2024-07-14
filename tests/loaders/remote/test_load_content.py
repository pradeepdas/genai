import unittest
from loaders.remote.remote_loader import ContentLoader

class TestContentLoader(unittest.TestCase):

    def setUp(self):
        self.urls = {
            'html': 'https://www.example.com',
            'pdf': 'https://arxiv.org/pdf/2101.06869.pdf',
            'docx': 'https://calibre-ebook.com/downloads/demos/demo.docx',
            'json': 'https://jsonplaceholder.typicode.com/todos/1',
            'yaml': 'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/examples/v3.0/petstore.yaml',
            'csv': 'https://people.sc.fsu.edu/~jburkardt/data/csv/hw_200.csv',  # Sample CSV file
            'xml': 'https://www.w3schools.com/xml/note.xml',  # Example XML file
            'apple_health': 'https://github.com/HealthKitSampleData/HealthKitSampleData/blob/master/SampleData.zip?raw=true',
            'standard_zip': 'https://github.com/HealthKitSampleData/HealthKitSampleData/blob/master/SampleData.zip?raw=true'
        }

    def test_load_html(self):
        loader = ContentLoader(self.urls['html'], file_format='html')
        content = loader.load_content()
        self.assertIn('html', content)

    def test_load_pdf(self):
        loader = ContentLoader(self.urls['pdf'], file_format='pdf')
        content = loader.load_content()
        self.assertIn('blob', content)

    def test_load_docx(self):
        loader = ContentLoader(self.urls['docx'], file_format='docx')
        content = loader.load_content()
        self.assertIn('blob', content)

    def test_load_json(self):
        loader = ContentLoader(self.urls['json'], file_format='json')
        content = loader.load_content()
        self.assertIn('userId', content)

    def test_load_yaml(self):
        loader = ContentLoader(self.urls['yaml'], file_format='yaml')
        content = loader.loa

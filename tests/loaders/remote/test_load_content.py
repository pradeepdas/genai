from loader import load_content, get_wiki_docs

# Example usage with different URLs for each file type
urls = {
    'html': 'https://www.example.com',
    'pdf': 'https://arxiv.org/pdf/2101.06869.pdf',
    'docx': 'https://calibre-ebook.com/downloads/demos/demo.docx',
    'json': 'https://jsonplaceholder.typicode.com/todos/1',
    'yaml': 'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/examples/v3.0/petstore.yaml',
    'csv': 'https://people.sc.fsu.edu/~jburkardt/data/csv/hw_200.csv',  # Sample CSV file
    'apple_health': 'https://github.com/HealthKitSampleData/HealthKitSampleData/blob/master/SampleData.zip?raw=true',
    'wiki': 'Python (programming language)'
}

for filetype, url in urls.items():
    if filetype == 'wiki':
        content = get_wiki_docs(url)
    else:
        content = load_content(url, is_timeseries=(filetype == 'csv'))
    print(f"Content for {filetype}:")
    print(content)
    print("\n" + "="*50 + "\n")

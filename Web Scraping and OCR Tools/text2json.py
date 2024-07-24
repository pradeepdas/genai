import json
import re

# Read the content from the file
with open('merged_text.txt', 'r') as file:
    content = file.read()

# Split the content into individual articles
articles = re.split(r'Text from article_\d+:', content)[1:]  # Skip the first empty split result

# Create a list of dictionaries for each article
articles_list = []
for index, article in enumerate(articles):
    article_data = {
        "title": f"Text from article_{index + 1}",
        "content": article.strip()
    }
    articles_list.append(article_data)

# Create the final JSON structure
data = {
    "articles": articles_list
}

# Write the JSON data to a file
with open('textData.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print("JSON file created successfully.")

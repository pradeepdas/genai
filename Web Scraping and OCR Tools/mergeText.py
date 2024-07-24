import os
import json

def merge_text_files_to_json(root_dir, output_file_path):
    articles_data = {}
    
    # Iterate through all subdirectories
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.txt'):
                file_path = os.path.join(subdir, file)
                # Extract the article number from the subdirectory name
                article_number = os.path.basename(subdir).split('_')[-1]
                if not article_number.isdigit():
                    print(f"Skipping folder {subdir} due to non-numeric article number.")
                    continue
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        file_content = f.read().strip()  # Remove leading/trailing whitespaces
                        # Store the content in a dictionary
                        if article_number not in articles_data:
                            articles_data[article_number] = []
                        articles_data[article_number].append(file_content)
                        print(f"Processed file: {file_path}")
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
    
    # Write the combined data to a JSON file
    try:
        with open(output_file_path, "w", encoding='utf-8') as json_file:
            json.dump({"Articles": articles_data}, json_file, ensure_ascii=False, indent=4)
        print(f"Text has been merged and saved to {output_file_path}")
    except Exception as e:
        print(f"Error writing to output file {output_file_path}: {e}")

# Root directory containing article subfolders with .txt files
root_dir = r"C:\Users\aiman\Documents\thankful2plants\Articles\Articles"

# Output file path
output_file_path = r"C:\Users\aiman\Documents\thankful2plants\merged_text.json"

# Merge text from all .txt files in articles subfolders and save to a JSON file
merge_text_files_to_json(root_dir, output_file_path)

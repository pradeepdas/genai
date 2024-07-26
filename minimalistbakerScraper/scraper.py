from bs4 import BeautifulSoup
import requests
import json
import re
# Function to get a list of URLs from a file
def get_urls_from_file(filepath):
    with open(filepath, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    return urls

# Function to parse the nutrition information
def parse_nutrition_info(nutrition_text):
    nutrition_data = {}
    # Split the text on specific points, ensuring correct key-value pairs
    parts = re.split(r'(?<=\d)(?=[A-Z])', nutrition_text)
    current_label = None
    
    for part in parts:
        if ':' in part:
            label, value = part.split(':', 1)
            label = label.strip()
            value = value.strip()
            nutrition_data[label] = value
            current_label = label
        elif current_label:
            nutrition_data[current_label] += ' ' + part.strip()
    
    return nutrition_data

# Function to parse the total time
def parse_total_time(total_time_text):
    return ' '.join(sorted(set(total_time_text.split()), key=total_time_text.split().index))

# Function to scrape recipe data from a list of URLs
def scrape_recipe_data(article_urls):
    recipes = []

    for url in article_urls[:1555]:
        print(f"Scraping URL: {url}")
        
        page_content = requests.get(url)
        soup = BeautifulSoup(page_content.content, 'html.parser')
        
        try:
            title = soup.select_one('.wprm-recipe-name').text.strip()
        except AttributeError:
            title = "Title not found"
        
        try:
            description = soup.select_one('.wprm-recipe-summary > span:nth-child(1)').text.strip()
        except AttributeError:
            description = "Description not found"

        try:
            prep_time = soup.select_one('.wprm-recipe-prep_time').text.strip()
        except AttributeError:
            prep_time = "Prep time not found"
        
        try:
            total_time_selector = "div.wprm-recipe-time-container:nth-child(2) > span:nth-child(2)"
            total_time_text = soup.select_one(total_time_selector).text.strip()
            total_time = parse_total_time(total_time_text)
        except AttributeError:
            total_time = "Total time not found"
        
        try:
            servings = soup.select_one('.wprm-recipe-servings').text.strip()
        except AttributeError:
            servings = "Servings not found"

        try:
            course = soup.select_one('.wprm-recipe-course').text.strip()
        except AttributeError:
            course = "Course not found"

        try:
            cuisine = soup.select_one('.wprm-recipe-cuisine').text.strip()
        except AttributeError:
            cuisine = "Cuisine not found"
        
        ingredients = []
        try:
            ingredient_sections = soup.select('.wprm-recipe-ingredient-group')
            for section in ingredient_sections:
                group_name = section.select_one('.wprm-recipe-group-name')
                if group_name:
                    group_name = group_name.text.strip()
                else:
                    group_name = "Main Ingredients"

                group_ingredients = section.select('li.wprm-recipe-ingredient')
                ingredients_list = [ingredient.get_text(separator=" ", strip=True) for ingredient in group_ingredients]

                ingredients.append({
                    'group_name': group_name,
                    'ingredients': ingredients_list
                })
        except AttributeError:
            ingredients = [{"group_name": "Ingredients not found", "ingredients": []}]
        
        try:
            instructions = soup.select('div.wprm-recipe-instruction-text')
            instructions_list = [instruction.get_text(separator=" ", strip=True) for instruction in instructions]
        except AttributeError:
            instructions_list = ["Instructions not found"]
        
        try:
            notes = soup.select_one('.wprm-recipe-notes').text.strip()
        except AttributeError:
            notes = "Notes not found"
        
        try:
            nutrition_text = soup.select_one('.wprm-nutrition-label-container').get_text(separator=" ", strip=True)
            nutrition = parse_nutrition_info(nutrition_text)
        except AttributeError:
            nutrition = "Nutrition information not found"
        
        recipes.append({
            'title': title,
            'description': description,
            'prep_time': prep_time,
            'total_time': total_time,
            'servings': servings,
            'course': course,
            'cuisine': cuisine,
            'ingredients': ingredients,
            'instructions': instructions_list,
            'notes': notes,
            'nutrition': nutrition
        })
        print(f"Scraped data for URL: {url}\n")

    print(f"Total recipes scraped: {len(recipes)}")
    return recipes

# Function to save data to a JSON file
def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")

# Example usage
file_path = r'C:\Users\aiman\Documents\thankful2plants\article_urls.txt'
article_urls = get_urls_from_file(file_path)

# Debug: Confirm the first URL
print(f"First URL to scrape: {article_urls[0]}")

recipe_data = scrape_recipe_data(article_urls)
save_to_json(recipe_data, 'recipes.json')

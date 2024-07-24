import os
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

# Specify the path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    try:
        image = Image.open(image_path)
        # Convert image to grayscale
        image = image.convert('L')
        # Apply some filters
        image = image.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)
        # Resize image if needed
        image = image.resize((image.width * 2, image.height * 2), Image.LANCZOS)
        return image
    except Exception as e:
        print(f"Error preprocessing image {image_path}: {e}")
        return None

def extract_text_from_image(image_path):
    try:
        # Preprocess image
        image = preprocess_image(image_path)
        if image is None:
            return ""
        # Extract text from image
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error extracting text from image {image_path}: {e}")
        return ""

def extract_text_from_articles(root_dir, output_file_path):
    combined_text = ""
    
    for i in range(1, 2279):
        subdir = os.path.join(root_dir, f"article_{i}")
        if os.path.exists(subdir) and os.path.isdir(subdir):
            print(f"Processing directory: {subdir}")
            for file in os.listdir(subdir):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                    image_path = os.path.join(subdir, file)
                    print(f"Processing image: {image_path}")
                    text = extract_text_from_image(image_path)
                    if text:
                        combined_text += f"Text from {image_path}:\n{text}\n\n"
                    else:
                        print(f"Skipping image {image_path} due to extraction failure.")
    
    # Save combined text to a file
    with open(output_file_path, "w") as file:
        file.write(combined_text)
    
    print(f"Text has been extracted and saved to {output_file_path}")

# Root directory containing articles subfolders
root_dir = r"C:\Users\aiman\Documents\thankful2plants\Articles\Articles"

# Output file path
output_file_path = r"C:\Users\aiman\Documents\thankful2plants\Articles\Articles\image_2_text.txt"

# Extract text from all images in articles subfolders and save to file
extract_text_from_articles(root_dir, output_file_path)

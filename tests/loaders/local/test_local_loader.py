from src.loaders.local.local_loader import get_document_text, load_txt_files, load_csv_files

if __name__ == "__main__":
    base_path = "tests/test_data/"
    example_pdf_path = base_path + "healthy_meal_10_tips.pdf"
    docs = get_document_text(open(example_pdf_path, "rb"))
    for doc in docs:
        print(doc)
    example_pdf_path = base_path + "cardio_diabetes_guideline1.pdf"
    docs = get_document_text(open(example_pdf_path, "rb"))
    for doc in docs:
        print(doc)
    docs = get_document_text(open(base_path + "us_army_recipes.txt", "rb"))
    for doc in docs:
        print(doc)
    txt_docs = load_txt_files(base_path)
    for doc in txt_docs:
        print(doc)
    csv_docs = load_csv_files(base_path)
    for doc in csv_docs:
        print(doc)
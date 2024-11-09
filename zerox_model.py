from PIL import Image
import pytesseract
import sqlite3
import re
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database setup (SQLite)
def init_db():
    conn = sqlite3.connect("passport_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passport_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn

# Function to insert extracted name into the database
def insert_name_to_db(conn, name):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passport_info (name) VALUES (?)", (name,))
    conn.commit()

# Function to extract name using regex
def extract_name_from_text(text):
    # Regular expression for typical name format in passports
    name_pattern = re.compile(r'(?i)name\s*[:\s]*([A-Z\s]+)')
    match = name_pattern.search(text)
    if match:
        return match.group(1).strip()
    return None

# Function to perform OCR on JPEG image
def perform_ocr(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        st.error(f"Failed to extract text from image: {e}")
        return ""

# Streamlit UI for file upload
def main():
    st.title("Passport Name Extraction from JPEG")

    uploaded_file = st.file_uploader("Upload Passport Image (JPEG)", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Save the uploaded file temporarily
        input_doc_path = f"./temp/{uploaded_file.name}"
        os.makedirs("./temp", exist_ok=True)
        with open(input_doc_path, "wb") as f:
            f.write(uploaded_file.read())

        st.info("Performing OCR to extract text from image...")
        ocr_text = perform_ocr(input_doc_path)

        # Display extracted text
        st.write("Extracted Text:")
        st.text(ocr_text)

        # Extract name using regex
        extracted_name = extract_name_from_text(ocr_text)
        if extracted_name:
            st.write(f"Extracted Name: {extracted_name}")

            # Store extracted name in the database
            conn = init_db()
            insert_name_to_db(conn, extracted_name)
            st.success("Name successfully stored in the database.")
        else:
            st.error("Could not extract the name from the text.")

if __name__ == "__main__":
    main()

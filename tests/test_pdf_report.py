import pdfplumber
import pandas as pd
import pytest
import json
import os
import csv
from pdf2image import convert_from_path
import pytesseract

def load_config(config_file="config.json"):
    config_path = os.path.join(os.path.dirname(__file__), config_file)
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r") as file:
        config = json.load(file)

    return config

config = load_config()

# Dynamically load paths from config
pdf_path = config["production_pdf"]
output_csv_path = config["output_csv_path"]
# output_json_path = config["output_json_path"]

print(f"PDF Path: {pdf_path}")
print(f"Output CSV Path: {output_csv_path}")
# print(f"Output JSON Path: {output_json_path}")


# Extract text from a PDF
"""
def extract_text_with_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image) + "\n"
    print("Extracted Text:", text)
    return text

def process_text_to_table(raw_text):
    rows = raw_text.split("\n")
    structured_data = [row.split() for row in rows if row.strip()]  # Adjust split logic as needed
    return structured_data

raw_text = extract_text_from_pdf(pdf_path)
table = process_text_to_table(raw_text)
print("Structured Data:", table)
"""

# Extract text and save it to a CSV file, one line per row.
"""
def extract_text_by_line_to_csv(pdf_path, output_csv_path):
    
    with pdfplumber.open(pdf_path) as pdf:
        lines = []
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                lines.extend(page_text.split("\n"))

    with open(output_csv_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Production Data"])  # Header
        for line in lines:
            writer.writerow([line])

extract_text_by_line_to_csv(pdf_path, output_csv_path)

print(f"Text extracted and saved to {output_csv_path}")

"""

# Extract text and organize in a table, save it to a CSV file

def extract_text_and_process(pdf_path):
    structured_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            raw_text = page.extract_text()

            if not raw_text:
                print(f"No text found on page {page_number}. Skipping...")
                continue

            # Split text into lines and process
            lines = raw_text.split("\n")

            # Ignore the first two lines (as per your requirement)
            lines = lines[2:]

            for line in lines:
                # Split the line into fields by whitespace
                row = line.split()
                structured_data.append(row)

    if not structured_data:
        raise ValueError("No data extracted from the PDF.")

    # Dynamically find the longest row to determine the number of columns
    max_columns = max(len(row) for row in structured_data)
    print(f"Maximum columns detected: {max_columns}")

    # Handle header and data
    header = structured_data[0] if len(structured_data[0]) == max_columns else ["Column" + str(i) for i in range(max_columns)]
    data_rows = structured_data[1:]

    # Normalize rows to match the header length
    normalized_rows = [row + [""] * (max_columns - len(row)) for row in data_rows]

    # Create DataFrame
    df = pd.DataFrame(normalized_rows, columns=header)
    return df

def save_to_csv(df, output_csv_path):
    df.to_csv(output_csv_path, index=False)
    print(f"Data saved to {output_csv_path}")

try:
    # Extract and organize data from PDF
    data_df = extract_text_and_process(pdf_path)

    # Save the organized data to a CSV file
    save_to_csv(data_df, output_csv_path)

    print("Extracted Data:\n", data_df.head())
except Exception as e:
    print(f"Error during extraction: {e}")
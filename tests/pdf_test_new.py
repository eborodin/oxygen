import pytest
import pdfplumber
import pandas as pd
from pandas import DataFrame
import os
import json
from pdf2image import convert_from_path
from PIL import Image
import pytesseract



def get_dynamic_path_from_config(key):
    # Define the path to config.json (assumes it's in the same directory as this script)
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    # Load the configuration
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    # Retrieve the value associated with the key
    if key not in config:
        raise KeyError(f"Key '{key}' not found in configuration file.")
    return config[key]

# Fixtures for production and staging PDF data
@pytest.fixture
def production_pdf_data():
    production_pdf_path = get_dynamic_path_from_config("production_pdf_file")
    assert os.path.exists(production_pdf_path), f"File not found: {production_pdf_path}"
    return extract_table_from_pdf(production_pdf_path)

@pytest.fixture
def staging_pdf_data():
    staging_pdf_path = get_dynamic_path_from_config("staging_pdf_file")
    assert os.path.exists(staging_pdf_path), f"File not found: {staging_pdf_path}"
    return extract_table_from_pdf(staging_pdf_path)

# Function to extract tables from a PDF
def extract_table_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        data = []
        for page_num, page in enumerate(pdf.pages, start=1):
            print(f"Extracting data from page {page_num} of {pdf_path}")
            tables = page.extract_tables()
            if not tables:
                print(f"No tables found on page {page_num}.")
            else:
                print(f"Tables found on page {page_num}: {tables}")
                for table in tables:
                    data.extend(table)
    # If no data was extracted, return an empty DataFrame
    if not data:
        print(f"No tables extracted from {pdf_path}.")
        return pd.DataFrame()
    # Convert to DataFrame and set the first row as header
    df = pd.DataFrame(data)
    df.columns = df.iloc[0]  # Set first row as header
    df = df[1:].reset_index(drop=True)  # Remove the header row
    return df

# Test for column name consistency
@pytest.mark.pdf
def test_pdf_column_names(production_pdf_data, staging_pdf_data):
    # Ensure DataFrames are not empty before comparing columns
    assert not production_pdf_data.empty, "Production PDF data is empty"
    assert not staging_pdf_data.empty, "Staging PDF data is empty"
    assert list(production_pdf_data.columns) == list(staging_pdf_data.columns), "Column structure mismatch in PDFs"

"""
# OCR Example: Convert PDF pages to images and extract text
def test_ocr_production_pdf():
    # Get the production PDF path dynamically from config.json
    production_pdf_path = get_dynamic_path_from_config("production_pdf_file")

    # Convert PDF pages to images
    images = convert_from_path(production_pdf_path)

    for i, image in enumerate(images):
        # Save each page as an image
        image_path = f'page_{i + 1}.png'
        image.save(image_path, 'PNG')
        print(f"Saved page {i + 1} as {image_path}")

    # Example: Extract text from the first page for validation
    text = pytesseract.image_to_string(images[0])  # Assuming the first page exists
    print("Extracted text from page 1:")
    print(text)


@pytest.mark.pdf
def test_pdf_column_names(production_pdf_data, staging_pdf_data):
    # Ensure DataFrames are not empty before comparing columns
    assert not production_pdf_data.empty, "Production PDF data is empty"
    assert not staging_pdf_data.empty, "Staging PDF data is empty"
#    assert list(production_pdf_data.columns) == list(staging_pdf_data.columns), "Column structure mismatch in PDFs"

@pytest.mark.pdf
def test_pdf_column_names(production_pdf_data, staging_pdf_data):
    # Validate that the data is not empty
    assert not production_pdf_data.empty, "Production PDF data is empty"
    assert not staging_pdf_data.empty, "Staging PDF data is empty"

    # Compare column names
    assert list(production_pdf_data.columns) == list(staging_pdf_data.columns), "Column structure mismatch in PDFs"

# Test: Handle Empty PDFs
@pytest.mark.pdf
def test_pdf_column_names(production_pdf_data, staging_pdf_data):
    if production_pdf_data.empty or staging_pdf_data.empty:
        pytest.skip("One or both PDFs contain no table data.")
    assert list(production_pdf_data.columns) == list(staging_pdf_data.columns), "Column structure mismatch in PDFs"
    

# Test 1: Verify Column Names Match
@pytest.mark.pdf
def test_pdf_column_names(production_pdf_data, staging_pdf_data):
    assert list(production_pdf_data.columns) == list(staging_pdf_data.columns), "Column structure mismatch in PDFs"


# Test 2: Verify Row Count Match
@pytest.mark.pdf
def test_pdf_row_count(production_pdf_data, staging_pdf_data):
    assert len(production_pdf_data) == len(staging_pdf_data), "Row count mismatch in PDFs"


# Test 3: Verify Data Isn't Null
@pytest.mark.pdf
def test_pdf_no_null_values(production_pdf_data, staging_pdf_data):
    assert production_pdf_data.isnull().sum().sum() == 0, "Production PDF contains null values"
    assert staging_pdf_data.isnull().sum().sum() == 0, "Staging PDF contains null values"


# Test 4: Verify Values Consistency
@pytest.mark.pdf
def test_pdf_value_consistency(production_pdf_data, staging_pdf_data):
    mismatches = production_pdf_data.compare(staging_pdf_data, align_axis=1)
    assert mismatches.empty, f"Value mismatches found in PDF data:\n{mismatches}"


# Test 5: Verify Time Logic
@pytest.mark.pdf
def test_pdf_time_logic(production_pdf_data, staging_pdf_data):
    # Replace column names with actual names from the PDFs
    prod_dates = pd.to_datetime(production_pdf_data['Last Received Date'])
    stage_dates = pd.to_datetime(staging_pdf_data['Last Received Date'])

    prod_marked_at = pd.to_datetime(production_pdf_data['Marked At'])
    stage_marked_at = pd.to_datetime(staging_pdf_data['Marked At'])

    assert all(prod_dates <= prod_marked_at), "Invalid dates in production PDF"
    assert all(stage_dates <= stage_marked_at), "Invalid dates in staging PDF"

"""
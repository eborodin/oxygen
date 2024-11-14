import os
import json
import pytest
import fitz
import difflib
import pandas as pd
import pdfplumber
import chardet
import re
import subprocess
from diff_pdf_visually import pdf_similar

# Dynamic path retrieval
# Retrieve file path from config.json
def get_dynamic_path_from_config(key):
    possible_locations = [
        os.path.join(os.path.dirname(__file__), "config.json"),
        os.path.abspath("config.json"),
        "/Users/eugeneborodin/PycharmProjects/pythonProject/focal_system_env/config.json"
    ]
    for config_path in possible_locations:
        if os.path.exists(config_path):
            with open(config_path, "r") as config_file:
                config = json.load(config_file)
            if key not in config:
                raise KeyError(f"Key '{key}' not found in configuration file.")
            return config[key]
    raise FileNotFoundError("Configuration file not found in expected locations.")

@pytest.fixture
def production_pdf_data():
    production_pdf_path = get_dynamic_path_from_config("production_pdf_file")
    assert os.path.exists(production_pdf_path), f"File not found: {production_pdf_path}"
    return extract_text_from_pdf(production_pdf_path)

@pytest.fixture
def staging_pdf_data():
    staging_pdf_path = get_dynamic_path_from_config("staging_pdf_file")
    assert os.path.exists(staging_pdf_path), f"File not found: {staging_pdf_path}"
    return extract_text_from_pdf(staging_pdf_path)
"""
def test_print_columns(production_pdf_data, staging_pdf_data):
    print("Production PDF Columns:", production_pdf_data)
    print("Staging PDF Columns:", staging_pdf_data)
"""

# Text extraction from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    extracted_text = "\n".join(page.get_text() for page in doc)
    doc.close()
    # print("Extracted text type:", extracted_text)
    return extracted_text

def compare_pdfs_visually(production_pdf_path, staging_pdf_path, output_diff_path):
    """
    Compare two PDF files visually using diff-pdf-visually.

    Args:
        pdf1_path (str): Path to the first PDF file (production).
        pdf2_path (str): Path to the second PDF file (staging).
        output_diff_path (str): Path to save the visual difference file.

    Returns:
        bool: True if the files are identical, False otherwise.
    """
    try:
        if not os.path.isabs(output_diff_path):
            output_diff_path = os.path.join(os.getcwd(), output_diff_path)
        os.makedirs(os.path.dirname(output_diff_path), exist_ok=True)

        command = [
            "diff-pdf",
            "--output-diff=" + output_diff_path,
            "--view",
            production_pdf_path,
            staging_pdf_path,
        ]
        subprocess.run(command, check=True)
        print(f"PDF comparison completed. Differences saved to: {output_diff_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"PDF comparison failed with error: {e}")
        return False
    except FileNotFoundError:
        print("diff-pdf is not installed or not found in PATH.")
        return False

production_pdf = get_path_from_config("production_pdf_file")
staging_pdf = get_path_from_config("staging_pdf_file")
output_diff = get_path_from_config("output_diff_path")

compare_pdfs_visually(production_pdf, staging_pdf, output_diff)


"""
# Organize text into a table
def organize_text_into_table(extracted_text, delimiter="\t"):
    rows = extracted_text.split("\n")
    table_data = [row.split(delimiter) for row in rows if row.strip()]
    df = pd.DataFrame(table_data)
    df.columns = df.iloc[0]  # First row as header
    df = df[1:].reset_index(drop=True)  # Remove header row from data
    return df

# Function to extract tabular data from PDF
def extract_table_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        data = []
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    data.append(row)
    df = pd.DataFrame(data)  # Convert to DataFrame
    df = df.dropna(how='all').reset_index(drop=True)  # Clean up empty rows
    return df


# Example test
def test_table_to_csv(production_pdf_data):
    assert not production_pdf_data.empty, "Production table is empty!"
    production_pdf_data.to_csv("output.csv", index=False)
    print("CSV saved successfully!")



# Unified diff comparison
@pytest.mark.pdf
def test_pdf_text_diff(production_pdf_data, staging_pdf_data):

    # Compare text content of production and staging PDFs and report differences.

    diff = difflib.unified_diff(
        production_pdf_data.splitlines(),
        staging_pdf_data.splitlines(),
        lineterm=""
    )
    differences = list(diff)
    assert not differences, f"Differences found in PDF text:\n{''.join(differences)}"

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
    mismatches = production_pdf_data.compare(staging_pdf_data)
    assert mismatches.empty, f"Value mismatches found in PDF data:\n{mismatches}"

# Test 5: Verify Time Logic
@pytest.mark.pdf
def test_pdf_time_logic(production_pdf_data, staging_pdf_data):
    # Assume 'Last Received Date' and 'Marked At' are columns 12 and 11 respectively
    prod_dates = pd.to_datetime(production_pdf_data[12])  # Replace index with actual column index or name
    stage_dates = pd.to_datetime(staging_pdf_data[12])

    prod_marked_at = pd.to_datetime(production_pdf_data[11])  # Replace index with actual column index or name
    stage_marked_at = pd.to_datetime(staging_pdf_data[11])

    assert all(prod_dates <= prod_marked_at), "Invalid dates in production PDF"
    assert all(stage_dates <= stage_marked_at), "Invalid dates in staging PDF"
"""
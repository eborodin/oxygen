import pytest
import pdfplumber
import pandas as pd

def pytest_configure(config):
    if config.pluginmanager.hasplugin("html"):
        config._metadata["PDF report"] = "Focal Report Test Results"

def extract_table_from_pdf(pdf_path):

    # Extract tabular data from a PDF file using pdfplumber.
    # Returns a pandas DataFrame containing the data.

    with pdfplumber.open(pdf_path) as pdf:
        data = []
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    data.append(row)
    # Convert to DataFrame and clean up empty rows
    df = pd.DataFrame(data)
    df = df.dropna(how='all').reset_index(drop=True)  # Remove rows that are completely empty
    return df

"""
def extract_table_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        data = []
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    data.append(row)
    # Print extracted data for debugging
    print(f"Extracted data from {pdf_path}:")
    print(data)
    # Convert to DataFrame
    df = pd.DataFrame(data)
    df = df.dropna(how='all').reset_index(drop=True)
    return df
"""

@pytest.fixture
def production_pdf_data():

    # Fixture to load production PDF data.
    prod_file = "/Users/eugeneborodin/PycharmProjects/pythonProject/focal_system_env/tests/prod/gap_report_grocery_focal_superstore_101_2024-10-28_2024-10-28_prod.pdf"
    return extract_table_from_pdf(prod_file)

@pytest.fixture
def staging_pdf_data():
    # Fixture to load staging PDF data.
    stage_file = "/Users/eugeneborodin/PycharmProjects/pythonProject/focal_system_env/tests/staging/gap_report_grocery_focal_superstore_101_2024-10-28_2024-10-28_stage.pdf"
    return extract_table_from_pdf(stage_file)

def test_table_structure(production_pdf_data, staging_pdf_data):

    # Test to ensure table structure (columns) matches between production and staging.
    assert list(production_pdf_data.columns) == list(staging_pdf_data.columns), \
        "Table structure mismatch between production and staging PDFs."

def test_row_count(production_pdf_data, staging_pdf_data):

    # Test to ensure row counts match between production and staging.
    assert len(production_pdf_data) == len(staging_pdf_data), \
        "Row count mismatch between production and staging PDFs."

def test_value_consistency(production_pdf_data, staging_pdf_data):

    # Test to compare values row by row between production and staging.

    mismatches = production_pdf_data.compare(staging_pdf_data)
    assert mismatches.empty, f"Value mismatches found:\n{mismatches}"

"""
def test_dates_rules(production_pdf_data, staging_pdf_data):

    # Verify dates and logical relationships.
    # Last Received Date <= Marked At

    # Extract relevant columns
    prod_dates = pd.to_datetime(production_pdf_data[12])  # Example column for 'Last Received Date'
    stage_dates = pd.to_datetime(staging_pdf_data[12])

    prod_marked_at = pd.to_datetime(production_pdf_data[11])  # Example column for 'Marked At'
    stage_marked_at = pd.to_datetime(staging_pdf_data[11])

    assert all(prod_dates <= prod_marked_at), "Invalid dates in production PDF"
    assert all(stage_dates <= stage_marked_at), "Invalid dates in staging PDF"
"""
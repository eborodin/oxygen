import pytest
import pandas as pd
import pdfplumber
import json

mport json

# Sample function to load data (use your actual loading logic)
def load_csv(file_path):
    return pd.read_csv(file_path)

def get_dynamic_path_from_config():
    # Directory of this script
    config_path = os.path.join(os.path.dirname(__file__), "config.json")

    # Ensure the file exists
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    # Load the configuration file
    with open(config_path) as config_file:
        config = json.load(config_file)

    project_root = os.path.abspath(os.path.dirname(__file__))
    production_file = os.path.join(project_root, config["production_pdf_file"])
    staging_file = os.path.join(project_root, config["staging_pdf_file"])
    return production_file, staging_file

# Fixtures for loading production and staging data
@pytest.fixture
def production_pdf_data():
    production_file, _ = get_dynamic_path_from_config()
    return pd.read_csv(production_file)

#    return extract_table_from_pdf(
#        '/Users/eugeneborodin/PycharmProjects/pythonProject/focal_system_env/tests/prod/gap_report_grocery_focal_superstore_101_2024-10-28_2024-10-28_Prod.pdf')

@pytest.fixture
def staging_pdf_data():
    staging_file, _  = get_dynamic_path_from_config()
    return pd.read_csv(staging_file)

#    return extract_table_from_pdf(
#        '/Users/eugeneborodin/PycharmProjects/pythonProject/focal_system_env/tests/staging/gap_report_grocery_focal_superstore_101_2024-10-28_2024-10-28_stage.pdf')

# Function to extract tables from a PDF
def extract_table_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        data = []
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    data.append(row)
    # Convert to DataFrame and clean up
    df = pd.DataFrame(data)
    df = df.dropna(how='all').reset_index(drop=True)  # Remove empty rows
    return df

def test_print_columns(production_pdf_data, staging_pdf_data):
    print("Production PDF Columns:", production_pdf_data.columns)
    print("Staging PDF Columns:", staging_pdf_data.columns)

'''

def extract_table_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        data = []
        for page_num, page in enumerate(pdf.pages, start=1):
            print(f"\n--- Extracting data from page {page_num} ---")
            tables = page.extract_tables()
            if tables:
                print(f"Found {len(tables)} table(s) on page {page_num}.")
                for table_num, table in enumerate(tables, start=1):
                    print(f"\n--- Table {table_num} on page {page_num} ---")
                    for row in table:
                        print(row)  # Print each row
                        data.append(row)
            else:
                print(f"No tables found on page {page_num}.")

    # Convert to DataFrame and return
    df = pd.DataFrame(data)
    print("\n--- Final Extracted DataFrame ---")
    print(df.head())  # Print the first few rows for inspection
    return df

production_pdf_path = '/Users/eugeneborodin/PycharmProjects/pythonProject/focal_system_env/tests/prod/gap_report_grocery_focal_superstore_101_2024-10-28_2024-10-28_Prod.pdf'
staging_pdf_path = '/Users/eugeneborodin/PycharmProjects/pythonProject/focal_system_env/tests/staging/gap_report_grocery_focal_superstore_101_2024-10-28_2024-10-28_stage.pdf'

# Extract and inspect production PDF
print("\n--- Inspecting Production PDF ---")
production_data = extract_table_from_pdf(production_pdf_path)

# Extract and inspect staging PDF
print("\n--- Inspecting Staging PDF ---")
staging_data = extract_table_from_pdf(staging_pdf_path)


'''
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

'''
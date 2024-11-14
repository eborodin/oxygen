import pytest
import pandas as pd
import pdfplumber
import camelot


'''
tables = camelot.read_pdf(pdf_path, pages="all")
for table in tables:
    print(table.df)
'''

# Loading production and staging PDF data
@pytest.fixture
def production_pdf_data():
    return extract_table_from_pdf(
        '/Users/eugeneborodin/PycharmProjects/pythonProject/focal_system_env/tests/prod/gap_report_grocery_focal_superstore_101_2024-10-28_2024-10-28_Prod.pdf'
    )

@pytest.fixture
def staging_pdf_data():
    return extract_table_from_pdf(
        '/Users/eugeneborodin/PycharmProjects/pythonProject/focal_system_env/tests/staging/gap_report_grocery_focal_superstore_101_2024-10-28_2024-10-28_stage.pdf'
    )

# Function to extract tables from a PDF
def extract_table_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        data = []
        for page_num, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            if tables:
                print(f"Tables found on page {page_num}: {len(tables)}")
                for table in tables:
                    for row in table:
                        print(f"Row: {row}")
                        data.append(row)
            else:
                print(f"No tables found on page {page_num}")
    # Convert to DataFrame
    df = pd.DataFrame(data)
    print(f"Extracted DataFrame from {pdf_path}:\n{df.head()}")
    return df

print("Production PDF Columns:", production_pdf_data.columns)
print("Staging PDF Columns:", staging_pdf_data.columns)

'''
@pytest.mark.pdf
def test_pdf_time_logic(production_pdf_data, staging_pdf_data):
    assert not production_pdf_data.empty, "Production PDF data is empty!"
    assert not staging_pdf_data.empty, "Staging PDF data is empty!"

    # Skip further checks if DataFrame is empty
    if production_pdf_data.empty or staging_pdf_data.empty:
        pytest.skip("Skipping test due to empty data")


# Test 1: Verify Column Names Match
@pytest.mark.pdf
# def test_pdf_column_names(production_pdf_data, staging_pdf_data):
#    assert list(production_pdf_data.columns) == list(staging_pdf_data.columns), "Column structure mismatch in PDFs"

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

@pytest.mark.pdf
def test_pdf_time_logic(production_pdf_data, staging_pdf_data):
    assert not production_pdf_data.empty, "Production PDF data is empty!"
    assert not staging_pdf_data.empty, "Staging PDF data is empty!"

    # Replace with actual column names or indices
    prod_dates = pd.to_datetime(production_pdf_data.get('Last Received Date', pd.NaT))
    prod_marked_at = pd.to_datetime(production_pdf_data.get('Marked At', pd.NaT))
    assert all(prod_dates <= prod_marked_at), "Invalid dates in production PDF"

'''

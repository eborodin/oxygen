import pytest
import pandas as pd

# Sample function to load data (use your actual loading logic)
def load_csv(file_path):
    return pd.read_csv(file_path)

# Fixtures for loading production and staging data
@pytest.fixture
def production_data():
    return load_csv(
        '/focal_system_env/tests/prod/gap_report_grocery_focal_superstore_101_2024-10-28_2024-10-28_prod.csv')

@pytest.fixture
def staging_data():
    return load_csv(
        '/focal_system_env/tests/staging/gap_report_grocery_focal_superstore_101_2024-10-28_2024-10-28_prod.csv')

# Tests Case 1: Verify Column Names Match
def test_column_names(production_data, staging_data):
    assert list(production_data.columns) == list(staging_data.columns), "Column structure mismatch"

# Tests Case 2: Verify Row Count Match
def test_row_count(production_data, staging_data):
    assert len(production_data) == len(staging_data), "Row count mismatch"

# Tests Case 3: Verify Data Isn't Null
def test_no_null_values(production_data, staging_data):
    assert production_data.isnull().sum().sum() == 0, "Production data contains null values"
    assert staging_data.isnull().sum().sum() == 0, "Staging data contains null values"

# Tests Case 4: Verify Values Consistency
def test_value_consistency(production_data, staging_data):
    mismatches = production_data.compare(staging_data)
    assert mismatches.empty, f"Value mismatches found:\n{mismatches}"

# Tests Case 5: Verify the Received Dates Greater Than Marked At
def test_time_logic(production_data, staging_data):
    # Example: Check if 'Last Received Date' <= 'Marked At'
    assert all(pd.to_datetime(production_data['Last Received Date']) <= pd.to_datetime(production_data['Marked At'])), \
        "Invalid dates in production data"
    assert all(pd.to_datetime(staging_data['Last Received Date']) <= pd.to_datetime(staging_data['Marked At'])), \
        "Invalid dates in staging data"

# Tests Case 6: Verify
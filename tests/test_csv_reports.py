import pytest
import os
import json
import pandas as pd
import string

# Sample function to load data (use your actual loading logic)
# def load_csv(file_path):
#     return pd.read_csv(os.path.join(os.getcwd(), file_path))

# Make the csv file dynamic
def get_dynamic_path_from_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path) as config_file:
        config = json.load(config_file)

    project_root = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..")
    production_file = os.path.join(project_root, config["production_csv_file"])
    staging_file = os.path.join(project_root, config["staging_csv_file"])

    if not os.path.exists(production_file):
        raise FileNotFoundError(f"Production file not found: {production_file}")
    if not os.path.exists(staging_file):
        raise FileNotFoundError(f"Staging file not found: {staging_file}")

    return production_file, staging_file

# Fixtures for loading production and staging data
@pytest.fixture
def production_data():

    production_file, _ = get_dynamic_path_from_config()
    return pd.read_csv(production_file)

@pytest.fixture
def staging_data():

    _, staging_file = get_dynamic_path_from_config()
    return pd.read_csv(staging_file)

# Tests Case 1: Verify Column Names Match
@pytest.mark.csv
def test_column_names(production_data, staging_data):
    assert list(production_data.columns) == list(staging_data.columns), "Column structure mismatch"

"""
# Test Case 1.1: Checking for a specific column
@pytest.mark.csv
def test_specific_column(production_data, staging_data):
    columns  = production_data.columns.tolist()
    for column in columns:
        production_column = production_data[column]
        staging_column = staging_data[column]
        print ("Production columns: ", columns)
    assert production_column.equals(staging_column), f"Mismatch in column: {column}"
"""

# Tests Case 2: Verify Row Count Match
@pytest.mark.csv
def test_row_count(production_data, staging_data):
    assert len(production_data) == len(staging_data), "Row count mismatch"

# Tests Case 3: Verify Column Count Match
@pytest.mark.csv
def test_column_count(production_data, staging_data):
    assert production_data.shape[1] == staging_data.shape[1], "Column count mismatch"

# Tests Case 4: Verify Values Consistency
@pytest.mark.csv
def test_value_consistency(production_data, staging_data):
    mismatches = production_data.compare(staging_data)
    # print("Production Data: \n", (production_data))
    # print("Staging Data: \n", (staging_data))
    assert mismatches.empty, f"Value mismatches found:\n{mismatches}"

"""
# Tests Case 4.1: Verify a Specific Values in Column
@pytest.mark.csv
def test_specific_column_value_consistency(production_data, staging_data):
    column_to_test = "Product Name"  # Replace with the column you want to check
    production_column = production_data[column_to_test]
    staging_column = staging_data[column_to_test]

    # Compare the values in the specified column
    mismatches = production_column.compare(staging_column)

    # Print mismatches if found
    if not mismatches.empty:
        print(f"Mismatches found in column '{column_to_test}':\n{mismatches}")

    # Assert no mismatches are found
    assert mismatches.empty, f"Value mismatches found in column '{column_to_test}':\n{mismatches}"
"""

# Tests Case 5: Verify the Received Dates Greater Than Marked At
@pytest.mark.csv
def test_time_logic(production_data, staging_data):
    # Check if 'Last Received Date' <= 'Marked At'
    assert all(pd.to_datetime(production_data['Last Received Date']) <= pd.to_datetime(production_data['Marked At'])), \
        "Invalid dates in production data"
    assert all(pd.to_datetime(staging_data['Last Received Date']) <= pd.to_datetime(staging_data['Marked At'])), \
        "Invalid dates in staging data"

"""
# Tests Case 6: There are no Duplicate rows
@pytest.mark.csv
def test_duplicate_values(production_data, staging_data):
    assert production_data.duplicated().sum() == staging_data.duplicated().sum(), "Duplicate row mismatch"

# Tests Case 7: Verify Data Isn't Null
@pytest.mark.csv
def test_no_null_values(production_data, staging_data):
    # Replace null values with "Missing"
    # production_data = production_data.fillna("Missing")
    # staging_data = staging_data.fillna("Missing")

    assert production_data.isnull().sum().sum() == 0, "Production data contains null values"
    assert staging_data.isnull().sum().sum() == 0, "Staging data contains null values"

# Tests Case 7.1: Checks for null values in the PROD data
@pytest.mark.csv
def test_no_null_values_debug(production_data, staging_data):
    # Find rows with null values
    prod_null_rows = production_data[production_data.isnull().any(axis=1)]
    stage_null_rows = staging_data[staging_data.isnull().any(axis=1)]

    # Assert no null values
    assert prod_null_rows.empty, f"Production data contains null rows:\n{prod_null_rows}"
    assert stage_null_rows.empty, f"Staging data contains null rows:\n{stage_null_rows}"

# Tests Case 8: Row and Column Order
@pytest.mark.csv
def test_order_row_column(production_data, staging_data):
    production_sorted = production_data.sort_values(by="Store Name").reset_index(drop=True)
    staging_sorted = staging_data.sort_values(by="Store Name").reset_index(drop=True)
    assert production_sorted.equals(staging_sorted), "Mismatch in sorted data"

# Tests Case 9: File-size Check
@pytest.mark.csv
def test_file_size():
    assert os.path.getsize("production.csv") == os.path.getsize("staging.csv"), "File size mismatch"

"""
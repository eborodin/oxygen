import pytest
import pandas as pd
import os
import json

# Sample function to load data (use your actual loading logic)
def load_csv(file_path):
    return pd.read_csv(file_path)

# Load the config file
def get_dynamic_path_from_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path) as config_file:
        config = json.load(config_file)

    project_root = os.path.abspath(os.path.dirname(__file__))
    production_file = os.path.join(project_root, config["production_csv_file"])
    staging_file = os.path.join(project_root, config["staging_csv_file"])
    return production_file, staging_file

# Fixtures for loading production and staging data
@pytest.fixture
def production_data():
    production_file, _ = get_dynamic_path_from_config()
    return pd.read_csv(production_file)

@pytest.fixture
def staging_data():
    staging_file, _  = get_dynamic_path_from_config()
    return pd.read_csv(staging_file)


# Tests Case 1: Verify Column Names Match
@pytest.mark.csv
def test_column_names(production_data, staging_data):
    assert list(production_data.columns) == list(staging_data.columns), "Column structure mismatch"

# Tests Case 2: Verify Row Count
@pytest.mark.csv
def test_row_count(production_data, staging_data):
    assert len(production_data) == len(staging_data), "Row count mismatch"

# Tests Case 3: Verify Column Count
@pytest.mark.csv
def test_column_count(production_data, staging_data):
    assert production_data.shape[1] == staging_data.shape[1], "Column count mismatch"

# Tests Case 4: Verify Values Consistency
@pytest.mark.csv
def test_value_consistency(production_data, staging_data):
    mismatches = production_data.compare(staging_data)
    assert mismatches.empty, f"Value mismatches found:\n{mismatches}"

# Tests Case 5: Verify the Received Dates Greater Than Marked At
@pytest.mark.csv
def test_time_logic(production_data, staging_data):
    # Check if 'Last Received Date' <= 'Marked At'
    assert all(pd.to_datetime(production_data['Last Received Date']) <= pd.to_datetime(production_data['Marked At'])), \
        "Invalid dates in production data"
    assert all(pd.to_datetime(staging_data['Last Received Date']) <= pd.to_datetime(staging_data['Marked At'])), \
        "Invalid dates in staging data"

# Tests Case 6: There are no Duplicate rows
@pytest.mark.csv
def test_duplicate_values(production_data, staging_data):
    assert production_data.duplicated().sum() == staging_data.duplicated().sum(), "Duplicate row mismatch"

# Tests Case 7: Verify Data Isn't Null
@pytest.mark.csv
def test_no_null_values(production_data, staging_data):
    assert production_data.isnull().sum().sum() == 0, "Production data contains null values"
    assert staging_data.isnull().sum().sum() == 0, "Staging data contains null values"

"""
# Tests Case 8: Row and Column Order
@pytest.mark.csv
def test_order_row_column(production_data, staging_data):
    production_sorted = production_data.sort_values(by="Store Name").reset_index(drop=True)
    staging_sorted = staging_data.sort_values(by="Store Name").reset_index(drop=True)
    assert production_sorted.equals(staging_sorted), "Mismatch in sorted data"

# Tests Case 9: File-Level Check
@pytest.mark.csv
def test_file_size():
    assert os.path.getsize("production.csv") == os.path.getsize("staging.csv"), "File size mismatch"

"""
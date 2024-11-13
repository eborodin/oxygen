import pandas as pd
import json


# Load the production and staging data
prod_data = pd.read_csv(
    '/focal_system_env/tests/prod/gap_report_grocery_focal_superstore_101_2024-10-28_2024-10-28_prod.csv')
stage_data = pd.read_csv(
    '/focal_system_env/tests/staging/gap_report_grocery_focal_superstore_101_2024-10-28_2024-10-28_prod.csv')

# Check if the columns match
if list(prod_data.columns) != list(stage_data.columns):
    print("Column mismatch detected!")
else:
    print("Column structure is consistent.")

# Check if the number of rows matches
if len(prod_data) != len(stage_data):
    print("Row count mismatch detected!")
else:
    print("Row count is consistent.")

# Identify mismatches row by row
discrepancies = []


for col in prod_data.columns:
    mismatches = prod_data[col] != stage_data[col]
    if mismatches.any():
        discrepancies.append(col)
        print(f"Discrepancy found in column: {col}")

# Check for valid 'Last Received Date' and 'Marked At'
invalid_dates = stage_data[stage_data['Last Received Date'] > stage_data['Marked At']]
if not invalid_dates.empty:
    print("Invalid date relationships found!")

# Generate a report of discrepancies
    validation_report = pd.DataFrame(discrepancies, columns=['Column'])
    validation_report.to_csv('validation_report.csv', index=False)

# Ensure the identifiers are the same data type
prod_data['Barcode'] = prod_data['Barcode'].astype(str)
stage_data['Barcode'] = stage_data['Barcode'].astype(str)

# Load the columns to compare
with open('columns.json', 'r') as file:
    columns_check = json.load(file)['columns_check']

# Merge the files
comparison_files = prod_data.merge(stage_data, on=['columns_check'], suffixes=('_prod', '_stage'))

# Check for mismatches
for column in columns_check:
    comparison_files[f"{column}_match"] = comparison_files[f"{column}_prod"] == comparison_files[f"{column}_stage"]

# Filter mismatched rows
mismatches = comparison_files[~comparison_files[[f"{col}_match" for col in columns_check]].all(axis=1)]

# Output the mismatches
print(mismatches)
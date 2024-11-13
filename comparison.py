import pandas as pd
from pandas import DataFrame

# Load CSV files
prod_data: DataFrame= pd.read_csv(
    "/focal_system_env/tests/prod/gap_report_grocery_focal_superstore_101_2024-10-28_2024-10-28_stage.csv")
stage_data: DataFrame = pd.read_csv(
    "/focal_system_env/tests/stage/gap_report_grocery_focal_superstore_101_2024-10-28_2024-10-28_stage.csv")
# Merge production and staging data on a common key (e.g., Barcode, Article Number)
comparison = prod_data.merge(stage_data, on=["Barcode", "Article Number"], suffixes=('_prod', '_stage'))
# Define columns to compare
columns_to_check = ['Product Name', 'Brand', 'Case Pack Size', 'Current SR', 'Marked As', 'Last Received Date']

# Find mismatches
for column in columns_to_check:
    comparison[f"{column}_match"] = comparison[f"{column}_prod"] == comparison[f"{column}_stage"]

# Filter rows with mismatches
mismatches = comparison[comparison[[f"{col}_match" for col in columns_to_check]].any(axis=1)]
# Save mismatches to a file for review
mismatches.to_csv("comparison_mismatches.csv", index=False)
from pdfplumber import open

# Extract text from production PDF
with open('/focal_system_env/tests/prod/gap_report_grocery_focal_superstore_101_2024-10-28_2024-10-28_prod.pdf') as pdf:
    production_text = ''
    for page in pdf.pages:
        production_text += page.extract_text()


# Extract text from staging PDF
with open('/focal_system_env/tests/staging/gap_report_grocery_focal_superstore_101_2024-10-28_2024-10-28_prod.pdf') as pdf:
    staging_text = ''
    for page in pdf.pages:
        staging_text += page.extract_text()

print("Production PDF Content:")
print(production_text[:500])  # Print first 500 characters for verification

print("Staging PDF Content:")
print(staging_text[:500])
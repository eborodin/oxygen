# Focal Systems - QA Challenge
The task is to automate regression testing for our reports. Attached you will find two packages for the same report - production and staging. Production data is correct and complete. Based on this, prepare sets of validation rules, and then run them on staging data to determine if and what regressions might exist.

## The rules for data validation
The focus on key aspects of the data:

1. Structure Validation:
 Column names must match between production and staging 
| Column count must match
| Row count must match 
2. Data Integrity:
Key columns are required 
| No missing values in columns
3. Data Consistency:
Production values must match Staging values 
| Specific column validations (numeric ranges, date order) 
4.	Additional Logic:
Valid format for date and time fields
| “Last Received Date” must be earlier than “Marked At”
---
## Test Cases
1. Verify the Page Header (PDF only)
2. Verify the Report Name (PDF only)
3. Verify selected data range (PDF only)
4. Verify the column count
4. Verify the column names
5. Verify the row count
6. Verify the page count
7. Verify barcode placement 
8. Verify Article Number field
9. Verify Store Name field
10. Verify Brand field
11. Verify Aisle field
12. Verify Department field
13. Verify Case Pack Size field
14. Verify SR at Marked at Time field
15. Verify Current SR field
16. Verify Marked by field
17. Verify Marked At field
18. Verify Marked As field
19. Verify Last Received Date field
20. Verify Approval's field
21. Verify the format of Marked At (YYYY-MM-DD HH:MM:SS)
22. Verify the format of Last Received Date (YYYY-MM-DD HH:MM:SS)

Optioinal/Good to have:

23. Verify if FocalOS logo is centered
24. Think about how to verify multiple PDFs
25. Verify the correct column order
26. Verify sorting of columns
27. Check for empty fields in PDF

---
## Installation

Python Version: Python 3.8 or above.
Dependencies: Install the required Python libraries using the following command:

        python3 --version
        brew install python

Install pip

        pip3 --version
        sudo easy_install pip

Installing pandas

        pip3 install pandas

Install Required Libraries

        pip install pdfplumber
        pip install PyPDF2

Install Pytest:

        pip install pytest

PDF Required Libraries

        pip install pytest pdfplumber pandas

Files:

*	Make sure production and staging files are ```focal_system_env/data``` directory. Ensure the paths are correctly configured in the script.

---
## Steps to Run

**Clone the repository**:

    git clone https://github.com/eborodin/oxygen.git
    cd oxygen/ 


Run all Tests:

        pytest tests/

Individual Tests:

        pytest tests/test_csv_reports.py
        pytest tests/test_pdf_visual.py
        pytest tests/test_csv_reports.py
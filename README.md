How to Run the Test

Requirements

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

*	Place the production and staging CSV or PDF files in the appropriate directories. Ensure the paths are correctly configured in the script.

Steps to Run

Clone the repository or download the project files:
    
    git clone https://github.com/eborodin/oxygen.git
    cd oxygen/

Run the Tests:
From your project directory, run:

In order to get HTML report

        pytest tests

Only CSV or PDF test

        pytest tests/test_csv_reports.py
        pytest -s tests/test_pdf_visual.py
        pytest tests/test_csv_reports.py

----

The rules for data validation
Let's assume that the PROD data is correct and is our source of truth. 
The rules are the following:


1. Verify the Page Header (PDF only)
2. Verify the Report Name (PDF only)
3. Verify selected data range (PDF only)
4. Verify the column count
4. Verify the column names
5. Verify the row count
6. Verify the page count
7. Verify barcode placement
8. Verify Article Number 
9. Verify Store Name
10. Verify Brand
11. Verify Aisie 
12. Verify Department
13. Verify Case Pack Size
14. Verify SR at Marked at Time
15. Verify Current SR
16. Verify Marked by
17. Verify Marked At 
18. Verify Marked As
19. Verify Last Received Date
20. Verify Approval's
21. Verify the format of Marked At 
22. Verify the format of Last Received Date

Optioinal/Good to have:
23. Verify if FocalOS logo is centered
24. Think about how to verify multiple PDFs
25. Verify the correct column order
26. Verify sorting 
27. Verify for empty fields in PDF
28. 


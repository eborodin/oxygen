How to Run the Test

Requirements

1.  Python Version: Python 3.8 or above.
Dependencies: Install the required Python libraries using the following command:

    pip install -r requirements.txt
 
2.  The requirements.txt file should include:

* 	pandas
* 	pdfplumber

Install Pytest:

    pip install pytest

3.	Files:

*	Place the production and staging CSV or PDF files in the appropriate directories. Ensure the paths are correctly configured in the script.

Steps to Run

4.	Clone the repository or download the project files:
    
    git clone https://github.com/eborodin/oxygen.git
    cd oxygen/

5. Run the Tests:
From your project directory, run:

        pytest tests/test_reports.py
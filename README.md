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

Files:

*	Place the production and staging CSV or PDF files in the appropriate directories. Ensure the paths are correctly configured in the script.

Steps to Run

Clone the repository or download the project files:
    
    git clone https://github.com/eborodin/oxygen.git
    cd oxygen/

Run the Tests:
From your project directory, run:

        pytest tests/test_reports.py


3
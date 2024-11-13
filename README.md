How to Run the Test

Requirements

1.	Python Version: Python 3.8 or above.
Dependencies: Install the required Python libraries using the following command:

    pip install -r requirements.txt
 
The requirements.txt file should include:
* 	pandas
* 	pdfplumber
* 	Any other library you use (e.g., pytest if applicable).

3.	Files:
*	Place the production and staging CSV or PDF files in the appropriate directories. Ensure the paths are correctly configured in the script.

Steps to Run

1.	Clone the repository or download the project files:
    
    git clone https://github.com/your-repo-name.git
    cd your-repo-name

2.	Run the script to validate the reports:
    
    python app.py

3.	Review the generated reports for discrepancies:
*	CSV discrepancies will be saved as csv_discrepancies.csv.
*	PDF discrepancies will be saved as pdf_discrepancies.csv.
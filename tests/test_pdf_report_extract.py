import difflib
import chardet
import pytest
import json
import os
import pytesseract
from pdf2image import convert_from_path
import fitz

def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read())
    encoding = result.get("encoding", "utf-8")  # Default to utf-8 if detection fails
    confidence = result.get("confidence", 0)

    # Debugging information
    print(f"Detected encoding: {encoding} with confidence: {confidence}")

    # If confidence is low, fallback to utf-8 or another robust encoding
    if confidence < 0.8 or encoding is None:
        print("Low confidence in detected encoding. Falling back to 'utf-8'.")
        encoding = "utf-8"
    return encoding

def get_dynamic_path_from_config():
    # Directory of this script
    config_path = os.path.join(os.path.dirname(__file__), "config.json")

    # Ensure the file exists
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    # Load the configuration file
    with open(config_path) as config_file:
        config = json.load(config_file)

    project_root = os.path.abspath(os.path.dirname(__file__))
    production_file = os.path.join(project_root, config["production_pdf"])
    staging_file = os.path.join(project_root, config["staging_pdf"])

    # Print file paths for debugging
    print(f"Production PDF Path: {production_file}")
    print(f"Staging PDF Path: {staging_file}")

    return production_file, staging_file

"""
# Extracts text from a PDF using OCR (Tesseract)
def extract_text_from_pdf(pdf_path):

    pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"  # Update path as needed
    extracted_text = []
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        print(f"Processing page {i + 1} of {pdf_path}")
        text = pytesseract.image_to_string(image)
        extracted_text.append(text.strip())
    return "\n".join(extracted_text)

# Extracts text from a PDF using by convertion to an image
def extract_text_from_pdf(pdf_path):
    extracted_text = []
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        print(f"Processing page {i + 1} of {pdf_path}")
        text = pytesseract.image_to_string(image)
        print(f"Extracted Text from Page {i + 1}:\n{text[:500]}")
        extracted_text.append(text.strip())
    return "\n".join(extracted_text)
    
"""

# Text extraction from PDF
def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using PyMuPDF (fitz).

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    # Open the PDF document
    doc = fitz.open(pdf_path)

    # Extract text from all pages and join with newline
    extracted_text = "\n".join(page.get_text() for page in doc)

    # Close the document
    doc.close()

    return extracted_text

def save_extracted_text_to_file(pdf_path, output_txt_path):
    extracted_text = extract_text_from_pdf(pdf_path)
    with open(output_txt_path, "w", encoding="utf-8") as file:
        file.write(extracted_text)
    print(f"Extracted text saved to {output_txt_path}")

try:
    # Get dynamic paths for production and staging files
    production_pdf, staging_pdf = get_dynamic_path_from_config()

    # Define dynamic paths for output text files based on the PDF paths
    production_txt = production_pdf.replace(".pdf", "_text.txt")
    staging_txt = staging_pdf.replace(".pdf", "_text.txt")

    # Save extracted text for both PDFs
    save_extracted_text_to_file(production_pdf, production_txt)
    save_extracted_text_to_file(staging_pdf, staging_txt)

except Exception as e:
    print(f"Error occurred: {e}")

except Exception as e:
    print(f"Error occurred: {e}")

def test_pdf_text_extraction():
    # Get dynamic paths from configuration
    production_pdf, staging_pdf = get_dynamic_path_from_config()

    # Extract text from both PDFs
    production_text = extract_text_from_pdf(production_pdf)
    staging_text = extract_text_from_pdf(staging_pdf)

    # Assert the extracted text matches
    assert production_text == staging_text, "Text mismatch between production and staging PDFs"

def preprocess_text(text):
    """
    Normalizes text by removing extra spaces, line breaks, and standardizing case.
    """
    return " ".join(text.lower().replace("|", " ").split())

@pytest.mark.pdf
def test_extract_text_and_process():
    # Get dynamic paths
    production_pdf, staging_pdf, = get_dynamic_path_from_config()

    # Ensure files exist
    assert os.path.exists(production_pdf), f"File not found: {production_pdf}"
    assert os.path.exists(staging_pdf), f"File not found: {staging_pdf}"

    # Extract text
    production_text = extract_text_from_pdf(production_pdf)
    staging_text = extract_text_from_pdf(staging_pdf)
    # output_directory = extract_text_from_pdf(output_diff)


    # Save formatted text
    save_extracted_text(production_text, "formatted_production_text.txt")
    save_extracted_text(staging_text, "formatted_staging_text.txt")

    # Save text for manual inspection
    with open("production_text.txt", "w") as prod_file:
        prod_file.write(production_text)
    with open("staging_text.txt", "w") as stage_file:
        stage_file.write(staging_text)

    # Compare text
    if production_text != staging_text:
        diff = "\n".join(difflib.unified_diff(
            production_text.splitlines(), staging_text.splitlines(),
            lineterm="", fromfile="Production", tofile="Staging"
        ))
        with open("text_differences.txt", "w") as diff_file:
            diff_file.write(diff)
        pytest.fail("Mismatch between Production and Staging PDFs. See 'text_differences.txt'.")


    with open("production_text.txt", "w") as prod_file:
        prod_file.write(production_text)

    with open("staging_text.txt", "w") as stage_file:
        stage_file.write(staging_text)

# Saves extracted text to a file with readable formatting
def save_text_to_file(text, file_path):

    with open(file_path, "w", encoding="utf-8") as file:
        pages = text.split("\n\nPage Break\n\n")  # Assuming a page-break marker for separation
        for page_number, page in enumerate(pages, start=1):
            file.write(f"===== Page {page_number} =====\n\n")
            file.write(page.strip() + "\n\n")

# Organizes text into sections for better readability, assuming sections start with "Focal"
def format_text_by_sections(text):

    sections = []
    current_section = []

    for line in text.splitlines():
        if line.strip().startswith("Focal"):  # Check for section header
            if current_section:
                sections.append("\n".join(current_section))
                current_section = []
        current_section.append(line)

    if current_section:
        sections.append("\n".join(current_section))

    return "\n\n===== New Section =====\n\n".join(sections)

# Adds indentation and extra spacing to the text
def add_indentation_and_spacing(text):

    formatted_text = ""
    for line in text.splitlines():
        if line.strip():  # Skip blank lines
            formatted_text += f"  {line.strip()}\n"  # Add two spaces before each line
        else:
            formatted_text += "\n"  # Add a blank line for paragraph separation
    return formatted_text

# Processes and saves extracted text to a file
def save_extracted_text(text, output_file):

    # Format text
    text = format_text_by_sections(text)  # Group by sections
    text = add_indentation_and_spacing(text)  # Add spacing and indentation

    # Save to file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(text)

    print(f"Formatted text saved to {output_file}")
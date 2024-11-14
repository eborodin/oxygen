import os
import json
import pytest
import subprocess
import pytest_html


# Load the config file
def get_dynamic_path_from_config(key):
    config_path = os.path.join(os.path.dirname(__file__), "/Users/eugeneborodin/PycharmProjects/pythonProject/focal_system_env/config.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path) as config_file:
        config = json.load(config_file)

    if key not in config:
        raise KeyError(f"Key '{key}' not found in config.json")

    return config[key]

# Compare two PDF files visually by using diff-pdf-visually
def compare_pdfs_visually(production_pdf, staging_pdf, output_diff_path):
    try:
        if not os.path.isabs(output_diff_path):
            output_diff_path = os.path.join(os.getcwd(), output_diff_path)
        os.makedirs(os.path.dirname(output_diff_path), exist_ok=True)

        command = [
            "diff-pdf",
            "--output-diff=" + output_diff_path,
            "--view",
            production_pdf,
            staging_pdf,
        ]
        subprocess.run(command, check=True)
        print(f"PDF comparison completed. Differences saved to: {output_diff_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"PDF comparison failed with error: {e}")
        return False
    except FileNotFoundError:
        print("diff-pdf is not installed or not found in PATH.")
        return False

@pytest.mark.pdf
def test_visual_pdf_comparison(request):
    production_pdf = get_dynamic_path_from_config("production_pdf")
    staging_pdf = get_dynamic_path_from_config("staging_pdf")
    output_diff = get_dynamic_path_from_config("output_diff_path")

    result = compare_pdfs_visually(production_pdf, staging_pdf, output_diff)
    assert result, "PDFs are not visually identical"

# [TBD] Attach the difference.pdf to the HTML report if the test fails
"""
    if not result:
        if request.config.pluginmanager.hasplugin("html"):
            with open(output_diff, "rb") as diff_file:
                attachment_content = diff_file.read()
            extra = getattr(request.node, "extra", [])
            extra.append(
                {
                    "name": "Difference PDF",
                    "mime_type": "application/pdf",
                    "content": attachment_content,
                }
            )
            request.node.extra = extra
            pytest.fail("PDFs are not visually identical. See the attached Difference PDF.")
"""


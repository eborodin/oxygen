import pytest

def pytest_html_report_title(report):
    """Set a custom title for the HTML report."""
    report.title = "Focal Report Test Results"

def pytest_html_results_summary(prefix, summary, postfix):
    """Add additional content to the summary section of the HTML report."""
    prefix.append("<h1>Focal Report Metadata</h1>")
    prefix.append("<p>Environment: Local</p>")
    prefix.append("<p>Generated by Pytest HTML Report</p>")
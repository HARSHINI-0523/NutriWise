import sys, os

# Ensure backend root is on path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lab_report_analysis.pipeline import process_lab_report

# Test on one file
output = process_lab_report("uploads/lab_reports/report1.png")

print("\n======== CLEANED TEXT ========\n")
print(output["cleaned_text"])

print("\n======== EXTRACTED DATA ========\n")
print(output["extracted_data"])

print("\n======== PATTERN ANALYSIS ========\n")
print(output["patterns"])

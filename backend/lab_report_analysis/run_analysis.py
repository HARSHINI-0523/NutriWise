import sys
import os
import json


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../.."))

sys.path.append(CURRENT_DIR)
sys.path.append(BACKEND_DIR)
sys.path.append(ROOT_DIR)

try:
    from lab_report_analysis.pipeline import process_lab_report
except Exception as e:
    # ONLY JSON OUTPUT
    print(json.dumps({"error": f"Import error: {e}"}))
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No file path provided"}))
        sys.exit(0)

    file_path = sys.argv[1]

    try:
        # RUN ANALYSIS
        output = process_lab_report(file_path)

        # STRIP ANY NON–SERIALIZABLE THINGS
        clean_output = {
            "raw_text": output.get("raw_text", ""),
            "cleaned_text": output.get("cleaned_text", ""),
            "extracted_data": output.get("extracted_data", {}),
            "patterns": output.get("patterns", {})
        }

        print(json.dumps(clean_output))   # ONLY JSON

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(0)

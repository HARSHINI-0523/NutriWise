import sys, os
sys.path.append(os.getcwd())


from lab_report_analysis.pipeline import process_lab_report

INPUT_DIR = "uploads/lab_reports_bulk/"
OUTPUT_DIR = "lab_report_analysis/dataset/cleaned_texts/"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def collect_all():
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(INPUT_DIR, filename)
            print(f"\nProcessing: {filename}")

            result = process_lab_report(path)
            cleaned = result["cleaned_text"]

            out_path = os.path.join(OUTPUT_DIR, filename + ".txt")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(cleaned)

    print("\n Dataset collection complete!")

if __name__ == "__main__":
    collect_all()

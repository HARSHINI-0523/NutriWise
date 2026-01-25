import os
import re
from difflib import SequenceMatcher

INPUT_DIR = "lab_report_analysis/dataset/cleaned_texts/"

# Medical keyword whitelist
MEDICAL_KEYWORDS = [
    "bilirubin", "protein", "albumin", "globulin", "phosphatase", "cholesterol",
    "triglyceride", "hdl", "ldl", "vldl", "creatinine", "urea", "bun",
    "sgot", "ast", "sgpt", "alt", "ggt", "gammagt", "alp", "tsh", "t3", "t4",
    "hemoglobin", "hb", "rbc", "wbc", "platelet", "count", "neutrophils",
    "lymphocytes", "monocytes", "eosinophils", "basophils", "esr",
    "sodium", "potassium", "calcium", "phosphorus", "magnesium",
    "glucose", "sugar", "hba1c", "crp", "vitamin", "iron", "ferritin",
    "bilirubin", "alkaline", "lipid", "profile", "lft", "rft", "kft"
]


def is_value_line(line):
    return bool(re.search(r"\d", line))


def is_valid_test_name(line):
    original = line.strip()
    lower = original.lower()

    # Length check
    if len(original) < 3 or len(original) > 40:
        return False

    # No digits allowed
    if re.search(r"\d", original):
        return False

    # Remove garbage lines with weird symbols
    if re.search(r"[^A-Za-z\s\-/()]", original):
        return False

    # Must contain at least one medical keyword
    if not any(k in lower for k in MEDICAL_KEYWORDS):
        return False

    # Should look alphabetic
    if not re.match(r"^[A-Za-z][A-Za-z\s\-/()]+$", original):
        return False

    return True


def extract_candidates():
    candidates = set()

    for filename in os.listdir(INPUT_DIR):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(INPUT_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f.readlines()]

        for i, line in enumerate(lines):
            if is_valid_test_name(line):
                # Ensure next lines contain numeric values → real test
                if i + 1 < len(lines) and is_value_line(lines[i + 1]):
                    candidates.add(line)

    return list(candidates)


def cluster_similar(names, threshold=0.80):
    clusters = []
    used = set()

    for i in range(len(names)):
        if names[i] in used:
            continue

        group = [names[i]]
        used.add(names[i])

        for j in range(i + 1, len(names)):
            if names[j] in used:
                continue

            sim = SequenceMatcher(None, names[i].lower(), names[j].lower()).ratio()
            if sim > threshold:
                group.append(names[j])
                used.add(names[j])

        clusters.append(group)

    return clusters


def main():
    print(" Scanning cleaned texts...")

    candidates = extract_candidates()
    print(f"\n Found {len(candidates)} REAL test-name candidates")

    clusters = cluster_similar(candidates)

    print("\n CLEAN CLUSTERS (TRUE TEST NAMES ONLY)\n")
    for i, c in enumerate(clusters, 1):
        print(f"{i}. {c}")

    print("\n These clusters will form your MASTER KEYWORD MAP.")


if __name__ == "__main__":
    main()

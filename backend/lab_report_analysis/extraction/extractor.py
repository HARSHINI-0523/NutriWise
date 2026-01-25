import re
from lab_report_analysis.config.master_dictionary import MASTER_DICT

class LabExtractor:

    def normalize_test_name(self, raw):
        """
        Attempt exact + fuzzy normalization of test names.
        """
        raw = raw.strip().upper()

        # Exact match
        for key, variants in MASTER_DICT.items():
            for v in variants:
                if raw == v.upper():
                    return key

        # Fuzzy partial match
        for key, variants in MASTER_DICT.items():
            for v in variants:
                v_upper = v.upper()
                if len(v_upper) > 3 and v_upper in raw:
                    return key

        # Pattern: sometimes OCR returns "TOTAL CHOL 175"
        for key in MASTER_DICT.keys():
            if key.replace("_", " ").upper() in raw:
                return key

        return None

    def extract_number(self, text):
        """
        Extract float/integer from a line.
        """
        match = re.search(r"(\d+\.\d+|\d+)", text)
        if match:
            try:
                return float(match.group(1))
            except:
                return None
        return None

    def extract(self, cleaned_text):
        """
        FULL extraction engine:
        Supports Liver, Kidney, CBC, Lipids, Thyroid, Urine, Vitamins, Electrolytes.
        """
        data = {}
        lines = cleaned_text.split("\n")

        for i, line in enumerate(lines):

            # Normalize this line as a possible test name
            norm = self.normalize_test_name(line)

            if norm:
                # 1. Same line
                value = self.extract_number(line)

                # 2. Next line
                if value is None and i + 1 < len(lines):
                    value = self.extract_number(lines[i + 1])

                # 3. Two lines below
                if value is None and i + 2 < len(lines):
                    value = self.extract_number(lines[i + 2])

                # 4. Three lines below (OCR commonly splits badly)
                if value is None and i + 3 < len(lines):
                    value = self.extract_number(lines[i + 3])

                if value is not None:
                    data[norm] = value

        return data

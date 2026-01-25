import re

class TextCleaner:
    def clean_text(self, text):
        lines = text.split("\n")
        cleaned_lines = []

        for line in lines:
            original = line

            # Remove garbage lines (strange symbols, random words)
            if re.match(r'^[^A-Za-z0-9]+$', line.strip()):
                continue
            if len(line.strip()) < 3:
                continue

            # Fix decimal commas
            line = line.replace(",", ".")

            # Remove multiple weird symbols
            line = re.sub(r"[^A-Za-z0-9\.\-/\s:]", " ", line)

            # Normalize units
            line = line.replace("mgidl", "mg/dL")
            line = line.replace("mgdL", "mg/dL")
            line = line.replace("gmidl", "g/dL")
            line = line.replace("IUIL", "IU/L")
            line = line.replace("IUL", "IU/L")
            line = line.replace("UIL", "IU/L")

            # Remove repeated spaces
            line = re.sub(r"\s+", " ", line).strip()

            cleaned_lines.append(line)

        return "\n".join(cleaned_lines)

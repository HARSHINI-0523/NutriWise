class PatternAnalyzer:

    def __init__(self):
        # Reference ranges (can be expanded per test)
        self.ref = {
            "bilirubin_total": (0.3, 1.2),
            "bilirubin_conjugated": (0.0, 0.3),
            "bilirubin_unconjugated": (0.0, 0.7),

            "sgot": (0, 46),
            "sgpt": (0, 49),
            "alkaline_phosphatase": (42, 128),

            "total_protein": (6.2, 8.0),
            "albumin": (3.8, 5.4),
            "globulin": (1.5, 3.6),
            "ag_ratio": (1.0, 2.0),
            "gammagt": (11, 50),
        }

    def analyze_value(self, key, value):
        if key not in self.ref:
            return "unknown", "No reference range available."

        low, high = self.ref[key]

        if value < low:
            return "low", f"{key.replace('_',' ').title()} is low. Suggests decreased synthesis or nutritional deficiency."
        elif value > high:
            return "high", f"{key.replace('_',' ').title()} is high. Indicates possible stress or overload."
        else:
            return "normal", f"{key.replace('_',' ').title()} is within the normal physiological range."

    def analyze_patterns(self, data):
        results = {}

        # 1. Individual parameter classification
        param_status = {}
        for key, value in data.items():
            status, message = self.analyze_value(key, value)
            param_status[key] = {"status": status, "message": message}
        results["parameter_status"] = param_status

        # 2. Pattern recognition
        patterns = []

        # LIVER CELL DAMAGE (hepatocellular pattern)
        if data.get("sgot", 0) > 80 or data.get("sgpt", 0) > 80:
            patterns.append("Hepatocellular stress pattern due to elevated liver enzymes.")

        # CHOLESTASIS PATTERN (bile flow obstruction)
        if data.get("alkaline_phosphatase", 0) > 200 or data.get("gammagt", 0) > 60:
            patterns.append("Cholestatic pattern (possible bile flow impairment).")

        # HYPERBILIRUBINEMIA PATTERNS
        if data.get("bilirubin_total", 0) > 2:
            if data.get("bilirubin_conjugated", 0) > data.get("bilirubin_unconjugated", 0):
                patterns.append("Predominantly conjugated hyperbilirubinemia pattern.")
            else:
                patterns.append("Predominantly unconjugated hyperbilirubinemia pattern.")

        # PROTEIN SYNThetic CAPACITY PATTERN (liver production)
        if data.get("albumin", 0) < 3.5:
            patterns.append("Reduced albumin suggests decreased liver synthetic capacity or malnutrition.")

        # PROTEIN BALANCE PATTERN
        if data.get("ag_ratio", 1.2) < 1.0:
            patterns.append("Low A/G ratio suggests increased globulins or reduced albumin.")

        # HIGH GGT (alcohol, drug stress)
        if data.get("gammagt", 0) > 100:
            patterns.append("Gamma-GT elevated: indicates oxidative stress, alcohol, or liver inflammation.")

        results["patterns"] = patterns

        return results

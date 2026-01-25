# backend/lab_report_analysis/config/master_dictionary.py

MASTER_DICT = {
    # --- LFT ---
    "bilirubin_total": [
        "BILIRUBIN TOTAL", "Bilirubin Total", "SERUM BILIRUBIN TOTAL",
        "SERUM BILIRUBIN", "TOTAL BILIRUBIN", "Bilirubin Total DPD",
        "BILIRUBIN", "Bilirubin", "Serum Bilirubin Tolal"
    ],

    "bilirubin_direct": [
        "Direct Bilirubin", "BILIRUBIN DIRECT", "CONJUGATED D Bilirubin",
        "Bilirubin Direct DPD", "DRRECT BILIRUBIN", "CONJUGATED BILIRUBIN"
    ],

    "bilirubin_indirect": [
        "Indirect Bilirubin", "BILIRUBIN INDIRECT",
        "UNCONJUGATED BILIRUBIN", "UNCONJUGATED LDBilirubin",
        "UNCONJUGATED I D Bilirubin", "Bilirubin Indirect Calculated"
    ],

    "sgot_ast": [
        "SGOT", "AST", "SGOT/AST", "SGOT AST",
        "Aspartate Transaminase ASTISGOT",
        "Aspatate Amlnotrandferusc AST /SGOI"
    ],

    "sgpt_alt": [
        "SGPT", "ALT", "SGPT/ALT", "SGPT ALT",
        "Alanine Transaminase ALTISGPT",
        "ALANINE AMINOTRANSFERASE ALTISGPT",
        "ALT SGPT"
    ],

    "alkaline_phosphatase": [
        "ALKALINE PHOSPHATASE", "Alkaline Phosphatase",
        "Alkaline Phosphate ALP", "ALKALINE PHOSPHATASE ALP",
        "ALK PHOSPHATASE ALP", "Alkaline Phosphalase"
    ],

    "gammagt": [
        "GGTP", "GGT", "Gamma GT", "GAMMA GT", "GAMMAT-GT"
    ],

    "total_protein": [
        "TOTAL PROTEIN", "Total Protein", "Totai Protein",
        "Proteins Total", "Total Protein Biuret"
    ],

    "albumin": [
        "ALBUMIN", "SERUM ALBUMIN", "Albumin", "ALBUMIN SERUM"
    ],

    "globulin": [
        "GLOBULIN", "SERUM GLOBULIN", "Globulin", "Globulin Calculated"
    ],

    "ag_ratio": [
        "ALBUMIN/GLOBULIN RATIO", "ALBUMINIGLOBULIN",
        "GLOBULIN RATIO", "Albumin Globuln Ratio"
    ],

    # --- KFT ---
    "urea": ["Urea", "UREA", "Blood Urea", "Blooc Urea", "BLcwdd Urea"],
    "bun": [
        "BLOOD UREA NITROGEN", "BUN", "BUN/CREAT RATIO",
        "JOD UREA NITROGEN BUN", "BLZCD UREA NTKOGEN"
    ],
    "creatinine": [
        "CREATININE", "Serum Creatinine", "SERUM CREATININE",
        "CREATININE SERUM", "CREATININE skeus"
    ],

    # --- CBC ---
    "hemoglobin": [
        "HEMOGLOBIN", "Haemoglobin Hb", "HB", "HBAIC", "HB HAEMOGLOBIN"
    ],
    "rbc_count": [
        "RBC COUNT", "Red Blood Count", "Rdc Count",
        "TOTAL ERYTHROCYTE RBC COUNT", "Red Cell Count"
    ],
    "wbc_count": [
        "WBC count", "WBC Count", "TOTAL WBC COUNT", "Total Leukocyte Count"
    ],
    "platelet_count": [
        "PLATELET COUNT", "Platelet Count", "Platelet count"
    ],

    "neutrophils": [
        "Neutrophils", "NEUTROPHILS", "Neutrophils abs"
    ],
    "lymphocytes": [
        "Lymphocytes", "LYMPHOCYTES", "Absolute Lymphocyte Count"
    ],
    "eosinophils": [
        "Eosinophils", "EOSINOPHILS", "Absolute Eosinophil Count AEC"
    ],
    "basophils": [
        "Basophils", "BASOPHILS", "Absolute Basophil Count"
    ],
    "monocytes": [
        "MONOCYTES", "Monocytes", "Absolute Monocyte Count"
    ],
    "esr": ["ESR", "E S R", "ES R"],

    "platelet_indices": [
        "PLATELET INDICES", "Mean Platelet Volume",
        "IMMATURE PLATELET FRACTION"
    ],

    # --- Electrolytes ---
    "sodium": ["SODIUM", "SODIUM Na -", "Serum Sodium", "SERUM SODIUM"],
    "potassium": [
        "POTASSIUM", "SERUM POTASSIUM", "Potassium K",
        "POTASSIUM SERUM", "Serum Potassium"
    ],
    "chloride": ["CHLORIDE", "Serum Chloride"],
    "calcium_total": ["Calcium", "CALCIUM", "Calcium Total"],
    "calcium_ionized": ["Calcium Ionized", "IONIC CALCIUM"],
    "phosphorus": [
        "PHOSPHORUS", "S Phosphorus", "INORGANIC PHOSPHORUS"
    ],
    "magnesium": ["MAGNESIUM", "Magnesium"],

    # --- Diabetes ---
    "hba1c": ["HbA1c", "HBA IC", "HEMOGLOBIN HBAIC"],
    "glucose_fasting": ["BLOOD SUGAR FASTING", "Fasting Blood Sugar"],
    "glucose_random": [
        "Blood Sugar Random", "RANDOM BLOOD GLUCOSE",
        "Blood Glucose Random -Plasma", "Glucose Random Hexokinase"
    ],
    "mean_plasma_glucose": [
        "MEAN PLASMA GLUCOSE", "Random Plasma Glucose"
    ],

    # --- Lipids ---
    "cholesterol_total": ["TOTAL CHOLESTEROL", "CHOLESTEROL"],
    "hdl": ["HDL CHOLESTEROL", "HDL CHOLESTEROL RATIO"],
    "ldl": ["LDL", "LDL CHOLESTEROL DIRECT", "L DL CHOLESTEROL DIRECT"],

    # --- CRP ---
    "crp": [
        "CRP", "C-REACTIVE PROTEIN",
        "CRP QUANTITATIVE", "CRP Quantitatiw"
    ],

    # --- Thyroid ---
    "tsh": ["TSH", "TSH Thyroid Stimulating Hormone"]
}

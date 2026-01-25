from lab_report_analysis.preprocessing.image_preprocessor import ImagePreprocessor
from lab_report_analysis.ocr.ocr_engine import OCRReader
from lab_report_analysis.cleaning.text_cleaner import TextCleaner
from lab_report_analysis.extraction.extractor import LabExtractor
from lab_report_analysis.reasoning.pattern_analyzer import PatternAnalyzer

import cv2
import os

def process_lab_report(image_path):

    # PREPROCESSING
    preprocessor = ImagePreprocessor(save_intermediate=True)
    cleaned_image = preprocessor.preprocess(image_path)

    cleaned_path = "processed_reports/cleaned_output.png"
    os.makedirs("processed_reports", exist_ok=True)
    cv2.imwrite(cleaned_path, cleaned_image)

    # OCR
    ocr = OCRReader()
    raw_text = ocr.extract_text(cleaned_path)

    # CLEANING
    cleaner = TextCleaner()
    cleaned_text = cleaner.clean_text(raw_text)

    # EXTRACTION
    extractor = LabExtractor()
    data = extractor.extract(cleaned_text)

    # PATTERN ANALYSIS
    analyzer = PatternAnalyzer()
    pattern_results = analyzer.analyze_patterns(data)

    # RETURN JSON-friendly structure
    return {
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "extracted_data": data,
        "patterns": pattern_results
    }

import easyocr

class OCRReader:
    def __init__(self):
        # English OCR model
        self.reader = easyocr.Reader(['en'], gpu=False)

    def extract_text(self, image_path):
        # detail=0 → returns only text
        results = self.reader.readtext(image_path, detail=0)
        return "\n".join(results)

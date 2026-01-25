import cv2
import numpy as np
import os
from .utils import deskew_image

class ImagePreprocessor:
    def __init__(self, save_intermediate=False):
        self.save_intermediate = save_intermediate

    def _save_step(self, step_name, image):
        if self.save_intermediate:
            os.makedirs("processed_reports/steps", exist_ok=True)
            cv2.imwrite(f"processed_reports/steps/{step_name}.png", image)


    def load_image(self, path):
        image = cv2.imread(path)
        if image is None:
            raise FileNotFoundError("Unable to load image. Check path.")
        self._save_step("01_original", image)
        return image

    def to_grayscale(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self._save_step("02_grayscale", gray)
        return gray

    def remove_noise(self, image):
        denoised = cv2.fastNlMeansDenoising(image, h=30)
        self._save_step("03_denoised", denoised)
        return denoised

    def adjust_contrast(self, image):
        alpha = 1.8  # contrast factor
        beta = -30   # brightness
        adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        self._save_step("04_contrast", adjusted)
        return adjusted

    def threshold(self, image):
        thresh = cv2.adaptiveThreshold(
            image, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            8
        )
        self._save_step("05_threshold", thresh)
        return thresh

    def sharpen(self, image):
        kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
        sharp = cv2.filter2D(image, -1, kernel)
        self._save_step("06_sharpen", sharp)
        return sharp

    def resize(self, image):
        height, width = image.shape[:2]
        scale = 1.3
        resized = cv2.resize(image, (int(width*scale), int(height*scale)))
        self._save_step("07_resized", resized)
        return resized

    def preprocess(self, image_path):
        img = self.load_image(image_path)
        img = self.to_grayscale(img)
        img = self.remove_noise(img)
        img = self.adjust_contrast(img)
        img = deskew_image(img)
        img = self.threshold(img)
        img = self.sharpen(img)
        img = self.resize(img)

        self._save_step("08_final_preprocessed", img)
        return img

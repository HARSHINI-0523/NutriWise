import cv2
import numpy as np

def deskew_image(image):
    gray = image.copy()

    # Compute moments to detect skew angle
    coords = np.column_stack(np.where(gray > 0))
    if coords.size == 0:
        return image

    angle = cv2.minAreaRect(coords)[-1]

    # Fix angle
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # Rotate to deskew
    (h, w) = gray.shape[:2]
    center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    deskewed = cv2.warpAffine(gray, M, (w, h), flags=cv2.INTER_CUBIC)

    return deskewed

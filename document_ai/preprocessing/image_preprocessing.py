from pathlib import Path

import cv2  # type: ignore[import-not-found]
import numpy as np  # type: ignore[import-not-found]
import pdfplumber  # type: ignore[import-not-found]

from common.logging_config import get_logger

logger = get_logger(__name__)


MIN_TEXT_CHARS_FOR_TEXT_PDF = 20


def pdf_needs_ocr(pdf_path: str | Path) -> bool:
    
    pdf_path = Path(pdf_path)
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if not pdf.pages:
                return True
            sample_pages = pdf.pages[: min(3, len(pdf.pages))]
            total_chars = sum(len((p.extract_text() or "")) for p in sample_pages)
            avg_chars = total_chars / len(sample_pages)
            return avg_chars < MIN_TEXT_CHARS_FOR_TEXT_PDF
    except Exception as exc:  # noqa: BLE001 — genuinely want to fall back to OCR on any failure
        logger.warning("Could not inspect PDF text layer (%s); assuming OCR needed", exc)
        return True


def deskew(image: np.ndarray) -> np.ndarray:
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    gray = cv2.bitwise_not(gray)
    coords = np.column_stack(np.where(gray > 0))
    if coords.size == 0:
        return image
    angle = cv2.minAreaRect(coords)[-1]
    angle = -(90 + angle) if angle < -45 else -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(
        image, matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )


def denoise_and_binarize(image: np.ndarray) -> np.ndarray:
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    _, binarized = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binarized


def preprocess_image(image: np.ndarray) -> np.ndarray:
    
    image = deskew(image)
    image = denoise_and_binarize(image)
    return image


def load_image(path: str | Path) -> np.ndarray:
    path = Path(path)
    image = cv2.imread(str(path))
    if image is None:
        raise FileNotFoundError(f"Could not read image at {path}")
    return image

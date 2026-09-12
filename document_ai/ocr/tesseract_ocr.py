from dataclasses import dataclass

import numpy as np  # type: ignore[import-not-found]
import pytesseract  # type: ignore[import-not-found]

from common.constants import DEFAULT_OCR_LANGUAGE, MIN_OCR_CONFIDENCE
from common.exceptions import LowConfidenceOCRError
from common.logging_config import get_logger
from common.text_utils import normalize_unicode, normalize_whitespace

logger = get_logger(__name__)


@dataclass
class OCRResult:
    text: str
    confidence: float  # 0-100, mean word-level confidence
    language: str
    below_min_confidence: bool


def run_ocr(
    image: np.ndarray,
    language: str = DEFAULT_OCR_LANGUAGE,
    strict: bool = False,
) -> OCRResult:
    
    data = pytesseract.image_to_data(
        image, lang=language, output_type=pytesseract.Output.DICT
    )

    words = [w for w in data["text"] if w.strip()]
    confidences = [int(c) for c, w in zip(data["conf"], data["text"]) if w.strip() and int(c) >= 0]

    raw_text = " ".join(words)
    text = normalize_whitespace(normalize_unicode(raw_text))
    mean_confidence = float(np.mean(confidences)) if confidences else 0.0
    below_min = mean_confidence < MIN_OCR_CONFIDENCE

    if below_min:
        logger.warning("OCR confidence %.1f below minimum %.1f", mean_confidence, MIN_OCR_CONFIDENCE)
        if strict:
            raise LowConfidenceOCRError(mean_confidence)

    return OCRResult(
        text=text,
        confidence=mean_confidence,
        language=language,
        below_min_confidence=below_min,
    )


def run_ocr_multi_page(
    images: list[np.ndarray], language: str = DEFAULT_OCR_LANGUAGE
) -> list[OCRResult]:
    return [run_ocr(img, language=language) for img in images]

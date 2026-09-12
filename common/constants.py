SOURCE_LABEL_OFFICIAL = "official"
SOURCE_LABEL_LICENSED_SANDBOX = "licensed_sandbox"
SOURCE_LABEL_SYNTHETIC = "synthetic"

SOURCE_LABEL_DISPLAY_NAMES = {
    SOURCE_LABEL_OFFICIAL: "Official / Authorized",
    SOURCE_LABEL_LICENSED_SANDBOX: "Licensed third-party (sandbox)",
    SOURCE_LABEL_SYNTHETIC: "Synthetic / demonstration",
}


SUPPORTED_DOCUMENT_TYPES = [
    "gst_certificate",
    "pan_card",
    "udyam_certificate",
    "turnover_statement",
    "oem_authorization_letter",
    "epfo_esic_certificate",
    "startup_india_certificate",
    "nsic_certificate",
    "tender_pdf",
]


DEFAULT_OCR_LANGUAGE = "eng"
MIN_OCR_CONFIDENCE = 60  

SYNTHETIC_DATA_WATERMARK = "SYNTHETIC DEMONSTRATION DATA — NOT A GOVERNMENT DOCUMENT"
DEFAULT_SYNTHETIC_DATA_DIR = "data/synthetic"
DEFAULT_GROUND_TRUTH_CSV = "data/ground_truth.csv"
DEFAULT_MODEL_ARTIFACT_DIR = "risk_classifier/artifacts"

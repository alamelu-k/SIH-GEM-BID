class Pod4BaseError(Exception):
    """Base class for all Pod 4 (AI/ML) exceptions."""
    
class ExtractionError(Pod4BaseError):
    """Raised when structured field extraction fails outright"""


class LowConfidenceOCRError(Pod4BaseError):
    def __init__(self, confidence: float, document_id: str | None = None):
        self.confidence = confidence
        self.document_id = document_id
        super().__init__(
            f"OCR confidence {confidence:.1f} below minimum threshold"
            + (f" for document {document_id}" if document_id else "")
        )


class InvalidIDFormatError(Pod4BaseError):
    def __init__(self, id_type: str, value: str):
        self.id_type = id_type
        self.value = value
        super().__init__(f"'{value}' is not a valid {id_type} format")


class DocumentClassificationError(Pod4BaseError):
    """Raised when the document classifier cannot confidently assign a DocumentType."""



class ClauseExtractionError(Pod4BaseError):
    """Raised when tender clause extraction fails to produce a valid structured requirement list."""



class InsufficientDataError(Pod4BaseError):
    def __init__(self, required: int, actual: int, context: str = ""):
        self.required = required
        self.actual = actual
        super().__init__(
            f"Insufficient data{f' for {context}' if context else ''}: "
            f"need at least {required}, got {actual}"
        )


class ModelNotTrainedError(Pod4BaseError):
    """Raised when risk_classifier inference is requested but no
    trained model artifact has been loaded."""


class GraphConstructionError(Pod4BaseError):
    """Raised when the shell-company relationship graph cannot be
    built from the provided bidder data."""


class AggregationError(Pod4BaseError):
    """Raised when the risk aggregator cannot combine signals — e.g.
    a required signal is missing entirely rather than just low-confidence."""

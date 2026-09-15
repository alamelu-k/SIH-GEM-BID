from document_ai.classification.document_classifier import classify_document


class DocumentMLService:
    """Service wrapper around the existing document classifier."""

    @staticmethod
    def classify(text: str):
        """Classify document text using the existing classification pipeline."""
        return classify_document(text)
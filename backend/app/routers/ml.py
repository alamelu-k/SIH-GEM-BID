from fastapi import APIRouter

from app.ml.service import DocumentMLService
from app.schemas import (
    DocumentClassificationRequest,
    DocumentClassificationResponse,
)


router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning"],
)


@router.post(
    "/classify",
    response_model=DocumentClassificationResponse,
)
def classify_document_endpoint(
    request: DocumentClassificationRequest,
):
    result = DocumentMLService.classify(request.text)

    return DocumentClassificationResponse(
        document_type=result.document_type.value,
        confidence=result.confidence,
    )
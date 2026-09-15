from fastapi.testclient import TestClient

from app.main import app


from app import models
from app.auth import get_current_officer

officer_user = models.Officer(
    id=998,
    email="test.officer@cpcl.gov.in",
    hashed_password="fake",
    role="officer",
    is_active=True,
)
app.dependency_overrides[get_current_officer] = lambda: officer_user

client = TestClient(app)


def test_ml_classification_gst_certificate():
    response = client.post(
        "/api/v1/ml/classify",
        json={
            "text": "GOODS AND SERVICES TAX GSTIN CERTIFICATE OF REGISTRATION"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["document_type"] == "gst_certificate"
    assert data["confidence"] == 1.0
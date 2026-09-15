from fastapi.testclient import TestClient

from app.main import app


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
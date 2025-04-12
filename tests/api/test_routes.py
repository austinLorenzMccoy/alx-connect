import pytest
from fastapi import status
from fastapi.testclient import TestClient
from alx_connect.main import app
from alx_connect.models.profile import ProfileInput
from alx_connect.models.chat import QuestionInput
import io

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_profile_input():
    return ProfileInput(
        id="test123",
        full_name="John Doe",
        email="john@example.com",
        personal_summary="Experienced software engineer",
        professional_summary="5+ years in backend development",
        cumulative_year=5,
        portfolio="https://github.com/johndoe"
    )

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_mentor_matching_endpoint(client, sample_profile_input):
    response = client.post(
        "/api/v1/mentor-matching/",
        json=[sample_profile_input.model_dump()]
    )
    assert response.status_code == 200
    assert "matches" in response.json()

def test_ask_question_endpoint(client):
    response = client.post(
        "/api/v1/ask-question/",
        json={
            "question": "What are the best practices for system design interviews?",
            "conversation_id": None
        }
    )
    assert response.status_code == 200
    assert "answer" in response.json()

def test_generate_summary_endpoint(client, sample_profile_input):
    response = client.post(
        "/api/v1/generate-summary/",
        json=sample_profile_input.model_dump()
    )
    assert response.status_code == 200
    assert "summary" in response.json()

def test_cv_review_endpoint(client):
    # Create a sample PDF-like content
    sample_cv = io.BytesIO(b"Sample CV content")
    sample_cv.name = "test_cv.pdf"
    
    files = {
        "file": ("test_cv.pdf", sample_cv, "application/pdf")
    }
    
    response = client.post(
        "/api/v1/cv-review/",
        files=files
    )
    
    assert response.status_code == 200
    assert "analysis" in response.json()
    assert "suggestions" in response.json()
    assert "extracted_info" in response.json()
    assert response.json()["status"] == "success"

def test_cv_review_endpoint_invalid_file(client):
    # Test with empty file
    files = {
        "file": ("empty.pdf", io.BytesIO(b""), "application/pdf")
    }
    
    response = client.post(
        "/api/v1/cv-review/",
        files=files
    )
    
    assert response.status_code == 500 
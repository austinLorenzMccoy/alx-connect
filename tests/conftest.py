import pytest
from fastapi.testclient import TestClient
from alx_connect.main import app
from alx_connect.models.profile import Profile, ProfileInput
from alx_connect.models.chat import Message, MessageRole, ConversationState
import numpy as np
from datetime import datetime

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

@pytest.fixture
def sample_profile():
    return Profile(
        id="test123",
        full_name="John Doe",
        email="john@example.com",
        personal_summary="Experienced software engineer",
        professional_summary="5+ years in backend development",
        cumulative_year=5,
        portfolio="https://github.com/johndoe",
        extracted_skills={"Python", "FastAPI", "Docker"},
        industry_domains={"Software Development", "Cloud Computing"},
        seniority_keywords={"Senior", "Lead"},
        semantic_embedding=np.random.rand(384)  # Mock embedding
    )

@pytest.fixture
def sample_message():
    return Message(
        role=MessageRole.USER,
        content="What are the best practices for system design interviews?",
        timestamp=datetime.now()
    )

@pytest.fixture
def sample_conversation_state():
    return ConversationState(
        messages=[
            Message(
                role=MessageRole.USER,
                content="What are the best practices for system design interviews?",
                timestamp=datetime.now()
            )
        ],
        last_activity=datetime.now(),
        active=True
    ) 
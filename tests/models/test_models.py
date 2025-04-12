import pytest
from datetime import datetime
from alx_connect.models.profile import Profile, ProfileInput
from alx_connect.models.chat import Message, MessageRole, ConversationState, QuestionInput

def test_profile_input_validation():
    # Test valid profile input
    profile = ProfileInput(
        id="test123",
        full_name="John Doe",
        email="john@example.com",
        personal_summary="Experienced developer",
        professional_summary="5+ years experience",
        cumulative_year=5,
        portfolio="https://github.com/johndoe"
    )
    assert profile.id == "test123"
    assert profile.email == "john@example.com"
    
    # Test invalid email
    with pytest.raises(ValueError):
        ProfileInput(
            id="test123",
            full_name="John Doe",
            email="invalid-email",
            personal_summary="Test",
            professional_summary="Test",
            cumulative_year=5,
            portfolio="https://github.com/johndoe"
        )
    
    # Test invalid portfolio URL
    with pytest.raises(ValueError):
        ProfileInput(
            id="test123",
            full_name="John Doe",
            email="john@example.com",
            personal_summary="Test",
            professional_summary="Test",
            cumulative_year=5,
            portfolio="not-a-url"
        )

def test_profile_initialization():
    profile = Profile(
        id="test123",
        full_name="John Doe",
        email="john@example.com",
        personal_summary="Test",
        professional_summary="Test",
        cumulative_year=5,
        portfolio="https://github.com/johndoe"
    )
    
    assert profile.extracted_skills == set()
    assert profile.industry_domains == set()
    assert profile.seniority_keywords == set()
    assert profile.semantic_embedding is None

def test_profile_to_dict():
    profile = Profile(
        id="test123",
        full_name="John Doe",
        email="john@example.com",
        personal_summary="Test",
        professional_summary="Test",
        cumulative_year=5,
        portfolio="https://github.com/johndoe",
        industry_domains={"Software", "Cloud"}
    )
    
    profile_dict = profile.to_dict()
    assert profile_dict["id"] == "test123"
    assert profile_dict["domains"] == ["Software", "Cloud"]
    assert "extracted_skills" not in profile_dict
    assert "semantic_embedding" not in profile_dict

def test_message_validation():
    # Test valid message
    message = Message(
        role=MessageRole.USER,
        content="Hello, world!"
    )
    assert message.role == MessageRole.USER
    assert message.content == "Hello, world!"
    assert isinstance(message.timestamp, datetime)
    
    # Test empty content
    with pytest.raises(ValueError):
        Message(
            role=MessageRole.USER,
            content=""
        )
    
    # Test whitespace content
    with pytest.raises(ValueError):
        Message(
            role=MessageRole.USER,
            content="   "
        )

def test_conversation_state():
    messages = [
        Message(
            role=MessageRole.USER,
            content="Hello"
        ),
        Message(
            role=MessageRole.ASSISTANT,
            content="Hi there!"
        )
    ]
    
    state = ConversationState(
        messages=messages,
        last_activity=datetime.now(),
        active=True
    )
    
    assert len(state.messages) == 2
    assert state.active is True
    assert isinstance(state.last_activity, datetime)

def test_question_input_validation():
    # Test valid question input
    question = QuestionInput(
        question="What is system design?",
        conversation_id="test123"
    )
    assert question.question == "What is system design?"
    assert question.conversation_id == "test123"
    
    # Test empty question
    with pytest.raises(ValueError):
        QuestionInput(
            question="",
            conversation_id="test123"
        )
    
    # Test whitespace question
    with pytest.raises(ValueError):
        QuestionInput(
            question="   ",
            conversation_id="test123"
        ) 
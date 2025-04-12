import pytest
from datetime import datetime, timedelta
from alx_connect.services.interview_coach import InterviewCoach
from alx_connect.models.chat import MessageRole

@pytest.fixture
def interview_coach():
    return InterviewCoach()

def test_initialization(interview_coach):
    assert interview_coach.llm is not None
    assert interview_coach.embeddings is not None
    assert interview_coach.text_splitter is not None
    assert interview_coach.vectorstore is not None

def test_process_csv_data(interview_coach):
    csv_data = [
        {
            "question": "What is system design?",
            "answer": "System design is the process of defining the architecture...",
            "category": "System Design",
            "difficulty": "Medium"
        }
    ]
    processed_texts = interview_coach.process_csv_data(csv_data)
    assert len(processed_texts) == 1
    assert "Question:" in processed_texts[0]
    assert "Answer:" in processed_texts[0]
    assert "Category:" in processed_texts[0]
    assert "Difficulty:" in processed_texts[0]

def test_create_rag_chain(interview_coach):
    chain = interview_coach.create_rag_chain()
    assert chain is not None
    assert hasattr(chain, 'run')

def test_clean_response(interview_coach):
    # Test with markdown
    response = "```python\nprint('Hello')\n```"
    cleaned = interview_coach.clean_response(response)
    assert "```" not in cleaned
    
    # Test with HTML
    response = "<p>Hello <strong>World</strong></p>"
    cleaned = interview_coach.clean_response(response)
    assert "<" not in cleaned
    assert ">" not in cleaned

def test_get_conversation_context(interview_coach, sample_conversation_state):
    conversation_id = "test123"
    interview_coach.conversations[conversation_id] = sample_conversation_state
    
    context = interview_coach.get_conversation_context(conversation_id)
    assert context is not None
    assert "user:" in context.lower()
    assert "what are the best practices" in context.lower()

def test_add_message_to_conversation(interview_coach):
    conversation_id = "test123"
    message_content = "New test message"
    
    interview_coach.add_message_to_conversation(
        conversation_id,
        MessageRole.USER,
        message_content
    )
    
    assert conversation_id in interview_coach.conversations
    assert len(interview_coach.conversations[conversation_id].messages) == 1
    assert interview_coach.conversations[conversation_id].messages[0].content == message_content

def test_clean_inactive_conversations(interview_coach):
    # Create an active conversation
    active_id = "active123"
    interview_coach.conversations[active_id] = interview_coach.conversations.get(
        active_id,
        interview_coach.conversations[active_id]
    )
    
    # Create an inactive conversation
    inactive_id = "inactive123"
    interview_coach.conversations[inactive_id] = interview_coach.conversations.get(
        inactive_id,
        interview_coach.conversations[inactive_id]
    )
    interview_coach.conversations[inactive_id].last_activity = datetime.now() - timedelta(hours=2)
    
    # Clean up inactive conversations
    interview_coach.clean_inactive_conversations()
    
    # Verify results
    assert active_id in interview_coach.conversations
    assert inactive_id not in interview_coach.conversations 
import pytest
from alx_connect.services.cv_review import CVReviewService

@pytest.fixture
def cv_reviewer():
    return CVReviewService()

def test_initialization(cv_reviewer):
    assert cv_reviewer.llm is not None
    assert cv_reviewer.parser is not None
    assert cv_reviewer.resume_analysis_prompt is not None

@pytest.mark.asyncio
async def test_analyze_resume(cv_reviewer):
    sample_resume = """
    John Doe
    Software Engineer
    
    Experience:
    - Senior Software Engineer at Tech Corp (2018-Present)
      * Led development of microservices architecture
      * Managed team of 5 engineers
    
    Education:
    - BS Computer Science, University of Technology (2014-2018)
    
    Skills:
    - Python, Java, Docker, Kubernetes
    - Team Leadership, Project Management
    """
    
    result = await cv_reviewer.analyze_resume(sample_resume)
    assert result["status"] == "success"
    assert "feedback" in result
    assert len(result["feedback"]) > 0

def test_extract_key_information(cv_reviewer):
    sample_parsed_resume = {
        "contact": {
            "name": "John Doe",
            "email": "john@example.com"
        },
        "work_experience": [
            {
                "title": "Senior Software Engineer",
                "company": "Tech Corp",
                "duration": "2018-Present",
                "description": "Led development of microservices architecture"
            }
        ],
        "education": [
            {
                "degree": "BS Computer Science",
                "institution": "University of Technology",
                "year": "2018"
            }
        ],
        "skills": ["Python", "Java", "Docker"],
        "certifications": ["AWS Certified Developer"]
    }
    
    key_info = cv_reviewer.extract_key_information(sample_parsed_resume)
    
    assert "contact_info" in key_info
    assert "work_experience" in key_info
    assert "education" in key_info
    assert "skills" in key_info
    assert "certifications" in key_info
    
    assert key_info["contact_info"]["name"] == "John Doe"
    assert len(key_info["work_experience"]) == 1
    assert len(key_info["education"]) == 1
    assert len(key_info["skills"]) == 3
    assert len(key_info["certifications"]) == 1

def test_generate_improvement_suggestions(cv_reviewer):
    # Test with empty resume
    empty_info = {
        "contact_info": {},
        "work_experience": [],
        "education": [],
        "skills": [],
        "certifications": []
    }
    suggestions = cv_reviewer.generate_improvement_suggestions(empty_info)
    assert len(suggestions) > 0
    assert any("contact information" in s.lower() for s in suggestions)
    assert any("work experience" in s.lower() for s in suggestions)
    assert any("education" in s.lower() for s in suggestions)
    assert any("skills" in s.lower() for s in suggestions)
    
    # Test with incomplete work experience
    incomplete_info = {
        "contact_info": {"name": "John Doe"},
        "work_experience": [{"company": "Tech Corp", "description": ""}],
        "education": [{"degree": "BS", "institution": "University"}],
        "skills": ["Python"],
        "certifications": []
    }
    suggestions = cv_reviewer.generate_improvement_suggestions(incomplete_info)
    assert any("Tech Corp" in s for s in suggestions) 
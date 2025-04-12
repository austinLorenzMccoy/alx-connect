import pytest
import numpy as np
from alx_connect.services.matching import ImprovedMentorMatchingSystem

def test_calculate_domain_similarity():
    matching_system = ImprovedMentorMatchingSystem()
    
    # Test with overlapping domains
    mentor_domains = {"Software", "Cloud", "AI"}
    mentee_domains = {"Software", "Cloud", "Web"}
    similarity = matching_system.calculate_domain_similarity(mentor_domains, mentee_domains)
    assert 0 <= similarity <= 1
    assert similarity == 0.5  # 2 common domains out of 4 total
    
    # Test with no overlapping domains
    mentor_domains = {"Software", "Cloud"}
    mentee_domains = {"Marketing", "Sales"}
    similarity = matching_system.calculate_domain_similarity(mentor_domains, mentee_domains)
    assert similarity == 0.0
    
    # Test with empty sets
    similarity = matching_system.calculate_domain_similarity(set(), set())
    assert similarity == 0.0

def test_calculate_experience_score():
    matching_system = ImprovedMentorMatchingSystem()
    
    # Test within valid range
    score = matching_system.calculate_experience_score(5.0, 2.0)
    assert 0 <= score <= 1
    
    # Test below minimum gap
    score = matching_system.calculate_experience_score(2.0, 1.9)
    assert score == 0.0
    
    # Test above maximum gap
    score = matching_system.calculate_experience_score(15.0, 2.0)
    assert score == 0.0

def test_calculate_semantic_similarity():
    matching_system = ImprovedMentorMatchingSystem()
    
    # Create mock embeddings
    emb1 = np.random.rand(384)
    emb2 = np.random.rand(384)
    
    # Test with valid embeddings
    similarity = matching_system.calculate_semantic_similarity(emb1, emb2)
    assert 0 <= similarity <= 1
    
    # Test with None embeddings
    similarity = matching_system.calculate_semantic_similarity(None, emb2)
    assert similarity == 0.0

def test_calculate_match_score(sample_profile):
    matching_system = ImprovedMentorMatchingSystem()
    
    # Create a mentee profile with different experience
    mentee_profile = sample_profile
    mentee_profile.cumulative_year = 2
    
    # Test match score calculation
    score, breakdown = matching_system.calculate_match_score(sample_profile, mentee_profile)
    assert 0 <= score <= 1
    assert "experience_score" in breakdown
    assert "semantic_score" in breakdown
    assert "domain_score" in breakdown
    assert "skill_score" in breakdown

def test_find_matches(sample_profile):
    matching_system = ImprovedMentorMatchingSystem()
    
    # Create a list of profiles with varying experience levels
    profiles = [
        sample_profile,  # Mentor (5 years)
        sample_profile.copy(update={"cumulative_year": 2}),  # Mentee
        sample_profile.copy(update={"cumulative_year": 1}),  # Mentee
        sample_profile.copy(update={"cumulative_year": 6})   # Mentor
    ]
    
    # Test matching
    matches = matching_system.find_matches(profiles)
    assert len(matches) > 0
    
    # Verify match structure
    for mentor, mentee, score, breakdown in matches:
        assert mentor.cumulative_year >= 5
        assert mentee.cumulative_year < 5
        assert 0 <= score <= 1
        assert isinstance(breakdown, dict) 
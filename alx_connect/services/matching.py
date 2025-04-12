import numpy as np
from typing import Set, Dict, List, Tuple, Optional
from sklearn.metrics.pairwise import cosine_similarity
from ..models.profile import Profile
from ..config.config import MATCHING_CONFIG

class ImprovedMentorMatchingSystem:
    def __init__(self, 
                 experience_weight: float = MATCHING_CONFIG["experience_weight"],
                 semantic_weight: float = MATCHING_CONFIG["semantic_weight"],
                 skill_weight: float = MATCHING_CONFIG["skill_weight"],
                 domain_weight: float = MATCHING_CONFIG["domain_weight"],
                 min_experience_gap: float = MATCHING_CONFIG["min_experience_gap"],
                 max_experience_gap: float = MATCHING_CONFIG["max_experience_gap"]):
        self.experience_weight = experience_weight
        self.semantic_weight = semantic_weight
        self.skill_weight = skill_weight
        self.domain_weight = domain_weight
        self.min_experience_gap = min_experience_gap
        self.max_experience_gap = max_experience_gap

    def calculate_domain_similarity(self, mentor_domains: Set[str], mentee_domains: Set[str]) -> float:
        if not mentor_domains or not mentee_domains:
            return 0.0
        intersection = mentor_domains.intersection(mentee_domains)
        union = mentor_domains.union(mentee_domains)
        return len(intersection) / len(union) if union else 0.0

    def calculate_experience_score(self, mentor_exp: float, mentee_exp: float) -> float:
        experience_gap = mentor_exp - mentee_exp
        if experience_gap < self.min_experience_gap:
            return 0.0
        if experience_gap > self.max_experience_gap:
            return 0.0
        return 1.0 - (experience_gap / self.max_experience_gap)

    def calculate_semantic_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        if emb1 is None or emb2 is None:
            return 0.0
        return float(cosine_similarity([emb1], [emb2])[0][0])

    def calculate_match_score(self, mentor: Profile, mentee: Profile) -> Tuple[float, Dict]:
        experience_score = self.calculate_experience_score(
            mentor.cumulative_year, mentee.cumulative_year
        )
        
        semantic_score = self.calculate_semantic_similarity(
            mentor.semantic_embedding, mentee.semantic_embedding
        )
        
        domain_score = self.calculate_domain_similarity(
            mentor.industry_domains, mentee.industry_domains
        )
        
        skill_score = self.calculate_domain_similarity(
            mentor.extracted_skills, mentee.extracted_skills
        )
        
        total_score = (
            self.experience_weight * experience_score +
            self.semantic_weight * semantic_score +
            self.domain_weight * domain_score +
            self.skill_weight * skill_score
        )
        
        breakdown = {
            "experience_score": experience_score,
            "semantic_score": semantic_score,
            "domain_score": domain_score,
            "skill_score": skill_score
        }
        
        return total_score, breakdown

    def find_matches(self, profiles: List[Profile]) -> List[Tuple[Profile, Profile, float, Dict]]:
        mentors = [p for p in profiles if p.cumulative_year >= 5]
        mentees = [p for p in profiles if p.cumulative_year < 5]
        
        matches = []
        for mentee in mentees:
            mentee_matches = []
            for mentor in mentors:
                score, breakdown = self.calculate_match_score(mentor, mentee)
                if score > 0:
                    mentee_matches.append((mentor, mentee, score, breakdown))
            
            # Sort matches by score in descending order
            mentee_matches.sort(key=lambda x: x[2], reverse=True)
            matches.extend(mentee_matches)
        
        return matches 
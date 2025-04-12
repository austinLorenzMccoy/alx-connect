from dataclasses import dataclass
from typing import Set, Dict, List
import numpy as np
from pydantic import BaseModel, EmailStr, HttpUrl, Field

class ProfileInput(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    personal_summary: str
    professional_summary: str
    cumulative_year: int
    portfolio: str

    def model_dump(self) -> dict:
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "personal_summary": self.personal_summary,
            "professional_summary": self.professional_summary,
            "cumulative_year": self.cumulative_year,
            "portfolio": self.portfolio
        }

@dataclass
class Profile:
    id: str
    full_name: str
    email: str
    personal_summary: str
    professional_summary: str
    cumulative_year: int
    portfolio: str
    extracted_skills: Set[str] = None
    industry_domains: Set[str] = None
    seniority_keywords: Set[str] = None
    semantic_embedding: np.ndarray = None

    def __post_init__(self):
        self.extracted_skills = set() if self.extracted_skills is None else self.extracted_skills
        self.industry_domains = set() if self.industry_domains is None else self.industry_domains
        self.seniority_keywords = set() if self.seniority_keywords is None else self.seniority_keywords

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "personal_summary": self.personal_summary,
            "professional_summary": self.professional_summary,
            "cumulative_year": self.cumulative_year,
            "portfolio": self.portfolio,
            "domains": list(self.industry_domains) if self.industry_domains else []
        }

    def copy(self, **kwargs):
        """Create a copy of the profile with optional updates."""
        profile_dict = {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "personal_summary": self.personal_summary,
            "professional_summary": self.professional_summary,
            "cumulative_year": self.cumulative_year,
            "portfolio": self.portfolio,
            "extracted_skills": self.extracted_skills.copy() if self.extracted_skills else set(),
            "industry_domains": self.industry_domains.copy() if self.industry_domains else set(),
            "seniority_keywords": self.seniority_keywords.copy() if self.seniority_keywords else set(),
            "semantic_embedding": self.semantic_embedding.copy() if self.semantic_embedding is not None else None
        }
        profile_dict.update(kwargs)
        return Profile(**profile_dict) 
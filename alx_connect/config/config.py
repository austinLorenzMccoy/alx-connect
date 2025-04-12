import os
from dotenv import load_dotenv
from typing import List

# Load environment variables
load_dotenv()

# API Configuration
API_TITLE = "ALX Connect Hub"
API_VERSION = "1.0.0"
API_DESCRIPTION = "ALX Connect Hub API for mentor matching and interview coaching"

# CORS Configuration
ALLOWED_ORIGINS = [
    "https://alxconnect.pythonanywhere.com",
    "https://alx-connect.netlify.app",
    "http://localhost",
    "http://localhost:5173",
]

# Groq Configuration
GROQ_MODEL_NAME = "llama3-8b-8192"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Matching System Configuration
MATCHING_CONFIG = {
    "experience_weight": 0.3,
    "semantic_weight": 0.2,
    "skill_weight": 0.2,
    "domain_weight": 0.3,
    "min_experience_gap": 0.5,
    "max_experience_gap": 10.0,
}

# Interview Coach Configuration
INTERVIEW_COACH_CONFIG = {
    "context_window": 5,
    "max_conversation_age": 3600,  # 1 hour in seconds
    "cleanup_interval": 300,  # 5 minutes in seconds
}

# File Upload Configuration
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_FILE_TYPES = ["application/pdf", "text/plain", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"] 
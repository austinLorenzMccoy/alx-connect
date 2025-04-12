import logging
from typing import Dict, List
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from llama_parse import LlamaParse
from ..config.config import GROQ_MODEL_NAME, GROQ_API_KEY

class CVReviewService:
    def __init__(self):
        self.setup_logging()
        self.llm = ChatGroq(
            model_name=GROQ_MODEL_NAME,
            api_key=GROQ_API_KEY,
            temperature=0.7
        )
        self.parser = LlamaParse()
        self.resume_analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert CV/Resume reviewer. Analyze the provided resume and provide detailed feedback in the following areas:
            1. Overall Structure and Format
            2. Professional Experience
            3. Skills and Qualifications
            4. Education
            5. Achievements and Impact
            6. Areas for Improvement
            
            Resume Content:
            {resume_content}
            """),
            ("human", "Please provide a comprehensive review of this resume.")
        ])

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    async def parse_resume(self, file_path: str) -> Dict:
        """Parse a resume file and extract structured information."""
        try:
            result = await self.parser.aparse_file(file_path)
            return result
        except Exception as e:
            self.logger.error(f"Error parsing resume: {str(e)}")
            raise

    async def analyze_resume(self, resume_content: str) -> Dict[str, str]:
        """Analyze a resume and provide detailed feedback."""
        try:
            response = await self.llm.ainvoke(
                self.resume_analysis_prompt.format(resume_content=resume_content)
            )
            
            return {
                "feedback": response.content,
                "status": "success"
            }
        except Exception as e:
            self.logger.error(f"Error analyzing resume: {str(e)}")
            return {
                "feedback": "An error occurred while analyzing the resume.",
                "status": "error",
                "error": str(e)
            }

    def extract_key_information(self, parsed_resume: Dict) -> Dict:
        """Extract key information from the parsed resume."""
        key_info = {
            "contact_info": {},
            "work_experience": [],
            "education": [],
            "skills": [],
            "certifications": []
        }
        
        # Extract contact information
        if "contact" in parsed_resume:
            key_info["contact_info"] = parsed_resume["contact"]
        
        # Extract work experience
        if "work_experience" in parsed_resume:
            for exp in parsed_resume["work_experience"]:
                key_info["work_experience"].append({
                    "title": exp.get("title", ""),
                    "company": exp.get("company", ""),
                    "duration": exp.get("duration", ""),
                    "description": exp.get("description", "")
                })
        
        # Extract education
        if "education" in parsed_resume:
            for edu in parsed_resume["education"]:
                key_info["education"].append({
                    "degree": edu.get("degree", ""),
                    "institution": edu.get("institution", ""),
                    "year": edu.get("year", "")
                })
        
        # Extract skills
        if "skills" in parsed_resume:
            key_info["skills"] = parsed_resume["skills"]
        
        # Extract certifications
        if "certifications" in parsed_resume:
            key_info["certifications"] = parsed_resume["certifications"]
        
        return key_info

    def generate_improvement_suggestions(self, key_info: Dict) -> List[str]:
        """Generate specific suggestions for improving the resume."""
        suggestions = []
        
        # Check contact information
        if not key_info["contact_info"]:
            suggestions.append("Add complete contact information including email and phone number.")
        
        # Check work experience
        if not key_info["work_experience"]:
            suggestions.append("Add detailed work experience with specific achievements and responsibilities.")
        else:
            for exp in key_info["work_experience"]:
                if not exp.get("description"):
                    suggestions.append(f"Add more details about your role at {exp.get('company', 'your company')}.")
        
        # Check education
        if not key_info["education"]:
            suggestions.append("Include your educational background with degrees and institutions.")
        
        # Check skills
        if not key_info["skills"]:
            suggestions.append("Add a comprehensive skills section highlighting your technical and soft skills.")
        
        return suggestions 
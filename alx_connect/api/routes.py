from fastapi import APIRouter, File, Form, UploadFile, HTTPException, WebSocket, WebSocketDisconnect, Depends, Request
from typing import List, Optional
import asyncio
import uuid
import tempfile
import os
from ..models.profile import Profile, ProfileInput
from ..models.chat import QuestionInput
from ..services.matching import ImprovedMentorMatchingSystem
from ..services.interview_coach import InterviewCoach
from ..services.cv_review import CVReviewService
from ..config.config import ALLOWED_FILE_TYPES, MAX_UPLOAD_SIZE

router = APIRouter()
matching_system = ImprovedMentorMatchingSystem()
interview_coach = InterviewCoach()
cv_reviewer = CVReviewService()

@router.get("/")
async def root():
    return {
        "message": "Welcome to ALX Connect Hub API",
        "version": "1.0.0",
        "status": "operational"
    }

@router.post("/generate_summary")
async def generate_summary(
    user_id: str = Form(...),
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    if resume.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF, TXT, DOC, and DOCX files are allowed."
        )
    
    if resume.size > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds maximum limit of 5MB"
        )
    
    # Process the resume and generate summary
    # Implementation details would go here
    
    return {
        "status": "success",
        "message": "Summary generated successfully",
        "user_id": user_id
    }

@router.post("/api/v1/mentor-matching/")
async def find_mentor_matches(profiles: List[ProfileInput]):
    try:
        mentee_profile = profiles[0].model_dump()
        matches = matching_system.find_matches(mentee_profile)
        return {"matches": matches}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/ask-question/")
async def ask_interview_question(question_input: QuestionInput):
    try:
        chain = interview_coach.create_rag_chain()
        response = await chain.ainvoke({"question": question_input.question})
        
        # Add to conversation history if conversation_id provided
        if question_input.conversation_id:
            interview_coach.add_message_to_conversation(
                question_input.conversation_id,
                "user",
                question_input.question
            )
            interview_coach.add_message_to_conversation(
                question_input.conversation_id,
                "assistant",
                response
            )
        
        return {
            "answer": interview_coach.clean_response(response),
            "conversation_id": question_input.conversation_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/generate-summary/")
async def generate_resume_summary(profile: ProfileInput):
    try:
        summary = matching_system.generate_profile_summary(profile.model_dump())
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/cv-review/")
async def review_cv(
    file: UploadFile = File(...),
    sections: Optional[List[str]] = None
):
    """
    Upload and analyze a CV/resume file.
    Returns detailed feedback and suggestions for improvement.
    """
    try:
        # Create a temporary file to store the uploaded resume
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            
            # Parse the resume
            parsed_resume = await cv_reviewer.parse_resume(temp_file.name)
            
            # Extract key information
            key_info = cv_reviewer.extract_key_information(parsed_resume)
            
            # Generate improvement suggestions
            suggestions = cv_reviewer.generate_improvement_suggestions(key_info)
            
            # Get detailed analysis
            analysis = await cv_reviewer.analyze_resume(str(parsed_resume))
            
            # Clean up the temporary file
            os.unlink(temp_file.name)
            
            return {
                "analysis": analysis["feedback"],
                "suggestions": suggestions,
                "extracted_info": key_info,
                "status": "success"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws/chat/{conversation_id}")
async def websocket_chat(websocket: WebSocket, conversation_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response = await interview_coach.generate_response(
                data,
                conversation_id
            )
            await websocket.send_text(response)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.close(code=1000) 
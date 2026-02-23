"""
Chat Routes — POST /api/chat/message
Handles all conversational AI requests through the NLP pipeline.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from nlp_service import process_chat_message

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    conversation_phase: str = "icebreaker"
    language: str = "en-US"

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Hi, I've been feeling really stressed lately.",
                "session_id": None,
                "conversation_phase": "icebreaker",
            }
        }


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    crisis_detected: bool
    extracted_data: dict
    phase: str
    sentiment: str


@router.post("/chat/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """
    Main chat endpoint.
    Processes user message through the NLP pipeline and returns
    Aura's response with extracted data and crisis flag.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    if len(request.message) > 2000:
        raise HTTPException(status_code=400, detail="Message too long. Max 2000 characters.")

    result = await process_chat_message(
        user_message=request.message,
        session_id=request.session_id,
        conversation_phase=request.conversation_phase,
        language=request.language
    )

    return ChatResponse(**result)


@router.delete("/chat/session/{session_id}")
async def clear_session(session_id: str):
    """Clear a conversation session from memory (GDPR right to be forgotten)."""
    from nlp_service import _sessions
    if session_id in _sessions:
        del _sessions[session_id]
        return {"status": "cleared", "session_id": session_id}
    return {"status": "not_found", "session_id": session_id}

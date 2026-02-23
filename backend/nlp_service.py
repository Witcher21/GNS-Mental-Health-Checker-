"""
NLP Service — Core LangChain + DeepSeek Integration
Handles all NLP processing: entity extraction, sentiment analysis,
crisis detection, and conversational AI response generation.
"""

import os
import re
import json
import uuid
from typing import Optional
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

# ── Crisis Detection Keywords (Offline Safety Net) ─────────────
CRISIS_KEYWORDS = [
    "kill myself", "end my life", "suicide", "suicidal",
    "self harm", "self-harm", "hurt myself", "want to die",
    "no reason to live", "better off dead", "overdose",
    "cut myself", "cannot go on", "end it all", "not worth living",
    "give up on life", "disappear forever",
    "මාව මරාගන්නවා", "පණ නසාගන්නවා", "ජීවිතේ එපා වෙලා", "ජීවත් වෙලා වැඩක් නෑ",
    "මැරෙන්න හිතෙනවා", "දිවි නසාගන්නවා", "මට මැරෙන්න ඕනේ", "අන්තිම කැමැත්ත"
]

# ── Extracted Data Schema ───────────────────────────────────────
class ExtractedUserData(BaseModel):
    name: Optional[str] = Field(None, description="User's name if mentioned")
    occupation: Optional[str] = Field(None, description="User's job or occupation")
    symptoms: list[str] = Field(default_factory=list, description="Reported symptoms")
    sleep_issues: Optional[bool] = Field(None, description="Whether sleep issues were mentioned")
    appetite_issues: Optional[bool] = Field(None, description="Whether appetite issues were mentioned")
    severity_score: Optional[int] = Field(None, ge=0, le=100, description="Estimated severity 0-100")
    primary_concern: Optional[str] = Field(None, description="Main concern in one phrase")
    sentiment: Optional[str] = Field(None, description="positive/neutral/negative/distressed/crisis")


# ── System Prompt ───────────────────────────────────────────────
SYSTEM_PROMPT = """You are 'Aura', an empathetic first-line mental health triage assistant built for the VibeSync ecosystem.

STRICT RULES:
1. PROACTIVE QUESTIONS — You MUST actively evaluate the user's mental health. Ask one clear question per response about their mood, stress, sleep, or appetite. Do not just wait for them to talk.
2. ACTIVE LISTENING — Validate feelings concisely before asking the next question.
3. NO DIAGNOSIS — Never diagnose. Guide them gently to reflect.
4. TONE — Be warm, professional, and soothing, similar to a real-world counselor.

CLINICAL FLOW:
- Phase 1: Ask their name and how they are currently feeling.
- Phase 2: Probe deeper (e.g., "How is your sleep lately?" or "Are there specific stressors at work/home?").
- Phase 3: Once you have enough context (at least 3-4 turns of them explaining their issues), you MUST provide a final analysis. If you are doing this, start your response with <ANALYSIS_READY>.

FINAL ANALYSIS FORMAT:
When you output <ANALYSIS_READY>, follow it with a beautiful, encouraging markdown summary of their mental state. Use bolding and emojis.
Example:
"Thank you for sharing all of that with me. Here is a brief check-in on your current state:
**Mental Health Analysis** 🧠
- **Mood:** ...
- **Stressors:** ...
- **Actionable Advice:** Try the Box Breathing module in the Wellness tab to help lower your immediate anxiety.

I'm always here if you need to talk more."

ADDITIONALLY — After your conversational response, on a NEW LINE, output a JSON block wrapped in ```json ... ``` with extracted data matching this schema:
{{
  "name": string or null,
  "occupation": string or null,
  "symptoms": [string],
  "sleep_issues": boolean or null,
  "appetite_issues": boolean or null,
  "severity_score": integer 0-100 or null,
  "primary_concern": string or null,
  "sentiment": "positive" | "neutral" | "negative" | "distressed" | "crisis"
}}

Remember: You are evaluating and triaging."""

# ── Session Memory Store ────────────────────────────────────────
# In production, replace with Redis or a DB-backed store
_sessions: dict[str, ConversationBufferWindowMemory] = {}


def get_or_create_session(session_id: Optional[str]) -> tuple[str, ConversationBufferWindowMemory]:
    """Get existing session memory or create a new one."""
    sid: str = session_id if session_id else str(uuid.uuid4())
    if sid not in _sessions:
        _sessions[sid] = ConversationBufferWindowMemory(
            k=10,
            memory_key="chat_history",
            return_messages=True,
        )
    return sid, _sessions[sid]


def check_crisis_offline(text: str) -> bool:
    """
    Rule-based offline crisis scanner.
    Runs BEFORE hitting the LLM to ensure zero-latency crisis detection.
    """
    lower_text = text.lower()
    return any(keyword in lower_text for keyword in CRISIS_KEYWORDS)


def extract_json_block(text: str) -> Optional[dict]:
    """Extract JSON from LLM response."""
    pattern = r"```json\s*([\s\S]*?)\s*```"
    match = re.search(pattern, text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return None
    return None


def clean_response(text: str) -> str:
    """Remove the JSON block from the conversational response."""
    return re.sub(r"```json[\s\S]*?```", "", text).strip()


def build_llm() -> ChatOpenAI:
    """Build the LLM client."""
    return ChatOpenAI(
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
        temperature=0.7,
        max_tokens=512,
    )


async def process_chat_message(
    user_message: str,
    session_id: Optional[str],
    conversation_phase: str = "icebreaker",
    language: str = "en-US",
) -> dict:
    """
    Main NLP pipeline:
    1. Offline crisis scan
    2. LLM response generation
    3. Crisis tag detection in response
    4. JSON data extraction
    5. Return structured response
    """

    # Step 1 — Offline crisis detection (fastest, zero latency)
    crisis_offline = check_crisis_offline(user_message)

    # Step 2 — Session management
    sid, memory = get_or_create_session(session_id)

    # Step 3 — Build LLM chain
    try:
        llm = build_llm()

        lang_instruction = "IMPORTANT: You MUST respond in English."
        if language == "si-LK":
            lang_instruction = "IMPORTANT: You MUST respond in Sinhala (සිංහල). Maintain the same empathetic and professional persona."

        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT + "\n\n" + lang_instruction),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ])

        chain = LLMChain(llm=llm, prompt=prompt, memory=memory, verbose=False)

        # Step 4 — Run the chain
        result = await chain.arun(input=user_message)

    except Exception as e:
        # Graceful fallback if LLM is unavailable
        print(f"LLM error: {e}")
        result = (
            "I'm having a moment of difficulty connecting. "
            "If you're in immediate distress, please call **1333** right now. "
            "I'll be right back with you. 💜"
        )

    # Step 5 — Check if LLM itself flagged a crisis
    crisis_llm = "<CRISIS_FLAG_TRIGGERED>" in result

    # Step 6 — Extract structured data
    extracted_data = extract_json_block(result) or {}

    # Step 7 — Build clean reply
    reply = clean_response(result)
    if crisis_llm:
        reply = reply.replace("<CRISIS_FLAG_TRIGGERED>", "").strip()
    
    # Clean up the analysis tag for the UI
    if "<ANALYSIS_READY>" in reply:
        reply = reply.replace("<ANALYSIS_READY>", "").strip()

    # Step 8 — Determine phase progression
    phase_map = {
        "icebreaker": "intake",
        "intake": "assessment",
        "assessment": "assessment",
        "completed": "completed",
    }
    new_phase = phase_map.get(conversation_phase, conversation_phase)

    # If we have name and occupation, move to assessment faster
    if extracted_data.get("name") and extracted_data.get("occupation"):
        new_phase = "assessment"

    return {
        "session_id": sid,
        "reply": reply or "I'm here. Please continue — I'm listening. 💜",
        "crisis_detected": crisis_offline or crisis_llm or extracted_data.get("sentiment") == "crisis",
        "extracted_data": extracted_data,
        "phase": new_phase,
        "sentiment": extracted_data.get("sentiment", "neutral"),
    }

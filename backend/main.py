from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import logging
from bedrock import ask_question
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)

# Defining Pydantic class for request
class UserQuestion(BaseModel):
    question: str

# Defining Pydantic class for source
class Source(BaseModel):
    rank: int
    document: str
    page_number: int | None
    text: str

# Defining Pydantic class for response
class ParsedResponse(BaseModel):
    answer: str
    sources: list[Source]

app = FastAPI()

# Adding CORS middleware for API to respond to browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://clinical-evidence-assistant.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint to get response from Bedrock
@app.post("/ask", response_model=ParsedResponse)
def ask(question: UserQuestion):
    try:
        response = ask_question(question.question)
    except Exception:
        logger.exception("Failed to process question")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response
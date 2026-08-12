from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from bedrock import ask_question

# Defining Pydantic class for request
class UserQuestion(BaseModel):
    question: str

app = FastAPI()

# Endpoint to get response from Bedrock
@app.post("/ask")
def ask(question: UserQuestion):
    try:
        response = ask_question(question.question)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response
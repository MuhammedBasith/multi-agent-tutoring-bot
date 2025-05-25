from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from agents.tutor_agent import tutor_agent
import os

app = FastAPI(title="Gemini Tutor - Your AI Learning Companion")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

class Question(BaseModel):
    query: str

@app.post("/ask")
async def ask_question(question: Question):
    try:
        answer = tutor_agent(question.query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

from agents.math_agent import handle_math_question
from agents.physics_agent import handle_physics_question
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def classify_subject(question: str) -> str:
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"""
    Classify the subject of this question into one of these categories: "math", "physics", or "general".
    
    Math questions involve calculations, equations, mathematical concepts, or numerical problems.
    Physics questions involve physical phenomena, forces, energy, motion, or scientific principles.
    General questions are anything else, including personal questions, greetings, or non-academic topics.
    
    Question: "{question}"
    
    Respond with just one word: math, physics, or general.
    """
    response = model.generate_content(prompt)
    return response.text.strip().lower()

def tutor_agent(question: str) -> str:
    subject = classify_subject(question)
    if "math" in subject:
        return handle_math_question(question)
    elif "physics" in subject:
        return handle_physics_question(question)
    else:
        return "Sorry, I can only answer math or physics questions right now."

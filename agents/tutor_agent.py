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
    elif "general" in subject:
        # Handle general questions in a friendly way
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""
        You are a friendly educational tutor bot. The user has asked a general question: "{question}"
        
        If this is a greeting, personal question, or casual conversation, respond in a friendly way.
        If it's not related to education, politely remind them that you're primarily a math and physics tutor.
        Keep your response brief and friendly.
        """
        response = model.generate_content(prompt)
        return response.text
    else:
        # Fallback for any other classification
        return "I'm your math and physics tutor. How can I help you with a math or physics question today?"

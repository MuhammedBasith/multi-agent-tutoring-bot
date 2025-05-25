import google.generativeai as genai
from tools.calculator import solve_equation
import os
from dotenv import load_dotenv
import json

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def handle_math_question(question: str) -> str:
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    # First, ask Gemini to decide if we should use the calculator tool
    tool_decision_prompt = f"""
    You are a math tutor assistant that can decide when to use a calculator tool.
    
    Question: {question}
    
    Does this question require a direct calculation? If yes, extract just the mathematical expression to calculate.
    
    Respond in JSON format like this:
    {{"needs_calculator": true/false, "expression": "extracted expression if applicable"}}
    """
    
    decision_response = model.generate_content(tool_decision_prompt)
    
    try:
        decision = json.loads(decision_response.text)
        
        if decision.get("needs_calculator", False) and decision.get("expression"):
            # Use the calculator tool with the extracted expression
            calculation_result = solve_equation(decision["expression"])
            
            # Now ask Gemini to provide a complete answer using the calculation
            final_prompt = f"""
            You are a helpful math tutor. The question was: {question}
            
            I've calculated: {calculation_result}
            
            Please provide a complete, educational answer incorporating this calculation result.
            """
            
            final_response = model.generate_content(final_prompt)
            return final_response.text
    except (json.JSONDecodeError, AttributeError, KeyError):
        # If there's any error in parsing or processing, fall back to direct answer
        pass
        
    # If we didn't use the calculator or there was an error, just answer directly
    response = model.generate_content(f"You are a helpful math tutor. Answer this question thoroughly: {question}")
    return response.text

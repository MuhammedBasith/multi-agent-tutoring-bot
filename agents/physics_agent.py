import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from tools.physics_calculator import solve_physics_problem

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def handle_physics_question(question: str) -> str:
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    # First, ask Gemini to analyze if this is a calculation-based physics problem
    analysis_prompt = f"""
    You are a physics teaching assistant that can decide when to use calculation tools.
    
    Question: {question}
    
    Analyze if this question requires numerical calculations or if it's more conceptual.
    If it requires calculations, identify what type of physics problem it is (kinematics, forces, energy, etc.)
    
    Respond in JSON format like this:
    {{"needs_calculation": true/false, "problem_type": "kinematics/forces/energy/etc", "conceptual_elements": ["list of physics concepts involved"]}}
    """
    
    analysis_response = model.generate_content(analysis_prompt)
    
    try:
        analysis = json.loads(analysis_response.text)
        
        if analysis.get("needs_calculation", False):
            # Try to solve using our physics calculator tool
            calculation_result = solve_physics_problem(question)
            
            # Ask Gemini to provide a complete educational answer incorporating the calculation
            final_prompt = f"""
            You are a physics professor explaining a problem to a student. The question was: {question}
            
            I've calculated: {calculation_result}
            
            Please provide a complete, educational answer that:
            1. Explains the relevant physics concepts ({', '.join(analysis.get('conceptual_elements', ['']))})
            2. Shows the approach to solving this problem step-by-step
            3. Incorporates the calculation result
            4. Explains what the result means physically
            """
            
            final_response = model.generate_content(final_prompt)
            return final_response.text
    except (json.JSONDecodeError, AttributeError, KeyError) as e:
        # If there's any error in parsing or processing, fall back to direct answer
        pass
    
    # For conceptual questions or if calculation failed, provide a comprehensive explanation
    conceptual_prompt = f"""
    You are a physics professor explaining a concept to a student. The question is: {question}
    
    Please provide a comprehensive explanation that:
    1. Identifies the core physics principles involved
    2. Explains the concepts clearly with everyday analogies where helpful
    3. Provides relevant equations if applicable (but don't solve numerically)
    4. Connects the concept to real-world applications
    """
    
    response = model.generate_content(conceptual_prompt)
    return response.text

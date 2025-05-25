import google.generativeai as genai
import os
import re
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def balance_chemical_equation(equation: str) -> str:
    """Attempt to balance a chemical equation"""
    try:
        # Simple regex to check if it looks like a chemical equation
        if not re.search(r'[A-Z][a-z]?\d*', equation) or not '->' in equation:
            return None
            
        # Use Gemini to balance the equation
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""
        Balance this chemical equation: {equation}
        
        Return only the balanced equation, with coefficients as needed.
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return None

def identify_functional_groups(compound: str) -> dict:
    """Identify functional groups in an organic compound"""
    try:
        # Use Gemini to identify functional groups
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""
        Identify all functional groups present in this organic compound: {compound}
        
        Return the result as a comma-separated list of functional groups.
        """
        response = model.generate_content(prompt)
        groups = [group.strip() for group in response.text.split(',')]
        return {"compound": compound, "functional_groups": groups}
    except Exception:
        return {"compound": compound, "functional_groups": []}

def handle_chemistry_question(question: str) -> str:
    """Handle chemistry questions using specialized tools when appropriate"""
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    # First, analyze if this is a specialized chemistry question
    analysis_prompt = f"""
    You are a chemistry teaching assistant that can decide when to use specialized tools.
    
    Question: {question}
    
    Analyze if this question is about:
    1. Balancing chemical equations
    2. Identifying functional groups in organic compounds
    3. General chemistry concepts
    
    Respond in JSON format like this:
    {{"question_type": "equation_balancing/functional_groups/general", "extract": "extracted equation or compound if applicable"}}
    """
    
    analysis_response = model.generate_content(analysis_prompt)
    
    try:
        # Extract the analysis as text and try to parse it
        analysis_text = analysis_response.text
        
        # Check for equation balancing
        if "equation_balancing" in analysis_text and "->" in question:
            # Extract the equation using regex
            equation_match = re.search(r'([A-Za-z0-9\s\+\(\)]+\s*->\s*[A-Za-z0-9\s\+\(\)]+)', question)
            if equation_match:
                equation = equation_match.group(1).strip()
                balanced_equation = balance_chemical_equation(equation)
                
                if balanced_equation:
                    final_prompt = f"""
                    You are a chemistry professor explaining how to balance equations. The question was: {question}
                    
                    The balanced equation is: {balanced_equation}
                    
                    Explain step by step how to balance this equation, discussing:
                    1. The law of conservation of mass
                    2. How to count atoms on each side
                    3. The systematic approach to balancing
                    """
                    
                    final_response = model.generate_content(final_prompt)
                    return final_response.text
        
        # Check for functional group identification
        if "functional_groups" in analysis_text:
            # Look for organic compound names or formulas
            compound_match = re.search(r'([A-Za-z0-9\-]+ol|[A-Za-z0-9\-]+ane|[A-Za-z0-9\-]+ene|[A-Za-z0-9\-]+oic acid|[A-Za-z0-9\-]+aldehyde|[A-Za-z0-9\-]+one|[A-Za-z0-9\-]+amine)', question, re.IGNORECASE)
            if compound_match:
                compound = compound_match.group(1).strip()
                result = identify_functional_groups(compound)
                
                if result and result["functional_groups"]:
                    groups_text = ", ".join(result["functional_groups"])
                    final_prompt = f"""
                    You are a chemistry professor explaining functional groups. The question was: {question}
                    
                    The compound {result["compound"]} contains these functional groups: {groups_text}
                    
                    Explain what each of these functional groups is, their properties, and how they affect the overall molecule's behavior.
                    """
                    
                    final_response = model.generate_content(final_prompt)
                    return final_response.text
    
    except Exception as e:
        # If there's any error in parsing or processing, fall back to general answer
        pass
    
    # For general chemistry questions or if specialized tools failed
    chemistry_prompt = f"""
    You are a chemistry professor answering a student's question. The question is: {question}
    
    Provide a comprehensive explanation that:
    1. Addresses the core chemistry concepts involved
    2. Uses clear examples and analogies where helpful
    3. Includes relevant chemical equations or structures if applicable
    4. Connects the concept to real-world applications in chemistry
    
    Be educational, accurate, and engaging in your response.
    """
    
    response = model.generate_content(chemistry_prompt)
    return response.text

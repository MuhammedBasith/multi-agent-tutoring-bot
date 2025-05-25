import google.generativeai as genai
import os
import re
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_code(code: str) -> dict:
    """Analyze code for errors and improvements"""
    try:
        # Use Gemini to analyze the code
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""
        Analyze this code for errors and potential improvements:
        
        ```
        {code}
        ```
        
        Provide your analysis in JSON format:
        {{
            "language": "detected programming language",
            "errors": ["list of errors found"],
            "improvements": ["list of suggested improvements"],
            "complexity": "assessment of time/space complexity if applicable"
        }}
        """
        response = model.generate_content(prompt)
        
        # Try to parse as JSON, but handle cases where it's not valid JSON
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            # Extract structured data using regex if JSON parsing fails
            language_match = re.search(r'"language":\s*"([^"]+)"', response.text)
            language = language_match.group(1) if language_match else "unknown"
            
            errors = []
            improvements = []
            complexity = "unknown"
            
            # Extract other fields using regex
            errors_match = re.findall(r'"errors":\s*\[(.*?)\]', response.text, re.DOTALL)
            if errors_match:
                errors = re.findall(r'"([^"]+)"', errors_match[0])
                
            improvements_match = re.findall(r'"improvements":\s*\[(.*?)\]', response.text, re.DOTALL)
            if improvements_match:
                improvements = re.findall(r'"([^"]+)"', improvements_match[0])
                
            complexity_match = re.search(r'"complexity":\s*"([^"]+)"', response.text)
            if complexity_match:
                complexity = complexity_match.group(1)
                
            return {
                "language": language,
                "errors": errors,
                "improvements": improvements,
                "complexity": complexity
            }
    except Exception as e:
        return {
            "language": "unknown",
            "errors": ["Could not analyze code"],
            "improvements": [],
            "complexity": "unknown"
        }

def explain_algorithm(algorithm_name: str) -> str:
    """Explain a computer science algorithm"""
    try:
        # Use Gemini to explain the algorithm
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""
        Explain the {algorithm_name} algorithm in detail, covering:
        
        1. The problem it solves
        2. How it works step-by-step
        3. Its time and space complexity
        4. Common use cases
        5. Pseudocode implementation
        
        Make your explanation educational and clear.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return f"I couldn't generate an explanation for the {algorithm_name} algorithm."

def handle_cs_question(question: str) -> str:
    """Handle computer science questions using specialized tools when appropriate"""
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    # First, analyze if this is a specialized CS question
    analysis_prompt = f"""
    You are a computer science teaching assistant that can decide when to use specialized tools.
    
    Question: {question}
    
    Analyze if this question is about:
    1. Code analysis (debugging, improving code)
    2. Algorithm explanation
    3. General computer science concepts
    
    Respond in JSON format like this:
    {{"question_type": "code_analysis/algorithm/general", "extract": "extracted code or algorithm name if applicable"}}
    """
    
    analysis_response = model.generate_content(analysis_prompt)
    
    try:
        # Extract the analysis as text and try to parse it
        analysis_text = analysis_response.text
        
        # Check for code analysis
        if "code_analysis" in analysis_text:
            # Look for code blocks in the question
            code_match = re.search(r'```(?:\w+)?\s*([\s\S]+?)```', question)
            if not code_match:
                # Try to find code without markdown formatting
                code_match = re.search(r'((?:(?:public|private|protected|class|def|function|var|let|const)[\s\S]*?[{;])|(?:for|while|if)[\s\S]*?[{;])', question)
            
            if code_match:
                code = code_match.group(1).strip()
                analysis_result = analyze_code(code)
                
                if analysis_result:
                    errors_text = "\n".join([f"- {error}" for error in analysis_result["errors"]]) if analysis_result["errors"] else "No errors found."
                    improvements_text = "\n".join([f"- {improvement}" for improvement in analysis_result["improvements"]]) if analysis_result["improvements"] else "No specific improvements suggested."
                    
                    final_prompt = f"""
                    You are a computer science professor reviewing code. The question was: {question}
                    
                    I've analyzed the code (detected as {analysis_result["language"]}):
                    
                    Errors:
                    {errors_text}
                    
                    Suggested Improvements:
                    {improvements_text}
                    
                    Complexity: {analysis_result["complexity"]}
                    
                    Provide a detailed educational explanation that addresses these issues, explains the concepts involved, and teaches good programming practices.
                    """
                    
                    final_response = model.generate_content(final_prompt)
                    return final_response.text
        
        # Check for algorithm explanation
        if "algorithm" in analysis_text:
            # Look for algorithm names
            common_algorithms = [
                "binary search", "linear search", "bubble sort", "insertion sort", 
                "selection sort", "merge sort", "quick sort", "heap sort", 
                "breadth-first search", "depth-first search", "dijkstra", 
                "dynamic programming", "greedy algorithm", "backtracking"
            ]
            
            for algorithm in common_algorithms:
                if algorithm.lower() in question.lower():
                    explanation = explain_algorithm(algorithm)
                    return explanation
    
    except Exception as e:
        # If there's any error in parsing or processing, fall back to general answer
        pass
    
    # For general CS questions or if specialized tools failed
    cs_prompt = f"""
    You are a computer science professor answering a student's question. The question is: {question}
    
    Provide a comprehensive explanation that:
    1. Addresses the core computer science concepts involved
    2. Uses clear examples and code snippets where helpful
    3. Explains the theoretical underpinnings
    4. Discusses practical applications
    
    Be educational, accurate, and engaging in your response.
    """
    
    response = model.generate_content(cs_prompt)
    return response.text

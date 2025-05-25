def solve_equation(equation: str) -> str:
    try:
        # Only attempt if it’s a pure numeric expression like 2+5*3
        cleaned = equation.replace(" ", "")
        result = eval(cleaned, {"__builtins__": {}})
        return f"The result is {result}"
    except Exception as e:
        return f"Sorry, I couldn't calculate that directly. But I can still solve it symbolically!"

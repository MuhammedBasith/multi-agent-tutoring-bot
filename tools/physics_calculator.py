import math
import re

def calculate_kinematics(params):
    """
    Calculate missing kinematic values using standard equations.
    params should be a dictionary with some of these keys: 
    initial_velocity, final_velocity, acceleration, time, displacement
    """
    v0 = params.get('initial_velocity')
    v = params.get('final_velocity')
    a = params.get('acceleration')
    t = params.get('time')
    d = params.get('displacement')
    
    results = {}
    
    # Calculate missing values based on what's provided
    if v0 is not None and a is not None and t is not None:
        if v is None:
            results['final_velocity'] = v0 + a * t
        if d is None:
            results['displacement'] = v0 * t + 0.5 * a * t**2
    
    if v is not None and v0 is not None and t is not None:
        if a is None:
            results['acceleration'] = (v - v0) / t
        if d is None:
            results['displacement'] = 0.5 * (v0 + v) * t
    
    if v is not None and v0 is not None and a is not None:
        if d is None:
            results['displacement'] = (v**2 - v0**2) / (2 * a)
    
    if d is not None and v0 is not None and t is not None:
        if a is None:
            results['acceleration'] = 2 * (d - v0 * t) / t**2
        if v is None:
            results['final_velocity'] = 2 * d / t - v0
    
    return results

def calculate_force(mass, acceleration):
    """Calculate force using F = ma"""
    return mass * acceleration

def calculate_energy(mass, height=None, velocity=None):
    """Calculate potential or kinetic energy"""
    g = 9.8  # gravitational acceleration
    results = {}
    
    if height is not None:
        results['potential_energy'] = mass * g * height
    
    if velocity is not None:
        results['kinetic_energy'] = 0.5 * mass * velocity**2
    
    return results

def extract_values(text):
    """Extract numerical values with units from text"""
    # Extract numbers with units
    patterns = {
        'mass': r'(\d+(?:\.\d+)?)\s*(?:kg|kilograms?)',
        'velocity': r'(\d+(?:\.\d+)?)\s*(?:m/s|meters? per second)',
        'acceleration': r'(\d+(?:\.\d+)?)\s*(?:m/s²|meters? per second squared)',
        'time': r'(\d+(?:\.\d+)?)\s*(?:s|seconds?)',
        'displacement': r'(\d+(?:\.\d+)?)\s*(?:m|meters?)',
        'height': r'(\d+(?:\.\d+)?)\s*(?:m|meters?) high',
        'force': r'(\d+(?:\.\d+)?)\s*(?:N|newtons?)',
    }
    
    extracted = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            extracted[key] = float(match.group(1))
    
    return extracted

def solve_physics_problem(problem_text):
    """Attempt to solve a physics problem based on text description"""
    try:
        # Extract values from the problem text
        values = extract_values(problem_text)
        
        # Determine what type of problem it is
        if 'mass' in values and 'acceleration' in values:
            force = calculate_force(values['mass'], values['acceleration'])
            return f"Force = {force} N (using F = ma)"
        
        elif 'mass' in values and ('height' in values or 'velocity' in values):
            energy = calculate_energy(
                values['mass'], 
                values.get('height'), 
                values.get('velocity')
            )
            result = []
            if 'potential_energy' in energy:
                result.append(f"Potential energy = {energy['potential_energy']} J")
            if 'kinetic_energy' in energy:
                result.append(f"Kinetic energy = {energy['kinetic_energy']} J")
            return ", ".join(result)
        
        # Check if it's a kinematics problem
        kinematics_params = {}
        for key in ['initial_velocity', 'final_velocity', 'acceleration', 'time', 'displacement']:
            if key in values:
                kinematics_params[key] = values[key]
        
        if len(kinematics_params) >= 3:  # Need at least 3 parameters to solve
            results = calculate_kinematics(kinematics_params)
            if results:
                return ", ".join([f"{k.replace('_', ' ')} = {v}" for k, v in results.items()])
        
        return "I couldn't automatically solve this physics problem with the given information."
    
    except Exception as e:
        return f"I couldn't automatically solve this physics problem: {str(e)}"

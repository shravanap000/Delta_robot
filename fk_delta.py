import numpy as np
import sympy as sym
from math import sqrt, sin, cos, pi

# Constants from data (In[2])
sp = 76 * 10**(-3)  # 19/250
L = 524 * 10**(-3)   # 131/250
l = 1244 * 10**(-3)  # 311/250
wb = 164 * 10**(-3)  # 41/250
wp = 22 * 10**(-3)   # 11/500
up = 44 * 10**(-3)   # 11/250
sb = 567 * 10**(-3)  # 567/1000
ub = 327 * 10**(-3)  # 327/1000

def setup_equations(theta1, theta2, theta3):
    """Set up eq1, eq2, eq3 symbolically and compute sol and fineq"""
    # Define symbolic variables
    x, y, z = sym.symbols('x y z')
    t1, t2, t3 = sym.Symbol('theta1'), sym.Symbol('theta2'), sym.Symbol('theta3')
    
    # Equations from In[72], In[73], In[74]
    eq1 = (
        -l**2 + L**2 + up**2 - 2*up*wb + wb**2 + x**2 - 2*up*y +
        2*wb*y + y**2 + z**2 - 2*L*(up - wb - y)*sym.cos(t1) +
        2*L*z*sym.sin(t1)
    )
    eq2 = (
        -l**2 + L**2 + sp**2/4 - sym.sqrt(3)/2*sp*wb + wb**2 -
        wb*wp + wp**2 + sp*x - sym.sqrt(3)*wb*x + x**2 - wb*y +
        2*wp*y + y**2 + z**2 -
        L/2*(sym.sqrt(3)*sp + 2*(-2*wb + wp + sym.sqrt(3)*x + y))*sym.cos(t2) +
        2*L*z*sym.sin(t2)
    )
    eq3 = (
        -l**2 + L**2 + sp**2/4 - sym.sqrt(3)/2*sp*wb + wb**2 -
        wb*wp + wp**2 - sp*x + sym.sqrt(3)*wb*x + x**2 - wb*y +
        2*wp*y + y**2 + z**2 -
        L/2*(sym.sqrt(3)*sp + 2*(-2*wb + wp - sym.sqrt(3)*x + y))*sym.cos(t3) +
        2*L*z*sym.sin(t3)
    )
    
    # Substitute numerical angles
    subs = {t1: theta1, t2: theta2, t3: theta3}
    eq1 = eq1.subs(subs)
    eq2 = eq2.subs(subs)
    eq3 = eq3.subs(subs)
    
    # Compute eqb = eq2 - eq3 and eqc = eq1 - eq3 (In[76], In[77])
    eqb = sym.simplify(eq2 - eq3)
    eqc = sym.simplify(eq1 - eq3)
    
    # Solve eqb = 0 and eqc = 0 for x and y (In[78])
    sol = sym.solve([eqb, eqc], [x, y], dict=True)
    if not sol:
        return None, None, None, None
    
    # Substitute x and y into eq1 to get fineq (In[80])
    fineq = eq1.subs(sol[0])
    fineq = sym.together(fineq)
    fineq = sym.numer(fineq)
    
    return sol[0], fineq, x, y

def solve_z(fineq):
    """Solve fineq == 0 for z numerically"""
    if fineq is None:
        return None
    
    # Convert fineq to a polynomial in z
    z = sym.Symbol('z')
    try:
        poly = sym.Poly(fineq, z)
        coeffs = poly.all_coeffs()
        # Solve quadratic equation
        a, b, c = [float(coef) for coef in coeffs]
        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            return None
        z1 = (-b + sqrt(discriminant)) / (2*a)
        z2 = (-b - sqrt(discriminant)) / (2*a)
        return [z1, z2]
    except Exception:
        # Fallback to numerical solver if polynomial form fails
        z_solutions = sym.nsolve(fineq, z, [-1, 1], verify=False)
        return [float(z_solutions)] if not isinstance(z_solutions, list) else [float(z) for z in z_solutions]

def get_xyz(theta1, theta2, theta3):
    """Calculate x, y, z for given theta1, theta2, theta3"""
    # Get sol, fineq, and symbols
    sol, fineq, x_sym, y_sym = setup_equations(theta1, theta2, theta3)
    if sol is None:
        return None
    
    # Solve for z
    z_values = solve_z(fineq)
    if z_values is None:
        return None
    
    # Evaluate x and y for each z
    results = []
    for z_val in z_values:
        x_val = float(sol[x_sym].subs({sym.Symbol('z'): z_val}))
        y_val = float(sol[y_sym].subs({sym.Symbol('z'): z_val}))
        results.append({'x': x_val, 'y': y_val, 'z': z_val})
    
    return results

def main():
    # Get user input
    try:
        theta1 = float(input("Enter valθ1 (radians): "))
        theta2 = float(input("Enter valθ2 (radians): "))
        theta3 = float(input("Enter valθ3 (radians): "))
        
        # Calculate x, y, z
        results = get_xyz(theta1, theta2, theta3)
        
        if results is None:
            print("No real solutions exist for the given angles.")
            return
        
        # Print results
        print("\nResults:")
        for i, result in enumerate(results, 1):
            print(f"Solution {i}:")
            print(f"x: {result['x']:.6e}")
            print(f"y: {result['y']:.6e}")
            print(f"z: {result['z']:.6f}")
        
        # Verify with test case fkin = {θ1 -> -0.358327, θ2 -> -0.358194, θ3 -> -0.358194}
        if (abs(theta1 - (-0.358327)) < 1e-6 and
            abs(theta2 - (-0.358194)) < 1e-6 and
            abs(theta3 - (-0.358194)) < 1e-6):
            print("\nVerification with test case (θ1=-0.358327, θ2=-0.358194, θ3=-0.358194):")
            print(f"Expected x ≈ 0.0, y ≈ -1.02182e-16, z ≈ -0.9 or 1.26746")
            
    except ValueError:
        print("Please enter valid numerical values for valθ1, valθ2, valθ3.")

if __name__ == "__main__":
    main()
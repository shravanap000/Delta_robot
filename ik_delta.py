import numpy as np
from math import sqrt, atan2, pi

# Constants from data
sp = 76 * 10**(-3)  # 19/250
L = 524 * 10**(-3)   # 131/250
l = 1244 * 10**(-3)  # 311/250
wb = 164 * 10**(-3)  # 41/250
wp = 22 * 10**(-3)   # 11/500
up = 44 * 10**(-3)   # 11/250
sb = 567 * 10**(-3)  # 567/1000
ub = 327 * 10**(-3)  # 327/1000

# Rotation matrix for 2π/3 around z-axis
theta_z = 2 * np.pi / 3
Rz = np.array([
    [-1/2, -sqrt(3)/2, 0],
    [sqrt(3)/2, -1/2, 0],
    [0, 0, 1]
])

# Base points
b1 = np.array([0, -wb, 0])
b2 = Rz @ b1
b3 = Rz @ b2

# Platform points
p1 = np.array([0, -up, 0])
p2 = np.array([sp/2, wp, 0])
p3 = np.array([-sp/2, wp, 0])

# Rotation matrix Rx2 (π/2 around x-axis)
Rx2 = np.array([
    [1, 0, 0],
    [0, 0, -1],
    [0, 1, 0]
])

def rotation_matrix_x(theta):
    """Generate rotation matrix around x-axis for angle theta"""
    return np.array([
        [1, 0, 0],
        [0, np.cos(theta), -np.sin(theta)],
        [0, np.sin(theta), np.cos(theta)]
    ])

def solve_theta1(x, y, z):
    """Solve for theta1 given x, y, z"""
    L1 = Rx2 @ np.array([0, 0, L])
    v1a = b1 + L1
    v1b = p1 + np.array([x, y, z])
    eq1 = np.dot(v1b - v1a, v1b - v1a) - l**2
    
    # Substitute cos(θ1) and sin(θ1) with t1 = tan(θ1/2)
    A = -l**2 + L**2 + 2*L*up + up**2 - 2*L*wb - 2*up*wb + wb**2 + x**2 - 2*L*y - 2*up*y + 2*wb*y + y**2 + z**2
    B = -l**2 + L**2 - 2*L*up + up**2 + 2*L*wb - 2*up*wb + wb**2 + x**2 + 2*L*y - 2*up*y + 2*wb*y + y**2 + z**2
    C = 4*L*z
    
    # Solve quadratic equation for t1
    discriminant = 16*L**2*z**2 - 4*A*B
    if discriminant < 0:
        return None  # No real solutions
    t1_1 = (-C - sqrt(discriminant)) / (2*A)
    t1_2 = (-C + sqrt(discriminant)) / (2*A)
    
    # Convert t1 to theta1
    theta1_1 = 2 * atan2(t1_1, 1)
    theta1_2 = 2 * atan2(t1_2, 1)
    return [theta1_1, theta1_2]

def solve_theta2(x, y, z):
    """Solve for theta2 given x, y, z"""
    Rx3 = rotation_matrix_x(0)  # Placeholder, will use substitution
    L2 = Rz @ Rx2 @ np.array([0, 0, L])
    v2a = b2 + L2
    v2b = p2 + np.array([x, y, z])
    eq2 = np.dot(v2b - v2a, v2b - v2a) - l**2
    
    # Substitute cos(θ2) and sin(θ2) with t2 = tan(θ2/2)
    A = -4*l**2 + 4*L**2 + 2*sqrt(3)*L*sp + sp**2 - 8*L*wb - 2*sqrt(3)*sp*wb + 4*wb**2 + 4*L*wp - 4*wb*wp + 4*wp**2 + 4*sqrt(3)*L*x + 4*sp*x - 4*sqrt(3)*wb*x + 4*x**2 + 4*L*y - 4*wb*y + 8*wp*y + 4*y**2 + 4*z**2
    B = -4*l**2 + 4*L**2 - 2*sqrt(3)*L*sp + sp**2 + 8*L*wb - 2*sqrt(3)*sp*wb + 4*wb**2 - 4*L*wp - 4*wb*wp + 4*wp**2 - 4*sqrt(3)*L*x + 4*sp*x - 4*sqrt(3)*wb*x + 4*x**2 - 4*L*y - 4*wb*y + 8*wp*y + 4*y**2 + 4*z**2
    C = 16*L*z
    
    # Solve quadratic equation for t2
    discriminant = 256*L**2*z**2 - 4*A*B
    if discriminant < 0:
        return None  # No real solutions
    t2_1 = (-C - sqrt(discriminant)) / (2*A)
    t2_2 = (-C + sqrt(discriminant)) / (2*A)
    
    # Convert t2 to theta2
    theta2_1 = 2 * atan2(t2_1, 1)
    theta2_2 = 2 * atan2(t2_2, 1)
    return [theta2_1, theta2_2]

def solve_theta3(x, y, z):
    """Solve for theta3 given x, y, z"""
    Rx4 = rotation_matrix_x(0)  # Placeholder, will use substitution
    L3 = Rz @ Rz @ Rx2 @ np.array([0, 0, L])
    v3a = b3 + L3
    v3b = p3 + np.array([x, y, z])
    eq3 = np.dot(v3b - v3a, v3b - v3a) - l**2
    
    # Substitute cos(θ3) and sin(θ3) with t3 = tan(θ3/2)
    A = -4*l**2 + 4*L**2 + 2*sqrt(3)*L*sp + sp**2 - 8*L*wb - 2*sqrt(3)*sp*wb + 4*wb**2 + 4*L*wp - 4*wb*wp + 4*wp**2 - 4*sqrt(3)*L*x - 4*sp*x + 4*sqrt(3)*wb*x + 4*x**2 + 4*L*y - 4*wb*y + 8*wp*y + 4*y**2 + 4*z**2
    B = -4*l**2 + 4*L**2 - 2*sqrt(3)*L*sp + sp**2 + 8*L*wb - 2*sqrt(3)*sp*wb + 4*wb**2 - 4*L*wp - 4*wb*wp + 4*wp**2 + 4*sqrt(3)*L*x - 4*sp*x + 4*sqrt(3)*wb*x + 4*x**2 - 4*L*y - 4*wb*y + 8*wp*y + 4*y**2 + 4*z**2
    C = 16*L*z
    
    # Solve quadratic equation for t3
    discriminant = 256*L**2*z**2 - 4*A*B
    if discriminant < 0:
        return None  # No real solutions
    t3_1 = (-C - sqrt(discriminant)) / (2*A)
    t3_2 = (-C + sqrt(discriminant)) / (2*A)
    
    # Convert t3 to theta3
    theta3_1 = 2 * atan2(t3_1, 1)
    theta3_2 = 2 * atan2(t3_2, 1)
    return [theta3_1, theta3_2]

def get_thetas(x, y, z):
    """Calculate valθ1, valθ2, valθ3 for given x, y, z"""
    val_theta1 = solve_theta1(x, y, z)
    val_theta2 = solve_theta2(x, y, z)
    val_theta3 = solve_theta3(x, y, z)
    
    if val_theta1 is None or val_theta2 is None or val_theta3 is None:
        return None
    
    # Convert to degrees
    val_theta1_deg = [theta * 180 / pi for theta in val_theta1]
    val_theta2_deg = [theta * 180 / pi for theta in val_theta2]
    val_theta3_deg = [theta * 180 / pi for theta in val_theta3]
    
    return {
        'valθ1_rad': val_theta1,
        'valθ2_rad': val_theta2,
        'valθ3_rad': val_theta3,
        'valθ1_deg': val_theta1_deg,
        'valθ2_deg': val_theta2_deg,
        'valθ3_deg': val_theta3_deg
    }

def main():
    # Get user input
    try:
        x = float(input("Enter x coordinate: "))
        y = float(input("Enter y coordinate: "))
        z = float(input("Enter z coordinate: "))
        
        # Calculate thetas
        result = get_thetas(x, y, z)
        
        if result is None:
            print("No real solutions exist for the given coordinates.")
            return
        
        # Print results
        print("\nResults:")
        print(f"valθ1: {result['valθ1_rad'][0]:.6f} rad ({result['valθ1_deg'][0]:.6f}°), "
              f"{result['valθ1_rad'][1]:.6f} rad ({result['valθ1_deg'][1]:.6f}°)")
        print(f"valθ2: {result['valθ2_rad'][0]:.6f} rad ({result['valθ2_deg'][0]:.6f}°), "
              f"{result['valθ2_rad'][1]:.6f} rad ({result['valθ2_deg'][1]:.6f}°)")
        print(f"valθ3: {result['valθ3_rad'][0]:.6f} rad ({result['valθ3_deg'][0]:.6f}°), "
              f"{result['valθ3_rad'][1]:.6f} rad ({result['valθ3_deg'][1]:.6f}°)")
        
        # Verify with test case x=0, y=0, z=-0.9
        if abs(x - 0) < 1e-10 and abs(y - 0) < 1e-10 and abs(z - (-0.9)) < 1e-10:
            print("\nVerification with test case (x=0, y=0, z=-0.9):")
            print(f"Expected valθ1 ≈ -0.358327 rad (-20.5320°), -2.51816 rad (-144.2910°)")
            print(f"Expected valθ2 ≈ -0.358194 rad (-20.5237°), -2.51810 rad (-144.2874°)")
            print(f"Expected valθ3 ≈ -0.358194 rad (-20.5237°), -2.51810 rad (-144.2874°)")
            
    except ValueError:
        print("Please enter valid numerical values for x, y, z.")

if __name__ == "__main__":
    main()
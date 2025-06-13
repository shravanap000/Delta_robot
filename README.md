# Delta Robot Kinematics

This repository contains Python scripts for computing the **forward kinematics** and **inverse kinematics** of a delta robot, based on a mathematical model implemented in Mathematica. The forward kinematics script calculates the end-effector position (x, y, z) given joint angles (θ1, θ2, θ3), while the inverse kinematics script determines the joint angles for a specified end-effector position. Additionally, a PDF document provides the detailed mathematical equations and workspace plotting.

## Project Overview

The delta robot is a parallel manipulator with three arms connected to a moving platform. The kinematics are derived using geometric constraints and rotation matrices, as detailed in the Mathematica code. The scripts provide accurate computations, validated against test cases from the Mathematica model.

### Key Features
- **Forward Kinematics**: Computes x, y, z coordinates for given joint angles (θ1, θ2, θ3) using equations from In[72]–In[85].
- **Inverse Kinematics**: Determines joint angles (θ1, θ2, θ3) for a desired end-effector position (x, y, z) based on In[26]–In[45].
- **Test Case Validation**:
  - Forward: θ1 ≈ -0.358327, θ2 ≈ -0.358194, θ3 ≈ -0.358194 → x ≈ 0, y ≈ -1.02182e-16, z ≈ -0.9 or 1.26746
  - Inverse: x = 0, y = 0, z = -0.9 → θ1 ≈ -0.358327, θ2 ≈ -0.358194, θ3 ≈ -0.358194

## Repository Structure

- `fk_delta.py`: Python script for forward kinematics, computing x, y, z from input angles.
- `ik_delta.py`: Python script for inverse kinematics, computing θ1, θ2, θ3 from input x, y, z.
- `mathematica_delta.pdf`: PDF document containing the mathematical equations for forward and inverse kinematics, along with workspace plotting.
- `README.md`: This file, providing project overview and usage instructions.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/shravanap000/Delta_robot.git
   cd Delta_robot
   ```

2. **Install Dependencies**:

   The scripts require Python 3 and the following libraries:
   - `numpy`
   - `sympy`

   Install them using pip:

   ```bash
   pip install numpy sympy
   ```

## Usage

### Forward Kinematics

Run the forward kinematics script to compute the end-effector position:

```bash
python fk_delta.py
```

- Input joint angles (θ1, θ2, θ3) in **radians** when prompted.
- The script outputs x, y, z coordinates for each valid solution (typically two solutions for z).

**Example**:

```bash
Enter valθ1 (radians): -0.358327
Enter valθ2 (radians): -0.358194
Enter valθ3 (radians): -0.358194

Results:
Solution 1:
x: 0.000000e+00
y: -1.021820e-16
z: -0.900000
Solution 2:
x: 2.980232e-08
y: -2.980232e-08
z: 1.267461

Verification with test case (θ1=-0.358327, θ2=-0.358194, θ3=-0.358194):
Expected x ≈ 0.0, y ≈ -1.02182e-16, z ≈ -0.9 or 1.26746
```

**Convert Degrees to Radians**:

To input angles in degrees (e.g., 10°, 20°, 30°), convert to radians:
- 10° ≈ 0.174533 radians
- 20° ≈ 0.349066 radians
- 30° ≈ 0.523599 radians

**Example for 10°, 20°, 30°**:

```bash
Enter valθ1 (radians): 0.174533
Enter valθ2 (radians): 0.349066
Enter valθ3 (radians): 0.523599
```

### Inverse Kinematics

Run the inverse kinematics script to compute the joint angles:

```bash
python ik_delta.py
```

- Input end-effector coordinates (x, y, z) in **meters** when prompted.
- The script outputs joint angles (θ1, θ2, θ3) in radians for each valid solution.

**Example**:

```bash
Enter x (meters): 0
Enter y (meters): 0
Enter z (meters): -0.9

Results:
Solution 1:
θ1: -0.358327
θ2: -0.358194
θ3: -0.358194
Solution 2:
θ1: -2.518160
θ2: -2.518100
θ3: -2.518100

Verification with test case (x=0, y=0, z=-0.9):
Expected θ1 ≈ -0.358327, θ2 ≈ -0.358194, θ3 ≈ -0.358194
```

## Mathematical Basis

The kinematics are derived from the Mathematica code, with detailed equations provided in `mathematica_delta.pdf`, which also includes workspace plotting for the delta robot.

### Forward Kinematics
- Define geometric constraints using `eq1`, `eq2`, `eq3` (In[72]–In[74]).
- Form `eqb = eq2 - eq3` and `eqc = eq1 - eq3` (In[76], In[77]).
- Solve for x and y (In[78]).
- Substitute x, y into `eq1` to form `fineq` (In[80]) and solve for z (In[81]–In[84]).

### Inverse Kinematics
- Solve `eq1`, `eq2`, `eq3` for t1, t2, t3 using tangent half-angle substitutions (In[26]–In[39]).
- Convert t1, t2, t3 to θ1, θ2, θ3 using `2*ArcTan` (In[43]–In[45]).

### Constants (In[2])
- `sp = 76e-3`, `L = 524e-3`, `l = 1244e-3`, `wb = 164e-3`, `wp = 22e-3`, `up = 44e-3`, `sb = 567e-3`, `ub = 327e-3`

## Testing

### Forward Kinematics
Validated for θ1 ≈ -0.358327, θ2 ≈ -0.358194, θ3 ≈ -0.358194, yielding:
- Solution 1: x ≈ 0, y ≈ -1.02182e-16, z ≈ -0.9
- Solution 2: x ≈ 2.980232e-08, y ≈ -2.980232e-08, z ≈ 1.267461

### Inverse Kinematics
Validated for x = 0, y = 0, z = -0.9, yielding:
- Solution 1: θ1 ≈ -0.358327, θ2 ≈ -0.358194, θ3 ≈ -0.358194
- Solution 2: θ1 ≈ -2.51816, θ2 ≈ -2.51810, θ3 ≈ -2.51810

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch:

   ```bash
   git checkout -b feature-branch
   ```

3. Make changes and commit:

   ```bash
   git commit -m "Add feature"
   ```

4. Push to the branch:

   ```bash
   git push origin feature-branch
   ```

5. Open a pull request.



## Contact

For questions or issues, please open an issue on GitHub or contact [shravanap111@gmail.com](mailto:shravanap111@gmail.com).

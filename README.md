
![image](https://github.com/user-attachments/assets/36886825-4db5-4fcd-94b2-0c0765688f0d)




# Delta Robot Kinematics

This repository contains Python scripts for computing the **forward kinematics** and **inverse kinematics** of a delta robot, based on a mathematical model implemented in Mathematica. The forward kinematics script calculates the end-effector position (x, y, z) given joint angles (θ1, θ2, θ3), while the inverse kinematics script determines the joint angles for a specified end-effector position. Additionally, a PDF document provides the detailed mathematical equations and workspace plotting. The repository also includes Arduino codes for controlling Dynamixel AX-12A motors to execute random or absolute movements.

## Project Overview

The delta robot is a parallel manipulator with three arms connected to a moving platform. The kinematics are derived using geometric constraints and rotation matrices, as detailed in the Mathematica code. The scripts provide accurate computations, validated against test cases from the Mathematica model. Arduino codes enable motor control for random motion or precise positioning.

### Key Features
- **Forward Kinematics**: Computes x, y, z coordinates for given joint angles (θ1, θ2, θ3) using equations from In[72]–In[85].
- **Inverse Kinematics**: Determines joint angles (θ1, θ2, θ3) for a desired end-effector position (x, y, z) based on In[26]–In[45].
- **Motor Control**: 
  - Random Movement: Three separate Arduino sketches in `Random movement` folder for Dynamixel AX-12A motors to execute random motion.
  - Absolute Movement: Three Arduino sketches in `Absolute movement` folder for precise position control, integrated with Python scripts.
- **Test Case Validation**:
  - Forward: θ1 ≈ -0.358327, θ2 ≈ -0.358194, θ3 ≈ -0.358194 → x ≈ 0, y ≈ -1.02182e-16, z ≈ -0.9 or 1.26746
  - Inverse: x = 0, y = 0, z = -0.9 → θ1 ≈ -0.358327, θ2 ≈ -0.358194, θ3 ≈ -0.358194

## Repository Structure

- `ArduinoCodes/`
  - `Absolute movement/`
    - `motor3control.ino`
    - `motor4control.ino`
    - `motor6control.ino`
  - `Random movement/`
    - `working1.ino`
    - `working2.ino`
    - `working3.ino`
- `degree-based-motor-control.py`: Python script for degree-based motor control with absolute positioning.
- `discrete-motor-based-control.py`: Python script for discrete motor control with absolute positioning.
- `fk_delta.py`: Python script for forward kinematics, computing x, y, z from input angles.
- `ik_delta.py`: Python script for inverse kinematics, computing θ1, θ2, θ3 from input x, y, z.
- `mathematica_delta.pdf`: PDF document containing mathematical equations and workspace plotting.
- `README.md`: This file, providing project overview and usage instructions.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/shravanap000/Delta_robot.git
   cd Delta_robot
   ```

2. **Install Dependencies**:

   - Python scripts require Python 3 and the following libraries:
     - `numpy`
     - `sympy`
   - Install them using pip:

     ```bash
     pip install numpy sympy
     ```

   - Arduino sketches require the Arduino IDE and the Dynamixel AX-12A library (e.g., Dynamixel2Arduino).

3. **Hardware Setup**:
   - Connect three Dynamixel AX-12A motors to separate Arduino UNOs.
   - Set appropriate baud rate (default 1000000 bps) and COM ports.

## Usage

### Random Movement

- Upload the three Arduino sketches (`working1.ino`, `working2.ino`, `working3.ino`) from the `Random movement` folder to three separate Arduino UNOs connected to Dynamixel AX-12A motors.
- The motors will execute random motion simultaneously upon powering on.

### Absolute Movement

- Upload the three Arduino sketches (`motor3control.ino`, `motor4control.ino`, `motor6control.ino`) from the `Absolute movement` folder to three separate Arduino UNOs.
- Choose a control method:

  #### Python Script Control
  - Run `degree-based-motor-control.py` or `discrete-motor-based-control.py`:
    ```bash
    python degree-based-motor-control.py
    ```
    or
    ```bash
    python discrete-motor-based-control.py
    ```
  - Input desired joint angles (degrees) or discrete positions to actuate all motors simultaneously.

  #### Serial Monitor Control
  - Open the Serial Monitor in Arduino IDE.
  - Set the baud rate to match the Arduino sketch (e.g., 9600).
  - Enter individual motor positions manually for each Arduino to control motors independently.

### Forward Kinematics

Run the forward kinematics script to compute the end-effector position:
```bash
python fk_delta.py
```
- Input joint angles (θ1, θ2, θ3) in **radians** when prompted.
- Outputs x, y, z coordinates for each valid solution.

### Inverse Kinematics

Run the inverse kinematics script to compute the joint angles:
```bash
python ik_delta.py
```
- Input end-effector coordinates (x, y, z) in **meters** when prompted.
- Outputs joint angles (θ1, θ2, θ3) in radians.

## Mathematical Basis

The kinematics are derived from the Mathematica code, with detailed equations in `mathematica_delta.pdf`, including workspace plotting.

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

6. [Report](Internship_report.pdf)

## Contact

For questions or issues, please open an issue on GitHub or contact [shravanap111@gmail.com](mailto:shravanap111@gmail.com).

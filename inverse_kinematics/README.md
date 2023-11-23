# Inverse Kinematic Analysis Of A Quadruped Robot

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1iHY8kPjPlGhtklQylArtp3tgbvVNmGOO#scrollTo=-NJRDldfHYPJ) 

## Resurces
- [InverseKinematicQuadrupedRobot_PAPER](https://www.researchgate.net/publication/320307716_Inverse_Kinematic_Analysis_Of_A_Quadruped_Robot)

- [Modern Robotics, Chapter 6: Inverse Kinematics of Open Chains](https://www.youtube.com/watch?v=nin2TbMuhR0&list=PLggLP4f-rq02vX0OQQ5vrCxbJrzamYDfx&index=30)
- [Inverse kinematics and robot motion lesson](https://robotacademy.net.au/masterclass/inverse-kinematics-and-robot-motion/?lesson=289)
- [Solve IK](https://www.youtube.com/watch?v=qFE-zuD6jok)

## Abstract

- IK of a quadruped robot with **3 degrees of freedom** on each leg
- **Denavit-Hartenberg (D-H)** method are used for the **forward kinematic**.
    
    The **inverse kinematic equations** obtained by the geometrical and mathematical methods are **coded in MATLAB** ⇒ **program** is obtained ⇒ **calculate the body orientations of robot in graphical form** AND **legs joint angles corresponding to desired various orientations of robot and endpoints of legs**
    
- The angular positions of joints obtained corresponding to the desired different orientations of the robot and endpoints of legs are given in this study

## Introduction

- Less energy consumption, good stability, and locomotion on uneven and rough terrain are main **advantages** of quadruped robots.

- Low speed, difficulty to build and control, need for onboard power are **limitations** of quadruped robots.
- kinematic model is necessary to stability analysis and trajectory planning of the system.

- There are two types of kinematic analysis: **forward** and **inverse** kinematics analysis

### FORWARD

- The *joint variables* are given to find the *location of the body* of the robot
- Deals with the relationship between the positions, velocities, and accelerations of the robot links.
    
### INVERSE

- The *location of the body* is given to find the *joint variables* necessary to bring the body to the desired location.
- Process of finding the values of the joint variables according to the positions and orientations data of the endpoint of robot.
- In order to move the robot endpoint to the desired position, it is necessary to determine the rotational values of the joints with inverse kinematic analysis.

### MATLAB program
that calculates forward and inverse kinematics of a quadruped robot corresponding to desired different orientations of robot and endpoints of legs.


## **Kinematic Analysis**

- **Quadruped robot** = robotic system that consists of a **rigid body** and **four legs** with **3DoF**
    - 1. **Physical model:**        
    - 2. **Parameters of robot:**
  
### **Matrix**

- depending on the legs coordinates, the robot body can have different configurations
    
    ⇒ kinematic equation between the rotational movements (φ, ψ, ω) around the center of the body’s coordinate system (xm, ym, zm) and the coordinate system of each endpoint of leg (x4, y4, z4) [take center and calculate IK with end point]
    
    1. Determine the position and orientation of the robot center of body in the workspace 
        1. ⇒ transformation matrix is obtained using the rotation matrices
            - **rotation matrices:**
                
                Mathematical matrix that is used to perform a rotation transformation in a coordinate system
                
                These matrices preserve distances and angles, making them useful for representing rotations.
                
                $$
                
                ROOL\\Rx = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & cos(ω) & -sin(ω) & 0 \\ 0 & sin(ω) & cos(ω) & 0 \\ 0 & 0 & 0 & 1\end{bmatrix}
                $$
                
                $$
                
                PITCH\\Ry = \begin{bmatrix} cos(ϕ) & 0 & sin(ϕ) & 0 \\ 0 & 1 & 0 & 0 \\ -sin(ϕ) & 0 & cos(ϕ) & 0 \\ 0 & 0 & 0 & 1\end{bmatrix}
                $$
                
                $$
                
                JAW\\Rz = \begin{bmatrix} cos(ψ) & -sin(ψ) & 0 & 0 \\ sin(ψ) & cos(ψ) & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \\ \end{bmatrix}
                $$
                
                $$
                
                Rxyx = RxRyRz
                $$
                
            - **Transformation matrix:**
                
                Mathematical representation used to perform geometric transformations on points or objects in a coordinate space (transformations can include operations such as translation, rotation, …).
                
                Multiply identity matrix of the center of mass of the robot with rotation matrix R_xyz
                
        2. ⇒ The kinematic equation of the center of body’s coordinate system (xm, ym, zm) and The Main Coordinate System of each leg (x0, y0, z0) (The positions and orientations of each leg can be calculated according to the position and orientation of the robot's body):
            - **Transformation matrixes:**



## **Solution methods/approaches for IK:**

1. Analytic close-for solutions for our joints (what we had described here). This is possible because we know inside about structure of the robot, so we can get approximate solutions
    - **Process:**
        - **Tools:**
            1. **Two-argument arctangent function**: atan2 function takes x and y coordinates of a point in the plane and returns the angle the vector, from origin to endpoint, will have.
                
                [atan2 function](https://planetcalc.com/7955/?x=5&y=3)

                
            2. **Law of cosines**: The law of cosines is a formula that relates the lengths of the sides of a triangle to the cosine of one of its angles.
                
            
        - **Calculations:**
            
            $$
            γ = atan2(y,x)
            $$
            
            $$
            α,\ β\ form\ law\ of\ cosines
            $$
            
            ### **⇒ 2 solutions:**
            
            $$
            solution\ 1: \\ θ_1 = γ  - α,\\θ_2 = π - β
            $$
            
            $$
            solution\ 2: \\ θ_1 = γ + α,\\θ_2 = β - π 
            $$
            
2. Interative numerical method. For arbitrary solutions a robot. It requires an initial guess and then calculations toward the correct value. We will only find one solution, not all possible solutions.
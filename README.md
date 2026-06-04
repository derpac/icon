# icon
> interactive control webapp


1. System definition
   - The app allows a user to firstly define a dynamic system in LaTeX with states x, $$\dot{x}$$, $$\ddot{x}$$...
> **Note:** The user defined system can be arbitrarily complex ensuring that it is linear in its highest derivative.
  
2. System initialisation
   -  The app will generate the list of user defined algebraic parameters and ask for values
   -  It will present the user with options for:
      -  Control strategy:
         -  Feedback linearisation
         -  Robust Sliding Mode Control (SMC)
      - Desired state trajectory:
        - step (Heaviside)
        - sine
      - Controller Gains:
        - kp [0.1-50]
        - kd [0.1-30]
3. Simulation
   - The app will then simulate the controller and present the following plots:
     1.  Response x(t) vs $$x_d(t)$$
     2.  Tracking error e(t)
     3.  Control input u(t)
     4.  Phase plane x vs $$\dot{x}$$
   

Requirements:
- Flask
- flask_socketio
- latex2sympy2
- sympy
- numpy
- scipy

  
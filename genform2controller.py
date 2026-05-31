from diff2sympy import diff2sympy
# from symdiff2genform import symdiff2genform

# texin = r'4*\ddot{x} + \cos{\dot{x}} + x^2 - u'
# symans = diff2sympy(texin)
# hder = symdiff2genform(symans)
# print(hder)

# in this function i want to use the highester order general form:
# x^n = f(x) + b(x)u to find the controller u through three different methods.

# feedback linearisation
# assumption is that all params are known

# test function
from sympy import *
import sympy as sp


def genform2controller(f_str, b_str, control_type, trajectory_type, params):
    t = sp.symbols('t')
    x = sp.Function('x')(t)
    dx = x.diff(t)
    ddx = dx.diff(t)
    u = sp.symbols('u')

    xd = sp.Function('xd')(t)
    dxd = xd.diff(t)
    ddxd = dxd.diff(t)

    f_func = sp.parse_expr(f_str)
    b_coeff = sp.parse_expr(b_str)

    # trajectory generation considers time varying trig else heaviside step
    xd_expr = sp.sin(t) if trajectory_type == 'sine' else sp.Heaviside(t)
    dxd_expr = xd_expr.diff(t)
    ddxd_expr = dxd_expr.diff(t)

    # tracking
    e = x - xd_expr

# determine classification of parameters from: known, unknown_bounded, unknown_constant

# robust (SMC) 
# params are unknown bounded


# adaptive control
# params are unknown but constant


# turn any arbitrarily complex diff to sympy from latex input
# implementing the tex package amsmath you can use the following notation:
# \dot, \ddot, \dddot, \ddddot so the limit will be n=4 for nth order systems

# an important note will be that terms in the latex input must be seperated by *
# when necessary for example: $5\dot{x} + 10x$ -> $5*\dot{x} + 10*x$
# please note that for control input u format the closed loop equation = 0
# for example ... - u = 0 not ... = u

from latex2sympy2 import latex2latex, latex2sympy
from sympy import symbols, Derivative
import sympy as sp

# test input
#latstr = r"5*\ddot{x} + 2*\cos{\dot{x}^2} - 4*x^3" 

# this includes *, \cos and ^2 all edge cases to ensure work
def diff2sympy(latstr):
    t = sp.symbols('t') # this represents the time. As each state is time varient
    x = sp.Function('x')

    latans = latex2latex(latstr) # converts user input into ideal latex form

    print(latans)
    symans = latex2sympy(latans) # converts the new latex form to sympy
    print(symans)

    # the output for symans =  5*\ddot{x} + (-1)*4*x**3 + 2*cos(\dot{x}**2)
    # i need to firstly turn the \ddot{x} into 2nd derivative of x and then \dot{x}
    # into first derivative.


    #print(symans.free_symbols) # debug to idenfity if \dot, \ddot etc are free symbols

    #define a dict with all substitutions 
    subs_dict = { 
        sp.Symbol(r'\ddddot{x}'): sp.Derivative(x(t), t, 4),
        sp.Symbol(r'\dddot{x}'): sp.Derivative(x(t), t, 3),
        sp.Symbol(r'\ddot{x}'): sp.Derivative(x(t), t, 2),
        sp.Symbol(r'\dot{x}'): sp.Derivative(x(t), t),
        sp.Symbol('x'): x(t)
    }
    # substitude to turn dot notation to derivative form
    symans = symans.subs(subs_dict)
    # we now need to extract parameters from the equation given.
    params = []
    for sym in symans.free_symbols:
        params.append(sym)
        
    
    return symans, params
    #print(symans) # debug print

#now to turn into an actual function with def to be used by main code

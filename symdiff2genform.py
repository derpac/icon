from sympy import solve, Derivative, collect, expand, diff
import sympy as sp
from sympy.solvers import solve



# example diff equation in sympy form to work with. parsed from diff2sympy
# -4*x(t)**3 + 2*cos(Derivative(x(t), t)**2) + 5*Derivative(x(t), (t, 2))


# exfunc = -4*x(t)**3 + 2*cos(Derivative(x(t), t)**2) + 5*Derivative(x(t), (t, 2))

def symdiff2genform(exfunc):
    t = sp.symbols('t')
    x = sp.Function('x')
    u = sp.symbols('u')
    v = sp.symbols('v')


    exfunc_str = str(exfunc)
    n = 0
    # extract highest derivative noting the n=4 limit
    if 'Derivative(x(t), (t, 4))' in exfunc_str:
        n = 4
    elif 'Derivative(x(t), (t, 3))' in exfunc_str:
        n = 3
    elif 'Derivative(x(t), (t, 2))' in exfunc_str:
        n = 2
    elif 'Derivative(x(t), t)' in exfunc_str:
        n = 1
    else:
        print('System needs to be of an order greater than 0')

    # use the knowledge of highest order to solve for the highest order.
    if n == 4:
        ans = solve(exfunc,(Derivative(x(t), (t, 4))))
    elif n == 3:
        ans = solve(exfunc,(Derivative(x(t), (t, 3))))
    elif n == 2: 
        ans = solve(exfunc,(Derivative(x(t), (t, 2))))
    elif n == 1:
        ans = solve(exfunc,(Derivative(x(t), t)))
    # this solves for the highest derivative 
    #print(ans) # debug
    
    xn_expanded = expand(ans[0])

    eq = sp.Eq(ans[0], v)
    u_iso = sp.solve(eq, u)[0]

    b_expr = sp.diff(xn_expanded, u)   # coefficient of u (b(x))
    f_expr = xn_expanded.subs(u, 0)    # f(x)


    return ans[0],f_expr,b_expr, n 

# this provides the inputted equation in the form x^n = f(x) + b(x)u
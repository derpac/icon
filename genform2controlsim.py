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
import numpy as np
from scipy.integrate import solve_ivp
# define the function to find the controller assuming all is known
def genform2controller(f_expr, b_expr, n, control_type, trajectory_type, params, t_span=(0,10), dt=0.01):

    t = sp.Symbol('t')

    x_sym, dx_sym = sp.symbols('x_s dx_s')  # to remove the (t) so lambdify works 

    param_subs = {sp.Symbol(k): v for k, v in params.items()}
    f_num = f_expr.subs(param_subs)
    b_num = b_expr.subs(param_subs)

    # need to replace x(t) and Derivative forms with plain symbols for lambdify
    # so called sanitised form

    x_fn = sp.Function('x')
    deriv_subs = {
        x_fn(t): x_sym,
        sp.Derivative(x_fn(t), t): dx_sym
    }

    f_plain = f_num.subs(deriv_subs)
    b_plain = b_num.subs(deriv_subs)

    # lambdify for simulation 
    f_eval = sp.lambdify((x_sym, dx_sym), f_plain, 'numpy')
    b_eval = sp.lambdify((x_sym, dx_sym), b_plain, 'numpy')

    # preprocess desired trajectory
    if trajectory_type == 'sine':
        xd_sym = sp.sin(t)
        dxd_sym = sp.cos(t)
        ddxd_sym = -sp.sin(t)
    else:
        xd_sym = sp.Piecewise((0, t < 0), (1, True)) # diff of constant options
        dxd_sym = sp.Integer(0)
        ddxd_sym = sp.Integer(0)
    
    xd_eval = sp.lambdify(t, xd_sym, 'numpy')
    dxd_eval = sp.lambdify(t, dxd_sym, 'numpy')
    ddxd_eval = sp.lambdify(t, ddxd_sym, 'numpy')

    def compute_u(t_val, x_val, dx_val, gains):   # controller calcuations

        f_val = float(f_eval(x_val, dx_val))
        b_val = float(b_eval(x_val, dx_val))

        xd_val = float(xd_eval(t_val))
        dxd_val = float(dxd_eval(t_val))
        ddxd_val = float(ddxd_eval(t_val))

        e = x_val - xd_val
        de = dx_val - dxd_val

        if control_type == 'fbl':
            kp = gains.get('kp', 10)
            kd = gains.get('kd', 5)
            v = ddxd_val - kd * de - kp * e 
            u_val = (v - f_val) / b_val  # standard form for fbl controller
        elif control_type == 'smc':
                lam = gains.get('lam', 1.0)
                k_robust = gains.get('k_robust', 2.0)
                s = de + lam * e 
                u_val = (1.0/b_val) * (ddxd_val + lam * de - f_val - k_robust * np.sign(s))

        else:
            # expand to adaptive later me thinks...
            raise ValueError(f'nuh uh')
        return u_val

    def simulate(gains, x0 = 0.0, dx0 = 0.0): #maybe make these initial conditions changable?
        u_past = []

        def ode(t_val, y):
            x_v, dx_v = y
            u_v = compute_u(t_val, x_v, dx_v, gains)
            f_v = float(f_eval(x_v, dx_v))
            b_v = float(b_eval(x_v, dx_v))
            xddot = f_v + b_v * u_v
            u_past.append((t_val, u_v))
            return[dx_v, xddot] 
        
        t_eval = np.arange(t_span[0], t_span[1], dt)
        sol = solve_ivp(ode, t_span, [x0, dx0],
                        t_eval=t_eval, method='RK45', max_step=dt) # Runge-Kutta 45 a classic ;>

        xd_hist = np.array([float(xd_eval(tv)) for tv in sol.t])

        u_arr = np.zeros_like(sol.t)
        for i, tv in enumerate(sol.t):
            u_val = compute_u(tv, sol.y[0][i], sol.y[1][i], gains)
            u_arr[i] = u_val
        
        return {
            't': sol.t.tolist(),
            'x': sol.y[0].tolist(),
            'dx': sol.y[1].tolist(),
            'xd': xd_hist.tolist(),
            'tracking_error': (sol.y[0] - xd_hist).tolist(),
            'u': u_arr.tolist()
        }
    return simulate, compute_u

    # # trajectory generation considers time varying trig else heaviside step
    # xd_expr = sp.sin(t) if trajectory_type == 'sine' else sp.Heaviside(t)
    # dxd_expr = xd_expr.diff(t)
    # ddxd_expr = dxd_expr.diff(t)

    # # tracking
    # e = x - xd_expr
    # de = dx - dxd_expr

    # kp, kd, lam, k_robust = sp.symbols('kp kd lam k_robust')

    # if control_type == 'fbl':
    #     v = ddxd_expr - kd*de - kp*e
    #     u = (v - f_func) / b_coeff
    # elif control_type == 'smc':
    #     s = de - lam*e 
    #     u = (1/b_coeff) * (ddxd_expr - lam*de - f_func - k_robust * sp.sign(s))
    # else: 
    #     u = (1/b_coeff) * (ddxd_expr - lam*de - f_func) #not quite right for apdative control
    
    # param_symbols = [sp.symbols(p) for p in params]

    # return {
    #     'control_type': control_type,
    #     'f_eval': sp.lambdify((t, x, dx, *param_symbols), f_func, 'numpy'),
    #     'b_eval': sp.lambdify((t, x, dx, *param_symbols), b_coeff, 'numpy'),
    #     'xd_eval': sp.lambdify(t, xd_expr, 'numpy'),
    #     'dxd_eval': sp.lambdify(t, dxd_expr, 'numpy'),
    #     'ddxd_eval': sp.lambdify(t, ddxd_expr, 'numpy')
    # }
# determine classification of parameters from: known, unknown_bounded, unknown_constant

# robust (SMC) 
# params are unknown bounded


# adaptive control
# params are unknown but constant


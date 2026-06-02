from scipy.integrate import solve_ivp

def simulate(f_eval, b_eval, xd_eval, dxd_eval, ddxd_eval, control_type, gains, parmas_vals, t_span=(0,10)):
    def ode(t, y):
        x, dx = y
        u = compute_u(t, x, dx, ...)
        xddot = f_eval(t, x, dx) + b_eval(t, x, dx) * u
        return [dx , xddot]
    sol = solve_ivp(ode, t_span, [0, 0], max_step=0.01)
    return sol.t, sol.y
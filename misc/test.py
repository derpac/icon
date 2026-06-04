from diff2sympy import diff2sympy

latin = r'm*\ddot{x} + c*\dot{x} - k*x - u'

ans = diff2sympy(latin)
print(ans)
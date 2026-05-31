# import re

# eq = r"3\ddot{x}^2 + 10\dot{x} + \cos{x}^2"

# # 1. Split the equation into individual terms by + or -
# terms = [t.strip() for t in re.split(r"(\+|-)", eq) if t.strip()]

# sder = []
# fder = []
# zder = []

# current_sign = ""

# for term in terms:
#     if term in ("+", "-"):
#         current_sign = "-" if term == "-" else ""
#         continue

#     full_term = f"{current_sign}{term}"


#     if r"\ddot" in full_term:
#         match = re.search(r"(.*?)\\ddot\{.*?\}(.*)", full_term)
#         if match:
#             cleaned = (match.group(1) + match.group(2)).strip()
#             sder.append(cleaned)


#     elif r"\dot" in full_term:
#         match = re.search(r"(.*?)\\dot\{.*?\}(.*)", full_term)
#         if match:
#             cleaned = (match.group(1) + match.group(2)).strip()
#             fder.append(cleaned)


#     else:

#         cleaned = re.sub(r"\{x\}|\bx\b", "", full_term).strip()
#         zder.append(cleaned)

# print("sder =", sder)
# print("fder =", fder)
# print("zder =", zder)


# implement latex2sympy2 package

# based on example from docs:

# from latex2sympy2 import latex2latex, latex2sympy

# tex = r"\dot{x^2} + 3x"

# sympystr = latex2sympy(tex)
# latexstr = latex2latex(tex)

# print(sympystr)
# print(latexstr)

# based on sympy method
import sympy as sp
from sympy.parsing.latex import parse_latex

def parse_input_latex(latex_str):

    cleaned_str = latex_str.replace(r'\\', r' \\').replace(r'\ddot', r' \ddot').replace(r'\dot', r' \dot')
    raw_expr = parse_latex(cleaned_str)
    t = sp.Symbol('t')
    x = sp.Function('x')(t)

    replacements = {}
    for sym in raw_expr.free_symbols:
        if 'ddot{x}' in sym.name:
            replacements[sym] = sp.Derivative(x, (t,2))
        elif 'dot{x}' in sym.name:
            replacements[sym] = sp.Derivative(x, t)
        elif sym.name == 'x':
            replacements[sym] = x
    return t,x,raw_expr.subs(replacements)

latex_in = r"2\ddot{x} + 5\dot{x} + 3x"
t,x,ode = parse_input_latex(latex_in)
sp.pprint(ode)
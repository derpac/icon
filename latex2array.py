import re

eq = r"3\ddot{x}^2 + 10\dot{x} + \cos{x}^2"

# 1. Split the equation into individual terms by + or -
terms = [t.strip() for t in re.split(r"(\+|-)", eq) if t.strip()]

sder = []
fder = []
zder = []

current_sign = ""

for term in terms:
    if term in ("+", "-"):
        current_sign = "-" if term == "-" else ""
        continue

    full_term = f"{current_sign}{term}"


    if r"\ddot" in full_term:
        match = re.search(r"(.*?)\\ddot\{.*?\}(.*)", full_term)
        if match:
            cleaned = (match.group(1) + match.group(2)).strip()
            sder.append(cleaned)


    elif r"\dot" in full_term:
        match = re.search(r"(.*?)\\dot\{.*?\}(.*)", full_term)
        if match:
            cleaned = (match.group(1) + match.group(2)).strip()
            fder.append(cleaned)


    else:

        cleaned = re.sub(r"\{x\}|\bx\b", "", full_term).strip()
        zder.append(cleaned)

print("sder =", sder)
print("fder =", fder)
print("zder =", zder)

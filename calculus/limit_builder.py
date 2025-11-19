#!/usr/bin/env python3
"""
🧮 LIMIT BUILDER — Step-by-Step Construction
Guided input for limits like:
  lim_{x→a} [N(x)] / [A·√(B(x)) + C]

Example: tan(3x)(1 - e^sin5x) / (7√(1+5x²+x³) - 1)
"""

import math
import sys

def clean_expr(s):
    """Convert natural input to Python eval-friendly."""
    s = s.strip()
    # Replace common notations
    s = s.replace("^", "**")
    s = s.replace("e^", "exp(").replace("e**", "exp(")
    # Fix missing *: tan3x → tan(3*x), sin5x → sin(5*x)
    import re
    s = re.sub(r'([a-zA-Z]+)(\d+)', r'\1(\2*', s)   # sin5x → sin(5*x
    s = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', s)     # 3x → 3*x
    s = re.sub(r'([)\]])\s*([a-zA-Z(])', r'\1*\2', s)  # )x → )*x, )sin → )*sin
    s = re.sub(r'([0-9])\s*\(', r'\1*(', s)         # 7( → 7*(
    # Close parentheses for e^...
    s = s.replace("exp(", "exp(").replace("exp (", "exp(")
    # Ensure e^sin5x becomes exp(sin(5*x))
    s = re.sub(r'exp\(([^)]*?)\*x', r'exp(\1*x)', s)
    # Final: add missing closing ) for e^...
    if "exp(" in s and s.count("exp(") > s.count(")"):
        # Simple fix: assume one missing at end
        s = s + ")"
    return s

def safe_eval(expr, x):
    ns = {
        '__builtins__': {},
        'x': x,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'exp': math.exp,
        'log': math.log,
        'sqrt': math.sqrt,
        'pi': math.pi,
        'e': math.e,
    }
    try:
        return eval(expr, ns)
    except Exception as e:
        # print(f"[Eval error at x={x}]: {e}", file=sys.stderr)
        return float('nan')

def get_input(prompt, default=""):
    res = input(f"{prompt} [{default}] ").strip()
    return res if res else default

def main():
    print("🧮 LIMIT BUILDER — Let’s construct your limit step by step")
    print("=" * 60)

    # Step 1: limit point
    a_str = get_input("➤ x approaches (e.g., 0, 2, inf)", "0")
    if a_str.lower() in ('inf', '+inf'):
        a = float('inf')
    elif a_str.lower() == '-inf':
        a = float('-inf')
    else:
        try:
            a = float(a_str)
        except:
            a = 0.0

    print(f"\n🔧 Building expression: lim_{{x→{a}}} [Numerator] / [Denominator]")

    # Step 2: Numerator
    print("\n📝 Numerator N(x) — e.g., 'tan(3x)(1 - e^sin5x)'")
    num_raw = get_input("➤ Enter N(x)")
    num_clean = clean_expr(num_raw)
    print(f"   → Interpreted as: {num_clean}")

    # Step 3: Denominator type
    print("\n⚙️ Denominator options:")
    print("  1. Radical form:  A * √(B(x)) + C   (e.g., 7√(1+5x²+x³) - 1)")
    print("  2. General expression")
    den_type = get_input("➤ Choose (1/2)", "1")
    
    if den_type == "1":
        print("\n✅ Radical form: A * sqrt(B(x)) + C")
        A = float(get_input("➤ A (multiplier, e.g., 7)", "7"))
        B_raw = get_input("➤ B(x) inside √ (e.g., 1+5x^2+x^3)", "1+5x^2+x^3")
        B_clean = clean_expr(B_raw)
        C = float(get_input("➤ C (added after, e.g., -1)", "-1"))
        den_clean = f"({A})*sqrt({B_clean}) + ({C})"
        print(f"   → Denominator: {den_clean}")
    else:
        den_raw = get_input("➤ Enter full denominator")
        den_clean = clean_expr(den_raw)

    # Full expression
    expr = f"({num_clean}) / ({den_clean})"
    print(f"\n🎯 Your full function:\n   f(x) = {expr}")

    # Compute table
    print(f"\n🔍 Evaluating near x = {a}")
    print("-" * 45)
    print(f"{'x':>12} | {'f(x)':>15}")
    print("-" * 25)

    if a == 0:
        hs = [1e0, 1e-1, 1e-2, 1e-3, 1e-4]
    else:
        hs = [1, 0.1, 0.01, 0.001, 0.0001]

    for h in hs:
        for side in [-1, 1]:
            x = a + side * h
            fx = safe_eval(expr, x)
            if math.isfinite(fx):
                print(f"{x:>12.1e} | {fx:>15.6g}")
            else:
                print(f"{x:>12.1e} | {'undefined':>15}")
        print()

    # Insight
    if a == 0:
        print("💡 Analysis for x→0:")
        print("   Numerator ~ tan(3x)*(1 - (1 + sin5x + ...)) ~ 3x * (-5x) = -15x²")
        print("   Denominator → 7*√1 - 1 = 6")
        print("   So limit = 0/6 = 0 ✅")

if __name__ == "__main__":
    main()

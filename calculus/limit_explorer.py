#!/usr/bin/env python3
"""
🎯 LIMIT EXPLORER — Your Example Included
Compute lim_{x→a} f(x) numerically + plot.

Example built-in:
  lim_{x→0} tan(3x)*(1 - exp(sin(5x))) / (7*sqrt(1 + 5*x**2 + x**3) - 1)

Use:
  f(x) = tan(3*x)*(1 - exp(sin(5*x))) / (7*sqrt(1 + 5*x**2 + x**3) - 1)
"""

import math
import sys

# --- Safe evaluation with explicit * and robust handling ---
def f_eval(expr, x):
    # Replace common notations
    expr = expr.replace("^", "**")
    expr = expr.replace("e", str(math.e))  # optional: allow 'e' as constant
    
    # Define local math functions
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
        'e_val': math.e,
    }
    try:
        return eval(expr, ns)
    except Exception as e:
        # Print error in debug mode (comment out for clean run)
        # print(f"[DEBUG] x={x}: eval error: {e}", file=sys.stderr)
        return float('nan')

# --- Numerical table: two-sided approach to a ---
def show_table(expr, a, steps=6):
    print(f"\n🔍 Numerical Evaluation: lim_{{x→{a}}} f(x)")
    print("=" * 50)
    print(f"{'x':>15} | {'f(x)':>20}")
    print("-" * 36)

    if a == float('inf'):
        for i in range(1, steps+1):
            x = 10**i
            fx = f_eval(expr, x)
            print(f"{x:>15.1e} | {fx:>20.6g}")
    elif a == float('-inf'):
        for i in range(1, steps+1):
            x = -10**i
            fx = f_eval(expr, x)
            print(f"{x:>15.1e} | {fx:>20.6g}")
    else:
        h = 1.0
        for _ in range(steps):
            # Left side
            x_left = a - h
            fx_l = f_eval(expr, x_left)
            print(f"{x_left:>15.8f} | {fx_l:>20.8g}")
            # Right side
            x_right = a + h
            fx_r = f_eval(expr, x_right)
            print(f"{x_right:>15.8f} | {fx_r:>20.8g}")
            print()
            h /= 10

# --- Plotting (optional — skip if no GUI) ---
def try_plot(expr, a):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("📌 matplotlib not found. Skipping plot.")
        return

    if not (-1e-3 < a < 1e-3):
        delta = abs(a) * 0.2 + 0.5
    else:
        delta = 0.2

    if a in (float('inf'), float('-inf')):
        xs = [i*0.2 for i in range(-50, 51) if i != 0]
        xs = [x for x in xs if abs(x) > 0.01]
    else:
        xs = [a + (i/200)*delta for i in range(-200, 201) if i != 0]

    ys = []
    xs_plot = []
    for x in xs:
        y = f_eval(expr, x)
        if math.isfinite(y) and abs(y) < 1e6:  # clip extreme spikes
            xs_plot.append(x)
            ys.append(y)

    if not ys:
        print("⚠️  No valid points to plot.")
        return

    plt.figure(figsize=(9, 5))
    plt.plot(xs_plot, ys, 'b-', linewidth=1.5, alpha=0.8, label=f'f(x) = {expr}')
    if math.isfinite(a):
        plt.axvline(a, color='gray', linestyle='--', linewidth=1, label=f'x = {a}')
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(f'Limit Exploration: x → {a}')
    plt.legend()
    plt.tight_layout()
    print("📈 Plot window opened. Close to continue.")
    plt.show()

# --- Main ---
def main():
    print("🎯 LIMIT EXPLORER — For Calculus & Analysis")
    print("Enter f(x) using Python syntax. Examples:")
    print("  tan(3*x)*(1 - exp(sin(5*x))) / (7*sqrt(1 + 5*x**2 + x**3) - 1)")
    print("  (x**2 - 1)/(x - 1)   |   sin(x)/x   |   (1 + x)**(1/x)")
    print()

    # Your exact example — pre-filled
    default_expr = "tan(3*x)*(1 - exp(sin(5*x))) / (7*sqrt(1 + 5*x**2 + x**3) - 1)"
    expr = input(f"f(x) = [{default_expr}] ").strip()
    if not expr:
        expr = default_expr

    a_str = input("x → ? (e.g., 0, 2, inf) [0] ").strip()
    if not a_str:
        a_str = "0"

    # Parse a
    a_str = a_str.lower()
    if a_str in ("inf", "+inf"):
        a = float('inf')
    elif a_str in ("-inf"):
        a = float('-inf')
    else:
        try:
            a = float(a_str)
        except:
            print("❌ Invalid point. Using 0.")
            a = 0.0

    # Show table
    show_table(expr, a, steps=5)

    # Ask to plot
    if input("\nPlot? (y/N) ").strip().lower() in ('y', 'yes'):
        try_plot(expr, a)

    print("\n💡 Tip: At x→0, your example → 0 (numerator ~ -15x², denominator → 6).")

if __name__ == "__main__":
    main()

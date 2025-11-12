#!/usr/bin/env python3

import math
import matplotlib.pyplot as plt

def plot_line_from_general(A, B, C, label="Line", color='steelblue'):
    if abs(B) < 1e-9:  # Vertical
        x0 = -C / A
        plt.axvline(x=x0, color=color, linewidth=2, label=f"{label}: x = {x0:.3f}")
    elif abs(A) < 1e-9:  # Horizontal
        y0 = -C / B
        plt.axhline(y=y0, color=color, linewidth=2, label=f"{label}: y = {y0:.3f}")
    else:
        xs = [-10, 10]
        ys = [(-A * x - C) / B for x in xs]
        plt.plot(xs, ys, color=color, linewidth=2, label=label)

def get_input_and_compute():
    print("Choose how to define your line:")
    cases = [
        "① Point + Slope",
        "② Two Points",
        "③ Slope + y-intercept",
        "④ x- and y-intercepts",
        "⑤ Angle α + Point",
        "⑥ Normal Form (p, α)",
        "⑦ General Form (A, B, C)",
        "⑧ Vertical Line (x = a)",
        "⑨ Horizontal Line (y = b)",
        "⑩ Custom → Edit me in nano!"   # ← Your new option!
    ]
    for c in cases:
        print(c)
    
    try:
        choice = int(input("\n➤ Enter 1–10: "))
        A = B = C = None

        if choice == 1:  # Point + Slope
            x0 = float(input("x₀ = ")); y0 = float(input("y₀ = ")); m = float(input("m = "))
            A, B, C = m, -1, y0 - m * x0
            label = f"Point-Slope: ({x0},{y0}), m={m}"
        elif choice == 2:  # Two Points
            x1 = float(input("x₁ = ")); y1 = float(input("y₁ = "))
            x2 = float(input("x₂ = ")); y2 = float(input("y₂ = "))
            if x1 == x2:
                A, B, C = 1, 0, -x1
            else:
                m = (y2 - y1) / (x2 - x1)
                A, B, C = m, -1, y1 - m * x1
            label = f"Through ({x1},{y1}) & ({x2},{y2})"
        elif choice == 3:  # y = mx + b
            m = float(input("m = ")); b = float(input("y-intercept b = "))
            A, B, C = m, -1, b
            label = f"y = {m}x + {b}"
        elif choice == 4:  # x/a + y/b = 1
            a = float(input("x-int a = ")); b = float(input("y-int b = "))
            A, B, C = b, a, -a * b
            label = f"x/{a} + y/{b} = 1"
        elif choice == 5:  # Angle α + Point
            x0 = float(input("x₀ = ")); y0 = float(input("y₀ = "))
            alpha = float(input("α (degrees from +x axis) = "))
            m = math.tan(math.radians(alpha))
            A, B, C = m, -1, y0 - m * x0
            label = f"α = {alpha}° through ({x0},{y0})"
        elif choice == 6:  # Normal: x cosα + y sinα = p
            p = float(input("p (distance from origin, ≥0) = "))
            alpha_n = float(input("Normal angle αₙ (degrees) = "))
            A = math.cos(math.radians(alpha_n))
            B = math.sin(math.radians(alpha_n))
            C = -p
            label = f"Normal: p={p}, αₙ={alpha_n}°"
        elif choice == 7:  # A x + B y + C = 0
            A = float(input("A = ")); B = float(input("B = ")); C = float(input("C = "))
            label = f"{A}x + {B}y + {C} = 0"
        elif choice == 8:  # x = a
            a = float(input("x = a → a = "))
            A, B, C = 1, 0, -a
            label = f"x = {a}"
        elif choice == 9:  # y = b
            b = float(input("y = b → b = "))
            A, B, C = 0, 1, -b
            label = f"y = {b}"
        elif choice == 10:  # 🔧 NEW: Custom — Edit this block in nano!
            print("\n📝 Custom Line Definition")
            print("   Edit this part in ~/math_tools/straight_line_on_the_plane.py")
            print("   Example: line through (0,0) with slope 2 → A=2, B=-1, C=0")
            A = float(input("Enter A = "))
            B = float(input("Enter B = "))
            C = float(input("Enter C = "))
            label = f"Custom: {A}x + {B}y + {C} = 0"
        else:
            print("Invalid choice.")
            return None, None

    except Exception as e:
        print(f"❌ Input error: {e}")
        return None, None

    return (A, B, C), label

def main():
    print("🌐 STRAIGHT LINE ON THE PLANE")
    print("   — Clean, focused, no extra prompts —\n")

    result = get_input_and_compute()
    if result[0] is None:
        return

    (A, B, C), label = result
    plot_line_from_general(A, B, C, label=label)

    # Axes & grid
    plt.axhline(0, color='gray', linewidth=0.7)
    plt.axvline(0, color='gray', linewidth=0.7)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.gca().set_aspect('equal')
    plt.xlim(-8, 8)
    plt.ylim(-8, 8)
    plt.title("Straight Line on the Plane", fontsize=14)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    print("\n✅ Plot ready. Close window to exit.")
    plt.show()

if __name__ == "__main__":
    main()

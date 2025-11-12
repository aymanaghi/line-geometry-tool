#!/usr/bin/env python3
"""
🌟 LINE MASTER — Complete Straight Line Toolkit
Covers all classical representations of a line in 2D.
Interactive menu + conversion + plotting (matplotlib).
"""

import math
import matplotlib.pyplot as plt

# === Helper Functions ===

def deg2rad(d): return math.radians(d)
def rad2deg(r): return math.degrees(r)

def normalize_angle(deg):
    """Normalize to (-180, 180]"""
    return ((deg + 180) % 360) - 180

def line_from_general(A, B, C, label="Line", color='b'):
    """
    Plot line: Ax + By + C = 0
    Returns: slope, intercepts, angle α, normal angle, distance from origin
    """
    if A == 0 and B == 0:
        raise ValueError("A and B cannot both be zero.")
    
    # Normalize sign: ensure (A,B) points in 'standard' half-plane
    norm = math.hypot(A, B)
    A_n, B_n, C_n = A/norm, B/norm, C/norm
    
    # Distance from origin: p = |C| / √(A²+B²), but signed: p = -C/√(A²+B²)
    p_signed = -C_n  # = -(C / norm) = distance with sign
    p = abs(p_signed)
    
    # Normal angle α (angle of normal vector (A,B) from +x axis)
    alpha_normal = rad2deg(math.atan2(B_n, A_n))  # atan2(y, x) → (B, A)
    alpha_normal = normalize_angle(alpha_normal)
    
    # Direction angle of the LINE (not normal) = α_normal + 90°
    alpha_line = normalize_angle(alpha_normal + 90)
    
    # Slope (if not vertical)
    if abs(B) > 1e-9:
        m = -A / B
        y_int = -C / B if B != 0 else None
    else:
        m = float('inf')  # vertical
        y_int = None
    
    x_int = -C / A if abs(A) > 1e-9 else None

    # Plotting
    xs = [-10, 10]
    if abs(B) < 1e-9:  # vertical: Ax + C = 0 → x = -C/A
        x0 = -C / A
        plt.axvline(x=x0, color=color, linewidth=2,
                    label=f"{label}: x = {x0:.3f}")
    elif abs(A) < 1e-9:  # horizontal: By + C = 0 → y = -C/B
        y0 = -C / B
        plt.axhline(y=y0, color=color, linewidth=2,
                    label=f"{label}: y = {y0:.3f}")
    else:
        ys = [(-A * x - C) / B for x in xs]
        plt.plot(xs, ys, color=color, linewidth=2,
                 label=f"{label}: {A:+.2f}x {B:+.2f}y {C:+.2f} = 0")

    return {
        'A': A, 'B': B, 'C': C,
        'slope': m,
        'x_intercept': x_int,
        'y_intercept': y_int,
        'alpha_line_deg': alpha_line,
        'alpha_normal_deg': alpha_normal,
        'distance_from_origin': p,
        'normal_vector': (A_n, B_n),
        'p_signed': p_signed
    }

def print_properties(props, title="Line Properties"):
    print(f"\n📊 {title}")
    print("─" * 50)
    print(f"General form: {props['A']:+.3f}x {props['B']:+.3f}y {props['C']:+.3f} = 0")
    if props['slope'] == float('inf'):
        print("→ Vertical line")
    elif props['slope'] == 0:
        print("→ Horizontal line")
    else:
        print(f"Slope (m)        = {props['slope']:.5f}")
        print(f"Angle with +x (α) = {props['alpha_line_deg']:.2f}°")
    print(f"Normal angle      = {props['alpha_normal_deg']:.2f}°")
    print(f"Distance from O   = {props['distance_from_origin']:.4f}")
    if props['x_intercept'] is not None:
        print(f"x-intercept (a)   = {props['x_intercept']:.4f}")
    if props['y_intercept'] is not None:
        print(f"y-intercept (b)   = {props['y_intercept']:.4f}")
    nv = props['normal_vector']
    print(f"Unit normal vec   = ({nv[0]: .4f}, {nv[1]: .4f})")

# === Input Handlers ===

def case_point_slope():
    x0 = float(input("x₀ = ")); y0 = float(input("y₀ = ")); m = float(input("Slope m = "))
    # Convert to general: y - y0 = m(x - x0) → mx - y + (y0 - m x0) = 0
    A, B, C = m, -1, y0 - m * x0
    return A, B, C, f"Point-Slope: ({x0},{y0}), m={m}"

def case_two_points():
    x1 = float(input("x₁ = ")); y1 = float(input("y₁ = "))
    x2 = float(input("x₂ = ")); y2 = float(input("y₂ = "))
    if x1 == x2 and y1 == y2:
        raise ValueError("Points must be distinct.")
    if x1 == x2:
        # vertical
        A, B, C = 1, 0, -x1
    else:
        m = (y2 - y1) / (x2 - x1)
        A, B, C = m, -1, y1 - m * x1
    return A, B, C, f"Two Points: ({x1},{y1}) → ({x2},{y2})"

def case_slope_intercept():
    m = float(input("Slope m = ")); b = float(input("y-intercept b = "))
    A, B, C = m, -1, b  # y = mx + b → mx - y + b = 0
    return A, B, C, f"Slope-Intercept: y = {m}x + {b}"

def case_intercepts():
    a = float(input("x-intercept a (≠0) = ")); b = float(input("y-intercept b (≠0) = "))
    if a == 0 or b == 0:
        raise ValueError("Intercepts must be nonzero for this form.")
    # x/a + y/b = 1 → bx + ay - ab = 0
    A, B, C = b, a, -a * b
    return A, B, C, f"Intercept Form: x/{a} + y/{b} = 1"

def case_angle_point():
    x0 = float(input("x₀ = ")); y0 = float(input("y₀ = "))
    alpha = float(input("Angle α (with +x axis, in degrees) = "))
    m = math.tan(deg2rad(alpha))
    A, B, C = m, -1, y0 - m * x0
    return A, B, C, f"Angle α={alpha}° through ({x0},{y0})"

def case_normal_form():
    p = float(input("Distance from origin p (≥0) = "))
    if p < 0:
        raise ValueError("p must be ≥ 0 in normal form.")
    alpha = float(input("Normal angle α (with +x axis, degrees) = "))
    # x cos α + y sin α = p  →  cosα·x + sinα·y - p = 0
    A = math.cos(deg2rad(alpha))
    B = math.sin(deg2rad(alpha))
    C = -p
    return A, B, C, f"Normal Form: p={p}, α_normal={alpha}°"

def case_general():
    A = float(input("A = ")); B = float(input("B = ")); C = float(input("C = "))
    if A == 0 and B == 0:
        raise ValueError("A and B cannot both be zero.")
    return A, B, C, f"General Form: {A}x + {B}y + {C} = 0"

def case_vertical():
    a = float(input("x = a → a = "))
    return 1, 0, -a, f"Vertical Line: x = {a}"

def case_horizontal():
    b = float(input("y = b → b = "))
    return 0, 1, -b, f"Horizontal Line: y = {b}"

# === Menu ===

CASES = [
    ("Point + Slope", case_point_slope),
    ("Two Points", case_two_points),
    ("Slope + y-intercept", case_slope_intercept),
    ("x- and y-intercepts", case_intercepts),
    ("Angle α + Point", case_angle_point),
    ("Normal Form (p, α)", case_normal_form),
    ("General Form (A,B,C)", case_general),
    ("Vertical Line (x = a)", case_vertical),
    ("Horizontal Line (y = b)", case_horizontal),
]

def main():
    print("🌟 LINE MASTER — All Straight-Line Representations")
    print("Choose how to define your line:\n")

    for i, (desc, _) in enumerate(CASES, 1):
        print(f"{i:2}. {desc}")
    print()

    try:
        choice = int(input("Select (1–{}): ".format(len(CASES)))) - 1
        if not (0 <= choice < len(CASES)):
            raise ValueError
        desc, func = CASES[choice]
        print(f"\n🔹 {desc}")
        A, B, C, label = func()
    except (ValueError, IndexError):
        print("❌ Invalid choice or input.")
        return
    except Exception as e:
        print(f"❌ Input error: {e}")
        return

    # Compute & show properties
    try:
        props = line_from_general(A, B, C, label=label, color='steelblue')
    except Exception as e:
        print(f"❌ Plotting error: {e}")
        return

    print_properties(props)

    # Optional: perpendicular line (A = 90° case)
    if input("\nAlso draw perpendicular? [y/N]: ").strip().lower() == 'y':
        # Perpendicular line: swap A,B and negate one → (B, -A, C') for same point
        # But to pass through same point (x0,y0), we need C' = -(B x0 - A y0)
        # Let's pick a point on original line (e.g., use x=0 if possible)
        if props['x_intercept'] is not None:
            x0, y0 = props['x_intercept'], 0.0
        elif props['y_intercept'] is not None:
            x0, y0 = 0.0, props['y_intercept']
        else:
            # fallback: origin projection
            nx, ny = props['normal_vector']
            p = props['distance_from_origin']
            x0, y0 = p * nx, p * ny  # foot of perpendicular from origin

        A_perp, B_perp = B, -A  # rotate normal by 90°
        C_perp = -(A_perp * x0 + B_perp * y0)
        props_perp = line_from_general(A_perp, B_perp, C_perp,
                                       label="Perpendicular (A=90°)", color='crimson')
        print_properties(props_perp, "Perpendicular Line")

    # Final plot formatting
    plt.axhline(0, color='black', linewidth=0.6)
    plt.axvline(0, color='black', linewidth=0.6)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(-8, 8)
    plt.ylim(-8, 8)
    plt.title("Straight Line Visualization", fontsize=14)
    plt.xlabel("x"); plt.ylabel("y")
    plt.legend()
    plt.tight_layout()
    print("\n📈 Plot window opened. Close it to exit.")
    plt.show()

if __name__ == "__main__":
    main()

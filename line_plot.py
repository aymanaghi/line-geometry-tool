#!/usr/bin/env python3
import math
import matplotlib.pyplot as plt

def deg2rad(deg):
    return math.radians(deg)

def plot_line_from_angle(x0, y0, delta_deg, label="Line", color='b'):
    """Plot a line through (x0, y0) with angle delta_deg from +x axis."""
    m = math.tan(deg2rad(delta_deg))
    
    # To avoid near-vertical line issues, handle |m| > 100 as vertical-ish
    # We'll plot over a symmetric x-range unless it's near-vertical
    x_vals = [x0 - 5, x0 + 5]
    
    if abs(m) > 100:  # effectively vertical
        plt.axvline(x=x0, color=color, label=f"{label} (δ={delta_deg}°, vertical approx)")
    else:
        y_vals = [y0 + m * (x - x0) for x in x_vals]
        plt.plot(x_vals, y_vals, color=color, label=f"{label} (δ={delta_deg}°, m={m:.2f})")
        # Mark the given point
        plt.plot(x0, y0, 'o', color=color)

def main():
    print("📐 Straight Line Plotter (Angle-Based)")
    print("Enter point and angle δ (in degrees) that the line makes with +x-axis.")
    
    try:
        x0 = float(input("x₀ = "))
        y0 = float(input("y₀ = "))
        delta = float(input("δ (angle in degrees) = "))
        perpendicular = input("Draw perpendicular line (A = 90°)? [y/N]: ").strip().lower() == 'y'
    except ValueError:
        print("❌ Invalid input. Please enter numbers.")
        return

    plt.figure(figsize=(8, 6))
    plot_line_from_angle(x0, y0, delta, label="Given line", color='blue')
    
    if perpendicular:
        delta_perp = delta + 90
        # Normalize to [-180, 180] for readability
        delta_perp = (delta_perp + 180) % 360 - 180
        plot_line_from_angle(x0, y0, delta_perp, label="Perpendicular (A=90°)", color='red')
    
    # Formatting
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title(f"Line through ({x0}, {y0}) with δ = {delta}°")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.xlim(x0 - 6, x0 + 6)
    plt.ylim(y0 - 6, y0 + 6)
    
    print(f"\n✅ Slope m = tan({delta}°) = {math.tan(deg2rad(delta)):.4f}")
    if perpendicular:
        m_perp = math.tan(deg2rad(delta + 90))
        print(f"✅ Perpendicular slope = tan({delta}+90)° = {m_perp:.4f} (≈ -1/m if m ≠ 0)")

    plt.show()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Straight Line Plotter — Angle α (alpha) from +x axis
Input: point (x₀, y₀), angle α (degrees), optional perpendicular (A = 90°)
Output: Plot + slope info
"""

import math
import matplotlib.pyplot as plt

def plot_line(x0, y0, alpha_deg, label="Line", color='b'):
    """Plot infinite line through (x0, y0) with direction angle α (from +x axis)."""
    # Compute slope: m = tan(α)
    rad = math.radians(alpha_deg)
    m = math.tan(rad)

    # Choose x-range for plotting
    xs = [x0 - 6, x0 + 6]

    if abs(math.cos(rad)) < 1e-6:  # cos(α) ≈ 0 → vertical line (α ≈ ±90°, 270°, ...)
        plt.axvline(x=x0, color=color, linestyle='-', linewidth=2,
                    label=f"{label}: α = {alpha_deg}° (vertical)")
        plt.plot(x0, y0, 'o', color=color, markersize=6)
    else:
        ys = [y0 + m * (x - x0) for x in xs]
        plt.plot(xs, ys, color=color, linewidth=2,
                 label=f"{label}: α = {alpha_deg}°, m = tan(α) = {m:.3f}")
        plt.plot(x0, y0, 'o', color=color, markersize=6)

def main():
    print("📐 Straight Line from Angle α (alpha)")
    print("Define a line by a point (x₀, y₀) and angle α it makes with +x-axis.")
    
    try:
        x0 = float(input("x₀ = "))
        y0 = float(input("y₀ = "))
        alpha = float(input("α (angle in degrees) = "))
        draw_perp = input("Also draw perpendicular (i.e., α + 90°)? [y/N]: ").strip().lower() == 'y'
    except ValueError:
        print("❌ Invalid input. Please enter numbers only.")
        return

    plt.figure(figsize=(8, 7))
    plot_line(x0, y0, alpha, label="Given line", color='steelblue')

    if draw_perp:
        alpha_perp = alpha + 90
        # Normalize to (-180, 180] for neatness
        alpha_perp = ((alpha_perp + 180) % 360) - 180
        plot_line(x0, y0, alpha_perp, label="Perpendicular (α + 90°)", color='crimson')

    # Axes & grid
    ax = plt.gca()
    ax.axhline(0, color='gray', linewidth=0.8)
    ax.axvline(0, color='gray', linewidth=0.8)
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.set_aspect('equal', adjustable='box')
    
    plt.xlim(x0 - 7, x0 + 7)
    plt.ylim(y0 - 7, y0 + 7)
    plt.title(f"Line through ({x0}, {y0}) — α = {alpha}°", fontsize=14)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend(loc='upper right')
    plt.tight_layout()

    # Show key values
    m = math.tan(math.radians(alpha))
    print(f"\n✅ Slope m = tan(α) = tan({alpha}°) = {m:.5f}")
    if draw_perp:
        m_perp = math.tan(math.radians(alpha + 90))
        print(f"✅ Perpendicular slope = tan(α + 90°) = {m_perp:.5f}  (≈ -1/m if m ≠ 0)")

    plt.show()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

def point_slope_eq(x0, y0, m):
    """Return the point-slope form as a formatted string."""
    sign_x = " - " if x0 >= 0 else " + "
    sign_y = " - " if y0 >= 0 else " + "
    x_term = f"(x {sign_x}{abs(x0)})" if x0 != 0 else "x"
    y_term = f"y {sign_y}{abs(y0)}" if y0 != 0 else "y"
    return f"{y_term} = {m} * {x_term}"

def main():
    print("Enter point (x0, y0) and slope m to get point-slope equation.")
    try:
        x0 = float(input("x0 = "))
        y0 = float(input("y0 = "))
        m  = float(input("slope m = "))
    except ValueError:
        print("❌ Invalid input. Please enter numbers only.")
        return

    eq = point_slope_eq(x0, y0, m)
    print(f"\n✅ Point-slope equation:\n   {eq}")

    # Optional: Convert to slope-intercept (y = mx + b)
    b = y0 - m * x0
    print(f"   (Slope-intercept form: y = {m}x + {b:.3f})")

if __name__ == "__main__":
    main()

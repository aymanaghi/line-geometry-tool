#!/usr/bin/env python3
"""
📐 VECTOR CALCULATOR
2D & 3D vector operations — step by step.

Supported:
  • Magnitude, unit vector
  • Dot product → angle
  • Cross product (3D)
  • Projection of A onto B
  • Linear combination: αA + βB

Input examples:
  A = 1,2       (2D)
  B = 3,-1,4    (3D)
"""

import math

def parse_vector(s):
    s = s.strip().replace("(", "").replace(")", "").replace(" ", "")
    vals = list(map(float, s.split(",")))
    if len(vals) not in (2, 3):
        raise ValueError("Vector must be 2D (x,y) or 3D (x,y,z)")
    return vals

def magnitude(v):
    return math.sqrt(sum(x*x for x in v))

def dot(u, v):
    return sum(a*b for a, b in zip(u, v))

def cross(u, v):
    if len(u) != 3 or len(v) != 3:
        raise ValueError("Cross product only defined for 3D vectors.")
    x = u[1]*v[2] - u[2]*v[1]
    y = u[2]*v[0] - u[0]*v[2]
    z = u[0]*v[1] - u[1]*v[0]
    return [x, y, z]

def unit(v):
    m = magnitude(v)
    if m == 0:
        raise ValueError("Zero vector has no unit vector.")
    return [x/m for x in v]

def angle_rad(u, v):
    d = dot(u, v)
    mu, mv = magnitude(u), magnitude(v)
    if mu == 0 or mv == 0:
        raise ValueError("Cannot compute angle with zero vector.")
    cosθ = max(-1.0, min(1.0, d / (mu * mv)))
    return math.acos(cosθ)

def proj(u, v):
    """Projection of u onto v"""
    if magnitude(v) == 0:
        raise ValueError("Cannot project onto zero vector.")
    scalar = dot(u, v) / (magnitude(v)**2)
    return [scalar * x for x in v]

def print_vector(v, name="v"):
    if len(v) == 2:
        print(f"{name} = ({v[0]:.3g}, {v[1]:.3g})")
    else:
        print(f"{name} = ({v[0]:.3g}, {v[1]:.3g}, {v[2]:.3g})")

def main():
    print("📐 VECTOR CALCULATOR")
    print("Enter vectors as: x,y  or  x,y,z")
    print("-" * 40)

    try:
        A_str = input("➤ A = ").strip()
        B_str = input("➤ B = ").strip()
        A = parse_vector(A_str)
        B = parse_vector(B_str)
    except Exception as e:
        print(f"❌ Input error: {e}")
        return

    dim = max(len(A), len(B))
    if len(A) < dim:
        A += [0] * (dim - len(A))
    if len(B) < dim:
        B += [0] * (dim - len(B))

    print("\n📊 Results")
    print("=" * 40)

    # Magnitudes
    magA = magnitude(A)
    magB = magnitude(B)
    print(f"|A| = {magA:.5g}")
    print(f"|B| = {magB:.5g}")

    # Unit vectors
    try:
        uA = unit(A)
        uB = unit(B)
        print("\nUnit vectors:")
        print_vector(uA, "Â")
        print_vector(uB, "B̂")
    except Exception as e:
        print(f"\n⚠️ Unit vector: {e}")

    # Dot product & angle
    d = dot(A, B)
    print(f"\nA • B = {d:.5g}")
    try:
        θ = angle_rad(A, B)
        print(f"Angle θ = {math.degrees(θ):.3f}°")
    except Exception as e:
        print(f"Angle: {e}")

    # Cross product (3D only)
    if dim == 3:
        try:
            C = cross(A, B)
            print(f"\nA × B = ", end=""); print_vector(C, "")
            print(f"|A × B| = {magnitude(C):.5g}")
        except Exception as e:
            print(f"\n⚠️ Cross product: {e}")

    # Projection
    try:
        p = proj(A, B)
        print(f"\nProjection of A onto B:")
        print_vector(p, "proj_B(A)")
        comp = dot(A, B) / magB if magB != 0 else float('nan')
        print(f"Scalar component = {comp:.5g}")
    except Exception as e:
        print(f"\n⚠️ Projection: {e}")

    # Linear combo
    print("\n🔧 Linear combination: αA + βB")
    try:
        α = float(input("α = ") or "1")
        β = float(input("β = ") or "1")
        combo = [α*a + β*b for a, b in zip(A, B)]
        print("Result: ", end=""); print_vector(combo, f"{α}A+{β}B")
    except Exception as e:
        print(f"Linear combo: {e}")

    print("\n✅ Done.")

if __name__ == "__main__":
    main()

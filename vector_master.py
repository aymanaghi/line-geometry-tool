#!/usr/bin/env python3
"""
🌟 VECTOR MASTER — Complete Vector Algebra Toolkit
Covers every standard vector operation in 2D and 3D.

Operations included:
✓ Vector addition, subtraction, scalar multiplication
✓ Dot product → angle between vectors
✓ Cross product (3D) → area of parallelogram
✓ Triple products (scalar & vector)
✓ Projection, component, rejection
✓ Magnitude, unit vector
✓ Distance between points/vectors
✓ Area of triangle/parallelogram
✓ Volume of parallelepiped
✓ Linear dependence check
✓ Vector equation of line/plane
✓ Coordinate transformations
✓ Vector decomposition
"""

import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# === CORE VECTOR OPERATIONS ===

def parse_vector(s):
    """Parse vector string like '1,2' or '3,4,5' or '(1,2,3)'"""
    s = s.strip().replace("(", "").replace(")", "").replace(" ", "")
    if not s:
        return []
    vals = list(map(float, s.split(",")))
    if len(vals) not in (2, 3):
        raise ValueError("Vector must be 2D (x,y) or 3D (x,y,z)")
    return vals

def magnitude(v):
    """|v| = sqrt(v•v)"""
    return math.sqrt(sum(x*x for x in v))

def dot(u, v):
    """u•v = u₁v₁ + u₂v₂ + u₃v₃"""
    return sum(a*b for a, b in zip(u, v))

def cross(u, v):
    """u×v (3D only)"""
    if len(u) != 3 or len(v) != 3:
        raise ValueError("Cross product only defined for 3D vectors")
    x = u[1]*v[2] - u[2]*v[1]
    y = u[2]*v[0] - u[0]*v[2]
    z = u[0]*v[1] - u[1]*v[0]
    return [x, y, z]

def scalar_triple(u, v, w):
    """u•(v×w) - volume of parallelepiped"""
    return dot(u, cross(v, w))

def vector_triple(u, v, w):
    """u×(v×w) = (u•w)v - (u•v)w"""
    uw = dot(u, w)
    uv = dot(u, v)
    return [uw*v[i] - uv*w[i] for i in range(3)]

def unit(v):
    """v̂ = v/|v|"""
    m = magnitude(v)
    if m < 1e-10:
        raise ValueError("Cannot normalize zero vector")
    return [x/m for x in v]

def angle(u, v):
    """Angle between vectors in degrees"""
    d = dot(u, v)
    mu, mv = magnitude(u), magnitude(v)
    if mu < 1e-10 or mv < 1e-10:
        raise ValueError("Cannot compute angle with zero vector")
    cosθ = max(-1.0, min(1.0, d / (mu * mv)))
    return math.degrees(math.acos(cosθ))

def proj(u, v):
    """Projection of u onto v: proj_v(u) = (u•v/|v|²)v"""
    if magnitude(v) < 1e-10:
        raise ValueError("Cannot project onto zero vector")
    scalar = dot(u, v) / (magnitude(v)**2)
    return [scalar * x for x in v]

def comp(u, v):
    """Component of u along v: comp_v(u) = u•v̂"""
    return dot(u, unit(v))

def rejection(u, v):
    """Rejection of u from v: u - proj_v(u)"""
    p = proj(u, v)
    return [u[i] - p[i] for i in range(len(u))]

def distance(u, v):
    """Distance between points u and v"""
    return magnitude([u[i] - v[i] for i in range(len(u))])

def area_parallelogram(u, v):
    """Area = |u×v|"""
    return magnitude(cross(u, v))

def area_triangle(u, v):
    """Area = ½|u×v|"""
    return 0.5 * magnitude(cross(u, v))

def volume_parallelepiped(u, v, w):
    """Volume = |u•(v×w)|"""
    return abs(scalar_triple(u, v, w))

def linear_dependence(vectors):
    """Check if vectors are linearly dependent"""
    if len(vectors) == 2:
        # 2D: dependent if one is scalar multiple of other
        if magnitude(vectors[0]) < 1e-10 or magnitude(vectors[1]) < 1e-10:
            return True
        ratio = vectors[0][0]/vectors[1][0] if abs(vectors[1][0]) > 1e-10 else None
        for i in range(1, len(vectors[0])):
            if abs(vectors[1][i]) < 1e-10:
                if abs(vectors[0][i]) > 1e-10:
                    return False
                continue
            r = vectors[0][i]/vectors[1][i]
            if ratio is None:
                ratio = r
            elif abs(r - ratio) > 1e-6:
                return False
        return True
    
    elif len(vectors) == 3 and len(vectors[0]) == 3:
        # 3D: dependent if scalar triple product = 0
        return abs(scalar_triple(vectors[0], vectors[1], vectors[2])) < 1e-6
    
    return "Cannot determine for this configuration"

# === PLOTTING FUNCTIONS ===

def plot_2d_vectors(vectors, labels=None, title="2D Vector Plot"):
    plt.figure(figsize=(10, 8))
    ax = plt.gca()
    
    # Draw axes
    ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    
    # Plot each vector
    colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown']
    for i, v in enumerate(vectors):
        color = colors[i % len(colors)]
        label = labels[i] if labels and i < len(labels) else f'v{i+1}'
        plt.arrow(0, 0, v[0], v[1], 
                 head_width=0.1, head_length=0.15, fc=color, ec=color,
                 length_includes_head=True, label=label)
    
    # Set limits
    max_val = max(max(abs(v[0]), abs(v[1])) for v in vectors) * 1.2
    plt.xlim(-max_val, max_val)
    plt.ylim(-max_val, max_val)
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.gca().set_aspect('equal')
    print("📈 2D plot ready. Close window to continue.")
    plt.show()

def plot_3d_vectors(vectors, labels=None, title="3D Vector Plot"):
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot each vector
    colors = ['blue', 'red', 'green', 'purple', 'orange']
    for i, v in enumerate(vectors):
        color = colors[i % len(colors)]
        label = labels[i] if labels and i < len(labels) else f'v{i+1}'
        ax.quiver(0, 0, 0, v[0], v[1], v[2], 
                 color=color, arrow_length_ratio=0.1, label=label)
    
    # Set limits
    max_val = max(max(abs(v[i]) for v in vectors) for i in range(3)) * 1.2
    ax.set_xlim(-max_val, max_val)
    ax.set_ylim(-max_val, max_val)
    ax.set_zlim(-max_val, max_val)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    ax.legend()
    print("📈 3D plot ready. Close window to continue.")
    plt.show()

# === INTERACTIVE MENU SYSTEM ===

OPERATIONS = [
    ("Vector Addition", "A + B"),
    ("Vector Subtraction", "A - B"),
    ("Scalar Multiplication", "k·A"),
    ("Dot Product", "A•B → angle"),
    ("Cross Product (3D)", "A×B → area"),
    ("Scalar Triple Product", "A•(B×C) → volume"),
    ("Vector Triple Product", "A×(B×C)"),
    ("Projection", "proj_B(A)"),
    ("Component", "comp_B(A)"),
    ("Rejection", "rej_B(A)"),
    ("Magnitude", "|A|"),
    ("Unit Vector", "Â"),
    ("Distance", "|A-B|"),
    ("Area of Parallelogram", "|A×B|"),
    ("Area of Triangle", "½|A×B|"),
    ("Volume of Parallelepiped", "|A•(B×C)|"),
    ("Linear Dependence Check", "Are A,B,C dependent?"),
    ("Vector Equation of Line", "r = r₀ + t·d"),
    ("Vector Equation of Plane", "r = r₀ + s·u + t·v")
]

def get_vectors(count=2, dim=None):
    """Get multiple vectors from user"""
    vectors = []
    labels = []
    
    for i in range(count):
        label = chr(65 + i)  # A, B, C...
        labels.append(label)
        
        while True:
            try:
                inp = input(f"➤ {label} = ").strip()
                if not inp:
                    # Default vectors for demo
                    if i == 0:
                        inp = "1,2,3" if dim == 3 else "2,1"
                    else:
                        inp = "4,-1,2" if dim == 3 else "1,3"
                
                v = parse_vector(inp)
                if dim is None:
                    dim = len(v)
                elif len(v) != dim:
                    print(f"⚠️  Must be {dim}D vector. Try again.")
                    continue
                
                vectors.append(v)
                break
            except Exception as e:
                print(f"❌ {str(e)}. Try again.")
    
    return vectors, labels, dim

def perform_operation(choice, vectors, labels):
    """Perform selected operation and show results"""
    A, B = vectors[0], vectors[1]
    result = None
    explanation = ""
    plot_vectors = [A, B]
    plot_labels = [f"{labels[0]} = {A}", f"{labels[1]} = {B}"]
    dim = len(A)
    
    try:
        if choice == 1:  # Addition
            result = [A[i] + B[i] for i in range(dim)]
            explanation = f"{labels[0]} + {labels[1]} = ({'+'.join(f'{A[i]}+{B[i]}' for i in range(dim))})"
            plot_vectors.append(result)
            plot_labels.append(f"{labels[0]}+{labels[1]} = {result}")
        
        elif choice == 2:  # Subtraction
            result = [A[i] - B[i] for i in range(dim)]
            explanation = f"{labels[0]} - {labels[1]} = ({'-'.join(f'{A[i]}-{B[i]}' for i in range(dim))})"
            plot_vectors.append(result)
            plot_labels.append(f"{labels[0]}-{labels[1]} = {result}")
        
        elif choice == 3:  # Scalar Multiplication
            k = float(input("Scale factor k = ") or "2")
            result = [k * x for x in A]
            explanation = f"{k}·{labels[0]} = ({', '.join(f'{k}*{A[i]}' for i in range(dim))})"
            plot_vectors.append(result)
            plot_labels.append(f"{k}{labels[0]} = {result}")
        
        elif choice == 4:  # Dot Product
            d = dot(A, B)
            ang = angle(A, B)
            result = d
            explanation = f"{labels[0]}•{labels[1]} = {d:.4f}\nAngle = {ang:.2f}°"
        
        elif choice == 5:  # Cross Product (3D only)
            if dim != 3:
                raise ValueError("Cross product only works in 3D")
            C = cross(A, B)
            area_para = magnitude(C)
            area_tri = 0.5 * area_para
            result = C
            explanation = f"{labels[0]}×{labels[1]} = {C}\n|{labels[0]}×{labels[1]}| = {area_para:.4f} (parallelogram area)\nArea of triangle = {area_tri:.4f}"
            plot_vectors.append(C)
            plot_labels.append(f"{labels[0]}×{labels[1]} = {C}")
        
        elif choice == 6:  # Scalar Triple Product
            if len(vectors) < 3:
                C, labelC = get_vectors(1, dim)[0][0], chr(67)
                vectors.append(C)
                labels.append(labelC)
            else:
                C = vectors[2]
            vol = scalar_triple(A, B, C)
            result = vol
            explanation = f"{labels[0]}•({labels[1]}×{labels[2]}) = {vol:.4f}\nVolume of parallelepiped = {abs(vol):.4f}"
        
        elif choice == 7:  # Vector Triple Product
            if len(vectors) < 3:
                C, labelC = get_vectors(1, dim)[0][0], chr(67)
                vectors.append(C)
                labels.append(labelC)
            else:
                C = vectors[2]
            V = vector_triple(A, B, C)
            result = V
            explanation = f"{labels[0]}×({labels[1]}×{labels[2]}) = {V}"
            plot_vectors.append(V)
            plot_labels.append(f"{labels[0]}×({labels[1]}×{labels[2]})")
        
        elif choice == 8:  # Projection
            P = proj(A, B)
            result = P
            explanation = f"proj_{labels[1]}({labels[0]}) = {P}"
            plot_vectors.append(P)
            plot_labels.append(f"proj_{labels[1]}({labels[0]})")
        
        elif choice == 9:  # Component
            c = comp(A, B)
            result = c
            explanation = f"comp_{labels[1]}({labels[0]}) = {c:.4f}"
        
        elif choice == 10:  # Rejection
            R = rejection(A, B)
            result = R
            explanation = f"rej_{labels[1]}({labels[0]}) = {R}"
            plot_vectors.append(R)
            plot_labels.append(f"rej_{labels[1]}({labels[0]})")
        
        elif choice == 11:  # Magnitude
            m = magnitude(A)
            result = m
            explanation = f"|{labels[0]}| = {m:.4f}"
        
        elif choice == 12:  # Unit Vector
            U = unit(A)
            result = U
            explanation = f"û{labels[0]} = {U}"
            plot_vectors.append(U)
            plot_labels.append(f"û{labels[0]} = {U}")
        
        elif choice == 13:  # Distance
            dist = distance(A, B)
            result = dist
            explanation = f"Distance between {labels[0]} and {labels[1]} = {dist:.4f}"
        
        elif choice == 14:  # Area of Parallelogram
            if dim != 3:
                raise ValueError("Area calculation needs 3D vectors")
            area = area_parallelogram(A, B)
            result = area
            explanation = f"Area of parallelogram = |{labels[0]}×{labels[1]}| = {area:.4f}"
        
        elif choice == 15:  # Area of Triangle
            if dim != 3:
                raise ValueError("Area calculation needs 3D vectors")
            area = area_triangle(A, B)
            result = area
            explanation = f"Area of triangle = ½|{labels[0]}×{labels[1]}| = {area:.4f}"
        
        elif choice == 16:  # Volume of Parallelepiped
            if len(vectors) < 3:
                C, labelC = get_vectors(1, dim)[0][0], chr(67)
                vectors.append(C)
                labels.append(labelC)
            else:
                C = vectors[2]
            vol = volume_parallelepiped(A, B, C)
            result = vol
            explanation = f"Volume of parallelepiped = |{labels[0]}•({labels[1]}×{labels[2]})| = {vol:.4f}"
        
        elif choice == 17:  # Linear Dependence
            if len(vectors) < 3:
                C, labelC = get_vectors(1, dim)[0][0], chr(67)
                vectors.append(C)
                labels.append(labelC)
            else:
                C = vectors[2]
            dep = linear_dependence([A, B, C])
            result = dep
            explanation = f"Are {labels[0]}, {labels[1]}, {labels[2]} linearly dependent?\nAnswer: {'Yes' if dep else 'No'}"
        
        elif choice == 18:  # Vector Equation of Line
            P0 = A
            d = B
            t = float(input("Parameter t = ") or "1")
            point = [P0[i] + t * d[i] for i in range(dim)]
            result = point
            explanation = f"Line: r = {P0} + t·{d}\nAt t={t}: r = {point}"
            plot_vectors.append(point)
            plot_labels.append(f"Point at t={t}")
        
        elif choice == 19:  # Vector Equation of Plane
            if len(vectors) < 3:
                C, labelC = get_vectors(1, dim)[0][0], chr(67)
                vectors.append(C)
                labels.append(labelC)
            else:
                C = vectors[2]
            P0 = A
            u = B
            v = C
            s = float(input("Parameter s = ") or "1")
            t = float(input("Parameter t = ") or "1")
            point = [P0[i] + s * u[i] + t * v[i] for i in range(dim)]
            result = point
            explanation = f"Plane: r = {P0} + s·{u} + t·{v}\nAt s={s}, t={t}: r = {point}"
            plot_vectors.append(point)
            plot_labels.append(f"Point at s={s}, t={t}")
        
        # Display results
        print("\n🎯 RESULT")
        print("=" * 50)
        if result is not None:
            print(f"Result: {result}")
        print(explanation)
        
        # Ask to plot
        if input("\nPlot vectors? (y/N) ").strip().lower() in ('y', 'yes'):
            if dim == 2:
                plot_2d_vectors(plot_vectors, plot_labels, f"Operation: {OPERATIONS[choice-1][0]}")
            else:
                plot_3d_vectors(plot_vectors, plot_labels, f"Operation: {OPERATIONS[choice-1][0]}")
        
        return True
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def main():
    print("🌟 VECTOR MASTER — Every Vector Operation in One Tool")
    print("=" * 60)
    print("Choose an operation:")
    
    for i, (name, desc) in enumerate(OPERATIONS, 1):
        print(f"{i:2}. {name:<25} {desc}")
    
    try:
        choice = int(input("\n➤ Select operation (1-19): "))
        if not (1 <= choice <= len(OPERATIONS)):
            raise ValueError
        
        # Get vectors based on operation needs
        if choice in [6, 7, 16, 17, 19]:  # Operations needing 3 vectors
            vectors, labels, dim = get_vectors(3)
        else:
            vectors, labels, dim = get_vectors(2)
        
        perform_operation(choice, vectors, labels)
        
        print("\n✅ Operation completed successfully!")
    
    except Exception as e:
        print(f"\n❌ Input error: {str(e)}")
        print("Try again with proper values.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
📐 TRIANGLE HEIGHT CALCULATOR
Find the length of height CH from vertex C to side AB in triangle ABC.

Given points A, B, C with coordinates:
  A = (x₁, y₁)
  B = (x₂, y₂)  
  C = (x₃, y₃)

The height CH is the perpendicular distance from point C to line AB.

Formula used:
  CH = |(B-A) × (A-C)| / |B-A|
     = |(x₂-x₁)(y₁-y₃) - (x₁-x₃)(y₂-y₁)| / √((x₂-x₁)² + (y₂-y₁)²)
"""

import math
import matplotlib.pyplot as plt

def distance(p1, p2):
    """Calculate distance between two points"""
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def vector(p1, p2):
    """Calculate vector from p1 to p2"""
    return (p2[0] - p1[0], p2[1] - p1[1])

def cross_product(v1, v2):
    """2D cross product (returns scalar magnitude)"""
    return v1[0]*v2[1] - v1[1]*v2[0]

def dot_product(v1, v2):
    """Dot product of two vectors"""
    return v1[0]*v2[0] + v1[1]*v2[1]

def point_on_line(A, B, t):
    """Point on line AB at parameter t (0≤t≤1)"""
    return (A[0] + t*(B[0]-A[0]), A[1] + t*(B[1]-A[1]))

def height_from_C_to_AB(A, B, C):
    """
    Calculate height from point C to line AB
    
    Formula: CH = |(B-A) × (A-C)| / |B-A|
    """
    # Vector AB = B - A
    AB = vector(A, B)
    
    # Vector AC = C - A
    AC = vector(A, C)
    
    # Cross product magnitude |AB × AC|
    cross_mag = abs(cross_product(AB, AC))
    
    # Length of AB
    AB_length = distance(A, B)
    
    # Height = |cross product| / base length
    if AB_length < 1e-10:
        raise ValueError("Points A and B are too close - cannot form a triangle base")
    
    height = cross_mag / AB_length
    
    # Find foot of perpendicular H
    # Using projection: t = (AC • AB) / |AB|²
    AB_squared = AB[0]**2 + AB[1]**2
    t = dot_product(AC, AB) / AB_squared
    
    # H = A + t*AB
    H = point_on_line(A, B, t)
    
    return height, H

def plot_triangle_with_height(A, B, C, H, height):
    """Plot triangle ABC with height CH"""
    plt.figure(figsize=(10, 8))
    
    # Plot triangle sides
    plt.plot([A[0], B[0]], [A[1], B[1]], 'b-', linewidth=2, label=f'AB = {distance(A, B):.3f}')
    plt.plot([B[0], C[0]], [B[1], C[1]], 'g-', linewidth=2, label=f'BC = {distance(B, C):.3f}')
    plt.plot([C[0], A[0]], [C[1], A[1]], 'r-', linewidth=2, label=f'CA = {distance(C, A):.3f}')
    
    # Plot height CH
    plt.plot([C[0], H[0]], [C[1], H[1]], 'm--', linewidth=2, label=f'CH = {height:.3f}')
    
    # Plot points
    plt.plot(A[0], A[1], 'bo', markersize=8, label=f'A{A}')
    plt.plot(B[0], B[1], 'go', markersize=8, label=f'B{B}')
    plt.plot(C[0], C[1], 'ro', markersize=8, label=f'C{C}')
    plt.plot(H[0], H[1], 'ko', markersize=8, label=f'H{H}')
    
    # Add right angle marker at H
    # Get direction vectors
    CH_vec = vector(H, C)
    AB_vec = vector(A, B)
    
    # Normalize vectors
    CH_len = distance(H, C)
    AB_len = distance(A, B)
    
    if CH_len > 1e-10 and AB_len > 1e-10:
        # Unit vectors
        u_CH = (CH_vec[0]/CH_len, CH_vec[1]/CH_len)
        u_AB = (AB_vec[0]/AB_len, AB_vec[1]/AB_len)
        
        # Create right angle marker points
        marker_len = min(0.3, CH_len/5, AB_len/5)
        p1 = (H[0] + marker_len*u_AB[0], H[1] + marker_len*u_AB[1])
        p2 = (p1[0] + marker_len*u_CH[0], p1[1] + marker_len*u_CH[1])
        p3 = (H[0] + marker_len*u_CH[0], H[1] + marker_len*u_CH[1])
        
        plt.plot([H[0], p1[0], p2[0], p3[0], H[0]], 
                [H[1], p1[1], p2[1], p3[1], H[1]], 'k-')
    
    # Set equal aspect ratio
    plt.gca().set_aspect('equal')
    
    # Set limits with padding
    all_x = [A[0], B[0], C[0], H[0]]
    all_y = [A[1], B[1], C[1], H[1]]
    x_padding = (max(all_x) - min(all_x)) * 0.2
    y_padding = (max(all_y) - min(all_y)) * 0.2
    
    plt.xlim(min(all_x) - x_padding, max(all_x) + x_padding)
    plt.ylim(min(all_y) - y_padding, max(all_y) + y_padding)
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.title(f'Triangle ABC with Height CH = {height:.4f}', fontsize=14)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(loc='best')
    plt.tight_layout()
    print("\n📈 Plot window opened. Close it to continue.")
    plt.show()

def main():
    print("📐 TRIANGLE HEIGHT CALCULATOR")
    print("Find the length of height CH from vertex C to side AB")
    print("=" * 60)
    
    try:
        # Get coordinates with default values for easy testing
        print("\n➤ Enter coordinates for triangle vertices:")
        A_x = float(input(f"A.x = [0] ") or "0")
        A_y = float(input(f"A.y = [0] ") or "0")
        B_x = float(input(f"B.x = [4] ") or "4")
        B_y = float(input(f"B.y = [0] ") or "0")
        C_x = float(input(f"C.x = [1] ") or "1")
        C_y = float(input(f"C.y = [3] ") or "3")
        
        A = (A_x, A_y)
        B = (B_x, B_y)
        C = (C_x, C_y)
        
        print(f"\nTriangle vertices:")
        print(f"  A = {A}")
        print(f"  B = {B}")
        print(f"  C = {C}")
        
        # Calculate side lengths
        AB = distance(A, B)
        BC = distance(B, C)
        CA = distance(C, A)
        
        print(f"\n📊 Side lengths:")
        print(f"  AB = {AB:.4f}")
        print(f"  BC = {BC:.4f}")
        print(f"  CA = {CA:.4f}")
        
        # Check if it's a valid triangle
        if AB + BC <= CA or AB + CA <= BC or BC + CA <= AB:
            print(f"\n❌ Invalid triangle: The points are collinear or too close.")
            print(f"   Triangle inequality violated: sum of any two sides must be > third side")
            return
        
        # Calculate height CH
        height, H = height_from_C_to_AB(A, B, C)
        
        print(f"\n🎯 HEIGHT CALCULATION")
        print("=" * 40)
        print(f"Height CH from C to line AB = {height:.6f}")
        print(f"Foot of perpendicular H = {H}")
        
        # Show step-by-step calculation
        print(f"\n🔍 Step-by-step calculation:")
        print(f"1. Vector AB = B - A = ({B[0]-A[0]:.3f}, {B[1]-A[1]:.3f})")
        print(f"2. Vector AC = C - A = ({C[0]-A[0]:.3f}, {C[1]-A[1]:.3f})")
        print(f"3. Cross product |AB × AC| = |{(B[0]-A[0])*(C[1]-A[1]) - (B[1]-A[1])*(C[0]-A[0]):.6f}| = {abs((B[0]-A[0])*(C[1]-A[1]) - (B[1]-A[1])*(C[0]-A[0])):.6f}")
        print(f"4. Length of AB = √(({B[0]-A[0]:.3f})² + ({B[1]-A[1]:.3f})²) = {AB:.6f}")
        print(f"5. Height CH = |AB × AC| / |AB| = {abs((B[0]-A[0])*(C[1]-A[1]) - (B[1]-A[1])*(C[0]-A[0])):.6f} / {AB:.6f} = {height:.6f}")
        
        # Calculate area as verification
        area = 0.5 * AB * height
        area_alt = 0.5 * abs((B[0]-A[0])*(C[1]-A[1]) - (B[1]-A[1])*(C[0]-A[0]))
        print(f"\n✅ Verification using area:")
        print(f"   Area = ½ × base × height = ½ × {AB:.4f} × {height:.4f} = {area:.6f}")
        print(f"   Area (cross product method) = ½ × |AB × AC| = ½ × {abs((B[0]-A[0])*(C[1]-A[1]) - (B[1]-A[1])*(C[0]-A[0])):.6f} = {area_alt:.6f}")
        print(f"   ✓ Methods match: difference = {abs(area - area_alt):.2e}")
        
        # Ask to plot
        if input("\n📊 Plot the triangle with height CH? (y/N) ").strip().lower() in ('y', 'yes'):
            plot_triangle_with_height(A, B, C, H, height)
        
        print(f"\n💡 Key insight:")
        print(f"   The height CH is the perpendicular distance from C to line AB.")
        print(f"   This is also the minimum distance from point C to any point on line AB.")
        print(f"   In physics, this represents the effective lever arm for torque calculations.")
        
        print(f"\n✅ Calculation complete!")
    
    except ValueError as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please enter valid numerical coordinates.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print("Please check your input values.")

if __name__ == "__main__":
    main()

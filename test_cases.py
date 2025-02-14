import numpy as np
from matrix_operations import (
    add_matrices,
    subtract_matrices,
    multiply_matrices,
    compute_inverse,
    compute_eigenvalues_eigenvectors
)
from matrix_utils import string_to_matrix

def test_operations():
    # Test Case 1: Simple 2x2 matrices
    matrix_2x2_A = string_to_matrix("4 3; 2 1")
    matrix_2x2_B = string_to_matrix("1 2; 3 4")
    
    # Test Case 2: 3x3 matrices
    matrix_3x3_A = string_to_matrix("1 2 3; 4 5 6; 7 8 9")
    matrix_3x3_B = string_to_matrix("9 8 7; 6 5 4; 3 2 1")
    
    # Test Case 3: Matrix for inverse (must be non-singular)
    invertible_matrix = string_to_matrix("4 7; 2 6")
    
    # Test Case 4: Matrix for eigenvalues/vectors
    eigen_matrix = string_to_matrix("3 -2; 1 4")

    print("=== Test Cases for Matrix Operations ===\n")

    # Addition Tests
    print("1. Matrix Addition")
    print("Matrix A:")
    print(matrix_2x2_A)
    print("Matrix B:")
    print(matrix_2x2_B)
    print("A + B =")
    print(add_matrices(matrix_2x2_A, matrix_2x2_B))
    print("\n")

    # Subtraction Tests
    print("2. Matrix Subtraction")
    print("Matrix A:")
    print(matrix_3x3_A)
    print("Matrix B:")
    print(matrix_3x3_B)
    print("A - B =")
    print(subtract_matrices(matrix_3x3_A, matrix_3x3_B))
    print("\n")

    # Multiplication Tests
    print("3. Matrix Multiplication")
    print("Matrix A:")
    print(matrix_2x2_A)
    print("Matrix B:")
    print(matrix_2x2_B)
    print("A × B =")
    print(multiply_matrices(matrix_2x2_A, matrix_2x2_B))
    print("\n")

    # Inverse Tests
    print("4. Matrix Inverse")
    print("Original Matrix:")
    print(invertible_matrix)
    print("Inverse:")
    inverse = compute_inverse(invertible_matrix)
    print(inverse)
    print("Verification (should be near identity matrix):")
    print(multiply_matrices(invertible_matrix, inverse))
    print("\n")

    # Eigenvalues and Eigenvectors Tests
    print("5. Eigenvalues and Eigenvectors")
    print("Matrix:")
    print(eigen_matrix)
    eigenvalues, eigenvectors = compute_eigenvalues_eigenvectors(eigen_matrix)
    print("Eigenvalues:")
    print(eigenvalues)
    print("Eigenvectors:")
    print(eigenvectors)
    print("\nVerification:")
    for i in range(len(eigenvalues)):
        print(f"For eigenvalue {eigenvalues[i]:.2f}:")
        print(f"A·v = {multiply_matrices(eigen_matrix, eigenvectors[:, i:i+1]).flatten()}")
        print(f"λ·v = {(eigenvalues[i] * eigenvectors[:, i]).flatten()}")
        print()

if __name__ == "__main__":
    test_operations() 
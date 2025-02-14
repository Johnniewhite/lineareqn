import pytest
import numpy as np
from matrix_operations import (
    add_matrices,
    subtract_matrices,
    multiply_matrices,
    compute_inverse,
    compute_eigenvalues_eigenvectors
)
from matrix_utils import string_to_matrix

# Fixtures for commonly used matrices
@pytest.fixture
def matrix_2x2_A():
    return string_to_matrix("4 3; 2 1")

@pytest.fixture
def matrix_2x2_B():
    return string_to_matrix("1 2; 3 4")

@pytest.fixture
def matrix_3x3_A():
    return string_to_matrix("1 2 3; 4 5 6; 7 8 9")

@pytest.fixture
def matrix_3x3_B():
    return string_to_matrix("9 8 7; 6 5 4; 3 2 1")

@pytest.fixture
def invertible_matrix():
    return string_to_matrix("4 7; 2 6")

@pytest.fixture
def eigen_matrix():
    return string_to_matrix("3 -2; 1 4")

# Test matrix addition
def test_matrix_addition(matrix_2x2_A, matrix_2x2_B):
    result = add_matrices(matrix_2x2_A, matrix_2x2_B)
    expected = np.array([[5, 5], [5, 5]])
    np.testing.assert_array_almost_equal(result, expected)

def test_matrix_addition_3x3(matrix_3x3_A, matrix_3x3_B):
    result = add_matrices(matrix_3x3_A, matrix_3x3_B)
    expected = np.array([[10, 10, 10], [10, 10, 10], [10, 10, 10]])
    np.testing.assert_array_almost_equal(result, expected)

def test_matrix_addition_error():
    matrix1 = string_to_matrix("1 2; 3 4")
    matrix2 = string_to_matrix("1 2 3; 4 5 6")
    with pytest.raises(ValueError):
        add_matrices(matrix1, matrix2)

# Test matrix subtraction
def test_matrix_subtraction(matrix_2x2_A, matrix_2x2_B):
    result = subtract_matrices(matrix_2x2_A, matrix_2x2_B)
    expected = np.array([[3, 1], [-1, -3]])
    np.testing.assert_array_almost_equal(result, expected)

def test_matrix_subtraction_3x3(matrix_3x3_A, matrix_3x3_B):
    result = subtract_matrices(matrix_3x3_A, matrix_3x3_B)
    expected = np.array([[-8, -6, -4], [-2, 0, 2], [4, 6, 8]])
    np.testing.assert_array_almost_equal(result, expected)

def test_matrix_subtraction_error():
    matrix1 = string_to_matrix("1 2; 3 4")
    matrix2 = string_to_matrix("1 2 3; 4 5 6")
    with pytest.raises(ValueError):
        subtract_matrices(matrix1, matrix2)

# Test matrix multiplication
def test_matrix_multiplication(matrix_2x2_A, matrix_2x2_B):
    result = multiply_matrices(matrix_2x2_A, matrix_2x2_B)
    expected = np.array([[13, 20], [5, 8]])
    np.testing.assert_array_almost_equal(result, expected)

def test_matrix_multiplication_error():
    matrix1 = string_to_matrix("1 2 3; 4 5 6")
    matrix2 = string_to_matrix("1 2; 3 4")
    with pytest.raises(ValueError):
        multiply_matrices(matrix1, matrix2)

# Test matrix inverse
def test_matrix_inverse(invertible_matrix):
    result = compute_inverse(invertible_matrix)
    # Verify that A * A^(-1) = I
    identity = multiply_matrices(invertible_matrix, result)
    expected = np.eye(2)
    np.testing.assert_array_almost_equal(identity, expected)

def test_matrix_inverse_error():
    # Singular matrix
    singular_matrix = string_to_matrix("1 2; 2 4")
    with pytest.raises(ValueError):
        compute_inverse(singular_matrix)

# Test eigenvalues and eigenvectors
def test_eigenvalues_eigenvectors(eigen_matrix):
    eigenvalues, eigenvectors = compute_eigenvalues_eigenvectors(eigen_matrix)
    
    # Test eigenvalue equation: Av = λv
    for i in range(len(eigenvalues)):
        v = eigenvectors[:, i:i+1]
        Av = multiply_matrices(eigen_matrix, v)
        lambda_v = eigenvalues[i] * v
        np.testing.assert_array_almost_equal(Av, lambda_v)

# Test matrix input validation
def test_string_to_matrix_valid():
    matrix_str = "1 2; 3 4"
    result = string_to_matrix(matrix_str)
    expected = np.array([[1, 2], [3, 4]])
    np.testing.assert_array_equal(result, expected)

def test_string_to_matrix_invalid():
    invalid_inputs = [
        "1 2 3; 4 5",  # Uneven rows
        "a b; c d",    # Non-numeric
        "1,2;3,4",     # Wrong separator
        "",            # Empty string
    ]
    for invalid_input in invalid_inputs:
        with pytest.raises(ValueError):
            string_to_matrix(invalid_input) 
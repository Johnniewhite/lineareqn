import numpy as np

def add_matrices(matrix1, matrix2):
    """Add two matrices"""
    try:
        return np.add(matrix1, matrix2)
    except ValueError:
        raise ValueError("Matrices must have the same dimensions for addition")

def subtract_matrices(matrix1, matrix2):
    """Subtract two matrices"""
    try:
        return np.subtract(matrix1, matrix2)
    except ValueError:
        raise ValueError("Matrices must have the same dimensions for subtraction")

def multiply_matrices(matrix1, matrix2):
    """Multiply two matrices"""
    try:
        return np.matmul(matrix1, matrix2)
    except ValueError:
        raise ValueError("Number of columns in first matrix must equal number of rows in second matrix")

def compute_inverse(matrix):
    """Compute the inverse of a matrix"""
    try:
        return np.linalg.inv(matrix)
    except np.linalg.LinAlgError:
        raise ValueError("Matrix is not invertible")

def compute_eigenvalues_eigenvectors(matrix):
    """Compute eigenvalues and eigenvectors of a matrix"""
    try:
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        return eigenvalues, eigenvectors
    except np.linalg.LinAlgError:
        raise ValueError("Could not compute eigenvalues and eigenvectors") 
import numpy as np

def string_to_matrix(matrix_str):
    """Convert a string representation of a matrix to a numpy array"""
    if not matrix_str.strip():
        raise ValueError("Matrix string cannot be empty")
        
    try:
        # Split the string into rows
        rows = matrix_str.strip().split(';')
        # Convert each row into a list of numbers
        matrix = []
        expected_length = None
        
        for row in rows:
            # Convert row to list of numbers
            try:
                numbers = [float(x) for x in row.strip().split()]
            except ValueError:
                raise ValueError("Matrix elements must be numeric values")
                
            # Check if all rows have the same length
            if expected_length is None:
                expected_length = len(numbers)
            elif len(numbers) != expected_length:
                raise ValueError("All rows must have the same length")
                
            matrix.append(numbers)
            
        # Convert to numpy array
        return np.array(matrix)
        
    except Exception as e:
        if isinstance(e, ValueError):
            raise e
        raise ValueError("Invalid matrix format. Please use space-separated numbers and semicolons for new rows")

def validate_matrix(matrix):
    """Validate if the input is a valid matrix"""
    if not isinstance(matrix, np.ndarray):
        raise ValueError("Input must be a numpy array")
    if matrix.size == 0:
        raise ValueError("Matrix cannot be empty")
    if len(matrix.shape) != 2:
        raise ValueError("Input must be a 2D matrix") 
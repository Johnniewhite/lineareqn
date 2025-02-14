
# Matrix Calculator Web Application

A powerful web-based matrix calculator that supports various matrix operations, including addition, subtraction, multiplication, inverse calculation, and eigenvalue/eigenvector computation. The application provides step-by-step calculations and visual representation of matrices.

## Features

- Matrix Operations:
  - Addition (A + B)
  - Subtraction (A - B)
  - Multiplication (A × B)
  - Inverse (A⁻¹)
  - Eigenvalues and Eigenvectors

- Interactive Interface:
  - Dynamically resizable matrices
  - Real-time validation
  - Step-by-step calculation display
  - Support for complex numbers
  - Beautiful matrix formatting

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/matrix-calculator.git
cd matrix-calculator
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:

```bash
python app.py
```

2. Open your web browser and navigate to:

```
http://localhost:5000
```

## Usage Guide

### Basic Operations

1. Select an operation from the dropdown menu
2. Enter values in the matrix input fields
3. Use +Row/-Row and +Col/-Col buttons to adjust matrix dimensions
4. Click "Calculate" to see the result

### Sample Calculations

#### 1. Matrix Addition

Input:

```
Matrix A = [1 2]  Matrix B = [5 6]
           [3 4]             [7 8]

Result = [6  8]
         [10 12]
```

#### 2. Matrix Multiplication

Input:

```
Matrix A = [1 2]  Matrix B = [5 6]
           [3 4]             [7 8]

Result = [19 22]
         [43 50]
```

#### 3. Eigenvalues and Eigenvectors

Input:

```
Matrix = [3  -2]
         [1   4]

Eigenvalues: λ₁ = 5, λ₂ = 2
Eigenvectors: v₁ = [2]  v₂ = [-1]
                   [1]        [1]
```

### Matrix Input Rules

- Enter numerical values only
- Use decimal points for non-integer values
- Matrix dimensions must be compatible for the selected operation
- For eigenvalues/inverse, matrix must be square

## Technical Details

- Frontend: HTML5, CSS3, JavaScript (jQuery)
- Backend: Python (Flask)
- Mathematical Computations: NumPy
- Rendering: MathJax for mathematical notation

## Error Handling

The application validates:

- Matrix dimensions
- Input types
- Operation compatibility
- Singular matrices for inverse operations

Common error messages:

- "Matrix must be square for eigenvalues/inverse calculation"
- "Number of columns in first matrix must equal number of rows in second matrix for multiplication"
- "Matrices must have the same dimensions for addition/subtraction"

## Testing

Run the test suite:

```bash
pytest test_matrix_operations.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NumPy for matrix operations
- Flask for web framework
- MathJax for mathematical rendering
- Bootstrap for UI components

from flask import Flask, render_template, request, jsonify
from matrix_operations import (
    add_matrices,
    subtract_matrices,
    multiply_matrices,
    compute_inverse,
    compute_eigenvalues_eigenvectors
)
from matrix_utils import string_to_matrix
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        operation = data['operation']
        steps = []
        
        if operation in ['addition', 'subtraction', 'multiplication']:
            matrix1 = np.array(data['matrix1'])
            matrix2 = np.array(data['matrix2'])
            
            steps.append({
                'explanation': 'Input matrices:',
                'latex': f'A = {matrix_to_latex(matrix1)}, B = {matrix_to_latex(matrix2)}'
            })
            
            if operation == 'addition':
                result = add_matrices(matrix1, matrix2)
                steps.append({
                    'explanation': 'Add corresponding elements:',
                    'latex': f'A + B = {matrix_to_latex(result)}'
                })
            elif operation == 'subtraction':
                result = subtract_matrices(matrix1, matrix2)
                steps.append({
                    'explanation': 'Subtract corresponding elements:',
                    'latex': f'A - B = {matrix_to_latex(result)}'
                })
            else:  # multiplication
                result = multiply_matrices(matrix1, matrix2)
                steps.append({
                    'explanation': 'Multiply rows by columns:',
                    'latex': f'A \\times B = {matrix_to_latex(result)}'
                })
                
            return jsonify({
                'success': True,
                'result': result.tolist(),
                'steps': steps,
                'message': 'Calculation successful'
            })
            
        elif operation == 'inverse':
            matrix = np.array(data['matrix1'])
            steps.append({
                'explanation': 'Input matrix:',
                'latex': f'A = {matrix_to_latex(matrix)}'
            })
            
            result = compute_inverse(matrix)
            steps.append({
                'explanation': 'Compute inverse:',
                'latex': f'A^{{-1}} = {matrix_to_latex(result)}'
            })
            
            # Verification step
            verification = multiply_matrices(matrix, result)
            steps.append({
                'explanation': 'Verify: A × A⁻¹ should equal identity matrix',
                'latex': f'A \\times A^{{-1}} = {matrix_to_latex(verification)}'
            })
            
            return jsonify({
                'success': True,
                'result': result.tolist(),
                'steps': steps,
                'message': 'Inverse calculated successfully'
            })
            
        elif operation == 'eigen':
            # Convert input to float array first
            matrix_data = [[float(cell) for cell in row] for row in data['matrix1']]
            matrix = np.array(matrix_data)
            
            steps.append({
                'explanation': 'Input matrix:',
                'latex': f'A = {matrix_to_latex(matrix)}'
            })
            
            eigenvalues, eigenvectors = compute_eigenvalues_eigenvectors(matrix)
            
            steps.append({
                'explanation': 'Characteristic equation:',
                'latex': f'det(A - λI) = 0'
            })
            
            # Convert complex eigenvalues and eigenvectors to serializable format
            eigenvalues_serial = [complex_to_dict(ev) for ev in eigenvalues]
            eigenvectors_serial = [[complex_to_dict(x) for x in v] for v in eigenvectors.T]
            
            for i, (eigenvalue, eigenvector) in enumerate(zip(eigenvalues, eigenvectors.T)):
                steps.append({
                    'explanation': f'Eigenvalue {i+1} and its eigenvector:',
                    'latex': f'λ_{{{i+1}}} = {complex_to_latex(eigenvalue)}, v_{{{i+1}}} = {matrix_to_latex(eigenvector.reshape(-1,1))}'
                })
                
                # Verification step
                Av = multiply_matrices(matrix, eigenvector.reshape(-1,1))
                lambda_v = eigenvalue * eigenvector.reshape(-1,1)
                steps.append({
                    'explanation': f'Verify: Av = λv for eigenpair {i+1}:',
                    'latex': f'Av_{{{i+1}}} = {matrix_to_latex(Av)} = {matrix_to_latex(lambda_v)} = λ_{{{i+1}}}v_{{{i+1}}}'
                })
            
            return jsonify({
                'success': True,
                'eigenvalues': eigenvalues_serial,
                'eigenvectors': eigenvectors_serial,
                'steps': steps,
                'message': 'Eigenvalues and eigenvectors calculated successfully'
            })
            
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error during calculation: {str(e)}'
        })

def complex_to_dict(z):
    """Convert complex number to dictionary representation"""
    if isinstance(z, (int, float)):
        return {'real': float(z), 'imag': 0.0}
    return {'real': float(z.real), 'imag': float(z.imag)}

def matrix_to_latex(matrix):
    """Convert numpy array to LaTeX matrix notation"""
    rows = []
    for row in matrix:
        row_str = []
        for x in row:
            if isinstance(x, complex):
                if abs(x.imag) < 1e-10:  # Practically real
                    row_str.append(f'{x.real:.4f}')
                else:
                    row_str.append(f'{x.real:.2f}{x.imag:+.2f}i')
            else:
                row_str.append(f'{float(x):.4f}')
        rows.append(' & '.join(row_str))
    return '\\begin{bmatrix}' + ' \\\\ '.join(rows) + '\\end{bmatrix}'

def complex_to_latex(z):
    """Convert complex number to LaTeX string"""
    if abs(z.imag) < 1e-10:  # Practically real
        return f'{z.real:.4f}'
    elif abs(z.real) < 1e-10:  # Purely imaginary
        if abs(z.imag - 1) < 1e-10:
            return 'i'
        elif abs(z.imag + 1) < 1e-10:
            return '-i'
        return f'{z.imag:.4f}i'
    else:
        sign = '+' if z.imag >= 0 else '-'
        imag_part = abs(z.imag)
        if abs(imag_part - 1) < 1e-10:
            return f'{z.real:.4f}{sign}i'
        return f'{z.real:.4f}{sign}{imag_part:.4f}i'

if __name__ == '__main__':
    app.run(debug=True) 
$(document).ready(function() {
    // Initialize matrices
    initializeMatrix('matrix1', 3, 3);
    initializeMatrix('matrix2', 3, 3);
    
    const form = $('#matrixForm');
    const operation = $('#operation');
    const matrix1Container = $('#matrix1Container');
    const matrix2Container = $('#matrix2Container');
    const resultContent = $('#resultContent');
    const stepsContent = $('#stepsContent');
    const errorDiv = $('#error');

    // Show/hide second matrix based on operation
    operation.change(function() {
        const op = $(this).val();
        if (op === 'inverse' || op === 'eigen') {
            matrix2Container.hide();
            matrix1Container.find('label').text('Matrix:');
        } else {
            matrix2Container.show();
            matrix1Container.find('label').text('Matrix A:');
        }
    });

    // Add this function to validate matrix dimensions
    function validateMatrixDimensions() {
        const op = operation.val();
        const matrix1 = getMatrixValues('matrix1');
        const matrix2 = getMatrixValues('matrix2');
        
        if (op === 'eigen' || op === 'inverse') {
            // Check if matrix is square
            if (matrix1.length !== matrix1[0].length) {
                errorDiv.text('Matrix must be square for eigenvalues/inverse calculation.').show();
                return false;
            }
        } else if (op === 'multiplication') {
            // Check if matrices can be multiplied
            if (matrix1[0].length !== matrix2.length) {
                errorDiv.text('Number of columns in first matrix must equal number of rows in second matrix for multiplication.').show();
                return false;
            }
        } else if (op === 'addition' || op === 'subtraction') {
            // Check if matrices have same dimensions
            if (matrix1.length !== matrix2.length || matrix1[0].length !== matrix2[0].length) {
                errorDiv.text('Matrices must have the same dimensions for addition/subtraction.').show();
                return false;
            }
        }
        return true;
    }

    // Handle form submission
    form.submit(function(e) {
        e.preventDefault();
        const submitBtn = $(this).find('button[type="submit"]');
        submitBtn.html('<i class="fas fa-spinner fa-spin"></i> Calculating...').prop('disabled', true);
        errorDiv.hide();
        resultContent.empty();
        stepsContent.empty();

        if (!validateMatrixDimensions()) {
            submitBtn.html('Calculate').prop('disabled', false);
            return;
        }

        const matrix1 = getMatrixValues('matrix1');
        const matrix2 = getMatrixValues('matrix2');
        const op = operation.val();

        $.ajax({
            url: '/calculate',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                operation: op,
                matrix1: matrix1,
                matrix2: matrix2
            }),
            success: function(response) {
                if (response.success) {
                    displaySteps(response.steps);
                    if (response.eigenvalues) {
                        // Display eigenvalues and eigenvectors
                        displayEigenResults(response.eigenvalues, response.eigenvectors);
                    } else {
                        // Display matrix result
                        displayMatrix(response.result);
                    }
                } else {
                    errorDiv.text(response.message).show();
                }
                submitBtn.html('Calculate').prop('disabled', false);
            },
            error: function() {
                errorDiv.text('An error occurred during calculation.').show();
                submitBtn.html('Calculate').prop('disabled', false);
            }
        });
    });

    function initializeMatrix(id, rows, cols) {
        const grid = $(`#${id}Grid`);
        grid.css('grid-template-columns', `repeat(${cols}, 1fr)`);
        
        for (let i = 0; i < rows; i++) {
            for (let j = 0; j < cols; j++) {
                const input = $('<input>')
                    .addClass('matrix-cell')
                    .attr('type', 'number')
                    .attr('step', 'any')
                    .attr('data-row', i)
                    .attr('data-col', j);
                grid.append(input);
            }
        }
    }

    function adjustSize(matrixId, rowChange, colChange) {
        const grid = $(`#${matrixId}Grid`);
        const currentRows = grid.children('input').length / parseInt(grid.css('grid-template-columns').split(' ').length);
        const currentCols = parseInt(grid.css('grid-template-columns').split(' ').length);
        
        const newRows = Math.max(1, currentRows + rowChange);
        const newCols = Math.max(1, currentCols + colChange);
        
        // Store current values
        const currentValues = {};
        grid.children('input').each(function() {
            const row = $(this).attr('data-row');
            const col = $(this).attr('data-col');
            const value = $(this).val();
            currentValues[`${row}-${col}`] = value;
        });
        
        // Clear grid
        grid.empty();
        
        // Update grid template
        grid.css('grid-template-columns', `repeat(${newCols}, 1fr)`);
        
        // Recreate inputs
        for (let i = 0; i < newRows; i++) {
            for (let j = 0; j < newCols; j++) {
                const input = $('<input>')
                    .addClass('matrix-cell')
                    .attr('type', 'number')
                    .attr('step', 'any')
                    .attr('data-row', i)
                    .attr('data-col', j);
                
                // Restore value if it existed
                if (currentValues[`${i}-${j}`]) {
                    input.val(currentValues[`${i}-${j}`]);
                }
                
                grid.append(input);
            }
        }
    }

    function getMatrixValues(matrixId) {
        const grid = $(`#${matrixId}Grid`);
        const rows = grid.children().length / grid.css('grid-template-columns').split(' ').length;
        const cols = grid.css('grid-template-columns').split(' ').length;
        const matrix = [];
        
        for (let i = 0; i < rows; i++) {
            const row = [];
            for (let j = 0; j < cols; j++) {
                const value = parseFloat(grid.find(`input[data-row="${i}"][data-col="${j}"]`).val()) || 0;
                row.push(value);
            }
            matrix.push(row);
        }
        return matrix;
    }

    function displaySteps(steps) {
        stepsContent.empty();
        steps.forEach((step, index) => {
            const stepDiv = $('<div>')
                .addClass('step animate__animated animate__fadeIn')
                .css('animation-delay', `${index * 0.1}s`);
            stepDiv.html(`
                <strong class="text-primary">Step ${index + 1}:</strong>
                <div class="step-content mt-2">
                    <p class="mb-2">${step.explanation}</p>
                    ${step.latex ? `<div class="math-content">\\[${step.latex}\\]</div>` : ''}
                </div>
            `);
            stepsContent.append(stepDiv);
        });
        MathJax.typeset();
    }

    function displayMatrix(matrix) {
        let html = '<div class="matrix-bracket">';
        html += '<table class="matrix-table">';
        for (let row of matrix) {
            html += '<tr>';
            for (let cell of row) {
                html += `<td class="matrix-cell">${Number(cell).toFixed(4)}</td>`;
            }
            html += '</tr>';
        }
        html += '</table></div>';
        resultContent.html(html);
    }

    function displayEigenResults(eigenvalues, eigenvectors) {
        let html = '<h4>Eigenvalues:</h4>';
        html += '<div class="matrix-bracket">';
        html += '<table class="matrix-table">';
        for (let i = 0; i < eigenvalues.length; i++) {
            const ev = eigenvalues[i];
            let valueStr = formatComplex(ev);
            html += `<tr><td class="matrix-cell">λ${i+1} = ${valueStr}</td></tr>`;
        }
        html += '</table></div>';

        html += '<h4>Eigenvectors:</h4>';
        html += '<div class="matrix-bracket">';
        html += '<table class="matrix-table">';
        for (let i = 0; i < eigenvectors.length; i++) {
            html += '<tr>';
            for (let j = 0; j < eigenvectors[i].length; j++) {
                const value = eigenvectors[i][j];
                let valueStr = formatComplex(value);
                html += `<td class="matrix-cell">${valueStr}</td>`;
            }
            html += '</tr>';
        }
        html += '</table></div>';

        resultContent.html(html);
    }

    function formatComplex(value) {
        if (Math.abs(value.imag) < 1e-10) {
            return Number(value.real).toFixed(4);
        } else if (Math.abs(value.real) < 1e-10) {
            return `${Number(value.imag).toFixed(4)}i`;
        } else {
            const sign = value.imag >= 0 ? '+' : '';
            return `${Number(value.real).toFixed(4)}${sign}${Number(value.imag).toFixed(4)}i`;
        }
    }

    // Add this function for smooth animations
    function animateCSS(element, animation) {
        return new Promise((resolve) => {
            const node = document.querySelector(element);
            node.classList.add('animate__animated', `animate__${animation}`);
            
            function handleAnimationEnd(event) {
                event.stopPropagation();
                node.classList.remove('animate__animated', `animate__${animation}`);
                resolve('Animation ended');
            }
            
            node.addEventListener('animationend', handleAnimationEnd, {once: true});
        });
    }
}); 
/**
 * BridgeCanvas - Main JavaScript
 * Handles dynamic UI interactions and form submissions
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // File upload handling
    const fileInput = document.getElementById('file-upload');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name || 'No file selected';
            document.getElementById('file-name').textContent = fileName;
        });
    }

    // Form submission handling
    const bridgeForm = document.getElementById('bridge-design-form');
    if (bridgeForm) {
        bridgeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show loading state
            const submitButton = bridgeForm.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.innerHTML;
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
            
            // Submit form via AJAX if needed
            const formData = new FormData(bridgeForm);
            
            // Example AJAX call (uncomment and implement as needed)
            /*
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                // Handle success
                showAlert('Design generated successfully!', 'success');
                // Update UI with results
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('An error occurred while processing your request.', 'error');
            })
            .finally(() => {
                submitButton.disabled = false;
                submitButton.innerHTML = originalButtonText;
            });
            */
            
            // For now, just reset the button after a delay
            setTimeout(() => {
                submitButton.disabled = false;
                submitButton.innerHTML = originalButtonText;
                showAlert('Design generated successfully! (Demo)', 'success');
            }, 1500);
        });
    }
});

/**
 * Show a notification/alert to the user
 * @param {string} message - The message to display
 * @param {string} type - The type of alert (success, error, warning, info)
 */
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.getElementById('alerts-container') || document.body;
    container.prepend(alertDiv);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = bootstrap.Alert.getOrCreateInstance(alertDiv);
        alert.close();
    }, 5000);
}

/**
 * Toggle element visibility
 * @param {string} elementId - The ID of the element to toggle
 */
function toggleElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.toggle('d-none');
    }
}

// Add any additional utility functions here

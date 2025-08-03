// Bridge Design CAD Application JavaScript

document.addEventListener('DOMContentLoaded', function() {
    
    // File upload validation
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                validateFileUpload(file);
            }
        });
    }
    
    // Form submission handling
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            handleFormSubmission(e);
        });
    }
    
    // Initialize tooltips if Bootstrap is loaded
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (alert && alert.parentNode) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });
});

/**
 * Validate file upload before submission
 * @param {File} file - The selected file
 */
function validateFileUpload(file) {
    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', // .xlsx
        'application/vnd.ms-excel' // .xls
    ];
    
    // Check file size
    if (file.size > maxSize) {
        showAlert('File size exceeds 16MB limit. Please select a smaller file.', 'danger');
        clearFileInput();
        return false;
    }
    
    // Check file type
    if (!allowedTypes.includes(file.type)) {
        showAlert('Invalid file type. Please select an Excel file (.xlsx or .xls).', 'danger');
        clearFileInput();
        return false;
    }
    
    // Show file info
    showFileInfo(file);
    return true;
}

/**
 * Handle form submission with progress indication
 * @param {Event} e - Form submission event
 */
function handleFormSubmission(e) {
    const fileInput = document.getElementById('file');
    const uploadBtn = document.getElementById('uploadBtn');
    const uploadProgress = document.getElementById('uploadProgress');
    
    if (!fileInput.files.length) {
        e.preventDefault();
        showAlert('Please select a file to upload.', 'warning');
        return false;
    }
    
    // Validate file one more time
    if (!validateFileUpload(fileInput.files[0])) {
        e.preventDefault();
        return false;
    }
    
    // Show progress
    if (uploadProgress) {
        uploadProgress.style.display = 'block';
    }
    
    if (uploadBtn) {
        uploadBtn.disabled = true;
        uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
    }
    
    // Re-enable button after timeout (fallback)
    setTimeout(function() {
        if (uploadBtn) {
            uploadBtn.disabled = false;
            uploadBtn.innerHTML = '<i class="fas fa-cloud-upload-alt me-2"></i>Upload and Process';
        }
        if (uploadProgress) {
            uploadProgress.style.display = 'none';
        }
    }, 30000); // 30 seconds timeout
}

/**
 * Clear file input
 */
function clearFileInput() {
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.value = '';
    }
    hideFileInfo();
}

/**
 * Show file information
 * @param {File} file - The selected file
 */
function showFileInfo(file) {
    const fileSize = (file.size / 1024 / 1024).toFixed(2);
    const fileInfo = document.getElementById('fileInfo');
    
    if (fileInfo) {
        fileInfo.innerHTML = `
            <div class="alert alert-info">
                <i class="fas fa-file-excel me-2"></i>
                <strong>${file.name}</strong> (${fileSize} MB)
            </div>
        `;
        fileInfo.style.display = 'block';
    }
}

/**
 * Hide file information
 */
function hideFileInfo() {
    const fileInfo = document.getElementById('fileInfo');
    if (fileInfo) {
        fileInfo.style.display = 'none';
    }
}

/**
 * Show alert message
 * @param {string} message - Alert message
 * @param {string} type - Alert type (success, danger, warning, info)
 */
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer') || document.querySelector('.container');
    
    if (alertContainer) {
        const alertElement = document.createElement('div');
        alertElement.className = `alert alert-${type} alert-dismissible fade show`;
        alertElement.innerHTML = `
            <i class="fas fa-${getAlertIcon(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insert at the beginning of container
        alertContainer.insertBefore(alertElement, alertContainer.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(function() {
            if (alertElement && alertElement.parentNode) {
                const bsAlert = new bootstrap.Alert(alertElement);
                bsAlert.close();
            }
        }, 5000);
    }
}

/**
 * Get appropriate icon for alert type
 * @param {string} type - Alert type
 * @returns {string} Icon class name
 */
function getAlertIcon(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-triangle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

/**
 * Download file with progress indication
 * @param {string} filename - Name of file to download
 */
function downloadFile(filename) {
    const downloadBtn = document.querySelector(`[data-filename="${filename}"]`);
    
    if (downloadBtn) {
        const originalContent = downloadBtn.innerHTML;
        downloadBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Downloading...';
        downloadBtn.disabled = true;
        
        // Reset button after download starts
        setTimeout(function() {
            downloadBtn.innerHTML = originalContent;
            downloadBtn.disabled = false;
        }, 2000);
    }
}

/**
 * Toggle parameter details
 */
function toggleParameterDetails() {
    const detailsContainer = document.getElementById('parameterDetails');
    const toggleBtn = document.getElementById('toggleDetailsBtn');
    
    if (detailsContainer && toggleBtn) {
        if (detailsContainer.style.display === 'none') {
            detailsContainer.style.display = 'block';
            toggleBtn.innerHTML = '<i class="fas fa-chevron-up me-2"></i>Hide Details';
        } else {
            detailsContainer.style.display = 'none';
            toggleBtn.innerHTML = '<i class="fas fa-chevron-down me-2"></i>Show Details';
        }
    }
}

/**
 * Copy parameter value to clipboard
 * @param {string} value - Value to copy
 * @param {Element} button - Button element that triggered the action
 */
function copyToClipboard(value, button) {
    navigator.clipboard.writeText(value).then(function() {
        const originalContent = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check text-success"></i>';
        
        setTimeout(function() {
            button.innerHTML = originalContent;
        }, 1500);
    }).catch(function(err) {
        console.error('Could not copy text: ', err);
        showAlert('Failed to copy to clipboard', 'danger');
    });
}

/**
 * Format number for display
 * @param {number} value - Number to format
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted number
 */
function formatNumber(value, decimals = 2) {
    if (typeof value !== 'number') {
        return value;
    }
    return value.toFixed(decimals);
}

/**
 * Validate parameter values in real-time
 * @param {Object} parameters - Parameter object to validate
 */
function validateParameters(parameters) {
    const validationRules = {
        'scale1': { min: 1, max: 10000, type: 'number' },
        'scale2': { min: 1, max: 10000, type: 'number' },
        'skew': { min: -45, max: 45, type: 'number' },
        'nspan': { min: 1, max: 20, type: 'integer' },
        'lbridge': { min: 1, max: 1000, type: 'number' },
        'ccbr': { min: 1, max: 50, type: 'number' }
    };
    
    const errors = [];
    
    for (const [param, rules] of Object.entries(validationRules)) {
        if (parameters.hasOwnProperty(param)) {
            const value = parameters[param];
            
            if (rules.type === 'number' && (isNaN(value) || !isFinite(value))) {
                errors.push(`${param}: Must be a valid number`);
                continue;
            }
            
            if (rules.type === 'integer' && (!Number.isInteger(value) || value !== Math.floor(value))) {
                errors.push(`${param}: Must be an integer`);
                continue;
            }
            
            if (rules.min !== undefined && value < rules.min) {
                errors.push(`${param}: Must be at least ${rules.min}`);
            }
            
            if (rules.max !== undefined && value > rules.max) {
                errors.push(`${param}: Must be at most ${rules.max}`);
            }
        }
    }
    
    return {
        valid: errors.length === 0,
        errors: errors
    };
}

// Export functions for use in other scripts
window.BridgeApp = {
    validateFileUpload,
    showAlert,
    downloadFile,
    copyToClipboard,
    formatNumber,
    validateParameters
};

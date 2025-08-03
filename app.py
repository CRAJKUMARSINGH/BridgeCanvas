import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename
from bridge_processor import BridgeProcessor
import traceback
from smart_title import smart_recenter_title
smart_recenter_title(drawing.elements)
# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///bridge_designs.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# File upload configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['GENERATED_FOLDER'] = 'generated'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# Ensure upload and generated directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)

# initialize the app with the extension
db.init_app(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Get project name from form
            project_name = request.form.get('project_name', '').strip()
            if not project_name:
                project_name = "BRIDGE PROJECT"  # Default name
            
            # Process the bridge design
            processor = BridgeProcessor()
            try:
                results = processor.process_excel_file(filepath, project_name=project_name)
                
                # Store results in session or database for retrieval
                # For simplicity, we'll pass directly to results page
                return render_template('results.html', 
                                     results=results, 
                                     filename=filename)
                
            except Exception as e:
                app.logger.error(f"Processing error: {str(e)}")
                app.logger.error(traceback.format_exc())
                flash(f'Error processing file: {str(e)}', 'error')
                return redirect(url_for('index'))
        else:
            flash('Invalid file type. Please upload an Excel file (.xlsx or .xls)', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        app.logger.error(f"Upload error: {str(e)}")
        flash('An error occurred during file upload', 'error')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['GENERATED_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            flash('File not found', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        app.logger.error(f"Download error: {str(e)}")
        flash('Error downloading file', 'error')
        return redirect(url_for('index'))

@app.route('/validate', methods=['POST'])
def validate_parameters():
    """AJAX endpoint for parameter validation"""
    try:
        data = request.get_json()
        processor = BridgeProcessor()
        validation_result = processor.validate_parameters(data)
        return jsonify(validation_result)
    except Exception as e:
        return jsonify({'valid': False, 'errors': [str(e)]})

@app.errorhandler(413)
def too_large(e):
    flash('File is too large. Maximum size is 16MB.', 'error')
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(e):
    app.logger.error(f"Internal server error: {str(e)}")
    flash('An internal error occurred. Please try again.', 'error')
    return redirect(url_for('index'))

with app.app_context():
    import models
    db.create_all()

if __name__ == '__main__':
    import traceback
    import sys
    
    try:
        port = int(os.getenv("PORT", 5000))
        app.logger.info(f"Starting BridgeCanvas server on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    except Exception as e:
        app.logger.error(f"Failed to start server: {str(e)}")
        app.logger.error(traceback.format_exc())
        sys.exit(1)

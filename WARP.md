# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

BridgeCanvas is a hybrid professional bridge design and analysis application that combines multiple technologies:
- **Frontend**: Flask web application + Streamlit data science interface
- **Backend**: Python with ezdxf for DXF generation, pandas for Excel processing
- **Database**: SQLAlchemy with PostgreSQL/SQLite support
- **Output**: Professional AutoCAD-compatible DXF drawings, SVG previews, PDF reports

The application processes bridge parameters from Excel files and generates detailed engineering drawings with elevation views, plan views, cross-sections, and comprehensive analysis reports.

## Development Commands

### Python Flask Application
```powershell
# Main Flask application
python app.py
# Access at: http://localhost:5000

# Windows batch launcher
.\run_bridge_app.bat

# Install dependencies
pip install -r requirements.txt

# Database setup (if needed)
python -c "from app import db; db.create_all()"
```

### Streamlit Application
```powershell
# Streamlit interface (alternative UI)
cd streamlit_app
streamlit run streamlit_app.py
# Access at: http://localhost:8501

# Windows batch launcher
.\run_streamlit_app.bat

# Install Streamlit dependencies
pip install streamlit
cd streamlit_app
pip install -r requirements.txt
```

### Testing and Development
```powershell
# Test bridge processor logic
python test_lisp_logic.py

# Test bridge processor with batch file
.\test_bridge_processor.bat

# Run with specific Excel input
python bridge_processor.py input.xlsx
```

### Deployment
```powershell
# Vercel deployment (Flask)
vercel deploy

# Check deployment configuration
Get-Content vercel.json

# Environment setup
# DATABASE_URL=postgresql://user:pass@host:port/db
# SESSION_SECRET=your-secret-key
```

## Architecture Overview

### Core Components
1. **Bridge Processor** (`bridge_processor.py`): Core engineering calculation engine that converts LISP-based algorithms to Python
2. **Flask Application** (`app.py`): Web interface with file upload, processing, and download capabilities  
3. **Streamlit Interface** (`streamlit_app/streamlit_app.py`): Interactive data science interface for rapid prototyping
4. **Smart Title System** (`smart_title.py`): Intelligent text positioning for DXF drawings

### Data Flow
```
Excel Input → Parameter Validation → Bridge Calculations → DXF Generation → Web Display/Download
     ↓              ↓                      ↓                   ↓              ↓
- Variable list  - Required vars      - Geometric         - AutoCAD       - File serving
- Cross-section  - Value ranges       - Pier/Abutment     - Dimensions    - SVG preview  
- Bid summary    - Format checks      - Foundation        - Layer mgmt    - PDF reports
```

### Key Engineering Features
- **Multi-span Bridge Design**: Supports variable span configurations with pier placement
- **Abutment Geometry**: Complex abutment shapes with batter calculations and foundation details
- **Professional DXF Output**: AutoCAD-compatible drawings with proper dimensioning and layer management
- **Cross-section Plotting**: River bed profiles with chainage annotations and terrain representation
- **Skew Bridge Support**: Handles skewed bridges with proper geometric transformations
- **LISP-to-Python Conversion**: Core algorithms converted from AutoCAD LISP to modern Python

### File Structure Patterns
- `/`: Main Flask application files
- `/streamlit_app/`: Alternative Streamlit interface 
- `/templates/`: HTML templates for web interface
- `/static/`: CSS, JS, and image assets
- `/uploads/`: User-uploaded Excel files
- `/generated/`: Output DXF and analysis files
- `/attached_assets/`: LISP source code and reference materials

## Development Notes

### Excel Input Format
The application expects Excel files with specific structure:
- **Sheet1**: Variables (Variable, Value, Description columns)
- **Sheet2**: Cross-section profile (Chainage, RL columns)  
- **Sheet3**: Bid summary (optional)

Required variables include: `SCALE1`, `SCALE2`, `SKEW`, `DATUM`, `TOPRL`, `ABTL`, `NSPAN`, `LBRIDGE`, `CAPW`, `PIERTW`, `FUTW`, `FUTD`, etc.

### DXF Generation Process
The bridge processor creates professional drawings through:
1. **Coordinate transformation**: Converting real-world coordinates to drawing scale
2. **Layer management**: Organizing elements by type (BRIDGE_DECK, PIER, ABUTMENT, etc.)
3. **Dimensioning**: Adding professional dimensions with proper styles
4. **Text placement**: Smart title block positioning and annotation

### LISP Legacy Integration
This application is based on extensive AutoCAD LISP code found in `attached_assets/`:
- Original algorithms for pier placement, abutment geometry, and foundation design
- Complex skew calculations and coordinate transformations
- Professional drawing standards and dimensioning practices

### Common Development Tasks

#### Adding New Bridge Features
1. Identify required parameters in Excel format
2. Add validation logic in `validate_dataframe()`
3. Implement calculation methods following existing patterns
4. Add DXF generation logic in `generate_dxf()`
5. Test with sample Excel files

#### Debugging DXF Output  
- Check coordinate transformation functions (`hpos`, `vpos`, `h2pos`, `v2pos`)
- Verify layer assignments and drawing element properties
- Use `smart_recenter_title()` for text positioning issues
- Test with AutoCAD or compatible DXF viewer

#### Database Integration
- Models defined in `models.py` for design storage
- Flask-SQLAlchemy for ORM operations
- Support for PostgreSQL (production) and SQLite (development)

#### Performance Optimization
- Large bridges may require optimization of drawing generation
- Consider chunked processing for complex multi-span designs
- Monitor memory usage during DXF creation

## Deployment Configuration

### Environment Variables
```bash
# Production
DATABASE_URL=postgresql://user:pass@host:port/db
SESSION_SECRET=your-production-secret-key
FLASK_ENV=production

# Development  
FLASK_ENV=development
DATABASE_URL=sqlite:///bridge_designs.db
```

### File Upload Limits
- Maximum file size: 16MB
- Allowed extensions: .xlsx, .xls
- Upload directory: `uploads/`
- Generated files: `generated/`

### Security Considerations
- File validation for uploads
- Session management for user data
- Input sanitization for Excel parameters
- Rate limiting for API endpoints

This application represents a sophisticated engineering tool that bridges traditional AutoCAD LISP workflows with modern web technologies, providing professional bridge design capabilities through an accessible interface.

# Bridge Design CAD - User Manual

## Table of Contents
1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Excel Template](#excel-template)
4. [Using the Application](#using-the-application)
5. [Parameter Reference](#parameter-reference)
6. [Output Files](#output-files)
7. [Troubleshooting](#troubleshooting)
8. [Technical Support](#technical-support)

## Overview

Bridge Design CAD is a professional web-based application that converts bridge engineering parameters from Excel files into comprehensive technical CAD drawings. The system generates detailed DXF files suitable for AutoCAD and other professional CAD software, complete with:

- **Elevation Views**: Side profile views showing bridge superstructure, piers, and abutments
- **Plan Views**: Top-down structural layout with footings, pier layouts, and deck outline
- **Professional Formatting**: Industry-standard borders, title blocks, and technical annotations
- **Custom Project Information**: User-defined project names and drawing details

## Getting Started

### System Requirements
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Excel file with properly formatted bridge parameters
- No software installation required - runs entirely in your browser

### Quick Start
1. Open the Bridge Design CAD application in your web browser
2. Enter your project name in the "Project Name" field
3. Upload your Excel file containing bridge parameters
4. Click "Upload and Process" to generate your CAD drawings
5. Download the generated DXF file for use in CAD software

## Excel Template

### Downloading the Template
1. Click the "Download Excel Template" button on the homepage
2. Save the `bridge_design_template.xlsx` file to your computer
3. Open the template in Microsoft Excel or compatible software

### Template Structure
The Excel template contains 54 bridge engineering parameters organized in three columns:
- **Column A (Value)**: Enter your numerical values here
- **Column B (Variable)**: Parameter names (do not modify)
- **Column C (Description)**: Detailed explanations of each parameter

### Important Notes
- Only modify values in Column A
- All values must be numeric (no text or formulas)
- Do not add, remove, or reorder rows
- Units are typically in meters unless specified otherwise

## Using the Application

### Step 1: Project Information
Enter a descriptive name for your bridge project. This name will appear in:
- Drawing title blocks
- Main drawing titles
- Generated file names

**Examples of good project names:**
- "HIGHWAY 401 OVERPASS"
- "RIVER CROSSING BRIDGE"
- "MAIN STREET PEDESTRIAN BRIDGE"

### Step 2: File Upload
1. Click "Choose File" and select your completed Excel file
2. Ensure the file is in .xlsx or .xls format
3. Maximum file size is 16MB
4. The system will validate your file before processing

### Step 3: Processing
1. Click "Upload and Process"
2. Wait for the processing indicator to complete
3. Processing typically takes 10-30 seconds depending on complexity

### Step 4: Results
After successful processing, you'll see:
- **Visual Preview**: SVG representation of your bridge design
- **Parameter Summary**: Table showing all input values
- **Download Link**: Access to your generated DXF file
- **File Information**: Details about the generated drawing

## Parameter Reference

### Essential Bridge Geometry
| Parameter | Description | Typical Range | Units |
|-----------|-------------|---------------|-------|
| LBRIDGE | Total bridge length | 20-200 | meters |
| NSPAN | Number of spans | 1-10 | count |
| CCBR | Carriageway width | 6-15 | meters |
| DATUM | Reference datum level | 90-110 | meters |
| TOPRL | Top of rail level | 95-115 | meters |

### Scale and Display
| Parameter | Description | Default | Notes |
|-----------|-------------|---------|-------|
| SCALE1 | Elevation view scale | 186 | Controls drawing size |
| SCALE2 | Plan view scale | 1 | Relative to SCALE1 |
| SKEW | Bridge skew angle | 0 | Degrees (-45 to +45) |

### Structural Elements
| Category | Parameters | Purpose |
|----------|------------|---------|
| Abutments | ABTL, RTL, SOFL | Abutment geometry and positioning |
| Piers | CAPT, CAPB, CAPW, PIERTW | Pier cap and column dimensions |
| Deck | SLBTHC, SLBTHE, SLBTHT | Slab thickness variations |
| Footings | FUTRL, FUTD, FUTW, FUTL | Foundation dimensions |

### Approach Slabs
| Parameter | Description | Purpose |
|-----------|-------------|---------|
| APWTH | Approach slab width | Defines slab extent |
| APTHK | Approach slab thickness | Structural depth |
| LASLAB | Length of approach slab | Longitudinal dimension |

## Output Files

### DXF File Features
Your generated DXF file includes:

**Drawing Views:**
- Elevation view showing bridge profile
- Plan view with structural layout
- Footing plans and pier arrangements
- Complete bridge geometry

**Professional Elements:**
- Industry-standard drawing border
- Comprehensive title block with project information
- Scale indicators and general notes
- Date stamps and revision information
- View labels and annotations

**Technical Details:**
- Proportional Arial fonts for readability
- Proper line weights and styles
- Coordinate systems and reference grids
- Dimensional accuracy for construction use

### File Compatibility
- **AutoCAD**: Fully compatible with all versions
- **DraftSight**: Complete support
- **QCAD**: Full functionality
- **FreeCAD**: Import and view capabilities
- **Other CAD Software**: Standard DXF R2010 format

## Troubleshooting

### Common Issues

**"Parameter validation failed"**
- Check that all required parameters have numeric values
- Ensure no cells are empty in Column A
- Verify parameters are within reasonable ranges

**"Could not read Excel file"**
- Confirm file is in .xlsx or .xls format
- Check that the file isn't corrupted
- Ensure you're using the correct template structure

**"File too large"**
- Maximum file size is 16MB
- Remove unnecessary worksheets or data
- Save as .xlsx format for better compression

**Processing errors**
- Verify all parameter values are realistic
- Check for extremely large or small values
- Ensure bridge geometry is structurally feasible

### Parameter Validation
The system automatically validates:
- Scale values must be positive
- Skew angles between -45° and +45°
- Span counts must be whole numbers ≥ 1
- Bridge length must be positive
- All structural dimensions must be reasonable

### Getting Help
If you encounter persistent issues:
1. Double-check your Excel file against the template
2. Verify all parameter values are appropriate
3. Try with the original template file first
4. Contact technical support with specific error messages

## Technical Support

### File Formats Supported
- **Input**: Excel files (.xlsx, .xls)
- **Output**: DXF files (AutoCAD R2010 format)
- **Preview**: SVG format for web display

### Browser Compatibility
- Chrome 80+ (recommended)
- Firefox 75+
- Safari 13+
- Edge 80+

### Performance Notes
- Processing time: 10-30 seconds typical
- Complex bridges with many spans may take longer
- File size increases with bridge complexity
- Generated DXF files typically 50-100KB

### Data Security
- Files are processed securely on our servers
- No data is permanently stored
- Files are automatically deleted after processing
- Your bridge designs remain confidential

---

**Bridge Design CAD - Professional Bridge Engineering Tool**
*Generate professional CAD drawings from Excel parameters*

For additional support or feature requests, contact the development team.
# Bridge Design CAD Application

## Overview

This is a Flask-based web application for processing bridge design parameters from Excel files and generating comprehensive CAD drawings in DXF format. The application takes Excel files containing bridge engineering parameters and converts them into detailed technical drawings including piers, abutments, approach slabs, and complete bridge geometry. It includes parameter validation, DXF generation capabilities, SVG preview functionality for web display, and an Excel template download for new users.

## Recent Changes (August 3, 2025)

✓ **Complete Bridge Drawing Logic**: Integrated comprehensive drawing methods from original source code including detailed pier drawing with caps, columns, and footings
✓ **Excel Processing Fix**: Fixed header row handling and parameter validation for proper Excel file reading
✓ **DXF Generation**: Successfully generating 46KB DXF files with complete bridge geometry, layout grids, and coordinate transformations
✓ **Template System**: Created downloadable Excel template with 54 bridge parameters and descriptions for new users
✓ **Web Interface Fix**: Resolved template rendering issues and added template download functionality
✓ **SVG Preview**: Working bridge design preview with visual representation of generated CAD drawings

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Web Framework Architecture
- **Flask-based MVC pattern**: Uses Flask as the primary web framework with template rendering for the frontend
- **SQLAlchemy ORM**: Implements database abstraction layer with declarative base for model definitions
- **File Upload Processing**: Handles Excel file uploads with validation and secure filename processing

### Data Processing Pipeline
- **Excel Parameter Extraction**: Reads bridge design parameters from uploaded Excel files using pandas
- **Parameter Validation**: Validates required bridge engineering variables against a predefined schema
- **CAD Generation**: Converts validated parameters into DXF format using ezdxf library for CAD compatibility
- **Preview Generation**: Creates SVG representations for web-based preview of bridge designs

### Database Design
- **Bridge Design Storage**: Tracks uploaded files, processing status, and generated outputs
- **Parameter Tracking**: Stores individual bridge parameters with relationships to design records
- **File Management**: Maintains references to uploaded Excel files and generated DXF outputs

### Frontend Architecture
- **Bootstrap-based UI**: Uses Bootstrap with dark theme for responsive design
- **Progressive Enhancement**: JavaScript handles file validation and form submission with progress indicators
- **Template Inheritance**: Jinja2 templates with base template for consistent layout

### File Management System
- **Upload Directory Structure**: Segregated folders for uploads and generated files
- **File Type Validation**: Restricts uploads to Excel formats (.xlsx, .xls) with size limits
- **Secure Processing**: Uses werkzeug utilities for secure filename handling

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web application framework with SQLAlchemy integration
- **pandas**: Excel file reading and data manipulation
- **ezdxf**: DXF file generation for CAD output

### Frontend Libraries
- **Bootstrap**: UI component library with dark theme
- **Font Awesome**: Icon library for interface elements

### Database Options
- **SQLite**: Default development database (configured via DATABASE_URL environment variable)
- **PostgreSQL**: Production database support through SQLAlchemy configuration

### Development Tools
- **werkzeug**: WSGI utilities and development server
- **ProxyFix**: Handles proxy headers for deployment environments

### File Processing
- **Secure file handling**: Built-in werkzeug utilities for filename sanitization
- **Excel processing**: pandas for reading .xlsx and .xls files
- **CAD output**: ezdxf for generating industry-standard DXF files
# BridgeCanvas - New App

A Streamlit-based web application for bridge design and analysis.

## Getting Started

### Prerequisites

- Python 3.7+
- Required Python packages (install using `pip install -r requirements.txt`)

### Installation

1. Clone the repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the template generator to create an example Excel file:
   ```
   python create_template.py
   ```
   This will create a `templates` directory with a `bridge_template.xlsx` file.

### Excel File Format

The application expects an Excel file with the following columns:
- `variable`: The name of the bridge parameter (e.g., 'SCALE1', 'NSPAN')
- `value`: The numerical value for the parameter
- `description`: A description of what the parameter represents (optional but recommended)

### Running the Application

1. Start the Streamlit app:
   ```
   streamlit run streamlit_app.py
   ```
2. Open your web browser and navigate to `http://localhost:8501`
3. Upload your Excel file with bridge parameters
4. Click "Process Design" to generate the bridge drawing

## Features

- Upload Excel files with bridge parameters
- Preview uploaded data
- Generate DXF files for CAD software
- View SVG previews of the bridge design
- Download generated files

## Directory Structure

```
new_app/
├── __init__.py
├── streamlit_app.py       # Main application
├── bridge_processor.py    # Core bridge processing logic
├── models.py             # Database models
├── create_template.py     # Script to generate template Excel file
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore            # Git ignore file
├── static/               # Static files
│   ├── css/
│   │   └── custom.css
│   └── js/
│       └── app.js
├── uploads/              # Directory for uploaded files
└── generated/            # Directory for generated files
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

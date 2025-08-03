import pandas as pd
import os
from pathlib import Path

def create_template_excel():
    """Create an Excel template with all required variables for BridgeCanvas"""
    # Define the required variables and their descriptions
    variables = {
        'variable': [
            # Scale and Basic Parameters
            'SCALE1', 'SCALE2', 'SKEW', 'DATUM', 'TOPRL', 'LEFT', 'RIGHT', 
            'XINCR', 'YINCR', 'NOCH',
            
            # Bridge Dimensions
            'NSPAN', 'LBRIDGE', 'ABTL', 'RTL', 'SOFL', 'KERBW', 'KERBD', 
            'CCBR', 'SLBTHC', 'SLBTHE', 'SLBTHT',
            
            # Cap and Pier Details
            'CAPT', 'CAPB', 'CAPW', 'PIERTW', 'BATTR', 'PIERST', 'PIERN', 'SPAN1',
            
            # Future and Approach Slab
            'FUTRL', 'FUTD', 'FUTW', 'FUTL', 'DWTH',
            
            # Abutment and Wing Wall
            'ALCW', 'ALCD', 'ALFB', 'ALFBL', 'ALTB', 'ALTBL', 'ALFO',
            'ALBB', 'ALBBL', 'ABTLEN',
            
            # Additional Parameters
            'LASLAB', 'APWTH', 'APTHK', 'WCTH', 'ALFL', 'ARFL', 'ALFBR',
            'ALTBR', 'ALFD', 'ALBBR'
        ],
        'value': [
            # Scale and Basic Parameters (example values)
            1.0, 1.0, 0.0, 100.0, 10.0, 5.0, 5.0, 1.0, 1.0, 2,
            
            # Bridge Dimensions (example values)
            3, 30.0, 1.0, 1.0, 1.0, 0.5, 0.2, 0.5, 0.3, 0.25, 0.2,
            
            # Cap and Pier Details (example values)
            0.3, 0.3, 1.0, 0.5, 0.3, 1.0, 2, 10.0,
            
            # Future and Approach Slab (example values)
            5.0, 0.25, 0.3, 5.0, 0.5,
            
            # Abutment and Wing Wall (example values)
            0.5, 0.3, 0.5, 1.0, 0.4, 1.0, 0.3,
            0.3, 1.0, 2.0,
            
            # Additional Parameters (example values)
            0.15, 0.2, 0.2, 0.2, 0.5, 0.5, 0.5,
            0.4, 0.2, 0.3
        ],
        'description': [
            # Scale and Basic Parameters
            'Horizontal scale factor', 'Vertical scale factor', 'Skew angle in degrees',
            'Datum level', 'Top rail level', 'Left offset', 'Right offset',
            'X-increment for grid', 'Y-increment for grid', 'Number of chains',
            
            # Bridge Dimensions
            'Number of spans', 'Length of bridge', 'Abutment thickness',
            'Road thickness at left', 'Soffit level', 'Kerbing width',
            'Kerbing depth', 'Crossfall of carriageway', 'Slab thickness at center',
            'Slab thickness at edge', 'Slab thickness at tip',
            
            # Cap and Pier Details
            'Cap thickness', 'Cap breadth', 'Cap width', 'Pier top width',
            'Batter of pier', 'Pier stem thickness', 'Number of piers',
            'Span 1 length',
            
            # Future and Approach Slab
            'Future road level', 'Future depth', 'Future width', 'Future length',
            'Dwarf wall thickness',
            
            # Abutment and Wing Wall
            'Abutment length at crest', 'Abutment length at bottom',
            'Abutment front batter', 'Abutment front batter length',
            'Abutment toe batter', 'Abutment toe batter length',
            'Abutment front offset',
            'Abutment back batter', 'Abutment back batter length',
            'Abutment length',
            
            # Additional Parameters
            'Last slab length', 'Approach width', 'Approach thickness',
            'Wing wall cantilever thickness', 'Abutment left face length',
            'Abutment right face length', 'Abutment front batter right',
            'Abutment toe batter right', 'Abutment front depth',
            'Abutment back batter right'
        ]
    }
    
    # Create a DataFrame
    df = pd.DataFrame(variables)
    
    # Create output directory if it doesn't exist
    output_dir = Path("templates")
    output_dir.mkdir(exist_ok=True)
    
    # Save to Excel
    output_file = output_dir / "bridge_template.xlsx"
    df.to_excel(output_file, index=False, sheet_name="Bridge Parameters")
    
    print(f"Template created successfully at: {output_file.absolute()}")
    print("\nInstructions:")
    print("1. Open the template in Microsoft Excel or similar spreadsheet software")
    print("2. Update the 'value' column with your specific bridge parameters")
    print("3. Save the file")
    print("4. Upload the file in the BridgeCanvas app")

if __name__ == "__main__":
    create_template_excel()

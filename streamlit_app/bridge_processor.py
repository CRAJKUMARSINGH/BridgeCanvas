import pandas as pd
import ezdxf
import os
import math
import traceback
from datetime import datetime
import logging
from smart_title import smart_recenter_title

class BridgeProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.required_variables = [
            'SCALE1', 'SCALE2', 'SKEW', 'DATUM', 'TOPRL', 'LEFT', 'RIGHT', 'XINCR', 'YINCR', 'NOCH',
            'NSPAN', 'LBRIDGE', 'ABTL', 'RTL', 'SOFL', 'KERBW', 'KERBD', 'CCBR', 'SLBTHC', 'SLBTHE',
            'SLBTHT', 'CAPT', 'CAPB', 'CAPW', 'PIERTW', 'BATTR', 'PIERST', 'PIERN', 'SPAN1', 'FUTRL',
            'FUTD', 'FUTW', 'FUTL', 'DWTH', 'ALCW', 'ALCD', 'ALFB', 'ALFBL', 'ALTB', 'ALTBL', 'ALFO',
            'ALBB', 'ALBBL', 'ABTLEN', 'LASLAB', 'APWTH', 'APTHK', 'WCTH', 'ALFL', 'ARFL', 'ALFBR',
            'ALTBR', 'ALFD', 'ALBBR'
        ]
    
    def process_excel_file(self, filepath, project_name=None):
        """Process Excel file and generate bridge drawings"""
        try:
            # Read Excel file
            df = self.read_variables(filepath)
            if df is None:
                raise ValueError("Could not read Excel file")
            
            # Validate parameters
            validation_result = self.validate_dataframe(df)
            if not validation_result['valid']:
                raise ValueError(f"Parameter validation failed: {'; '.join(validation_result['errors'])}")
            
            # Extract variables
            variables = self.extract_variables(df)
            
            # Add project name to variables
            if project_name:
                variables['project_name'] = project_name
            else:
                variables['project_name'] = 'BRIDGE PROJECT'
            
            # Generate DXF file
            dxf_filename = self.generate_dxf(variables)
            
            # Generate SVG for web display
            svg_content = self.generate_svg_preview(variables)
            
            return {
                'success': True,
                'variables': variables,
                'dxf_filename': dxf_filename,
                'svg_preview': svg_content
            }
            
        except Exception as e:
            self.logger.error(f"Error processing file {filepath}: {str(e)}")
            self.logger.error(traceback.format_exc())
            return {
                'success': False,
                'error': str(e)
            }
    
    def read_variables(self, filepath):
        """Read variables from Excel file"""
        try:
            # Read the Excel file
            df = pd.read_excel(filepath, header=None, names=['variable', 'value', 'description'])
            return df.dropna(how='all')
        except Exception as e:
            self.logger.error(f"Error reading Excel file: {str(e)}")
            return None
    
    def validate_dataframe(self, df):
        """Validate the input DataFrame"""
        errors = []
        
        # Check if all required variables are present
        missing_vars = [var for var in self.required_variables 
                       if var not in df['variable'].values]
        
        if missing_vars:
            errors.append(f"Missing required variables: {', '.join(missing_vars)}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def extract_variables(self, df):
        """Extract variables from DataFrame into a dictionary"""
        return dict(zip(df['variable'], df['value']))
    
    def generate_dxf(self, variables):
        """Generate DXF file from variables"""
        try:
            # Create a new DXF document
            doc = ezdxf.new('R2010')
            msp = doc.modelspace()
            
            # Create a list to hold drawing elements
            elements = []
            
            # Create drawing elements based on variables
            # Example: Add a simple rectangle for the bridge deck
            elements.append({
                'type': 'RECTANGLE',
                'x': 0,
                'y': 0,
                'width': float(variables.get('LBRIDGE', 100)),
                'height': 10,
                'layer': 'BRIDGE_DECK',
                'tag': 'deck'
            })
            
            # Add a title block
            title_block = {
                'type': 'TEXT',
                'x': 10,
                'y': 20,
                'text': variables.get('project_name', 'BRIDGE DESIGN'),
                'height': 5,
                'layer': 'TITLE',
                'tag': 'title_block'  # This tag is used by smart_recenter_title
            }
            elements.append(title_block)
            
            # Apply smart recenter to position the title block
            smart_recenter_title(elements)
            
            # Add elements to the DXF modelspace
            for element in elements:
                if element['type'] == 'RECTANGLE':
                    msp.add_lwpolyline([
                        (element['x'], element['y']),
                        (element['x'] + element['width'], element['y']),
                        (element['x'] + element['width'], element['y'] + element['height']),
                        (element['x'], element['y'] + element['height']),
                        (element['x'], element['y'])
                    ], dxfattribs={'layer': element.get('layer', '0')})
                elif element['type'] == 'TEXT':
                    msp.add_text(
                        element['text'],
                        dxfattribs={
                            'height': element.get('height', 2.5),
                            'layer': element.get('layer', '0')
                        }
                    ).set_pos((element['x'], element['y']))
            
            # Save the DXF file
            os.makedirs('generated', exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"generated/bridge_design_{timestamp}.dxf"
            doc.saveas(filename)
            
            return filename
            
        except Exception as e:
            self.logger.error(f"Error generating DXF: {str(e)}")
            self.logger.error(traceback.format_exc())
            raise
    
    def generate_svg_preview(self, variables):
        """Generate SVG preview of the bridge design"""
        # This would generate an SVG preview of the bridge
        # For now, return a placeholder
        return "<svg width='400' height='200'><rect width='100%' height='100%' fill='#f0f0f0'/><text x='50%' y='50%' text-anchor='middle'>Bridge Preview</text></svg>"

import pandas as pd
import ezdxf
import os
import math
from datetime import datetime
import logging

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
    
    def process_excel_file(self, filepath):
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
            
            # Generate DXF file
            dxf_filename = self.generate_dxf(variables)
            
            # Generate SVG for web display
            svg_content = self.generate_svg_preview(variables)
            
            return {
                'success': True,
                'variables': variables,
                'dxf_filename': dxf_filename,
                'svg_content': svg_content,
                'validation': validation_result
            }
            
        except Exception as e:
            self.logger.error(f"Processing error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'variables': {},
                'dxf_filename': None,
                'svg_content': None
            }
    
    def read_variables(self, file_path):
        """Read variables from Excel file"""
        try:
            df = pd.read_excel(file_path, header=None)
            if df.shape[1] >= 3:
                df.columns = ['Value', 'Variable', 'Description']
            elif df.shape[1] == 2:
                df.columns = ['Value', 'Variable']
                df['Description'] = ''
            else:
                raise ValueError("Excel file must have at least 2 columns")
            return df
        except Exception as e:
            self.logger.error(f"Error reading Excel file: {e}")
            return None
    
    def validate_dataframe(self, df):
        """Validate that all required variables are present"""
        errors = []
        missing_vars = []
        
        if 'Variable' not in df.columns:
            return {'valid': False, 'errors': ['Excel file must have a Variable column']}
        
        # Check for required variables
        present_vars = df['Variable'].tolist()
        for var in self.required_variables:
            if var not in present_vars:
                missing_vars.append(var)
        
        if missing_vars:
            errors.append(f"Missing required variables: {', '.join(missing_vars)}")
        
        # Check for numeric values
        for index, row in df.iterrows():
            try:
                float(row['Value'])
            except (ValueError, TypeError):
                errors.append(f"Non-numeric value for variable {row['Variable']}: {row['Value']}")
        
        return {'valid': len(errors) == 0, 'errors': errors}
    
    def validate_parameters(self, parameters):
        """Validate individual parameters"""
        errors = []
        
        # Basic validation rules
        validations = {
            'SCALE1': lambda x: x > 0,
            'SCALE2': lambda x: x > 0,
            'SKEW': lambda x: -45 <= x <= 45,
            'NSPAN': lambda x: x >= 1 and x == int(x),
            'NOCH': lambda x: x >= 2 and x == int(x),
            'LBRIDGE': lambda x: x > 0,
            'CCBR': lambda x: x > 0,
        }
        
        for param, validation_func in validations.items():
            if param in parameters:
                try:
                    value = float(parameters[param])
                    if not validation_func(value):
                        errors.append(f"Invalid value for {param}: {value}")
                except (ValueError, TypeError):
                    errors.append(f"Non-numeric value for {param}")
        
        return {'valid': len(errors) == 0, 'errors': errors}
    
    def extract_variables(self, df):
        """Extract variables from dataframe into dictionary"""
        variables = {}
        for index, row in df.iterrows():
            try:
                variables[row['Variable'].lower()] = float(row['Value'])
            except (ValueError, TypeError):
                self.logger.warning(f"Could not convert {row['Variable']} value to float: {row['Value']}")
        return variables
    
    def generate_dxf(self, variables):
        """Generate DXF file from bridge parameters"""
        try:
            # Create DXF document
            doc = ezdxf.new("R2010", setup=True)
            msp = doc.modelspace()
            
            # Setup styles and dimensions
            self.setup_styles(doc)
            
            # Calculate derived values
            sc = variables.get('scale1', 1) / variables.get('scale2', 1)
            skew1 = variables.get('skew', 0) * 0.0174532  # Convert to radians
            
            # Generate bridge geometry
            self.draw_bridge_elevation(msp, variables, sc, skew1)
            self.draw_bridge_plan(msp, variables, sc, skew1)
            
            # Save DXF file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bridge_design_{timestamp}.dxf"
            filepath = os.path.join("generated", filename)
            doc.saveas(filepath)
            
            return filename
            
        except Exception as e:
            self.logger.error(f"DXF generation error: {str(e)}")
            raise
    
    def setup_styles(self, doc):
        """Setup DXF styles and dimension styles"""
        try:
            # Set up text style
            doc.styles.new("Arial", dxfattribs={'font': 'Arial.ttf'})
            
            # Set up dimension style
            dimstyle = doc.dimstyles.new('PMB100')
            dimstyle.dxf.dimasz = 150
            dimstyle.dxf.dimtdec = 0
            dimstyle.dxf.dimexe = 400
            dimstyle.dxf.dimexo = 400
            dimstyle.dxf.dimlfac = 1
            dimstyle.dxf.dimtxsty = "Arial"
            dimstyle.dxf.dimtxt = 400
            dimstyle.dxf.dimtad = 0
        except Exception as e:
            self.logger.warning(f"Style setup warning: {str(e)}")
    
    def draw_bridge_elevation(self, msp, variables, sc, skew1):
        """Draw bridge elevation view"""
        try:
            datum = variables.get('datum', 0)
            left = variables.get('left', 0)
            lbridge = variables.get('lbridge', 100)
            toprl = variables.get('toprl', 100)
            sofl = variables.get('sofl', 95)
            
            # Draw main bridge outline
            bridge_points = [
                (left, sofl),
                (left + lbridge, sofl),
                (left + lbridge, toprl),
                (left, toprl),
                (left, sofl)
            ]
            
            for i in range(len(bridge_points) - 1):
                msp.add_line(bridge_points[i], bridge_points[i + 1])
            
            # Draw abutments
            self.draw_abutments(msp, variables)
            
            # Draw piers if multiple spans
            nspan = int(variables.get('nspan', 1))
            if nspan > 1:
                self.draw_piers(msp, variables, nspan)
                
        except Exception as e:
            self.logger.error(f"Elevation drawing error: {str(e)}")
    
    def draw_abutments(self, msp, variables):
        """Draw abutment details"""
        try:
            left = variables.get('left', 0)
            right = variables.get('right', 100)
            datum = variables.get('datum', 0)
            abtlen = variables.get('abtlen', 10)
            alcw = variables.get('alcw', 5)
            alcd = variables.get('alcd', 3)
            
            # Left abutment
            left_abt_points = [
                (left - abtlen, datum),
                (left, datum),
                (left, datum + alcd),
                (left - alcw, datum + alcd),
                (left - abtlen, datum)
            ]
            
            for i in range(len(left_abt_points) - 1):
                msp.add_line(left_abt_points[i], left_abt_points[i + 1])
            
            # Right abutment (mirror of left)
            right_abt_points = [
                (right + abtlen, datum),
                (right, datum),
                (right, datum + alcd),
                (right + alcw, datum + alcd),
                (right + abtlen, datum)
            ]
            
            for i in range(len(right_abt_points) - 1):
                msp.add_line(right_abt_points[i], right_abt_points[i + 1])
                
        except Exception as e:
            self.logger.error(f"Abutment drawing error: {str(e)}")
    
    def draw_piers(self, msp, variables, nspan):
        """Draw pier details"""
        try:
            left = variables.get('left', 0)
            lbridge = variables.get('lbridge', 100)
            span1 = variables.get('span1', lbridge / nspan)
            datum = variables.get('datum', 0)
            capw = variables.get('capw', 5)
            capt = variables.get('capt', 100)
            capb = variables.get('capb', 95)
            
            # Draw piers between spans
            for i in range(1, nspan):
                pier_x = left + (i * span1)
                
                # Pier cap
                cap_points = [
                    (pier_x - capw/2, capb),
                    (pier_x + capw/2, capb),
                    (pier_x + capw/2, capt),
                    (pier_x - capw/2, capt),
                    (pier_x - capw/2, capb)
                ]
                
                for j in range(len(cap_points) - 1):
                    msp.add_line(cap_points[j], cap_points[j + 1])
                
                # Pier column
                piertw = variables.get('piertw', 2)
                msp.add_line((pier_x - piertw/2, capb), (pier_x - piertw/2, datum))
                msp.add_line((pier_x + piertw/2, capb), (pier_x + piertw/2, datum))
                
        except Exception as e:
            self.logger.error(f"Pier drawing error: {str(e)}")
    
    def draw_bridge_plan(self, msp, variables, sc, skew1):
        """Draw bridge plan view"""
        try:
            # Offset plan view vertically
            plan_offset = -200
            
            left = variables.get('left', 0)
            lbridge = variables.get('lbridge', 100)
            ccbr = variables.get('ccbr', 20)
            
            # Draw bridge deck outline in plan
            plan_points = [
                (left, plan_offset - ccbr/2),
                (left + lbridge, plan_offset - ccbr/2),
                (left + lbridge, plan_offset + ccbr/2),
                (left, plan_offset + ccbr/2),
                (left, plan_offset - ccbr/2)
            ]
            
            for i in range(len(plan_points) - 1):
                msp.add_line(plan_points[i], plan_points[i + 1])
                
        except Exception as e:
            self.logger.error(f"Plan drawing error: {str(e)}")
    
    def generate_svg_preview(self, variables):
        """Generate SVG preview of the bridge design"""
        try:
            # SVG dimensions
            width = 800
            height = 600
            
            # Scale factors for display
            display_scale = 2
            
            # Get key variables
            left = variables.get('left', 0)
            lbridge = variables.get('lbridge', 100)
            datum = variables.get('datum', 0)
            toprl = variables.get('toprl', 100)
            sofl = variables.get('sofl', 95)
            ccbr = variables.get('ccbr', 20)
            
            # Calculate display coordinates
            bridge_width = lbridge * display_scale
            bridge_height = (toprl - datum) * display_scale
            
            # Center the bridge in the SVG
            offset_x = (width - bridge_width) / 2
            offset_y = (height - bridge_height) / 2 - 100
            
            svg_content = f'''
            <svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <style>
                        .bridge-outline {{ fill: none; stroke: #007bff; stroke-width: 2; }}
                        .abutment {{ fill: none; stroke: #28a745; stroke-width: 2; }}
                        .pier {{ fill: none; stroke: #dc3545; stroke-width: 2; }}
                        .text {{ font-family: Arial, sans-serif; font-size: 12px; fill: #333; }}
                        .grid {{ stroke: #e0e0e0; stroke-width: 0.5; }}
                    </style>
                </defs>
                
                <!-- Grid -->
                <defs>
                    <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse">
                        <path d="M 50 0 L 0 0 0 50" fill="none" class="grid"/>
                    </pattern>
                </defs>
                <rect width="100%" height="100%" fill="url(#grid)" />
                
                <!-- Bridge elevation -->
                <g transform="translate({offset_x}, {offset_y})">
                    <!-- Main bridge deck -->
                    <rect x="0" y="{(toprl - sofl) * display_scale}" 
                          width="{bridge_width}" height="{(toprl - sofl) * display_scale}" 
                          class="bridge-outline"/>
                    
                    <!-- Abutments -->
                    <rect x="-20" y="0" width="20" height="{bridge_height}" class="abutment"/>
                    <rect x="{bridge_width}" y="0" width="20" height="{bridge_height}" class="abutment"/>
            '''
            
            # Add piers if multiple spans
            nspan = int(variables.get('nspan', 1))
            if nspan > 1:
                span_width = bridge_width / nspan
                for i in range(1, nspan):
                    pier_x = i * span_width
                    svg_content += f'''
                    <rect x="{pier_x - 5}" y="0" width="10" height="{bridge_height}" class="pier"/>
                    '''
            
            # Add dimensions and labels
            svg_content += f'''
                    <!-- Labels -->
                    <text x="{bridge_width/2}" y="-10" text-anchor="middle" class="text">
                        Bridge Length: {lbridge:.1f}m
                    </text>
                    <text x="-50" y="{bridge_height/2}" text-anchor="middle" class="text" 
                          transform="rotate(-90, -50, {bridge_height/2})">
                        Height: {toprl - datum:.1f}m
                    </text>
                </g>
                
                <!-- Plan view -->
                <g transform="translate({offset_x}, {height - 150})">
                    <text x="{bridge_width/2}" y="-10" text-anchor="middle" class="text">Plan View</text>
                    <rect x="0" y="0" width="{bridge_width}" height="{ccbr * display_scale}" 
                          class="bridge-outline"/>
                    <text x="{bridge_width/2}" y="{ccbr * display_scale + 20}" text-anchor="middle" class="text">
                        Width: {ccbr:.1f}m
                    </text>
                </g>
                
                <!-- Legend -->
                <g transform="translate(20, 20)">
                    <text x="0" y="0" class="text" style="font-weight: bold;">Legend:</text>
                    <line x1="0" y1="15" x2="20" y2="15" class="bridge-outline"/>
                    <text x="25" y="20" class="text">Bridge Deck</text>
                    <line x1="0" y1="35" x2="20" y2="35" class="abutment"/>
                    <text x="25" y="40" class="text">Abutments</text>
                    <line x1="0" y1="55" x2="20" y2="55" class="pier"/>
                    <text x="25" y="60" class="text">Piers</text>
                </g>
            </svg>
            '''
            
            return svg_content
            
        except Exception as e:
            self.logger.error(f"SVG generation error: {str(e)}")
            return f'<svg width="400" height="200"><text x="20" y="100">Error generating preview: {str(e)}</text></svg>'

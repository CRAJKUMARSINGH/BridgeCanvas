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
            # Read Excel file without headers first
            df = pd.read_excel(file_path, header=None)
            
            # Check if first row contains headers
            if (df.iloc[0, 0] == 'Value' and df.iloc[0, 1] == 'Variable'):
                # Skip header row and set proper column names
                df = df.iloc[1:].reset_index(drop=True)
                df.columns = ['Value', 'Variable', 'Description'] if df.shape[1] >= 3 else ['Value', 'Variable']
            else:
                # No headers, set column names directly
                if df.shape[1] >= 3:
                    df.columns = ['Value', 'Variable', 'Description']
                elif df.shape[1] == 2:
                    df.columns = ['Value', 'Variable']
                else:
                    raise ValueError("Excel file must have at least 2 columns")
            
            # Add description column if missing
            if 'Description' not in df.columns:
                df['Description'] = ''
                
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
        """Generate DXF file from bridge parameters using comprehensive bridge drawing logic"""
        try:
            # Create DXF document
            doc = ezdxf.new("R2010", setup=True)
            msp = doc.modelspace()
            
            # Setup styles and dimensions
            self.setup_styles(doc)
            
            # Calculate derived values like the original code
            scale1 = variables.get('scale1', 186)
            scale2 = variables.get('scale2', 1)
            skew = variables.get('skew', 0)
            datum = variables.get('datum', 95)
            left = variables.get('left', 0)
            right = variables.get('right', 100)
            toprl = variables.get('toprl', 100)
            
            # Scale calculations
            hs = 1
            vs = 1
            sc = scale1 / scale2
            vvs = 1000.0 / vs
            hhs = 1000.0 / hs
            skew1 = skew * 0.0174532  # Convert to radians
            
            # Position calculation functions
            def vpos(a):
                return datum + vvs * (a - datum)
            
            def hpos(a):
                return left + hhs * (a - left)
            
            # Draw comprehensive bridge design using original logic
            self.draw_layout_grid(msp, doc, variables, hpos, vpos, scale1, datum, left, toprl)
            self.draw_bridge_superstructure(msp, variables, hpos, vpos, scale1, hhs)
            self.draw_abutments_detailed(msp, variables, hpos, vpos, scale1)
            self.draw_piers_detailed(msp, variables, hpos, vpos, scale1, hhs)
            self.draw_approach_slabs(msp, variables, hpos, vpos, scale1)
            
            # Draw plan view (top-down view) with footings and plan details
            self.draw_plan_view(msp, variables, hpos, vpos, scale1, hhs, vvs, datum, left)
            
            # Save DXF file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bridge_design_{timestamp}.dxf"
            
            # Ensure generated directory exists (absolute path)
            generated_dir = os.path.abspath("generated")
            os.makedirs(generated_dir, exist_ok=True)
            filepath = os.path.join(generated_dir, filename)
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
    
    def draw_layout_grid(self, msp, doc, variables, hpos, vpos, scale1, datum, left, toprl):
        """Draw layout grid and axes based on original code"""
        try:
            # Distance parameters
            d1 = 20  # Distance in mm
            xincr = variables.get('xincr', 5)
            yincr = variables.get('yincr', 1)
            right = variables.get('right', 100)
            laslab = variables.get('laslab', 3.5)
            
            # Define grid points
            pta1 = (left - laslab, datum)
            pta2 = [hpos(variables.get('lbridge', 100) + laslab), datum]
            ptb1 = (left, datum - d1 * scale1)
            ptb2 = [hpos(right), datum - d1 * scale1]
            ptc1 = [left, datum - 2 * d1 * scale1]
            ptc2 = [hpos(right), datum - 2 * d1 * scale1]
            ptd1 = [left, vpos(toprl)]
            
            # Draw X-axis and parallel lines
            msp.add_line(pta1, pta2)
            msp.add_line(ptb1, ptb2)
            msp.add_line(ptc1, ptc2)
            msp.add_line(ptc1, ptd1)  # Y-axis
            
            # Add text labels
            ptb3 = (left - 25 * scale1, datum - d1 * 0.5 * scale1)
            msp.add_text("BED LEVEL", dxfattribs={'height': 2.5 * scale1, 'insert': ptb3})
            ptb3 = (left - 25 * scale1, datum - d1 * 1.5 * scale1)
            msp.add_text("CHAINAGE", dxfattribs={'height': 2.5 * scale1, 'insert': ptb3})
            
            # Draw small lines on Y axis with levels
            d2 = 2.5
            small_line_start = (left - d2 * scale1, datum)
            small_line_end = (left + d2 * scale1, datum)
            msp.add_line(small_line_start, small_line_end)
            
            # Write levels on Y axis
            nov = int((toprl - datum) // 1)
            n = max(1, int(nov // yincr))
            for a in range(n + 1):
                lvl = datum + a * yincr
                b1 = "{:.3f}".format(lvl)
                pta1 = [left - 13 * scale1, vpos(lvl) - 1.0 * scale1]
                text_height = 2.0 * scale1
                msp.add_text(b1, dxfattribs={'height': text_height, 'rotation': 0, 'insert': pta1})
                small_line_start = (left - d2 * scale1, vpos(lvl))
                small_line_end = (left + d2 * scale1, vpos(lvl))
                msp.add_line(small_line_start, small_line_end)
            
            # Write chainages on X axis
            noh = right - left
            n = int(noh // xincr)
            d4 = 2 * d1
            d5 = d4 - 2.0
            d6 = d1 + 2.0
            d7 = d1 - 2.0
            d8 = d4 - 4.0
            
            for a in range(0, n + 2):
                ch = left + a * xincr
                b1 = f"{ch:.3f}"
                pta1 = [scale1 + hpos(ch), datum - d8 * scale1]
                msp.add_text(b1, dxfattribs={'height': 2.0 * scale1, 'insert': pta1, 'rotation': 90})
                pta1 = [hpos(ch), datum - d4 * scale1]
                pta2 = [hpos(ch), datum - d5 * scale1]
                pta3 = [hpos(ch), datum - d6 * scale1]
                pta4 = [hpos(ch), datum - d7 * scale1]
                msp.add_line(pta1, pta2)
                msp.add_line(pta3, pta4)
                
        except Exception as e:
            self.logger.error(f"Layout grid drawing error: {str(e)}")
    
    def draw_bridge_superstructure(self, msp, variables, hpos, vpos, scale1, hhs):
        """Draw bridge superstructure with spans"""
        try:
            spans = variables.get('abtl', 0)
            span1 = variables.get('span1', 30)
            nspan = int(variables.get('nspan', 1))
            rtl = variables.get('rtl', 100)
            sofl = variables.get('sofl', 95)
            
            # Draw main spans
            x1 = hpos(spans)
            y1 = vpos(rtl)
            x2 = hpos(spans + span1)
            y2 = vpos(sofl)
            
            # Create base span rectangle
            pta1 = [x1 + 25.0, y1]
            pta2 = [x2 - 25.0, y2]
            
            # Draw first span
            msp.add_lwpolyline([pta1, [pta2[0], pta1[1]], pta2, [pta1[0], pta2[1]], pta1], close=True)
            
            # Copy for additional spans
            for i in range(1, nspan):
                new_pta1 = [pta1[0] + i * span1 * hhs, pta1[1]]
                new_pta2 = [pta2[0] + i * span1 * hhs, pta2[1]]
                msp.add_lwpolyline([new_pta1, [new_pta2[0], new_pta1[1]], new_pta2, [new_pta1[0], new_pta2[1]], new_pta1], close=True)
                
        except Exception as e:
            self.logger.error(f"Superstructure drawing error: {str(e)}")
    
    def draw_abutments_detailed(self, msp, variables, hpos, vpos, scale1):
        """Draw detailed abutments with caps and footings as per original working code"""
        try:
            # Draw left abutment using original abt1 logic
            self.draw_left_abutment(msp, variables, hpos, vpos, scale1)
            
            # Draw right abutment using original abt2 logic  
            self.draw_right_abutment(msp, variables, hpos, vpos, scale1)
            
        except Exception as e:
            self.logger.error(f"Abutment drawing error: {str(e)}")
    
    def draw_left_abutment(self, msp, variables, hpos, vpos, scale1):
        """Draw left abutment as per original abt1 function"""
        try:
            # Get required variables (as per original working code)
            abtl = variables.get('abtl', 0)
            alcw = variables.get('alcw', 0.75)
            alcd = variables.get('alcd', 1.2)
            dwth = variables.get('dwth', 0.3)
            capt = variables.get('capt', 100.5)
            alfb = variables.get('alfb', 10)
            alfbl = variables.get('alfbl', 101)
            altb = variables.get('altb', 10)
            altbl = variables.get('altbl', 100.5)
            alfo = variables.get('alfo', 0.5)
            alfd = variables.get('alfd', 1.5)
            albb = variables.get('albb', 5)
            albbl = variables.get('albbl', 101.5)
            rtl = variables.get('rtl', 105)
            apthk = variables.get('apthk', 0.2)
            slbtht = variables.get('slbtht', 0.15)
            
            # Calculations as per original abt1 function
            x1 = abtl
            alcwsq = alcw / 1  # c changed to 1 as per original
            x3 = x1 + alcwsq
            capb = capt - alcd
            p1 = (capb - alfbl) / alfb
            p1sq = p1 / 1  # c changed to 1
            x5 = x3 + p1sq
            p2 = (alfbl - altbl) / altb
            p2sq = p2 / 1  # c changed to 1
            x6 = x5 + p2sq
            alfosq = alfo / 1  # c changed to 1
            x7 = x6 + alfosq
            y8 = altbl - alfd
            dwthsq = dwth / 1  # c changed to 1
            x14 = x1 - dwthsq
            p3 = (capb - albbl) / albb
            p3sq = p3 / 1  # c changed to 1
            x12 = x14 - p3sq
            x10 = x12 - alfosq
            
            # Define points using hpos and vpos functions as per original
            pt1 = (hpos(x1), vpos(rtl + apthk - slbtht))
            pt2 = (hpos(x1), vpos(capt))
            pt3 = (hpos(x3), vpos(capt))
            pt4 = (hpos(x3), vpos(capb))
            pt5 = (hpos(x5), vpos(alfbl))
            pt6 = (hpos(x6), vpos(altbl))
            pt7 = (hpos(x7), vpos(altbl))
            pt8 = (hpos(x7), vpos(y8))
            pt9 = (hpos(x10), vpos(y8))
            pt10 = (hpos(x10), vpos(altbl))
            pt11 = (hpos(x12), vpos(altbl))
            pt12 = (hpos(x12), vpos(albbl))
            pt13 = (hpos(x14), vpos(capb))
            pt14 = (hpos(x14), vpos(rtl + apthk - slbtht))
            pt15 = (hpos(x12), vpos(rtl + apthk - slbtht))
            
            # Draw the abutment as per original code
            msp.add_lwpolyline([pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8, pt9, pt10, pt11, pt12, pt13, pt14, pt1], close=True)
            msp.add_line(pt13, pt4)
            msp.add_line(pt10, pt7)
            msp.add_line(pt12, pt15)
            msp.add_line(pt15, pt14)
            
        except Exception as e:
            self.logger.error(f"Left abutment drawing error: {str(e)}")
    
    def draw_right_abutment(self, msp, variables, hpos, vpos, scale1):
        """Draw right abutment as per original abt2 function"""
        try:
            # Get required variables 
            abtl = variables.get('abtl', 0)
            alcw = variables.get('alcw', 0.75)
            alcd = variables.get('alcd', 1.2)
            dwth = variables.get('dwth', 0.3)
            capt = variables.get('capt', 100.5)
            alfb = variables.get('alfb', 10)
            alfbr = variables.get('alfbr', 100.75)  # Right side equivalent
            altb = variables.get('altb', 10)
            altbr = variables.get('altbr', 100.5)   # Right side equivalent
            alfo = variables.get('alfo', 0.5)
            alfd = variables.get('alfd', 1.5)
            albb = variables.get('albb', 5)
            albbr = variables.get('albbr', 101.5)   # Right side equivalent
            rtl = variables.get('rtl', 105)
            apthk = variables.get('apthk', 0.2)
            slbtht = variables.get('slbtht', 0.15)
            lbridge = variables.get('lbridge', 100)
            left = variables.get('left', 0)
            
            # Right abutment calculations (as per original abt2 function)
            x1 = abtl
            alcwsq = alcw / 1  # c changed to 1
            x3 = x1 + alcwsq
            capb = capt - alcd
            p1 = (capb - alfbr) / alfb
            p1sq = p1 / 1  # c changed to 1
            x5 = x3 + p1sq
            p2 = (alfbr - altbr) / altb
            p2sq = p2 / 1  # c changed to 1
            x6 = x5 + p2sq
            alfosq = alfo / 1  # c changed to 1
            x7 = x6 + alfosq
            y8 = altbr - alfd
            dwthsq = dwth / 1  # c changed to 1
            x14 = x1 - dwthsq
            p3 = (capb - albbr) / albb
            p3sq = p3 / 1  # c changed to 1
            x12 = x14 - p3sq
            x10 = x12 - alfosq
            right_edge = left + lbridge
            
            # Define points for right abutment (mirrored from left edge)
            pt1 = (hpos(right_edge - x1), vpos(rtl + apthk - slbtht))
            pt2 = (hpos(right_edge - x1), vpos(capt))
            pt3 = (hpos(right_edge - x3), vpos(capt))
            pt4 = (hpos(right_edge - x3), vpos(capb))
            pt5 = (hpos(right_edge - x5), vpos(alfbr))
            pt6 = (hpos(right_edge - x6), vpos(altbr))
            pt7 = (hpos(right_edge - x7), vpos(altbr))
            pt8 = (hpos(right_edge - x7), vpos(y8))
            pt9 = (hpos(right_edge - x10), vpos(y8))
            pt10 = (hpos(right_edge - x10), vpos(altbr))
            pt11 = (hpos(right_edge - x12), vpos(altbr))
            pt12 = (hpos(right_edge - x12), vpos(albbr))
            pt13 = (hpos(right_edge - x14), vpos(capb))
            pt14 = (hpos(right_edge - x14), vpos(rtl + apthk - slbtht))
            pt15 = (hpos(right_edge - x12), vpos(rtl + apthk - slbtht))
            
            # Draw the right abutment as per original code
            msp.add_lwpolyline([pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8, pt9, pt10, pt11, pt12, pt13, pt14, pt1], close=True)
            msp.add_line(pt13, pt4)
            msp.add_line(pt10, pt7)
            msp.add_line(pt12, pt15)
            msp.add_line(pt15, pt14)
            
        except Exception as e:
            self.logger.error(f"Right abutment drawing error: {str(e)}")
    
    def draw_piers_detailed(self, msp, variables, hpos, vpos, scale1, hhs):
        """Draw detailed piers with caps and footings"""
        try:
            nspan = int(variables.get('nspan', 1))
            if nspan <= 1:
                return  # No piers needed for single span
                
            abtl = variables.get('abtl', 0)
            span1 = variables.get('span1', 30)
            capw = variables.get('capw', 1.2)
            capt = variables.get('capt', 100.5)
            capb = variables.get('capb', 99.3)
            piertw = variables.get('piertw', 0.6)
            battr = variables.get('battr', 10)
            pierst = variables.get('pierst', 5)
            futrl = variables.get('futrl', 90)
            futd = variables.get('futd', 2)
            futw = variables.get('futw', 2.5)
            futl = variables.get('futl', 3.5)
            skew = variables.get('skew', 0)
            
            # Draw piers between spans
            for i in range(1, nspan):
                pier_chainage = abtl + i * span1
                pier_x = hpos(pier_chainage)
                
                # Pier cap
                cap_left = pier_x - hpos(capw/2) + hpos(0)
                cap_right = pier_x + hpos(capw/2) - hpos(0)
                cap_top = vpos(capt)
                cap_bottom = vpos(capb)
                
                cap_points = [
                    [cap_left, cap_bottom],
                    [cap_right, cap_bottom],
                    [cap_right, cap_top],
                    [cap_left, cap_top],
                    [cap_left, cap_bottom]
                ]
                msp.add_lwpolyline(cap_points, close=True)
                
                # Pier column with batter
                pier_top_left = pier_x - hpos(piertw/2) + hpos(0)
                pier_top_right = pier_x + hpos(piertw/2) - hpos(0)
                pier_height = capb - futrl - futd
                
                # Calculate bottom width with batter
                batter_expansion = pier_height / battr
                pier_bottom_left = pier_top_left - hpos(batter_expansion) + hpos(0)
                pier_bottom_right = pier_top_right + hpos(batter_expansion) - hpos(0)
                
                pier_points = [
                    [pier_top_left, cap_bottom],
                    [pier_top_right, cap_bottom],
                    [pier_bottom_right, vpos(futrl + futd)],
                    [pier_bottom_left, vpos(futrl + futd)],
                    [pier_top_left, cap_bottom]
                ]
                msp.add_lwpolyline(pier_points, close=True)
                
                # Pier footing
                footing_left = pier_x - hpos(futw/2) + hpos(0)
                footing_right = pier_x + hpos(futw/2) - hpos(0)
                footing_top = vpos(futrl + futd)
                footing_bottom = vpos(futrl)
                
                footing_points = [
                    [footing_left, footing_bottom],
                    [footing_right, footing_bottom],
                    [footing_right, footing_top],
                    [footing_left, footing_top],
                    [footing_left, footing_bottom]
                ]
                msp.add_lwpolyline(footing_points, close=True)
                
        except Exception as e:
            self.logger.error(f"Pier drawing error: {str(e)}")
    
    def draw_approach_slabs(self, msp, variables, hpos, vpos, scale1):
        """Draw approach slabs"""
        try:
            abtl = variables.get('abtl', 0)
            nspan = int(variables.get('nspan', 1))
            span1 = variables.get('span1', 30)
            laslab = variables.get('laslab', 3.5)
            rtl = variables.get('rtl', 100)
            apthk = variables.get('apthk', 0.23)
            wcth = variables.get('wcth', 0.075)
            
            # Left approach slab
            x1_left = hpos(abtl - laslab)
            x2_left = hpos(abtl)
            y1_left = vpos(rtl)
            y2_left = vpos(rtl - apthk)
            
            left_slab_points = [
                [x1_left, y1_left],
                [x2_left, y1_left],
                [x2_left, y2_left],
                [x1_left, y2_left],
                [x1_left, y1_left]
            ]
            msp.add_lwpolyline(left_slab_points, close=True)
            
            # Right approach slab
            x1_right = hpos(abtl + (nspan * span1))
            x2_right = hpos(abtl + (nspan * span1) + laslab)
            y1_right = vpos(rtl)
            y2_right = vpos(rtl - apthk)
            
            right_slab_points = [
                [x1_right, y1_right],
                [x2_right, y1_right],
                [x2_right, y2_right],
                [x1_right, y2_right],
                [x1_right, y1_right]
            ]
            msp.add_lwpolyline(right_slab_points, close=True)
            
            # Wearing course (continuous across all slabs)
            wearing_course_points = [
                [x1_left, y1_left],
                [x2_right, y1_right],
                [x2_right, vpos(rtl + wcth)],
                [x1_left, vpos(rtl + wcth)],
                [x1_left, y1_left]
            ]
            msp.add_lwpolyline(wearing_course_points, close=True)
            
        except Exception as e:
            self.logger.error(f"Approach slab drawing error: {str(e)}")
    
    def draw_plan_view(self, msp, variables, hpos, vpos, scale1, hhs, vvs, datum, left):
        """Draw comprehensive plan view with footings, abutments, and piers as per original logic"""
        try:
            # Get plan view variables
            nspan = int(variables.get('nspan', 1))
            span1 = variables.get('span1', 30)  
            lspan = variables.get('lspan', span1)
            abtl = variables.get('abtl', 0)
            capw = variables.get('capw', 1.2)
            piertw = variables.get('piertw', 0.6)
            pierst = variables.get('pierst', 5)
            futw = variables.get('futw', 2.5)
            futl = variables.get('futl', 3.5)
            futrl = variables.get('futrl', 90)
            futd = variables.get('futd', 2)
            sc = scale1 / variables.get('scale2', 1)
            
            # Plan view coordinate transformation functions (as per original)
            def h2pos(a):
                return left + sc * hhs * (a - left)
            
            def v2pos(a):
                return datum + sc * vvs * (a - datum)
            
            def p2t(a, b):
                """Convert to plan view coordinates"""
                aa = h2pos(a)
                bb = v2pos(b)
                return [aa, bb]
            
            # Offset for plan view positioning (below elevation view)
            plan_offset_y = -5000  # Move plan view below elevation
            
            # Draw pier footings in plan view (as per original logic)
            if nspan > 1:
                self.draw_pier_footings_plan(msp, variables, h2pos, v2pos, p2t, plan_offset_y, nspan, lspan, hhs)
            
            # Draw abutment plans (left and right)
            self.draw_abutment_plans(msp, variables, h2pos, v2pos, p2t, plan_offset_y, hhs, vvs, datum, left)
            
            # Draw bridge deck outline in plan
            self.draw_bridge_deck_plan(msp, variables, h2pos, v2pos, p2t, plan_offset_y)
            
        except Exception as e:
            self.logger.error(f"Plan view drawing error: {str(e)}")
    
    def draw_pier_footings_plan(self, msp, variables, h2pos, v2pos, p2t, plan_offset_y, nspan, lspan, hhs):
        """Draw pier footings in plan view as per original logic"""
        try:
            # Get footing parameters
            abtl = variables.get('abtl', 0)
            futw = variables.get('futw', 2.5)  # Footing width
            futl = variables.get('futl', 3.5)  # Footing length
            datum = variables.get('datum', 95)
            
            # Plan view footing coordinates (as per original)
            yc = datum - 30.0
            
            # Draw footings for each pier
            for i in range(1, nspan):
                # Pier center position
                xc = abtl + i * lspan
                
                # Footing corners in plan (as per original pt function logic)
                x7 = xc - futw / 2  # Left edge of footing
                x8 = x7 + futw      # Right edge of footing
                y7 = yc + futl / 2  # Top edge of footing
                y8 = y7 - futl      # Bottom edge of footing
                
                # Convert to plan coordinates with offset
                pta7 = p2t(x7, y7)
                pta8 = p2t(x8, y8)
                pta7x = [pta7[0], pta8[1] + plan_offset_y]  # Bottom-left
                pta8x = [pta8[0], pta7[1] + plan_offset_y]  # Top-right
                pta7[1] += plan_offset_y  # Apply offset to top-left
                pta8[1] += plan_offset_y  # Apply offset to bottom-right
                
                # Draw footing rectangle (as per original gr1-gr4 functions)
                footing_points = [pta7, pta8x, pta8, pta7x, pta7]
                msp.add_lwpolyline(footing_points, close=True)
                
                # Draw pier column outline in plan
                pier_width = variables.get('piertw', 0.6)
                pier_length = variables.get('pierst', 5)
                
                # Pier corners
                pier_x1 = xc - pier_width / 2
                pier_x2 = xc + pier_width / 2
                pier_y1 = yc + pier_length / 2
                pier_y2 = yc - pier_length / 2
                
                # Convert pier coordinates
                pier_pt1 = p2t(pier_x1, pier_y1)
                pier_pt2 = p2t(pier_x2, pier_y1)
                pier_pt3 = p2t(pier_x2, pier_y2)
                pier_pt4 = p2t(pier_x1, pier_y2)
                
                # Apply offset
                pier_pt1[1] += plan_offset_y
                pier_pt2[1] += plan_offset_y
                pier_pt3[1] += plan_offset_y
                pier_pt4[1] += plan_offset_y
                
                # Draw pier outline
                pier_points = [pier_pt1, pier_pt2, pier_pt3, pier_pt4, pier_pt1]
                msp.add_lwpolyline(pier_points, close=True)
                
        except Exception as e:
            self.logger.error(f"Pier footing plan drawing error: {str(e)}")
    
    def draw_abutment_plans(self, msp, variables, h2pos, v2pos, p2t, plan_offset_y, hhs, vvs, datum, left):
        """Draw abutment plans (left and right) as per original abt1 and abt2 functions"""
        try:
            # Abutment parameters (as per original)
            abtl = variables.get('abtl', 0)
            abtlen = variables.get('abtlen', 12)
            alcw = variables.get('alcw', 0.75)
            alcd = variables.get('alcd', 1.2)
            dwth = variables.get('dwth', 0.3)
            lbridge = variables.get('lbridge', 100)
            ccbr = variables.get('ccbr', 0.5)
            kerbw = variables.get('kerbw', 0.3)
            
            # Plan view calculations (as per original abt1 function)
            ccbrsq = ccbr / 1  # As per original c=1 
            kerbwsq = kerbw / 1
            abtlen_plan = ccbrsq + kerbwsq + kerbwsq
            
            yc = datum - 30.0
            y20 = yc + (abtlen_plan / 2)   # D/S of abutment
            y21 = y20 - abtlen_plan        # U/S of abutment  
            y16 = y20 + 0.15               # D/S of footing
            y17 = y21 - 0.15               # U/S of footing
            
            # Left abutment plan (as per original abt1)
            x1 = abtl
            alcwsq = alcw / 1
            x3 = x1 + alcwsq
            dwthsq = dwth / 1
            x14 = x1 - dwthsq
            
            # Abutment footing points in plan
            pt16 = p2t(x14, y16)  # Left footing corner
            pt17 = p2t(x3, y16)   # Right footing corner  
            pt18 = p2t(x3, y17)   # Right footing corner
            pt19 = p2t(x14, y17)  # Left footing corner
            
            # Apply plan offset
            pt16[1] += plan_offset_y
            pt17[1] += plan_offset_y
            pt18[1] += plan_offset_y
            pt19[1] += plan_offset_y
            
            # Draw left abutment footing
            left_abt_points = [pt16, pt17, pt18, pt19, pt16]
            msp.add_lwpolyline(left_abt_points, close=True)
            
            # Right abutment plan (as per original abt2)  
            right_edge = left + lbridge
            x1_right = abtl
            x3_right = x1_right + alcwsq
            x14_right = x1_right - dwthsq
            
            # Right abutment footing points
            pt20 = p2t(right_edge - x14_right, y16)  # Right footing corner
            pt21 = p2t(right_edge - x3_right, y16)   # Left footing corner
            pt22 = p2t(right_edge - x3_right, y17)   # Left footing corner
            pt23 = p2t(right_edge - x14_right, y17)  # Right footing corner
            
            # Apply plan offset
            pt20[1] += plan_offset_y
            pt21[1] += plan_offset_y
            pt22[1] += plan_offset_y
            pt23[1] += plan_offset_y
            
            # Draw right abutment footing
            right_abt_points = [pt20, pt21, pt22, pt23, pt20]
            msp.add_lwpolyline(right_abt_points, close=True)
            
        except Exception as e:
            self.logger.error(f"Abutment plan drawing error: {str(e)}")
    
    def draw_bridge_deck_plan(self, msp, variables, h2pos, v2pos, p2t, plan_offset_y):
        """Draw bridge deck outline in plan view"""
        try:
            # Bridge parameters
            abtl = variables.get('abtl', 0)
            lbridge = variables.get('lbridge', 100)
            bridgew = variables.get('bridgew', 12)
            datum = variables.get('datum', 95)
            
            # Plan coordinates for deck outline
            yc = datum - 30.0
            deck_width_half = bridgew / 2
            
            # Deck corners
            deck_pt1 = p2t(abtl, yc + deck_width_half)          # Left-top
            deck_pt2 = p2t(abtl + lbridge, yc + deck_width_half) # Right-top  
            deck_pt3 = p2t(abtl + lbridge, yc - deck_width_half) # Right-bottom
            deck_pt4 = p2t(abtl, yc - deck_width_half)          # Left-bottom
            
            # Apply plan offset
            deck_pt1[1] += plan_offset_y
            deck_pt2[1] += plan_offset_y
            deck_pt3[1] += plan_offset_y
            deck_pt4[1] += plan_offset_y
            
            # Draw deck outline
            deck_points = [deck_pt1, deck_pt2, deck_pt3, deck_pt4, deck_pt1]
            msp.add_lwpolyline(deck_points, close=True)
            
        except Exception as e:
            self.logger.error(f"Bridge deck plan drawing error: {str(e)}")
    
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

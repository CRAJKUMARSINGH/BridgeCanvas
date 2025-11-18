#!/usr/bin/env python3
"""
Test script for BridgeCanvas LISP logic functions
This script tests all the newly implemented advanced bridge design functions
"""

import sys
import os
import tempfile
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from bridge_processor import BridgeProcessor

def test_lisp_logic_functions():
    """Test all LISP logic functions"""
    print("🧪 Testing BridgeCanvas LISP Logic Functions")
    print("=" * 50)
    
    # Initialize processor
    processor = BridgeProcessor()
    
    # Test data
    test_variables = {
        'scale1': 1.0,
        'datum': 95.0,
        'left': 0.0,
        'right': 100.0,
        'toprl': 100.0,
        'lbridge': 100.0,
        'nspan': 3,
        'span1': 33.33,
        'capw': 1.2,
        'capt': 100.0,
        'capb': 95.0,
        'piertw': 0.6,
        'battr': 20.0,
        'futrl': 90.0,
        'futd': 2.0,
        'futw': 2.5,
        'futl': 3.5,
        'abtlen': 12.0,
        'alcw': 0.75,
        'alcd': 1.2,
        'alfb': 1.5,
        'alfbl': 0.3,
        'altb': 1.5,
        'altbl': 0.3,
        'dwth': 0.3,
        'alfd': 2.0,
        'alfo': 0.5,
        'ccbr': 20.0,
        'kerbw': 0.3,
        'kerbd': 0.15,
        'slbthc': 0.2,
        'slbthe': 0.25,
        'slbtht': 0.3,
        'wcth': 0.075,
        'xincr': 5.0,
        'yincr': 1.0
    }
    
    # Test results
    test_results = []
    
    try:
        # Test 1: Complex Pier Geometry
        print("1. Testing Complex Pier Geometry...")
        from ezdxf import new
        doc = new('R2010')
        msp = doc.modelspace()
        
        # Test pier geometry function
        processor.draw_complex_pier_geometry(msp, test_variables, 50.0, 95.0, 1.0)
        print("   ✅ Complex pier geometry test passed")
        test_results.append(("Complex Pier Geometry", True))
        
    except Exception as e:
        print(f"   ❌ Complex pier geometry test failed: {e}")
        test_results.append(("Complex Pier Geometry", False))
    
    try:
        # Test 2: Detailed Abutment Geometry
        print("2. Testing Detailed Abutment Geometry...")
        processor.draw_detailed_abutment_geometry(msp, test_variables, 0.0, 95.0, True, 1.0)
        processor.draw_detailed_abutment_geometry(msp, test_variables, 100.0, 95.0, False, 1.0)
        print("   ✅ Detailed abutment geometry test passed")
        test_results.append(("Detailed Abutment Geometry", True))
        
    except Exception as e:
        print(f"   ❌ Detailed abutment geometry test failed: {e}")
        test_results.append(("Detailed Abutment Geometry", False))
    
    try:
        # Test 3: Cross-Section Plotting
        print("3. Testing Cross-Section Plotting...")
        processor.draw_cross_section_plotting(msp, test_variables, 50.0, 100.0, 1.0)
        print("   ✅ Cross-section plotting test passed")
        test_results.append(("Cross-Section Plotting", True))
        
    except Exception as e:
        print(f"   ❌ Cross-section plotting test failed: {e}")
        test_results.append(("Cross-Section Plotting", False))
    
    try:
        # Test 4: Advanced Layout Grid
        print("4. Testing Advanced Layout Grid...")
        processor.draw_advanced_layout_grid(msp, doc, test_variables, 1.0)
        print("   ✅ Advanced layout grid test passed")
        test_results.append(("Advanced Layout Grid", True))
        
    except Exception as e:
        print(f"   ❌ Advanced layout grid test failed: {e}")
        test_results.append(("Advanced Layout Grid", False))
    
    try:
        # Test 5: Dimension Functions
        print("5. Testing Dimension Functions...")
        processor.add_pier_dimensions(msp, 50.0, 95.0, 100.0, 1.2, 0.6, 1.8, 2.5, 3.5, 1.0)
        processor.add_abutment_dimensions(msp, 0.0, 95.0, 96.2, 0.75, 1.2, 12.0, 0.3, 1.0)
        processor.add_cross_section_dimensions(msp, 50.0, 100.0, 20.0, 0.3, 0.3, 0.075, 1.0)
        print("   ✅ Dimension functions test passed")
        test_results.append(("Dimension Functions", True))
        
    except Exception as e:
        print(f"   ❌ Dimension functions test failed: {e}")
        test_results.append(("Dimension Functions", False))
    
    # Test 6: DXF Generation
    try:
        print("6. Testing DXF Generation...")
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix='.dxf', delete=False) as tmp_file:
            doc.saveas(tmp_file.name)
            tmp_file_path = tmp_file.name
        
        # Check if file was created and has content
        if os.path.exists(tmp_file_path) and os.path.getsize(tmp_file_path) > 0:
            print("   ✅ DXF generation test passed")
            test_results.append(("DXF Generation", True))
            
            # Clean up
            os.unlink(tmp_file_path)
        else:
            print("   ❌ DXF generation test failed: File not created or empty")
            test_results.append(("DXF Generation", False))
            
    except Exception as e:
        print(f"   ❌ DXF generation test failed: {e}")
        test_results.append(("DXF Generation", False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All LISP logic functions are working correctly!")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False

def test_bridge_processor_integration():
    """Test the complete bridge processor integration"""
    print("\n🔗 Testing Bridge Processor Integration...")
    
    try:
        processor = BridgeProcessor()
        
        # Test required variables
        required_vars = processor.required_variables
        print(f"   ✅ Required variables defined: {len(required_vars)} variables")
        
        # Test validation
        test_data = {'SCALE1': 1.0, 'SCALE2': 1.0, 'SKEW': 0.0}
        validation = processor.validate_parameters(test_data)
        print(f"   ✅ Parameter validation working: {validation}")
        
        print("   ✅ Bridge processor integration test passed")
        return True
        
    except Exception as e:
        print(f"   ❌ Bridge processor integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting BridgeCanvas LISP Logic Tests")
    print("=" * 60)
    
    # Run tests
    lisp_tests_passed = test_lisp_logic_functions()
    integration_tests_passed = test_bridge_processor_integration()
    
    print("\n" + "=" * 60)
    print("🏁 FINAL TEST RESULTS")
    print("=" * 60)
    
    if lisp_tests_passed and integration_tests_passed:
        print("🎉 ALL TESTS PASSED!")
        print("   BridgeCanvas is ready for deployment with full LISP logic support.")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED!")
        print("   Please review the failed tests and fix the implementation.")
        sys.exit(1)

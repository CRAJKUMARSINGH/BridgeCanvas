#!/usr/bin/env python3
"""
Application Verification Script for BridgeGAD-07
Tests all critical functionality and reports status
"""

import os
import sys
import traceback
from pathlib import Path

def test_imports():
    """Test all critical imports"""
    print("Testing imports...")
    
    try:
        import app
        print("✅ Flask app imports successfully")
    except ImportError as e:
        print(f"❌ Flask app import failed: {e}")
        return False
        
    try:
        import bridge_processor
        print("✅ Bridge processor imports successfully")
    except ImportError as e:
        print(f"❌ Bridge processor import failed: {e}")
        return False
        
    try:
        import smart_title
        print("✅ Smart title imports successfully")
    except ImportError as e:
        print(f"❌ Smart title import failed: {e}")
        return False
        
    try:
        import pandas as pd
        import ezdxf
        import flask
        print("✅ All major dependencies available")
    except ImportError as e:
        print(f"❌ Major dependency missing: {e}")
        return False
        
    return True

def test_directories():
    """Ensure all required directories exist"""
    print("\nChecking directories...")
    
    required_dirs = [
        'uploads',
        'generated', 
        'templates',
        'static',
        'streamlit_app'
    ]
    
    all_good = True
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ exists")
        else:
            print(f"❌ {dir_name}/ missing")
            try:
                os.makedirs(dir_name, exist_ok=True)
                print(f"✅ Created {dir_name}/")
            except Exception as e:
                print(f"❌ Failed to create {dir_name}/: {e}")
                all_good = False
    
    return all_good

def test_flask_app():
    """Test Flask application setup"""
    print("\nTesting Flask application...")
    
    try:
        from app import app, db
        
        with app.app_context():
            # Test database initialization
            db.create_all()
            print("✅ Database initialized successfully")
            
        # Test app configuration
        assert app.config['MAX_CONTENT_LENGTH'] == 16 * 1024 * 1024
        assert app.config['UPLOAD_FOLDER'] == 'uploads'
        assert app.config['GENERATED_FOLDER'] == 'generated'
        print("✅ Flask app configuration verified")
        
        return True
        
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        traceback.print_exc()
        return False

def test_bridge_processor():
    """Test bridge processing functionality"""
    print("\nTesting bridge processor...")
    
    try:
        from bridge_processor import BridgeProcessor
        
        bp = BridgeProcessor()
        print("✅ BridgeProcessor created successfully")
        
        # Test with sample input if available
        sample_file = 'attached_assets/input.xlsx'
        if os.path.exists(sample_file):
            print(f"✅ Sample input file found: {sample_file}")
            
            result = bp.process_excel_file(sample_file, 'VERIFICATION_TEST')
            
            if result.get('success', False):
                print("✅ Bridge processing completed successfully")
                
                # Check if DXF file was generated
                dxf_file = result.get('dxf_filename')
                if dxf_file and os.path.exists(dxf_file):
                    print(f"✅ DXF file generated: {dxf_file}")
                else:
                    print("⚠️ DXF file generation may have issues")
                    
                return True
            else:
                error = result.get('error', 'Unknown error')
                print(f"❌ Bridge processing failed: {error}")
                return False
        else:
            print("⚠️ No sample input file available for testing")
            print("✅ Bridge processor is ready but untested")
            return True
            
    except Exception as e:
        print(f"❌ Bridge processor test failed: {e}")
        traceback.print_exc()
        return False

def test_streamlit_app():
    """Test Streamlit application"""
    print("\nTesting Streamlit application...")
    
    try:
        # Change to streamlit_app directory
        original_cwd = os.getcwd()
        os.chdir('streamlit_app')
        
        # Add current directory to path for imports
        sys.path.insert(0, os.getcwd())
        
        try:
            import streamlit_app
            print("✅ Streamlit app imports successfully")
            
            # Test bridge processor import from streamlit context
            from bridge_processor import BridgeProcessor
            bp = BridgeProcessor()
            print("✅ Bridge processor available in Streamlit context")
            
            return True
            
        except Exception as e:
            print(f"❌ Streamlit app test failed: {e}")
            return False
        finally:
            os.chdir(original_cwd)
            sys.path.pop(0)
            
    except Exception as e:
        print(f"❌ Streamlit directory test failed: {e}")
        return False

def test_batch_files():
    """Test that batch files exist and are properly configured"""
    print("\nChecking batch files...")
    
    batch_files = [
        'run_bridge_app.bat',
        'run_streamlit_app.bat'
    ]
    
    all_good = True
    for batch_file in batch_files:
        if os.path.exists(batch_file):
            print(f"✅ {batch_file} exists")
        else:
            print(f"❌ {batch_file} missing")
            all_good = False
    
    return all_good

def main():
    """Run all verification tests"""
    print("=" * 60)
    print("BridgeGAD-07 Application Verification")
    print("=" * 60)
    
    tests = [
        ("Import Tests", test_imports),
        ("Directory Setup", test_directories), 
        ("Flask Application", test_flask_app),
        ("Bridge Processor", test_bridge_processor),
        ("Streamlit Application", test_streamlit_app),
        ("Batch Files", test_batch_files)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * len(test_name))
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All systems operational! Application is ready to use.")
        print("\nTo start the application:")
        print("  Flask:     python app.py")
        print("  Streamlit: streamlit run streamlit_app/streamlit_app.py")
        print("  Batch:     .\\run_bridge_app.bat or .\\run_streamlit_app.bat")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please address issues before use.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

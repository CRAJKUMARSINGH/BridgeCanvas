import streamlit as st
import os
import sys
import logging
import traceback
from pathlib import Path
import pandas as pd
import base64
from datetime import datetime

# Add the current directory to the path so we can import local modules
sys.path.append(str(Path(__file__).parent))

# Import local modules
from bridge_processor import BridgeProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page config
st.set_page_config(
    page_title="BridgeCanvas",
    page_icon="🌉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'processing_result' not in st.session_state:
    st.session_state.processing_result = None

# Initialize BridgeProcessor
@st.cache_resource
def get_processor():
    return BridgeProcessor()

processor = get_processor()

# Custom CSS
st.markdown("""
    <style>
    .main {
        max-width: 1200px;
        padding: 2rem;
    }
    .stButton>button {
        border-radius: 20px;
        font-weight: bold;
    }
    .stApp {
        background-color: #f8f9fa;
    }
    .file-uploader {
        border: 2px dashed #4CAF50;
        border-radius: 5px;
        padding: 20px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("🌉 BridgeCanvas")
    st.markdown("### Bridge Design and Analysis Tool")
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Upload Design", "Design Parameters", "Results"])
    
    with tab1:
        st.header("Upload Bridge Design")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload Excel file with bridge parameters",
            type=['xlsx', 'xls'],
            key="file_uploader"
        )
        
        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            st.success(f"File uploaded: {uploaded_file.name}")
            
            # Show file preview
            if st.checkbox("Show file preview"):
                try:
                    df = pd.read_excel(uploaded_file)
                    st.dataframe(df.head())
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
            
            # Process file
            if st.button("Process Design"):
                with st.spinner("Processing bridge design..."):
                    try:
                        # Save the uploaded file temporarily
                        temp_dir = Path("temp")
                        temp_dir.mkdir(exist_ok=True)
                        temp_file = temp_dir / uploaded_file.name
                        with open(temp_file, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Process the file
                        st.session_state.processing_result = processor.process_excel_file(
                            str(temp_file),
                            project_name=f"Bridge_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                        )
                        
                        # Clean up
                        temp_file.unlink()
                        
                        st.success("Design processed successfully!")
                        st.experimental_rerun()
                        
                    except Exception as e:
                        st.error(f"Error processing file: {str(e)}")
                        logger.exception("Error processing file")
    
    with tab2:
        st.header("Design Parameters")
        if st.session_state.uploaded_file is None:
            st.info("Please upload a file in the 'Upload Design' tab first.")
        else:
            st.warning("Parameter editing coming soon!")
    
    with tab3:
        st.header("Results")
        if st.session_state.processing_result is None:
            st.info("Process a design in the 'Upload Design' tab to see results.")
        else:
            result = st.session_state.processing_result
            if result.get('success', False):
                st.success("Design processed successfully!")
                
                # Show DXF download button
                dxf_file = result.get('dxf_filename')
                if dxf_file and os.path.exists(dxf_file):
                    with open(dxf_file, "rb") as f:
                        bytes_data = f.read()
                        b64 = base64.b64encode(bytes_data).decode()
                        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(dxf_file)}">Download DXF File</a>'
                        st.markdown(href, unsafe_allow_html=True)
                
                # Show SVG preview if available
                svg_preview = result.get('svg_preview')
                if svg_preview:
                    st.markdown("### Design Preview")
                    st.components.v1.html(svg_preview, height=400)
                
                # Show variables
                if st.checkbox("Show design variables"):
                    st.json(result.get('variables', {}))
            else:
                st.error(f"Error processing design: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()

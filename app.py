<<<<<<< Updated upstream
import tempfile
import streamlit as st
import logging
import asyncio
# from docling import docling
from zerox_model import zerox_model

def main():
    logging.basicConfig(level=logging.INFO)
    st.title('PDF to JSON Converter')
    
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        # Write the file to a temporary location on disk
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_file_path = tmp_file.name
            
        print(tmp_file_path)
        
        # Process the uploaded PDF file with Docling
        # docling(tmp_file_path)
        
        # Process the uploaded PDF file with ZeroX
        asyncio.run(zerox_model(tmp_file_path))
        
=======
import streamlit as st
from pages import upload, upscale, results
import time

st.set_page_config(page_title="SwiftAuth", page_icon="🔐", layout="wide")

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "upload"
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "upscaled" not in st.session_state:
    st.session_state.upscaled = False


# Main app logic
def main():
    if st.session_state.page == "upload":
        upload.show()
    elif st.session_state.page == "upscale":
        upscale.show()
    elif st.session_state.page == "results":
        results.show()

    # Footer with dark theme
    st.markdown(
        """
    <div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 8px; background-color: #1E1E1E;'>
        <p style='color: #888888; font-size: 12px; margin: 0;'>© 2023 SwiftAuth v1.0.0 | Document Authentication Made Easy — Developed by John Ong from EdgeRunners</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

>>>>>>> Stashed changes

if __name__ == "__main__":
    main()

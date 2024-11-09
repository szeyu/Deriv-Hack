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
        

if __name__ == "__main__":
    main()

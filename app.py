import tempfile
import streamlit as st
import logging
import asyncio
# from docling import docling
from zerox_model import zerox_model
from pdf_to_png import pdf_to_png

def main():
    logging.basicConfig(level=logging.INFO)
    st.title('PDF to PNG Converter')
    
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        # Write the file to a temporary location on disk
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_file_path = tmp_file.name
            
        # Create a temporary output folder
        output_folder = tempfile.mkdtemp()

        st.info(f"Converting PDF to PNG, please wait...")
        
        try:
            # Convert PDF to PNG using the function
            png_files = pdf_to_png(tmp_file_path, output_folder)
            
            # Display each generated PNG in Streamlit
            for png_file in png_files:
                st.image(png_file, caption=os.path.basename(png_file), use_column_width=True)
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        
        # Cleanup: Optionally delete temporary files (PDF and PNGs)
        if st.button("Clean Up Temporary Files"):
            os.remove(tmp_file_path)
            for png_file in png_files:
                os.remove(png_file)
            st.success("Temporary files deleted!")

if __name__ == "__main__":
    main()

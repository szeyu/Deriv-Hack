import tempfile
import streamlit as st
import logging
import asyncio
import os
from pdf_to_png import pdf_to_png

def main():
    logging.basicConfig(level=logging.INFO)
    st.title('PDF to PNG Converter')

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Write the file to a temporary location on disk
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            pdf_file_path = tmp_file.name
        
        # Create a temporary output folder for PNG files
        with tempfile.TemporaryDirectory() as output_folder:
            # Call the pdf_to_png function
            st.info("Converting PDF to PNG images...")
            pdf_to_png(pdf_file_path, output_folder)
            
            # Display the PNG images
            st.success("Conversion completed! Displaying images:")
            for file_name in sorted(os.listdir(output_folder)):
                if file_name.endswith(".png"):
                    image_path = os.path.join(output_folder, file_name)
                    st.image(image_path, caption=file_name)
            
if __name__ == "__main__":
    main()

import tempfile
import streamlit as st
import logging
import asyncio
# from docling import docling
from zerox_model import zerox_model
from PIL import Image
import numpy as np
from utils.image_vectorizer import image_to_vector

def main():
    # logging.basicConfig(level=logging.INFO)
    # st.title('PDF to JSON Converter')
    
    # uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    # if uploaded_file is not None:
    #     # Write the file to a temporary location on disk
    #     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
    #         tmp_file.write(uploaded_file.getbuffer())
    #         tmp_file_path = tmp_file.name
            
    #     print(tmp_file_path)
        
    #     # Process the uploaded PDF file with Docling
    #     # docling(tmp_file_path)
        
    #     # Process the uploaded PDF file with ZeroX
    #     asyncio.run(zerox_model(tmp_file_path))
    
    st.title('Image similarity score')

    uploaded_image_1 = st.file_uploader("Choose first image file", type=["jpg", "jpeg", "png"])
    uploaded_image_2 = st.file_uploader("Choose second image file", type=["jpg", "jpeg", "png"])

    if uploaded_image_1 is not None and uploaded_image_2 is not None:
        image1 = Image.open(uploaded_image_1)
        image2 = Image.open(uploaded_image_2)

        # Convert images to vectors
        vector1 = image_to_vector(image1)
        vector2 = image_to_vector(image2)

        # Calculate cosine similarity
        similarity = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

        st.write(f"Similarity score: {similarity}")
        

if __name__ == "__main__":
    main()

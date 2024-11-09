import asyncio
import os
import sys
import tempfile
import cv2
import numpy as np
import streamlit as st
import time
from utils.zerox_model import zerox_model
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from utils.crop_face import crop_face  # Import the crop_face function

# Add the utils folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

# Now try importing
from zerox_model import zerox_model
from crop_face import crop_face

# Ensure to initialize session state variables correctly
if "verification_complete" not in st.session_state:
    st.session_state.verification_complete = False

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if "upscaled_image" not in st.session_state:
    st.session_state.upscaled_image = None

if "verification_complete" not in st.session_state:
    st.session_state.verification_complete = False

# Allow the user to upload a passport image
uploaded_file = st.file_uploader("Upload Passport Image (JPEG, PNG)", type=["jpg", "jpeg", "png"])

# Display the form for passport verification
st.markdown(
    """
<style>
    .stButton > button {
        width: 150px !important;
        margin: 0 auto;
        display: block;
        background-color: #4A90E2;
        color: white;
        border-radius: 20px;
        padding: 8px 16px;
        border: none;
        transition: background-color 0.3s, color 0.3s;
    }
    .stButton > button:hover {
        background-color: white;
        color: #4A90E2;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("Passport Verification Results")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if uploaded_file is not None:
        with st.spinner("Verifying passport..."):
            # Create a temporary directory to save images
            temp_dir = tempfile.mkdtemp()
            try:
                # Read the uploaded image as bytes
                image_bytes = uploaded_file.read()

                # Call crop_face to detect and crop the face
                cropped_face_path = crop_face(image_bytes)

                if cropped_face_path:
                    # Display the cropped face image
                    st.image(cropped_face_path, caption="Cropped Face", use_column_width=True)
                    st.success(f"Cropped face saved at: {cropped_face_path}")
                else:
                    st.warning("No face detected in the uploaded image.")
                
                # You can also proceed with other steps (such as extracting passport info) here
                
                # Call zerox_model to extract information if needed
                # Example: custom_prompt, zerox_model call, etc.
                # If you need to work with the PDF, you can follow similar steps as before
                
            finally:
                # Cleanup temporary files
                if not st.session_state.get("cleanup_done", False):
                    try:
                        for file in os.listdir(temp_dir):
                            file_path = os.path.join(temp_dir, file)
                            if os.path.isfile(file_path):
                                os.unlink(file_path)
                        os.rmdir(temp_dir)
                    except Exception as e:
                        st.error(f"Error during cleanup: {e}")
                    st.session_state.cleanup_done = True  # Flag to prevent repeat cleanup
import streamlit as st
import time
from utils.upscale import nearestNeighboor
import tempfile
import os
import cv2
import numpy as np

def show():
    if st.session_state.uploaded_file is None:
        st.session_state.page = "bank_statement"
        st.rerun()

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
        .stButton > button:active, .stButton > button:focus {
            background-color: #4A90E2;
            color: white;
            border: none;
            outline: none;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h1 style='text-align: center;'>Bank Statement Enhancement</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: #4A90E2;'>Enhancing statement for better verification</p>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            "<h3 style='text-align: center; color: #B0B0B0;'>Original Image</h3>",
            unsafe_allow_html=True,
        )
        st.image(st.session_state.uploaded_file, use_container_width=True)

    with col2:
        st.markdown(
            "<h3 style='text-align: center; color: #B0B0B0;'>Enhanced Image</h3>",
            unsafe_allow_html=True,
        )
        if not st.session_state.get("upscaled", False):
            if st.button("Enhance Image"):
                with st.spinner("Enhancing statement..."):
                    # Create a temporary file to save the uploaded image
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                        tmp_file.write(st.session_state.uploaded_file)
                        tmp_file_path = tmp_file.name

                    # Upscale the image
                    upscale_factor = 2  # You can adjust this value
                    upscaled_image = nearestNeighboor(tmp_file_path, upscale_factor)

                    # Convert the numpy array to bytes
                    is_success, buffer = cv2.imencode(".png", upscaled_image)
                    upscaled_image_bytes = buffer.tobytes()

                    # Save upscaled image to session state
                    st.session_state.upscaled_image = upscaled_image_bytes

                    # Clean up the temporary file
                    os.unlink(tmp_file_path)

                    time.sleep(2)  # Simulating processing time

                st.session_state.upscaled = True
                st.rerun()
        else:
            # Convert bytes to numpy array for display
            nparr = np.frombuffer(st.session_state.upscaled_image, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            st.image(img_np, channels="BGR", use_container_width=True)

    if st.session_state.upscaled:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col2:
            if st.button("← Back"):
                st.session_state.upscaled = False
                st.session_state.page = "bank_statement"
                st.rerun()
        with col3:
            if st.button("Verify →"):
                st.session_state.page = "results_2"
                st.rerun()
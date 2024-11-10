import streamlit as st
import time
from utils.upscale import nearestNeighboor
import tempfile
import os
import cv2

def show():
    if st.session_state.uploaded_file is None:
        st.session_state.page = "passport"
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
        "<h1 style='text-align: center;'>Passport Image Enhancement</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: #4A90E2;'>Enhancing passport image for better verification</p>",
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
                with st.spinner("Enhancing passport image..."):
                    # Create a temporary file to save the uploaded image
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                        tmp_file.write(st.session_state.uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name

                    # Upscale the image
                    upscale_factor = 2  # You can adjust this value
                    upscaled_image = nearestNeighboor(tmp_file_path, upscale_factor)

                    # Convert the numpy array to bytes
                    is_success, buffer = cv2.imencode(".png", upscaled_image)
                    upscaled_image_bytes = buffer.tobytes()

                    # Save upscaled image to a local folder
                    st.session_state.upscaled_image = upscaled_image_bytes
                    upscaled_image_path = os.path.join("upscaled_images", "upscaled_image.png")
                    os.makedirs(os.path.dirname(upscaled_image_path), exist_ok=True)
                    with open(upscaled_image_path, "wb") as f:
                        f.write(upscaled_image_bytes)

                    # Save the path to session state
                    st.session_state.upscaled_image_path = upscaled_image_path

                    # Clean up the temporary file
                    os.unlink(tmp_file_path)

                    time.sleep(2)  # Simulating processing time

                st.session_state.upscaled = True
                st.rerun()
        else:
            st.image(st.session_state.upscaled_image, use_container_width=True)

    if st.session_state.upscaled:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col2:
            if st.button("← Back"):
                st.session_state.upscaled = False
                st.session_state.page = "identity"
                st.rerun()
        with col3:
            if st.button("Verify Identity →"):
                st.session_state.page = "selfie"
               # st.session_state.page = "results_1"
                st.rerun()
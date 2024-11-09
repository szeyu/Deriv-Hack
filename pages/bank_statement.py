import streamlit as st
import tempfile
import os
from utils.pdf_to_png import pdf_to_png

def show():
    st.markdown(
        """
        <style>
            .main > div:first-child {
                margin-top: -60px;
            }
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
            .fixed-height-container {
                max-height: 300px;
                overflow: hidden;
                margin: 10px auto;
                text-align: center;
            }
            .upload-section {
                margin-top: -20px;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            "<h1 style='text-align: center; margin-bottom: 0;'>SwiftAuth</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='text-align: center; color: #4A90E2; margin-top: 0;'>Bank Statement Verification</h3>",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div style='text-align: center; padding: 8px; background-color: #2E2E2E; border-radius: 10px; margin: 5px 0;'>
            <h4 style='color: #E0E0E0; margin: 3px 0;'>Step 2: Bank Statement Upload</h4>
            <p style='color: #B0B0B0; margin: 3px 0;'>Please upload your recent bank statement.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload bank statement", type=["png", "jpg", "jpeg", "pdf"]
        )

        if uploaded_file is not None:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()

            if file_extension == '.pdf':
                # Create a temporary directory to store PNG images
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Save the uploaded PDF to a temporary file
                    temp_pdf_path = os.path.join(temp_dir, "temp.pdf")
                    with open(temp_pdf_path, "wb") as f:
                        f.write(uploaded_file.getvalue())

                    # Convert PDF to PNG
                    pdf_to_png(temp_pdf_path, temp_dir)

                    # Get the first PNG image (assuming single-page statement)
                    png_files = [f for f in os.listdir(temp_dir) if f.endswith('.png')]
                    if png_files:
                        png_path = os.path.join(temp_dir, png_files[0])
                        with open(png_path, "rb") as f:
                            st.session_state.uploaded_file = f.read()
                    else:
                        st.error("Failed to convert PDF to PNG.")
                        return
            else:
                # For image uploads, just read the file
                st.session_state.uploaded_file = uploaded_file.getvalue()

            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.markdown(
                    '<div class="fixed-height-container">', unsafe_allow_html=True
                )
                st.image(st.session_state.uploaded_file, caption="Bank Statement", width=300)
                st.markdown("</div>", unsafe_allow_html=True)
                
                if st.button("Next →"):
                    st.session_state.page = "upscale_2"
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
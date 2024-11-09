import tempfile
import streamlit as st
import logging
import asyncio
import os
from utils.pdf_to_png import pdf_to_png
from utils.upscale import nearestNeighboor

from pages import passport, upscale_1, results_1, bank_statement, upscale_2, results_2
import time

st.set_page_config(
    page_title="SwiftAuth",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "passport"
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "upscaled" not in st.session_state:
    st.session_state.upscaled = False


# Main app logic
def main():
    # uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    # if uploaded_file is not None:
    #     # Write the file to a temporary location on disk
    #     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
    #         tmp_file.write(uploaded_file.getbuffer())
    #         pdf_file_path = tmp_file.name
        
    #     # Create a temporary output folder for PNG files
    #     with tempfile.TemporaryDirectory() as output_folder:
    #         # Call the pdf_to_png function
    #         st.info("Converting PDF to PNG images...")
    #         pdf_to_png(pdf_file_path, output_folder)
            
    #         # Display the PNG images
    #         st.success("Conversion completed! Displaying images:")
    #         for file_name in sorted(os.listdir(output_folder)):
    #             if file_name.endswith(".png"):
    #                 image_path = os.path.join(output_folder, file_name)
    #                 # st.image(image_path, caption=file_name)
    #                 resized = nearestNeighboor(image_path, 1.5)
    #                 st.image(resized, caption= file_name) 
    #                 st.success("Upscaling completed!")
            
    if st.session_state.page == "passport":
        passport.show()
    elif st.session_state.page == "upscale_1":
        upscale_1.show()
    elif st.session_state.page == "results_1":
        results_1.show()
    elif st.session_state.page == "bank_statement":
        bank_statement.show()
    elif st.session_state.page == "upscale_2":
        upscale_2.show()
    elif st.session_state.page == "results_2":
        results_2.show()

    # Footer with dark theme
    st.markdown(
        """
    <div style='position: fixed; left: 0; bottom: 0; width: 100%; background-color: #1E1E1E; padding: 10px 0;'>
        <div style='max-width: 800px; margin: 0 auto; text-align: center;'>
            <p style='color: #888888; font-size: 12px; margin: 0;'>© 2023 SwiftAuth v1.0.0 | Document Authentication Made Easy — Developed by John Ong from EdgeRunners</p>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

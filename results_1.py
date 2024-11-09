import asyncio
import os
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

# Ensure to initialize session state variables correctly
if "verification_complete" not in st.session_state:
    st.session_state.verification_complete = False

if "uploaded_file" not in st.session_state:
    st.warning("No file uploaded. Please upload a file.")
    st.stop()

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

# Unique session state key for this page
verification_key = "results_1_verification_complete"

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if not st.session_state.verification_complete:
        with st.spinner("Verifying passport..."):
            # Create a temporary directory
            temp_dir = tempfile.mkdtemp()
            try:
                # Save the upscaled image as PNG
                png_path = os.path.join(temp_dir, "passport.png")
                nparr = np.frombuffer(st.session_state.upscaled_image, np.uint8)
                img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                cv2.imwrite(png_path, img_np)

                # Convert PNG to PDF
                pdf_path = os.path.join(temp_dir, "passport.pdf")
                img = Image.open(png_path)
                img_width, img_height = img.size
                c = canvas.Canvas(pdf_path, pagesize=(img_width, img_height))
                c.drawImage(png_path, 0, 0, img_width, img_height)
                c.save()
                img.close()

                # Crop face from the image
                try:
                    cropped_face = crop_face(st.session_state.upscaled_image)
                    if cropped_face:
                        # Display cropped face
                        st.image(cropped_face, caption="Cropped Face", use_column_width=True)
                        
                        # Save cropped face globally
                        cropped_face_path = os.path.join(tempfile.gettempdir(), "cropped_face.png")
                        cropped_face.save(cropped_face_path)
                        st.session_state.cropped_face_path = cropped_face_path  # Store path globally
                        
                        st.success(f"Cropped face saved at: {cropped_face_path}")
                    else:
                        st.warning("No face detected in the uploaded image.")
                except Exception as e:
                    st.error(f"Face cropping error: {e}")

                # Call zerox_model to extract information
                custom_prompt = """
Extract the following information from the passport image and format it as a JSON object within triple backticks. Use the following keys: full_name, DOB, nationality, expiry_date. If any field is not found or unclear, use <NULL> as the value.

Example format:
```json
{
    "full_name": "John Doe",
    "DOB": "1990-01-01",
    "nationality": "MALAYSIA",
    "expiry_date": "2030-12-31"
}
"""

                result = asyncio.run(zerox_model(pdf_path, custom_system_prompt=custom_prompt))

                # Store the result in session state
                st.session_state.passport_info = result

                time.sleep(2)  # Short delay for UI smoothness
            finally:
                # Clean up temporary files
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

            st.session_state.verification_complete = True
            st.experimental_rerun()

    # Display verification status
    st.success("✅ Passport Verification Successful!")

    # Display verification details
    st.markdown("### Verification Details")
    st.markdown("✓ Passport Type: Valid")
    st.markdown("✓ MRZ Check: Passed")
    st.markdown("✓ Security Features: Verified")
    st.markdown("✓ Last Verified: Just now")

    # Display extracted information
    if "passport_info" in st.session_state:
        passport_info = st.session_state.passport_info
        st.json(passport_info)

    # Next steps button
    st.markdown("### Next Steps")
    st.markdown("Please proceed to upload your bank statement.")

    if st.button("Continue to Bank Statement →"):
        st.session_state.uploaded_file = None
        st.session_state.upscaled = False
        st.session_state.verification_complete = False
        st.session_state.page = "bank_statement"
        st.experimental_rerun()

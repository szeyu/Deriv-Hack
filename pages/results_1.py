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
from utils.verify import verify_user_data


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
        div.stSpinner > div {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h1 style='text-align: center;'>Passport Verification Results</h1>",
        unsafe_allow_html=True,
    )

    # Unique session state key for this page
    verification_key = "results_1_verification_complete"

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not st.session_state["verification_complete"]:
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
                    print(pdf_path)
                    img = Image.open(png_path)
                    img_width, img_height = img.size
                    c = canvas.Canvas(pdf_path, pagesize=(img_width, img_height))
                    c.drawImage(png_path, 0, 0, img_width, img_height)
                    c.save()

                    # Close the image file
                    img.close()

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
```
"""
                    result = asyncio.run(
                        zerox_model(pdf_path, custom_system_prompt=custom_prompt)
                    )

                    # Store the result in session state
                    st.session_state.passport_info = result

                    # Retrieve user email from session state
                    user_email = st.session_state.get("user_email", None)
                    if user_email is None:
                        st.error("User email not found. Please log in again.")
                        st.session_state.page = "login"
                        st.rerun()

                    # Verify user data against the database
                    verification_result = verify_user_data(user_email)

                    if verification_result["status"] == "success":
                        st.session_state.verification_status = "success"
                        st.session_state.verification_message = verification_result[
                            "message"
                        ]
                    else:
                        st.session_state.verification_status = "failure"
                        st.session_state.verification_message = verification_result[
                            "message"
                        ]
                        st.session_state.verification_alert = verification_result.get(
                            "alert", ""
                        )

                        time.sleep(2)  # Short delay for UI smoothness
                finally:
                    # Clean up temporary files
                    for file in os.listdir(temp_dir):
                        file_path = os.path.join(temp_dir, file)
                        try:
                            if os.path.isfile(file_path):
                                os.unlink(file_path)
                        except Exception as e:
                            print(f"Error deleting {file_path}: {e}")
                    os.rmdir(temp_dir)

            st.session_state.verification_complete = True
            st.rerun()

        # Display verification results based on the verification_status
        if st.session_state.get("verification_status") == "success":
            st.success("✅ Passport Verification Successful!")
            st.markdown(st.session_state.verification_message)
            st.markdown("### Next Steps")
            st.markdown("Please proceed to upload your bank statement.")
            if st.button("Continue to Bank Statement →"):
                st.session_state.uploaded_file = None
                st.session_state.upscaled = False
                st.session_state.verification_complete = False
                st.session_state.page = "bank_statement"
                st.rerun()
        elif st.session_state.get("verification_status") == "failure":
            st.error(
                f"❌ Passport Verification Failed: {st.session_state.verification_message}"
            )
            st.warning(f"**Alert:** {st.session_state.verification_alert}")
            st.markdown("### Next Steps")
            st.markdown("Please contact support or try submitting your passport again.")
            if st.button("← Start New Verification"):
                st.session_state.uploaded_file = None
                st.session_state.upscaled = False
                st.session_state.verification_complete = False
                st.session_state.page = "login"  # Navigate back to login
                st.rerun()

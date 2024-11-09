import streamlit as st
import time
import tempfile
import os
import cv2
import numpy as np
from PIL import Image
from reportlab.pdfgen import canvas
import asyncio
from utils.zerox_model import zerox_model
from utils.document_similarity import compare_images
from utils.verify import (
    verify_user_data_2,
    sucess_bank_statement_fallback,
    invalid_bank_statement_fallback,
)


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
        "<h1 style='text-align: center;'>Bank Statement Verification Results</h1>",
        unsafe_allow_html=True,
    )

    # Unique session state key for this page
    verification_key = "results_2_verification_complete"

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not st.session_state["verification_complete"]:
            with st.spinner("Verifying bank statement..."):
                # Create a temporary directory
                temp_dir = tempfile.mkdtemp()
                try:
                    # Save the upscaled image as PNG
                    png_path = os.path.join(temp_dir, "bank_statement.png")
                    nparr = np.frombuffer(st.session_state.upscaled_image, np.uint8)
                    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    cv2.imwrite(png_path, img_np)

                    # Compare the bank statement with other bank statements
                    highest_similarity_file, highest_similarity = compare_images(
                        png_path
                    )

                    if (
                        highest_similarity < 0.85
                    ):  # Threshold for similarity (adjust as needed)
                        st.error(
                            "❌ Verification Failed: The uploaded document does not match any known bank statement format."
                        )
                        invalid_bank_statement_fallback(
                            st.session_state.user_email
                        )  # Update fallback CSV
                        time.sleep(3)  # Short delay for UI smoothness
                        st.session_state.uploaded_file = None
                        st.session_state.upscaled = False
                        st.session_state.verification_complete = False
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        bank_name = highest_similarity_file.split(".")[0].capitalize()
                        st.success(f"✅ Bank Statement Verification Successful!")
                        st.info(
                            f"The uploaded document appears to be from {bank_name}."
                        )
                        sucess_bank_statement_fallback(
                            st.session_state.user_email, bank_name
                        )  # Update fallback CSV

                        time.sleep(2)  # Short delay for UI smoothness

                    # Convert PNG to PDF
                    pdf_path = os.path.join(temp_dir, "bank_statement.pdf")
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
Extract the following information from the bank statement and format it as a JSON object within triple backticks. Use the following keys: account_holder_name, address, account_number, statement_date. If any field is not found or unclear, use <NULL> as the value.

Example format:
```json
{
    "account_holder_name": "John Doe",
    "address": "123 Main St, Anytown, AN 12345",
    "account_number": "XXXXXXXX1234",
    "statement_date": "31/01/2023"
}
"""
                    result = asyncio.run(
                        zerox_model(pdf_path, custom_system_prompt=custom_prompt)
                    )
                    # Store the result in session state
                    st.session_state.statement_info = result

                    # Retrieve user email from session state
                    user_email = st.session_state.get("user_email", None)
                    if user_email is None:
                        st.error("User email not found. Please log in again.")
                        st.session_state.page = "login"
                        st.rerun()

                    # Verify user data against the database
                    verification_result = verify_user_data_2(user_email)

                    if verification_result["status"] == "success":
                        st.session_state.bank_verification_status = "success"
                        st.session_state.bank_verification_message = (
                            verification_result["message"]
                        )
                    else:
                        st.session_state.bank_verification_status = "failure"
                        st.session_state.bank_verification_message = (
                            verification_result["message"]
                        )
                        st.session_state.bank_verification_alert = (
                            verification_result.get("alert", "")
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

        # Update the display section
        if st.session_state.get("bank_verification_status") == "success":
            st.success("✅ Bank Statement Verification Successful!")
            st.markdown(st.session_state.bank_verification_message)
            st.markdown("### Verification Complete")
            st.markdown("Thank you for completing the verification process.")
        elif st.session_state.get("bank_verification_status") == "failure":
            st.error(
                f"❌ Bank Statement Verification Failed: {st.session_state.bank_verification_message}"
            )
            if st.session_state.get("bank_verification_alert"):
                st.warning(f"**Alert:** {st.session_state.bank_verification_alert}")
            st.markdown("### Next Steps")
            st.markdown(
                "Please contact support or try submitting your bank statement again."
            )

        # Reset button
        if st.button("← Start New Verification"):
            # Reset all relevant session states
            st.session_state.uploaded_file = None
            st.session_state.upscaled = False
            st.session_state.verification_complete = False
            st.session_state.bank_verification_status = None
            st.session_state.bank_verification_message = None
            st.session_state.bank_verification_alert = None
            st.session_state.statement_info = None
            st.session_state.page = "login"
            st.rerun()

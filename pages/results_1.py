import streamlit as st
import time


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
        "<h1 style='text-align: center;'>Passport Verification Results</h1>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if "verification_complete" not in st.session_state:
            with st.spinner("Verifying passport..."):
                time.sleep(5)
            st.session_state.verification_complete = True
            st.rerun()

        st.success("✅ Passport Verification Successful!")

        st.markdown("### Verification Details")
        st.markdown("✓ Passport Type: Valid")
        st.markdown("✓ MRZ Check: Passed")
        st.markdown("✓ Security Features: Verified")
        st.markdown("✓ Last Verified: Just now")

        st.markdown("### Next Steps")
        st.markdown("Please proceed to upload your bank statement.")

        if st.button("Continue to Bank Statement →"):
            st.session_state.uploaded_file = None
            st.session_state.upscaled = False
            st.session_state.verification_complete = False
            st.session_state.page = "bank_statement"
            st.rerun()

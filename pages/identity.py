import streamlit as st


def show():
    if st.session_state.user_email is None:
        st.session_state.page = "login"
        st.rerun()

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
            "<h3 style='text-align: center; color: #4A90E2; margin-top: 0;'>Identity Verification</h3>",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div style='text-align: center; padding: 8px; background-color: #2E2E2E; border-radius: 10px; margin: 5px 0;'>
            <h4 style='color: #E0E0E0; margin: 3px 0;'>Step 1: Identity Upload</h4>
            <p style='color: #B0B0B0; margin: 3px 0;'>Please upload a clear image of your Identity.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload Identity image", type=["png", "jpg", "jpeg"]
        )

        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file

            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.markdown(
                    '<div class="fixed-height-container">', unsafe_allow_html=True
                )
                st.image(uploaded_file, caption="Identity Image", width=300)
                st.markdown("</div>", unsafe_allow_html=True)
                if st.button("Next →"):
                    st.session_state.page = "upscale_1"
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

import streamlit as st


def show():
    # Center-aligned container with reduced vertical spacing
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            "<h1 style='text-align: center; margin-bottom: 0;'>SwiftAuth</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='text-align: center; color: #4A90E2; margin-top: 0;'>Document Authentication Made Easy</h3>",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div style='text-align: center; padding: 10px; background-color: #2E2E2E; border-radius: 10px; margin: 10px 0;'>
            <h4 style='color: #E0E0E0; margin: 5px 0;'>Welcome to SwiftAuth</h4>
            <p style='color: #B0B0B0; margin: 5px 0;'>Upload your document for secure verification.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "Choose a document to verify", type=["png", "jpg", "jpeg", "pdf"]
        )

        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            # Container with smaller fixed dimensions
            st.markdown(
                """
            <style>
                .fixed-height-container {
                    max-height: 300px;
                    overflow: hidden;
                    margin: 10px 0;
                    text-align: center;
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
            </style>
            """,
                unsafe_allow_html=True,
            )

            st.markdown('<div class="fixed-height-container">', unsafe_allow_html=True)
            st.image(uploaded_file, caption="Uploaded Document", width=300)
            st.markdown("</div>", unsafe_allow_html=True)

            # Centered button
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Next →"):
                    st.session_state.page = "upscale"
                    st.rerun()

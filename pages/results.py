import streamlit as st


def show():
    if st.session_state.uploaded_file is None:
        st.session_state.page = "upload"
        st.rerun()

    st.markdown(
        "<h1 style='text-align: center;'>Verification Results</h1>",
        unsafe_allow_html=True,
    )

    # Custom button styling
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
        .results-container {
            background-color: #2E2E2E;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        }
        .success-header {
            color: #4CAF50;
            margin-bottom: 20px;
        }
        .details-container {
            background-color: #1E1E1E;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }
        .details-header {
            color: #4A90E2;
            margin-bottom: 15px;
        }
        .details-list {
            color: #B0B0B0;
            list-style-type: none;
            padding-left: 0;
            text-align: left;
            margin-left: 20px;
        }
        .details-item {
            margin: 10px 0;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
    # Center content using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            """
            <div class="results-container">
                <h2 class="success-header">Document Verified Successfully! ✅</h2>
                
                <div class="details-container">
                    <h3 class="details-header">Verification Details:</h3>
                    <ul class="details-list">
                        <li class="details-item">✓ Document Type: Valid</li>
                        <li class="details-item">✓ Authentication Status: Passed</li>
                        <li class="details-item">✓ Integrity Check: Passed</li>
                        <li class="details-item">✓ Last Verified: Just now</li>
                    </ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("← Back to Start"):
            # Reset all states without showing verification spinner
            st.session_state.uploaded_file = None
            st.session_state.upscaled = False
            st.session_state.page = "upload"
            st.rerun()

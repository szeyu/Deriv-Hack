import streamlit as st


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
            .login-container {
                max-width: 400px;
                margin: 0 auto;
                padding: 20px;
            }
            .stTextInput > div > div > input {
                border-radius: 20px;
                padding: 8px 16px;
                margin-bottom: 10px;
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
            "<h3 style='text-align: center; color: #4A90E2; margin-top: 0;'>Welcome to Document Verification</h3>",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div style='text-align: center; padding: 8px; background-color: #2E2E2E; border-radius: 10px; margin: 5px 0;'>
            <h4 style='color: #E0E0E0; margin: 3px 0;'>Login</h4>
            <p style='color: #B0B0B0; margin: 3px 0;'>Please enter your credentials to continue.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input(
                "Password", type="password", placeholder="Enter your password"
            )

            if st.form_submit_button("Login"):
                if email and password:  # Basic validation
                    st.session_state.user_email = email
                    st.session_state.page = "identity"
                    st.rerun()
                else:
                    st.error("Please fill in all fields")

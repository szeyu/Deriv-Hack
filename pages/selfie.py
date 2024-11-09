import streamlit as st
import time

def show():
    if st.session_state.upscaled_image is None:
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
        "<h1 style='text-align: center;'>Selfie</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: #4A90E2;'>take a selfie for verification</p>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            "<h3 style='text-align: center; color: #B0B0B0;'>Original Image</h3>",
            unsafe_allow_html=True,
        )
        st.image(st.session_state.upscaled_image, use_container_width=True)

    with col2:
        st.markdown(
            "<h3 style='text-align: center; color: #B0B0B0;'>Enhanced Image</h3>",
            unsafe_allow_html=True,
        )
        if not st.session_state.get("selfied", False):
            if st.button("Take selfie"):
                with st.spinner("Verifying selfie..."):
                    
                    time.sleep(5)  # Simulating processing time

                st.session_state.selfied = True
                st.rerun()
        else:
            st.image(st.session_state.captured_image, use_container_width=True)

    if st.session_state.captured_image is not None:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col2:
            if st.button("← Back"):
                st.session_state.upscaled = False
                st.session_state.page = "passport"
                st.rerun()
        with col3:
            if st.button("Verify →"):
                st.session_state.page = "results_1"
                st.rerun()
import time
import streamlit as st
from deepface import DeepFace
import cv2
import numpy as np
from PIL import Image
import os

def crop_face(image_path, output_path="cropped_face.png"):
    # Read the image from the file path
    img = cv2.imread(image_path)

    # Use OpenCV's pre-trained Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Convert image to grayscale for face detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # If faces are found, crop the first face
    if len(faces) > 0:
        x, y, w, h = faces[0]  # Get the coordinates of the first face
        cropped_face = img[y:y+h, x:x+w]  # Crop the face

        # Convert the cropped face from BGR (OpenCV format) to RGB (PIL format)
        cropped_face_rgb = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB)

        # Convert to a PIL image
        pil_image = Image.fromarray(cropped_face_rgb)

        # Save the cropped face as a PNG image
        pil_image.save(output_path)

        return output_path  # Return the path to the saved cropped face
    else:
        return None  # No face detected

def show():
    # Streamlit App Title
    st.title("Face Similarity Comparison")

    cropped_face_path = None

    # Create two columns for photo upload (left) and selfie capture (right)
    col1, col2 = st.columns(2)

    # Left column for the photo
    with col1:
        st.subheader("Your Photo")

        if st.session_state.upscaled_image_path is not None:
            st.image(st.session_state.upscaled_image_path, use_container_width=True) 
            # Crop the face from the upscaled image
            try:
                cropped_face_path = crop_face(st.session_state.upscaled_image_path)
                if cropped_face_path:
                    st.image(cropped_face_path, use_container_width=True)
                else:
                    st.warning("No face detected in the uploaded image. Please try another image.")
            except Exception as e:
                st.error(f"An error occurred while processing the image: {str(e)}")

    # Right column for capturing the selfie
    with col2:
        st.subheader("Capture Selfie")
        image_placeholder = st.empty()
        video = cv2.VideoCapture(0)  # Open webcam

        if "captured_image" not in st.session_state:
            st.session_state.captured_image = None

        # Buttons for webcam control
        start = st.button('Start Camera')
        stop = st.button('Capture Selfie')

        if start:
            while not stop:
                success, frame = video.read()
                if not success:
                    break
                st.session_state.captured_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image_placeholder.image(st.session_state.captured_image, use_container_width=True)
                if stop:
                    video.release()
                    cv2.destroyAllWindows()
                    break
        if st.session_state.captured_image is not None:
            st.image(st.session_state.captured_image, caption="Captured Selfie", use_container_width=True)
            print("Captured selfie")

        if cropped_face_path is not None and st.session_state.captured_image is not None:
            print(cropped_face_path)
            # Save captured selfie temporarily
            captured_image_path = "captured_selfie.jpg"
            captured_image = Image.fromarray(st.session_state.captured_image)
            captured_image.save(captured_image_path)

            # Perform face similarity comparison using DeepFace
            st.subheader("Comparing Similarity...")
            try:
                result = DeepFace.verify(cropped_face_path, captured_image_path, model_name='Facenet', distance_metric='cosine')

                # Display similarity score
                similarity_score = result['distance']
                st.write(f"Cosine Similarity Score: {similarity_score}")

                # Show whether they are the same person based on a threshold
                if similarity_score < 0.6:  
                    st.success("The images are likely of the same person!")
                    # Navigate to result1 page
                    st.session_state.page = "results_1"
                    time.sleep(5)
                    st.rerun()
                else:
                    st.error("The images are likely of different people.")
                    # Navigate back
                    st.session_state.page = "identity"
                    time.sleep(5)
                    st.rerun()
            except Exception as e:
                st.error(f"An error occurred during face comparison: {str(e)}")

    # Add buttons for manual navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.page = "identity"
            st.rerun()
    with col2:
        if st.button("Next →"):
            st.session_state.page = "results_1"
            st.rerun()
import cv2

def crop_face(image_bytes):
    # Convert the bytes to an OpenCV image
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
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
        return cropped_face
    else:
        return None  # No face detected

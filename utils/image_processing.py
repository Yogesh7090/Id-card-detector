import cv2
import cvlib as cv
import numpy as np
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import streamlit as st

def loading_model():
    """
    Loads the pre-trained gender detection model.

    Returns:
    - model: The loaded Keras model.
    """
    model = load_model('GenDet.h5')
    return model

def preprocessing_face_croped(face_crop):
    """
    Preprocesses a cropped face image for gender detection.

    Parameters:
    - face_crop (numpy.ndarray): The cropped face image.

    Returns:
    - numpy.ndarray: The preprocessed face image.
    """
    # Resize face image to 96x96 pixels
    face_crop = cv2.resize(face_crop, (96, 96))
    face_crop = face_crop.astype("float") / 255.0  # Normalize pixel values
    face_crop = img_to_array(face_crop)  # Convert image to array
    face_crop = np.expand_dims(face_crop, axis=0)  # Add batch dimension
    return face_crop

def capture_image_from_webcam():
    """
    Captures an image from the webcam, detects faces, and classifies gender.

    Returns:
    - tuple: Contains the detected gender label and the captured image.
    """
    # Initialize webcam


    videoSource = 0
    cap = cv2.VideoCapture(videoSource)

    

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        st.error("Error: Could not open webcam.")
        return None, None
    
    

    frame_placeholder = st.empty()
    stop_button_pressed = st.button("Stop")

    classes = ['man', 'woman']
    captured_image = None
    captured_label = None

    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            st.error("Error: Failed to capture image from webcam.")
            break

        # Perform face detection
        faces, confidence = cv.detect_face(frame)
        
        for idx, f in enumerate(faces):
            startX, startY, endX, endY = f
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)  # Draw bounding box
            face_crop = frame[startY:endY, startX:endX]  # Crop face
            
            # Skip small face crops
            if face_crop.shape[0] < 10 or face_crop.shape[1] < 10:
                continue
            
            preprocessed_face_crop = preprocessing_face_croped(face_crop)
            model = loading_model()
            conf = model.predict(preprocessed_face_crop)[0]
            idx = np.argmax(conf)
            label_1 = classes[idx]
            label = "{}: {:.2f}%".format(label_1, conf[idx] * 100)
            Y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.putText(frame, label, (startX, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)  # Display label

        # Convert frame to RGB for Streamlit display
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Display the frame in Streamlit UI
        frame_placeholder.image(frame, channels="RGB")

        # Check for user input to stop the capture
        if stop_button_pressed:
            captured_image = frame.copy()
            captured_label = label_1
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

    return captured_label, captured_image

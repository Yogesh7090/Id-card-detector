import cv2 
import cvlib as cv
import numpy as np
from keras.preprocessing.image import img_to_array 
# from keras.preprocessing.image import  
# from keras.utils.image_utils import img_to_array
# from keras.utils import img_to_array
from keras.models import load_model
# import keras
import streamlit as st

def loading_model(): 
        model = load_model('GenDet.h5')
        # model = keras.layers.TFSMLayer('GenDet.model', call_endpoint='serving_default')
        return model
    
def preprocessing_face_croped(face_crop):
    # Preprocessing for gender detection model
        face_crop = cv2.resize(face_crop, (96, 96))
        face_crop = face_crop.astype("float") / 255.0
        face_crop = img_to_array(face_crop)
        face_crop = np.expand_dims(face_crop, axis=0)
        return face_crop
    
def capture_image_from_webcam():
    # Initialize webcam
    videoSource = 0
    cap = cv2.VideoCapture(videoSource)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        st.error("Error: Could not open webcam.")
        return

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

        # Perform face detection and gender classification
        face, confidence = cv.detect_face(frame)
        
        for idx, f in enumerate(face):
            startX, startY, endX, endY = f
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            face_crop = frame[startY:endY, startX:endX]
            
            if face_crop.shape[0] < 10 or face_crop.shape[1] < 10:
                continue
            
            preprocessed_face_crop = preprocessing_face_croped(face_crop)
            model = loading_model()
            conf = model.predict(preprocessed_face_crop)[0]
            idx = np.argmax(conf)
            label_1 = classes[idx]
            label = "{}: {:.2f}%".format(label_1, conf[idx] * 100)
            Y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.putText(frame, label, (startX, Y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Convert frame to RGB (Streamlit requires RGB format)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Display the frame in Streamlit UI
        frame_placeholder.image(frame, channels="RGB")

        # Check for user input to stop
        if stop_button_pressed:
            captured_image = frame.copy()
            captured_label = label_1
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

    return captured_label, captured_image

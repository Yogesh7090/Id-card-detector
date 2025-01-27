import streamlit as st
# from cv2 import cv2 # Uncomment if using OpenCV functions
from utils.image_processing import capture_image_from_webcam
from utils.text_extraction import extract_text_from_image
from utils.face_recognition import detect_faces, update_face_data_and_db
from utils.openai_integration import process_text_with_openai
from utils.database_operations import create_table_if_not_exists, fetch_all_data
from logo import add_logo
import pandas as pd

def load_css():
    """
    Loads custom CSS styles for the Streamlit application.
    """
    with open(r'D:\id card reader\AD_id_card_detector\utils\styles.css', "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

# Add the logo to the app
add_logo()

# Title for the Streamlit app
st.markdown('<h1 class="custom-title">ID Card Detector Tool!</h1>', unsafe_allow_html=True)

# Create the database table if it doesn't exist
create_table_if_not_exists()

# Header prompting the user to show their ID card
st.header('Please show your ID Card here')

# Capture image from the webcam when the button is clicked
label_1, image = capture_image_from_webcam()

# If an image was captured successfully, proceed with processing
if image is not None:
    # Extract text from the captured image
    text = extract_text_from_image(image)

    # Use OpenAI to process the extracted text and obtain the name
    query = "Extract the name from the following text and provide it as name only."
    name = process_text_with_openai(text, query)
    st.write("Detected Name:", name.strip())

    # Perform face detection and recognition on the captured image
    face_encodings = detect_faces(image)
    
    # Update the database with the detected face data and extracted name
    update_face_data_and_db(face_encodings, name, gender=label_1, image=image)

    # Notify the user that the information has been updated successfully
    st.success("Information updated successfully!")

    # Fetch all data from the database and display it in a styled HTML table
    data = fetch_all_data()
    load_css()
    
    html_table = "<table border='3px'>"
    html_table += "<tr>"

    # Add table headers
    for keys in data[0].keys():
        html_table += f"<th>{keys}</th>"

    html_table += "</tr>"

    # Add table rows with data
    for datum in data:
        html_table += "<tr>"
        for values in datum.values():
            html_table += f"<td>{values}</td>"
        html_table += "</tr>"

    html_table += "</table>"
 
    st.markdown(html_table, unsafe_allow_html=True)

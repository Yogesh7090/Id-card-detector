import streamlit as st
# import cv2
from utils.image_processing import capture_image_from_webcam
from utils.text_extraction import extract_text_from_image
from utils.face_recognition import detect_faces, update_face_data_and_db
from utils.openai_integration import process_text_with_openai
from utils.database_operations import create_table_if_not_exists, fetch_all_data
from logo import add_logo
import pandas as pd


def load_css():
    with open(r'D:\id card reader\id_card_demo_01\utils\styles.css', "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

add_logo()
st.markdown('<h1 class="custom-title">ID Card Detector Tool!</h1>', unsafe_allow_html=True)

# Create the table if it doesn't exist
create_table_if_not_exists()
st.header('Please show your ID Card here')
# if st.sidebar.button("Capture Image"):
label_1, image = capture_image_from_webcam()

if image is not None:
    # st.image(image, caption="Captured Image")
    
    text = extract_text_from_image(image)

    query = "Extract the name from the following text and provide it as name only."
    name = process_text_with_openai(text, query)
    st.write("Detected Name:", name.strip())
    print(f'{image=}')
    face_encodings = detect_faces(image)
    print(f'{face_encodings =}')
    update_face_data_and_db(face_encodings, name,gender = label_1, image=image)

    st.success("Information updated successfully!")

    # if st.sidebar.button("Show Database"):
    data = fetch_all_data()
    
    load_css()
    html_table = "<table border='3px'>"
    html_table += "<tr>"

    for keys in data[0].keys():
        html_table += f"<th>{keys}</th>"

    html_table += "</tr>"

    for datum in data:
        html_table += "<tr>"
        for values in datum.values():
            html_table += f"<td>{values}</td>"
        html_table += "</tr>"

    html_table += "</table>"
 
    st.markdown(html_table, unsafe_allow_html=True)




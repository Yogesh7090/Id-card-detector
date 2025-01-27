import json
import os
import uuid
from datetime import datetime
import face_recognition
from .database_operations import save_data_to_db
import cv2
import numpy as np

# Path constants
JSON_FILE = 'face_data.json'
CAPTURED_IMAGES_DIR = 'captured_images'

# Create the captured images directory if it doesn't exist
if not os.path.exists(CAPTURED_IMAGES_DIR):
    os.makedirs(CAPTURED_IMAGES_DIR)

def load_face_data():
    """
    Loads face data from a JSON file.

    Returns:
    - dict: A dictionary with face IDs as keys and face data as values.
    """
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {JSON_FILE} is empty or corrupted. Reinitializing it.")
            return {}
    else:
        return {}

def save_face_data(face_data):
    """
    Saves face data to a JSON file.

    Parameters:
    - face_data (dict): A dictionary with face IDs as keys and face data as values.
    """
    try:
        with open(JSON_FILE, 'w') as f:
            json.dump(face_data, f, indent=4)
    except Exception as e:
        print(f"Error saving face data: {e}")

def detect_faces(image):
    """
    Detects faces and their encodings from an image.

    Parameters:
    - image (numpy.ndarray): The image in which to detect faces.

    Returns:
    - list: A list of face encodings detected in the image.
    """
    face_locations = face_recognition.face_locations(image)
    return face_recognition.face_encodings(image, face_locations)

def save_image(image, face_id):
    """
    Saves an image to a file with the given face ID.

    Parameters:
    - image (numpy.ndarray): The image to save.
    - face_id (str): The unique ID to use for the filename.

    Returns:
    - str: The file path where the image was saved.
    """
    filename = f"{face_id}.jpg"
    filepath = os.path.join(CAPTURED_IMAGES_DIR, filename)
    cv2.imwrite(filepath, image)
    return filepath

def update_face_data_and_db(face_encodings, name, gender=None, image=None):
    """
    Updates face data and the database with detected faces.

    Parameters:
    - face_encodings (list): A list of face encodings detected in the image.
    - name (str): The name associated with the detected faces.
    - gender (str, optional): The gender associated with the detected faces.
    - image (numpy.ndarray, optional): The image containing the detected faces.
    """
    face_data = load_face_data()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_face_data = {}
    new_entries = []
    update_entries = []

    print('Before processing, face data:', face_data)

    for face_encoding in face_encodings:
        found_match = False
        
        # Compare face encodings to find a match
        for face_id, data in list(face_data.items()):  # Convert to list to avoid RuntimeError
            if face_recognition.compare_faces([data['face_encoding']], face_encoding, tolerance=0.6)[0]:
                found_match = True
                print('Matching person found.')
                
                if data['action'] == 'in':
                    # Update existing record
                    data['out_time'] = now
                    data['action'] = "out"
                    in_time = datetime.fromisoformat(data['in_time'])
                    out_time = datetime.fromisoformat(data['out_time'])
                    duration_seconds = (out_time - in_time).total_seconds()
                    duration_minutes = duration_seconds / 60
                    data['duration'] = round(duration_minutes, 2)
                    
                    update_entries.append((face_id, name, gender, data['in_time'], now, "out", data['duration']))
                break
        
        if not found_match:
            # Handle new face
            new_face_id = str(uuid.uuid4())
            print('New person detected.')
            if image is not None:
                save_image(image, new_face_id)
                
            new_face_data[new_face_id] = {
                'face_encoding': face_encoding.tolist(),  # Convert numpy array to list for JSON serialization
                'name': name,
                'gender': gender,
                'in_time': now,
                'out_time': None,
                'action': "in",
                'duration': 0
            }
            new_entries.append((new_face_id, name, gender, now, None, "in", 0))
    
    # Update face_data with new faces
    face_data.update(new_face_data)
    save_face_data(face_data)
    
    # Save updates to the database
    if update_entries:
        save_data_to_db(update_entries, update=True)
    
    # Save new entries to the database
    if new_entries:
        save_data_to_db(new_entries, update=False)

import easyocr

def extract_text_from_image(image):
    reader = easyocr.Reader(['en'])  # Change languages as needed
    result = reader.readtext(image)
    return ' '.join([res[1] for res in result])

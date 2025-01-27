import easyocr

def extract_text_from_image(image):
    """
    Extracts text from an image using EasyOCR.

    This function initializes an EasyOCR reader with English language support,
    processes the input image to extract text, and returns the combined text as a single string.

    Parameters:
    - image (str or numpy.ndarray): The image file path or image array from which to extract text.

    Returns:
    - str: The extracted text combined into a single string.
    """
    # Initialize EasyOCR reader with English language
    reader = easyocr.Reader(['en'])  # You can add other languages as needed
    
    # Perform text extraction
    result = reader.readtext(image)
    
    # Combine all extracted text into a single string
    extracted_text = ' '.join([res[1] for res in result])
    
    return extracted_text

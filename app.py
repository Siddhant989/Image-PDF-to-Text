import streamlit as st
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import util  # Ensure this util module is correctly defined

POPPLER_PATH = r'C:\poppler-24.02.0\Library\bin'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract(file_path):
    document_text = ''

    try:
        if file_path.endswith('.pdf'):
            pages = convert_from_path(file_path, poppler_path=POPPLER_PATH)
            for i, page in enumerate(pages):
                processed_image = util.preprocess_image(page)
                text = pytesseract.image_to_string(processed_image, lang='eng')
                document_text += f'\nPage {i + 1}:\n' + text
        else:
            image = Image.open(file_path)
            processed_image = util.preprocess_image(image)
            text = pytesseract.image_to_string(processed_image, lang='eng')
            document_text = text
    except Exception as e:
        st.error(f"Error extracting text: {e}")

    return document_text


def main():
    st.title('Document Text Extraction')

    uploaded_file = st.file_uploader("Choose an image or PDF file", type=["jpg", "jpeg", "png", "pdf"])

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1]
        file_path = f"temp_file.{file_extension}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        extracted_text = extract(file_path)
        st.text_area("Extracted Text", extracted_text, height=300)


if __name__ == "__main__":
    main()


import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import sympy as sp

st.title("Mr Wright AI Maths Marker")

uploaded_file = st.file_uploader("Upload a photo of the student's work", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert image to numpy array for EasyOCR
    image_np = np.array(image)

    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'], gpu=False)

    with st.spinner("Reading text from image..."):
        try:
            results = reader.readtext(image_np)
            extracted_text = " ".join([text for (_, text, _) in results])
        except Exception as e:
            extracted_text = ""
            st.error(f"OCR failed: {e}")

    if extracted_text:
        st.subheader("Extracted Text")
        st.write(extracted_text)

        # Try to parse and evaluate math expressions
        st.subheader("Math Evaluation")
        try:
            expr = sp.sympify(extracted_text)
            result = sp.simplify(expr)
            st.success(f"Result: {result}")
        except Exception as e:
            st.warning(f"Could not evaluate expression: {e}")
    else:
        st.warning("No text could be extracted from the image.")

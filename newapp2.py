
import streamlit as st
from PIL import Image
import easyocr
import numpy as np
from sympy import sympify, Eq, solve
import re

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

st.title("🧠 Mr Wright AI Maths Marker")

uploaded_file = st.file_uploader("Upload an image of the student's work", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Reading text from image..."):
        try:
            image_np = np.array(image)
            results = reader.readtext(image_np)
            extracted_lines = [text for (_, text, _) in results]
        except Exception as e:
            st.error(f"❌ OCR failed: {e}")
            extracted_lines = []

    if extracted_lines:
        st.subheader("📄 Extracted Text")
        for line in extracted_lines:
            st.text(line)

        st.subheader("🧮 Evaluation Results")
        for line in extracted_lines:
            # Filter for lines that look like math expressions
            if re.search(r"[=+\-*/^0-9a-zA-Z]", line):
                try:
                    # Try to parse and evaluate the expression
                    expr = sympify(line)
                    result = solve(expr) if isinstance(expr, Eq) else expr
                    st.success(f"{line} ⟶ {result}")
                except Exception as e:
                    st.warning(f"⚠️ Could not evaluate: '{line}' — {e}")
    else:
        st.warning("⚠️ No text could be extracted from the image.")

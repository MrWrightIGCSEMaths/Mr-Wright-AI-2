import streamlit as st
import pytesseract
from PIL import Image
import sympy as sp
import re

st.set_page_config(page_title="Mr Wright AI – Maths Work Marker", layout="centered")

st.title("🧠 Mr Wright AI – Maths Work Marker")
st.write("Upload a photo of your IGCSE Maths working and I’ll mark it just like Mr Wright would.")

uploaded_file = st.file_uploader("📤 Upload your handwritten maths work", type=["png", "jpg", "jpeg"])

def clean_expression(expr):
    expr = expr.lower()
    expr = re.sub(r"(solve for|simplify|factor|expand|find|calculate|work out|=\s*)", "", expr)
    expr = expr.replace("^", "**")
    return expr.strip()

def solve_expression(expr):
    x = sp.symbols('x')
    try:
        if "=" in expr:
            lhs, rhs = expr.split("=")
            eq = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
            sol = sp.solve(eq, x)
            return f"Solving equation: {expr}\nSolution: {sol}"
        else:
            simplified = sp.simplify(expr)
            expanded = sp.expand(expr)
            factored = sp.factor(expr)
            return f"Expression: {expr}\nSimplified: {simplified}\nExpanded: {expanded}\nFactored: {factored}"
    except Exception as e:
        return f"Error solving expression: {expr}\n{e}"

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Work", use_column_width=True)

    st.subheader("🔍 Extracted Text")
    ocr_text = pytesseract.image_to_string(image)
    st.code(ocr_text)

    st.subheader("🧠 Re-solved Maths")
    lines = [line.strip() for line in ocr_text.split("\n") if line.strip()]
    cleaned_lines = [clean_expression(line) for line in lines]
    for line in cleaned_lines:
        if line:
            st.text(solve_expression(line))
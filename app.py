import streamlit as st
from PIL import Image
import cv2
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import tempfile
import os

st.set_page_config(page_title="Document Scanner", layout="centered")

st.title("📄 Adobe Scan Style Document Scanner")
st.write("Upload an image/document, convert it to black & white, and download it as a PDF.")

uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["png", "jpg", "jpeg"]
)


def convert_to_bw(image):
    """Convert image to black and white like a scanned document."""
    img_np = np.array(image)

    # Convert RGB to BGR for OpenCV
    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    # Apply adaptive threshold for scanner effect
    scanned = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return scanned


if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    if st.button("Convert to Scanned PDF"):
        bw_image = convert_to_bw(image)

        st.subheader("Scanned Black & White Image")
        st.image(bw_image, clamp=True, use_container_width=True)

        # Save processed image temporarily
        temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        cv2.imwrite(temp_img.name, bw_image)

        # Create PDF
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

        c = canvas.Canvas(temp_pdf.name, pagesize=letter)
        width, height = letter

        img_reader = ImageReader(temp_img.name)

        # Fit image to page
        c.drawImage(img_reader, 30, 80, width=width - 60, height=height - 120)
        c.save()

        # Download button
        with open(temp_pdf.name, "rb") as pdf_file:
            st.download_button(
                label="⬇ Download PDF",
                data=pdf_file,
                file_name="scanned_document.pdf",
                mime="application/pdf"
            )

        # Cleanup
        os.unlink(temp_img.name)
        os.unlink(temp_pdf.name)

st.markdown("---")
st.markdown("### Requirements.txt")
st.code(
"""streamlit
pillow
opencv-python-headless
numpy
reportlab""",
language="text"
)

st.markdown("### Run Locally")
st.code(
"""pip install -r requirements.txt
streamlit run app.py""",
language="bash"
)

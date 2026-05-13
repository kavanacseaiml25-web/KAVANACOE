import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO

# Page Config
st.set_page_config(page_title="QR Code Generator")

st.title("🔳 QR Code Generator")

# User Input
data = st.text_input("Enter text or URL")

if st.button("Generate QR Code"):

    if data.strip() == "":
        st.warning("Please enter some text or URL")
    else:
        # Create QR Code
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Display Image
        st.image(img, caption="Generated QR Code")

        # Save image to bytes
        buffer = BytesIO()
        img.save(buffer, format="PNG")

        # Download Button
        st.download_button(
            label="⬇ Download QR Code",
            data=buffer.getvalue(),
            file_name="qrcode.png",
            mime="image/png"
        )

import streamlit as st
from PIL import Image
import tensorflow

st.set_page_config(page_title="Lost on Clayton Campus", page_icon="📍", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background-color: #8B6AD9;
    }

    .upload-header {
        text-align: center;
        padding: 2rem 0 1rem;
    }
    .upload-header h1 {
        color: #26215C;
        font-size: 2rem;
        font-weight: 600;
    }
    .upload-header p {
        color: black;
        font-size: 1rem;
    }
    .stFileUploader {
        background: #EEEDFE;
        border: 2px dashed #AFA9EC;
        border-radius: 16px;
        padding: 1rem;
    }
    .stButton > button {
        background-color: #7F77DD;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 500;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #534AB7;
        color: white;
    }
    .metric-container {
        background: white;
        border-radius: 12px;
        border: 1px solid #D3D1C7;
        padding: 1rem;
        text-align: center;
    }
    .result-box {
        background: white;
        border-radius: 12px;
        border: 1px solid #D3D1C7;
        padding: 1.25rem;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# header
st.markdown("""
    <div class="upload-header">
        <h1>📍Lost on Clayton Campus</h1>
        <p>Upload an image and let the model do the rest</p>
    </div>
""", unsafe_allow_html=True)

# upload
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", width=700)

    # stats row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Width", f"{image.width}px")
    with col2:
        st.metric("Height", f"{image.height}px")
    with col3:
        st.metric("Format", image.format or "PNG")

    # placeholder for model results
    st.markdown("### Predictions")
    st.info("Model output will appear here once connected.")

else:
    st.markdown("""
        <div style='text-align:center; color:black; padding: 1rem;'>
            Supported formats: JPG, PNG, WEBP
        </div>
    """, unsafe_allow_html=True)
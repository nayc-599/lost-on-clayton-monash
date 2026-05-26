import streamlit as st
from PIL import Image
import pandas as pd
from loc_locations import locations
import pydeck as pdk
import torch
from torchvision import transforms, models

def page_setup():
    st.set_page_config(page_title="Lost on Clayton Campus", page_icon="📍", layout="centered")
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #ffffff;
    }
    .stApp {
        background-color: #1a0a2e;
    }
    .upload-header {
        text-align: center;
        padding: 2rem 0 1rem;
    }
    .upload-header h1 {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 600;
    }
    .upload-header p {
        color: #c4b5fd;
        font-size: 1rem;
    }
    .stFileUploader {
        background: #2d1b4e;
        border: 2px dashed #7c3aed;
        border-radius: 16px;
        padding: 1rem;
    }
    .stButton > button {
        background-color: #67288E;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 500;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #6d28d9;
        color: white;
    }
    .metric-container {
        background: #2d1b4e;
        border-radius: 12px;
        border: 1px solid #4c1d95;
        padding: 1rem;
        text-align: center;
        color: #ffffff;
    }
    .result-box {
        background: #2d1b4e;
        border-radius: 12px;
        border: 1px solid #4c1d95;
        padding: 1.25rem;
        margin-top: 1rem;
        color: #ffffff;
    }
    .stMetric {
        background: #2d1b4e;
        border-radius: 12px;
        border: 1px solid #4c1d95;
        padding: 1rem;
    }
    .stMetric label {
        color: #c4b5fd !important;
    }
    .stMetric div {
        color: #ffffff !important;
    }
    h1, h2, h3, h4, p {
        color: #ffffff !important;
    }
    .stSuccess {
        background-color: #2d1b4e;
        color: #a78bfa !important;
        border: 1px solid #7c3aed;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="upload-header">
        <h1>✦ Lost on Clayton Campus</h1>
        <p>Upload an image to find where you are on campus!</p>
    </div>
""", unsafe_allow_html=True)


def upload_image():
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png", "webp"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded image", width=700)

        # stats row
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Width", f"{image.width}px")
        with col2:
            st.metric("Height", f"{image.height}px")
        with col3:
            st.metric("Format", image.format or "PNG")

    
        return image, uploaded_file

    else:
        st.markdown("""
            <div style='text-align:center; color:#888780; padding: 1rem;'>
                Supported formats: JPG, PNG, WEBP
            </div>
        """, unsafe_allow_html=True)
        return None, None

@st.cache_resource
def load_model():
    model = models.resnet18(weights=None)
    model.fc = torch.nn.Linear(model.fc.in_features, 11)
    model.load_state_dict(torch.load("model_pytorch.pth", map_location="cpu"))
    model.eval()
    return model

def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)

def predict(model, tensor):
    with torch.no_grad():
        output = model(tensor) 
        predicted_index = output.argmax(dim=1).item()
        return locations[predicted_index]["name"]

def find_location_name(name):
    for location in locations:
        if location["name"] == name:
            matched = location
            break
    return matched

def build_map(matched):
    st.success(f"Predicted location: {matched['name']}")

    df = pd.DataFrame([{
        "lat": matched["lat"], 
        "lon": matched["lon"], 
        "name": matched["name"],
        "icon": "pin"
    }])

    icon_data = {
        "url": "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 24 24'%3E%3Cpath fill='red' d='M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z'/%3E%3C/svg%3E",
        "width": 32,
        "height": 32,
        "anchorY": 32
    }

    df["icon_data"] = [icon_data]

    st.pydeck_chart(pdk.Deck(
        map_style="road",
        initial_view_state=pdk.ViewState(
            latitude=matched["lat"],
            longitude=matched["lon"],
            zoom=15
        ),
        layers=[
            pdk.Layer(
                "IconLayer",
                data=df,
                get_position="[lon, lat]",
                get_icon="icon_data",
                get_size=5,
                size_scale=8,
                pickable=True
            )
        ],
        tooltip={"text": "📍 {name}"}
    ))


page_setup()
model = load_model()
image, uploaded_file = upload_image()

if uploaded_file is not None:
    tensor = preprocess_image(image)
    ai_result = predict(model, tensor)
    matched = find_location_name(ai_result)
    build_map(matched)


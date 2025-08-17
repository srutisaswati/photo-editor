import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('models/gemini-1.5-flash')

# --- Utility Functions ---
def load_image(image_file):
    image = Image.open(image_file).convert('RGB')
    return np.array(image)

def apply_brightness(image, value):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)
    v = np.clip(v + value, 0, 255).astype(np.uint8)
    final_hsv = cv2.merge((h, s, v))
    return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2RGB)

def apply_resize(image, width, height):
    return cv2.resize(image, (width, height))

def apply_text_overlay(image, text, position, font_size=32):
    pil_img = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_img)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    draw.text(position, text, fill=(255, 255, 255), font=font)
    return np.array(pil_img)

def apply_black_white(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

def apply_highlight(image):
    return cv2.convertScaleAbs(image, alpha=1.2, beta=10)

def apply_filter(image, filter_type):
    if filter_type == "Sunny":
        return cv2.convertScaleAbs(image, alpha=1.1, beta=30)
    elif filter_type == "Cool":
        cool = image.copy()
        cool[..., 0] = np.clip(cool[..., 0] + 30, 0, 255)
        return cool
    elif filter_type == "Warm":
        warm = image.copy()
        warm[..., 2] = np.clip(warm[..., 2] + 30, 0, 255)
        return warm
    elif filter_type == "Dreamy":
        blur = cv2.GaussianBlur(image, (15, 15), 10)
        return cv2.addWeighted(image, 0.5, blur, 0.5, 0)
    elif filter_type == "Moody":
        return cv2.convertScaleAbs(image, alpha=0.8, beta=-30)
    return image

def generate_caption(image_np):
    img_pil = Image.fromarray(image_np)
    buffer = io.BytesIO()
    img_pil.save(buffer, format="PNG")
    buffer.seek(0)

    response = model.generate_content([
    "Give a short Instagram-style caption for this image:",
    {"mime_type": "image/png", "data": buffer.getvalue()}
])
    return response.text.strip()

# --- Streamlit UI ---
st.set_page_config(layout="wide")
st.title("📸 Smart Photo Editor with Gemini AI 🪻")

with st.sidebar:
    st.header(" Upload & Controls")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    edit_mode = st.radio("Select Mode", ["Basic Edits", "Color & Lighting", "Advanced Tools", "Text & Overlay", "Export"])

if uploaded_file:
    image = load_image(uploaded_file)
    result = image.copy()

    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Original Image", use_container_width=True)
    with col2:
        st.image(result, caption="Live Preview", use_container_width=True)

    if edit_mode == "Basic Edits":
        st.subheader("🧰 Basic Edits")
        new_name = st.text_input("Rename Image")
        if st.checkbox("Convert to B/W"):
            result = apply_black_white(result)
        width = st.slider("Resize Width", 50, 1000, result.shape[1])
        height = st.slider("Resize Height", 50, 1000, result.shape[0])
        if st.button("Apply Resize"):
            result = apply_resize(result, width, height)

    elif edit_mode == "Color & Lighting":
        st.subheader("🎨 Adjust Lighting")
        value = st.slider("Brightness", -100, 100, 0)
        result = apply_brightness(result, value)
        st.subheader("✨ Apply Mood Filter")
        mood_option = st.selectbox("Choose Mood Filter", ["None", "Sunny", "Cool", "Warm", "Dreamy", "Moody"])
        if mood_option != "None":
            result = apply_filter(result, mood_option)

    elif edit_mode == "Advanced Tools":
        st.subheader("🔆 Highlight Image")
        if st.button("Apply Highlight"):
            result = apply_highlight(result)

    elif edit_mode == "Text & Overlay":
        st.subheader(" Text Overlay")
        text = st.text_input("Enter Text", "Hello World!")
        x = st.slider("X Position", 0, result.shape[1], 10)
        y = st.slider("Y Position", 0, result.shape[0], 10)
        font_size = st.slider("Font Size", 10, 100, 32)
        if st.button("Apply Text"):
            result = apply_text_overlay(result, text, (x, y), font_size)

    elif edit_mode == "Export":
        st.subheader(" Caption & Music")
        if st.button("Generate Caption"):
            try:
                caption = generate_caption(result)
                st.success("✨ Caption:")
                st.markdown(f"**\"{caption}\"**")
            except Exception as e:
                st.error(f" Caption generation failed: {str(e)}")

        if st.button("Suggest Songs"):
            try:
                img_pil = Image.fromarray(result)
                buffer = io.BytesIO()
                img_pil.save(buffer, format="PNG")
                buffer.seek(0)

                response = model.generate_content([
                "Suggest 3 songs that match the mood or vibe of this image:",
                {"mime_type": "image/png", "data": buffer.getvalue()}
                ])
                songs = response.text.strip()
                st.success("🎶 Songs Suggested:")
                st.markdown(songs)
            except Exception as e:
                st.error(f" Song suggestion failed: {str(e)}")

        st.download_button(" Download Edited Image", data=cv2.imencode('.png', cv2.cvtColor(result, cv2.COLOR_RGB2BGR))[1].tobytes(), file_name="edited_image.png", mime="image/png")

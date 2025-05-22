import streamlit as st
import torch
from torchvision import transforms
from PIL import Image
import random, json, os
import matplotlib.pyplot as plt
from fpdf import FPDF

# ---- Setup ----
st.set_page_config(page_title="StylePulse AI", layout="wide")
st.title("🧥 StylePulse AI – Fashion Trend Analyzer & Outfit Generator")

# ---- Load Dummy Suggestions ----
with open("style_data/suggestions.json") as f:
    style_suggestions = json.load(f)

category_labels = list(style_suggestions.keys())

# ---- Preprocessing ----
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def predict_category(image):
    # Mock prediction - replace with actual model later
    return random.choice(category_labels)

def generate_caption(category):
    templates = {
        "casual": "Chilling in comfy casuals today! 😎",
        "formal": "Suited up for success! 👔",
        "sporty": "Power up with my sporty style! 🏋️",
        "party": "Shining through the party night! ✨",
        "traditional": "Rooted in tradition, styled for today. 🧵"
    }
    return templates.get(category, "Styled by StylePulse AI!")

def export_pdf(category, recommendations):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"StylePulse Outfit Guide - {category.title()} Look", ln=True)
    pdf.ln()
    for item in recommendations:
        pdf.cell(200, 10, f"- {item}", ln=True)
    output_path = "style_guide.pdf"
    pdf.output(output_path)
    return output_path

# ---- Upload Section ----
uploaded_file = st.file_uploader("Upload your fashion image", type=["jpg", "png", "jpeg"])
trend_tracker = st.session_state.get("trend", {})

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Look", use_column_width=True)

    category = predict_category(image)
    st.success(f"Predicted Style Category: **{category.upper()}**")

    # Track trends
    trend_tracker[category] = trend_tracker.get(category, 0) + 1
    st.session_state.trend = trend_tracker

    # Style Suggestions
    st.subheader("🛍️ Suggested Outfit Pieces")
    suggestions = style_suggestions[category]
    st.write(", ".join(suggestions))

    # Style Caption
    st.subheader("📸 Style Caption")
    caption = generate_caption(category)
    st.text_area("Suggested Caption:", caption, height=70)

    # Hashtags
    hashtags = "#StylePulseAI #FashionTrends"
    st.text_area("Suggested Hashtags:", hashtags, height=70)

    # Downloadable Style Guide
    pdf_path = export_pdf(category, suggestions)
    with open(pdf_path, "rb") as f:
        st.download_button("📄 Download Style Guide (PDF)", f, file_name="style_guide.pdf")

# ---- Trend Visualization ----
if trend_tracker:
    st.subheader("📊 Popular Style Categories")
    fig, ax = plt.subplots()
    ax.bar(trend_tracker.keys(), trend_tracker.values(), color='teal')
    ax.set_ylabel("Count")
    st.pyplot(fig)

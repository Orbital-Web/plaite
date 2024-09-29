import av
import numpy as np
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from streamlit_webrtc import webrtc_streamer

from plaite.food_detect import DetectionResult, detect

st.sidebar.image("./web/plAIte.png", use_column_width=True, caption="plAIte")
st.title("Welcome to plaite!")
st.write("Scan your food to get nutritional information.")


def video_callback(frame):
    img = frame.to_image()
    results = detect(np.array(img))
    img = draw_bbox(img, results)
    return av.VideoFrame.from_image(img)


def draw_bbox(image: Image, results: list[DetectionResult]) -> Image:
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    for result in results:
        x1, y1, x2, y2 = result["bbox"]

        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

        # Draw the label and confidence
        text = f"{result['label']} ({result['confidence']:.2f})"
        text_size = draw.textsize(text, font=font)
        draw.text((x1, y1 - text_size[1]), text, fill="white", font=font)

    return image


foodcam = webrtc_streamer(key="foodcam", video_frame_callback=video_callback)
modes = ["Barcode Scanner", "Food Scanner"]
option = st.radio("Choose a mode:", modes)

st.write(f"You selected: {option}")

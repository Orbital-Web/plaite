import os

import av
import numpy as np
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from streamlit_webrtc import webrtc_streamer

from plaite.food_detect import DetectionResult, detect

st.set_page_config(layout="wide")

style = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #395E66;
}

[data-testid="stSidebar"] {
    background-color: #204E4A;
}

[data-testid="stHeader"] {
    background-color: #395E66;
}

[data-testid="stToolbar"] {
    background-color: #395E66;
    color: white;
}

header {
    background-color: #395E66;
}
</style>
"""

st.markdown(style, unsafe_allow_html=True)

st.sidebar.image("./web/plAIte.png", use_column_width=True, caption="plAIte")
st.title("Welcome to plaite!")
st.write("Scan your food to get nutritional information.")

if st.sidebar.toggle("Developer Mode", False):
    if st.sidebar.button("[DEBUG] Clear food.txt"):
        with open("food.txt", "w") as ff:
            ff.write("")
        st.sidebar.success("File contents cleared!")

    if st.sidebar.button("[DEBUG] Write to food.txt"):
        with open("food.txt", "w") as file:
            file.write("apple,pineapple")
        st.sidebar.success("Written 'apple,pineapple' to food.txt!")

    with open("food.txt", "r") as file:
        food_contents = file.read()
    st.sidebar.write("Food.txt contents:")
    st.sidebar.write(food_contents)


def write_food_to_file(detected_food: str, file_path: str = "food.txt"):
    # Check if file exists and read its contents
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            contents = file.read().strip()
        # Convert contents to a list of food items
        existing_foods = contents.split(",") if contents else []
    else:
        existing_foods = []

    # If detected food is not in the file, append it
    if detected_food not in existing_foods:
        with open(file_path, "a") as file:
            if existing_foods:
                file.write(f",{detected_food}")
            else:
                file.write(detected_food)


def video_callback(frame):
    img = frame.to_image()
    # img = img.transpose(Image.FLIP_LEFT_RIGHT)
    results = detect(np.array(img))
    img = draw_bbox(img, results)

    for result in results:
        detected_food = result["label"]
        write_food_to_file(detected_food)
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


foodcam = webrtc_streamer(
    key="foodcam",
    video_frame_callback=video_callback,
    sendback_audio=False,
    media_stream_constraints={
        "video": {
            "facingMode": "environment"  # 'user' for front camera, 'environment' for rear camera
        },
        "audio": False,
    },
)

# if st.button("Go to Info!"):
#     switch_page("info")

# if st.button("Go to LLM!"):
#     switch_page("chat")

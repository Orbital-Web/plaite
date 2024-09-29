import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_APIKEY"))
st.set_page_config(layout="wide")
food_file_path = "./food.txt"
if os.path.exists(food_file_path):
    with open(food_file_path, "r") as file:
        food_data = file.read().strip()
else:
    food_data = ""

input_bg_color = """
<style>
[data-testid="stEmotionCache"] {
    background-color: #395E66;
    color: white;
}

input {
    background-color: #395E66;
    color: white;
}

textarea {
    background-color: #395E66;
    color: white;
}

button {
    background-color: #204E4A;
    color: white;
}
</style>
"""

header_toolbar_bg_color = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #395E66; 
}
</style>

<style>
[data-testid="stSidebar"] {
    background-color: #204E4A;
}
</style>

<style>
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

.stButton > button {
    background-color: white;
    color: black;           
    border: 1px solid #204E4A; 
    border-radius: 5px;    
    transition: background-color 0.3s ease; 
}

.stButton > button:hover {
    background-color: #d9d9d9; 
    color: #395E66;
    border-color: #395E66
}

</style>
"""
st.markdown(header_toolbar_bg_color, unsafe_allow_html=True)

bottom_block_bg_color = """
<style>
[data-testid="stBottomBlockContainer"] {
    background-color: #395E66;
}
</style>
"""
st.markdown(bottom_block_bg_color, unsafe_allow_html=True)

st.sidebar.image("./web/plAIte.png", use_column_width=True, caption="plAIte")
st.title("NomNom Chatbot, powered by OpenAI GPT-4o")

if st.sidebar.button("Clear chat"):
    st.session_state.messages = []
    st.session_state.food_response_given = False

st.sidebar.markdown(
    """
    NomNom Assistant is your friendly pal to help you with your food queries!
    """
)

if st.sidebar.toggle("Developer Mode", False):
    if st.sidebar.button("[DEBUG] Clear food.txt"):
        with open("food.txt", "w") as ff:
            ff.write("")
        st.sidebar.success("File contents cleared!")

    if st.sidebar.button("[DEBUG] Write to food.txt"):
        with open("food.txt", "w") as file:
            file.write("apple,pineapple")
        st.sidebar.success("Written 'apple,pineapple' to food.txt!")


if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.food_response_given = False
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": "Hello, I am the NomNom Assistant. I am here to help you with your questions.",
        }
    )

if food_data and not st.session_state.food_response_given:
    arr = [
        {
            "role": "system",
            "content": "TOPIC: Food and nutrition. Only answer questions that are directly related to food. Ignore any inquiries, discussions, or topics that are not specifically about food, its preparation, consumption, ingredients, cooking techniques, culinary traditions, or nutrition. Do not provide any information or engage in conversation outside of this context.",
        },
        {
            "role": "user",
            "content": f"Give nutritional advice for the following food items: {food_data}. Go into the a numbered list immediately after this message, do not include any other information or text.",
        },
    ]

    full_response = ""
    for response in client.chat.completions.create(
        model="gpt-4o",
        messages=arr,
        stream=True,
    ):
        full_response += response.choices[0].delta.content or ""

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.session_state.food_response_given = True

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(
    "You can ask ChatGPT to come up with recipe ideas, meal plans, or anything food related."
):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        arr = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        for response in client.chat.completions.create(
            model="gpt-4o",
            messages=arr,
            stream=True,
        ):
            full_response += response.choices[0].delta.content or ""
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

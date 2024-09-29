import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

st.title("NomNom Chatbot, powered by OpenAI GPT-4o")

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_APIKEY"))

# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-4o"

# add clear chat button to sidebar
if st.sidebar.button("Clear chat"):
    st.session_state.messages = []

st.sidebar.markdown(
    """
    The plaite chatbot is your frienly pal to help you with your food queiries.
    """
)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": "Hello, I am the NomNom Assistant. I am here to help you with your questions.",
        }
    )

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
        arr.pop(0)
        arr.insert(
            0,
            {
                "role": "system",
                "content": "TOPIC: Food and nutrition. Only answer questions that are directly related to food. Ignore any inquiries, discussions, or topics that are not specifically about food, its preparation, consumption, ingredients, cooking techniques, culinary traditions, or nutrition. Do not provide any information or engage in conversation outside of this context.",
            },
        )

        for response in client.chat.completions.create(
            # model=st.session_state["openai_model"],
            model="gpt-4o",
            messages=arr,
            stream=True,
        ):
            full_response += response.choices[0].delta.content or ""
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

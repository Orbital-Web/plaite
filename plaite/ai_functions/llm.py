# Interface with OpenAI

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_APIKEY"))

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "You are a food nutritionist helping a user make wise food choices. List only what you are asked and do not provide any additional information.",
        },
        {"role": "user", "content": "How many calories are in a bowl of ramen?"},
    ],
)

print(completion.choices[0].message.content)

"""
Chat Bot Features
"""
import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


def load_as_string(path: str) -> str:
    """
    loads a txt file as a string
    """
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
        return re.sub(r"\s+", " ", data).strip()


ctx_raw = load_as_string("context.txt")

def chatting(message: str):
    """
    chatting
    """
    context = ctx_raw
    support_bot = [
        {
            "role":
            "system",
            "content":
            ("You are Vizcom’s frinedly support assistant. "
            f" Do NOT guess or introduce outside information. Use ONLY the provided context: {context}. \n\n"
            "Answer politely and succinctly. Don't be formal, be cool. ALWAYS Link any relevant reference links for the user in your response \n\n"
            "Return a thought process and citation of the reference link(s) if possible (i.e. how you arrived at the answer and where you found it).\n\n"
            "Return ONLY a JSON object with keys:\n"
            "  • response (string)\n"
            "  • reference link (string)\n"
            "  • thought_process (string)\n\n"
            "Example:\n"
            '{"response": "…", "reference link": …, "thought_process": "…"}'),
        },
        {
            "role": "user",
            "content": message
        },
    ]

    completion = client.chat.completions.create(model="gpt-4o-mini",
                                                messages=support_bot)
    response = json.loads(completion.choices[0].message.content)

    return response.get("response")

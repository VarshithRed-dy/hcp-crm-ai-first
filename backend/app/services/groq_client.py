import os
from typing import List, Dict

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class GroqClientService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

        if not self.api_key:
            raise ValueError("GROQ_API_KEY is missing. Please add it to backend/.env")

        self.client = Groq(api_key=self.api_key)

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 800
    ) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return completion.choices[0].message.content


def get_groq_service():
    return GroqClientService()
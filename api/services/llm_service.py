import os
import requests


class LLMService:
    def __init__(self):
        self.endpoint = os.getenv("MODAL_LLM_URL")
        self.api_key = os.getenv("API_KEY")

    def get_reasoning(self, query: str, context: str):
        payload = {
            "prompt": query,
            "context": context,
            "temperature": 0.1,
            "top_p": 0.9,
            "max_tokens": 1024,
        }

        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

        response = requests.post(
            self.endpoint,
            json=payload,
            headers=headers,
            timeout=90,
        )

        response.raise_for_status()
        return response.json().get("answer")

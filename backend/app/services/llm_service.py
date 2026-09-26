import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLMService:
    """
    Service responsible for communicating with an LLM via OpenRouter.
    """

    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        model = os.getenv("OPENROUTER_MODEL")

        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

        if not model:
            raise ValueError("OPENROUTER_MODEL not found in environment variables.")

        self.model = model

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )

    def generate_response(self, prompt: str) -> str:
        """
        Sends a prompt to the configured LLM and returns its response.
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful AI assistant that answers questions "
                            "accurately and concisely."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.2,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            raise RuntimeError(f"OpenRouter API Error: {e}")
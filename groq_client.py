# groq_client.py
from groq import Groq
import constants  # Import constants

class GroqClient:
    def __init__(self):
        self.client = Groq(api_key=constants.GROQ_API_KEY)
        self.model = constants.MODEL_NAME
        self.temperature = constants.TEMPERATURE
        self.max_tokens = constants.MAX_TOKENS
        self.top_p = constants.TOP_P

    def get_completion(self, message_content):
        """Fetches a streamed response from the Groq LLaMA API"""
        messages = [{"role": "user", "content": message_content}]
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            stream=True,
            stop=None,
        )
        response = ""
        for chunk in completion:
            response_chunk = chunk.choices[0].delta.content or ""
            response += response_chunk
            yield response  # Streaming response for live updates

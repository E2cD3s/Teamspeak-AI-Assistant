import os
import requests
import json
import asyncio
import time

class GeminiClient:
    """A client to interact with the Google Gemini API, now using a key from config."""
    # --- CHANGE: Now accepts api_key from the main script ---
    def __init__(self, system_prompt, api_key):
        self.api_key = api_key
        if not self.api_key or "YOUR_KEY_HERE" in self.api_key:
            raise ValueError("Gemini API key not found or not set in config.json.")

        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.api_key}"
        self.system_prompt = {"role": "user", "parts": [{"text": f"SYSTEM INSTRUCTION: {system_prompt}"}]}
        self.history = [self.system_prompt, {"role": "model", "parts": [{"text": "Understood. I am ready."}]}]

    def _send_request_with_retry(self, payload, max_retries=3):
        # This function is unchanged
        for attempt in range(max_retries):
            try:
                response = requests.post(self.api_url, json=payload)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if e.response is not None and e.response.status_code == 429:
                    if attempt < max_retries - 1:
                        delay = 2 ** attempt
                        print(f"API rate limit hit. Retrying in {delay} second(s)...")
                        time.sleep(delay)
                        continue
                raise e
        raise requests.exceptions.RequestException("API request failed after multiple retries.")

    async def get_response(self, user_prompt):
        # This function is unchanged
        print(f"Sending to Grounded Gemini: '{user_prompt}'")
        self.history.append({"role": "user", "parts": [{"text": user_prompt}]})
        payload = {
            "contents": self.history,
            "tools": [{"google_search": {}}]
        }
        try:
            loop = asyncio.get_event_loop()
            response_data = await loop.run_in_executor(None, self._send_request_with_retry, payload)
            candidate = response_data.get("candidates", [{}])[0]
            content_part = candidate.get("content", {}).get("parts", [{}])[0]
            ai_response = content_part.get("text", "Sorry, I couldn't process that response.")
            self.history.append({"role": "model", "parts": [{"text": ai_response}]})
            print(f"Grounded Gemini responded: '{ai_response}'")
            return ai_response
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            return "I'm having trouble connecting to my brain right now."
        except (KeyError, IndexError) as e:
            print(f"Error parsing API response: {e}")
            return "I received a response, but I couldn't understand it."
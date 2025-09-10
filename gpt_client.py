import os
import openai
import asyncio

class GptClient:
    """A client to interact with the OpenAI GPT-4 API, now using a key from config."""
    # --- CHANGE: Now accepts api_key from the main script ---
    def __init__(self, system_prompt, api_key):
        self.api_key = api_key
        if not self.api_key or "YOUR_KEY_HERE" in self.api_key:
            raise ValueError("OpenAI API key not found or not set in config.json.")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.history = [{"role": "system", "content": system_prompt}]

    async def get_response(self, user_prompt):
        # This function is unchanged
        print(f"Sending to GPT-4: '{user_prompt}'")
        self.history.append({"role": "user", "content": user_prompt})
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=self.history
                )
            )
            ai_response = response.choices[0].message.content
            self.history.append({"role": "assistant", "content": ai_response})
            print(f"GPT-4 responded: '{ai_response}'")
            return ai_response
        except openai.APIError as e:
            print(f"OpenAI API Error: {e}")
            return "I'm having trouble connecting to my GPT brain right now."
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return "A critical error occurred with my GPT brain."
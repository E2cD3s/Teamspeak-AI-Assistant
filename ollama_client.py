import ollama
import asyncio

class OllamaClient:
    """A client to interact with a local Ollama LLM, now with a configurable model."""
    # --- CHANGE: model_name is now passed in during creation ---
    def __init__(self, system_prompt, model_name):
        try:
            # Check if the desired model is available locally
            models = ollama.list()['models']
            if not any(model['name'].startswith(model_name) for model in models):
                raise ConnectionError(f"Ollama model '{model_name}' not found. Please run 'ollama run {model_name}' first.")
        except Exception as e:
            raise ConnectionError(f"Could not connect to Ollama or find the model. Is Ollama running? Error: {e}")
            
        self.model_name = model_name
        self.history = [{"role": "system", "content": system_prompt}]

    async def get_response(self, user_prompt):
        print(f"Sending to Ollama ({self.model_name}): '{user_prompt}'")
        self.history.append({"role": "user", "content": user_prompt})

        try:
            loop = asyncio.get_event_loop()
            
            response = await loop.run_in_executor(
                None,
                lambda: ollama.chat(
                    model=self.model_name,
                    messages=self.history
                )
            )

            ai_response = response['message']['content']
            self.history.append({"role": "assistant", "content": ai_response})
            print(f"Ollama responded: '{ai_response}'")
            return ai_response

        except Exception as e:
            print(f"An error occurred while communicating with Ollama: {e}")
            return "I'm having trouble connecting to my local brain right now."
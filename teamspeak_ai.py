import asyncio
import os
import pyaudio
import wave
import numpy as np
import time
import logging
import json
import random
from gemini_client import GeminiClient
from gpt_client import GptClient
from ollama_client import OllamaClient
from local_voice_client import LocalVoiceClient

# --- Configuration Loading ---
def load_config():
    """Loads settings from config.json, creating it if it doesn't exist."""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("config.json not found. Creating a default configuration file.")
        default_config = {
            "wake_word": "assistant",
            "stop_word": "stop",
            "tts_speaker_id": "p228",
            "ollama_model_name": "llama3",
            "thinking_indicator_texts": ["One moment...", "Let me think about that."],
            "ai_personality_prompt": "You are a helpful AI assistant. Your name is Assistant. Keep your answers concise and conversational.",
            "gemini_api_key": "PASTE_YOUR_GEMINI_API_KEY_HERE",
            "openai_api_key": "PASTE_YOUR_OPENAI_API_KEY_HERE"
        }
        with open('config.json', 'w') as f:
            json.dump(default_config, f, indent=2)
        return default_config
config = load_config()
# --- End Config Loading ---

# --- Conversation Logging Setup (No Changes) ---
log_formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
log_handler = logging.FileHandler('conversation_log.txt')
log_handler.setFormatter(log_formatter)
conversation_logger = logging.getLogger('conversation_logger')
conversation_logger.setLevel(logging.INFO)
conversation_logger.addHandler(log_handler)

# --- Audio Configuration (No Changes) ---
INPUT_DEVICE_NAME = "CABLE-A Output"
OUTPUT_DEVICE_NAME = "CABLE-B Input"
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
VAD_THRESHOLD = 400
VAD_SILENCE_CHUNKS = 40
RECORDING_PATH = "user_speech.wav"
RESPONSE_PATH = "ai_response.wav"
THINKING_INDICATOR_PATH = "thinking.wav"

# --- AudioHandler Class (No Changes, but included for completeness) ---
class AudioHandler:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.input_device_index = self._find_device_index(INPUT_DEVICE_NAME, is_input=True)
        self.output_device_index = self._find_device_index(OUTPUT_DEVICE_NAME, is_input=False)
        if self.input_device_index is None or self.output_device_index is None:
            raise RuntimeError("Could not find required audio devices.")
    def _find_device_index(self, name, is_input):
        print(f"Searching for {'input' if is_input else 'output'} device containing: '{name}'")
        for i in range(self.p.get_device_count()):
            dev_info = self.p.get_device_info_by_index(i)
            if name in dev_info['name'] and ((is_input and dev_info['maxInputChannels'] > 0) or \
               (not is_input and dev_info['maxOutputChannels'] > 0)):
                print(f"Found device at index {i}: '{dev_info['name']}'")
                return i
        print(f"--- FATAL: Device Not Found: {name} ---")
        return None
    def listen_and_record(self):
        stream = None
        try:
            input_info = self.p.get_device_info_by_index(self.input_device_index)
            device_rate = int(input_info['defaultSampleRate'])
            device_channels = input_info['maxInputChannels']
            stream = self.p.open(format=pyaudio.paInt16, channels=device_channels, rate=device_rate,
                                 input=True, frames_per_buffer=CHUNK,
                                 input_device_index=self.input_device_index)
            print(f"\nListening for user speech... (VAD Threshold: {VAD_THRESHOLD})")
            frames, silence_chunks, is_speaking = [], 0, False
            for _ in range(0, int(device_rate / CHUNK * 15)):
                data = stream.read(CHUNK, exception_on_overflow=False)
                audio_array = np.frombuffer(data, dtype=np.int16)
                if audio_array.size == 0: continue
                if device_channels > 1: audio_array = audio_array[::device_channels]
                rms = np.sqrt(np.mean(audio_array.astype(np.float64)**2))
                if is_speaking:
                    frames.append(data)
                    if rms < VAD_THRESHOLD:
                        silence_chunks += 1
                        if silence_chunks > VAD_SILENCE_CHUNKS: break
                    else: silence_chunks = 0
                elif rms > VAD_THRESHOLD:
                    is_speaking = True
                    frames.append(data)
        finally:
            if stream: stream.stop_stream(); stream.close()
        if not frames: return None
        with wave.open(RECORDING_PATH, 'wb') as wf:
            wf.setnchannels(device_channels)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(device_rate)
            wf.writeframes(b''.join(frames))
        return RECORDING_PATH
    def play_audio(self, file_path=RESPONSE_PATH):
        if not os.path.exists(file_path): return
        stream = None
        try:
            with wave.open(file_path, 'rb') as wf:
                stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                                     channels=wf.getnchannels(), rate=wf.getframerate(), output=True,
                                     output_device_index=self.output_device_index)
                data = wf.readframes(CHUNK)
                while data: stream.write(data); data = wf.readframes(CHUNK)
        finally:
            if stream: stream.stop_stream(); stream.close()
    def cleanup(self):
        self.p.terminate()

async def main():
    print("Starting AI Companion Bot (Configurable)...")
    
    ai_brain = None
    while ai_brain is None:
        print("\n--- Choose an AI Brain ---")
        print("1. Gemini (Fast & Internet-Connected)")
        print("2. GPT-4 (Powerful & Creative)")
        print("3. Ollama (Local & Private)")
        choice = input("Enter your choice (1, 2, or 3): ")

        # --- THIS IS THE FINAL CHANGE ---
        # The personality is now loaded directly from the config file.
        personality = config['ai_personality_prompt']
        # --- END OF CHANGE ---

        try:
            if choice == '1':
                ai_brain = GeminiClient(system_prompt=personality, api_key=config.get('gemini_api_key'))
            elif choice == '2':
                ai_brain = GptClient(system_prompt=personality, api_key=config.get('openai_api_key'))
            elif choice == '3':
                ai_brain = OllamaClient(system_prompt=personality, model_name=config['ollama_model_name'])
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"\n--- ERROR INITIALIZING BRAIN: {e} ---")
            print("Please ensure API keys are set in config.json and services (like Ollama) are running.")
            ai_brain = None
            
    try:
        voice_client = LocalVoiceClient(speaker_id=config['tts_speaker_id'])
        audio_handler = AudioHandler()
    except Exception as e:
        print(f"Fatal error during audio/voice initialization: {e}")
        return

    print("\nBot is now live and listening to audio.")
    wake_word = config['wake_word']

    try:
        while True:
            recorded_audio_path = await asyncio.to_thread(audio_handler.listen_and_record)
            if recorded_audio_path:
                transcribed_text = voice_client.transcribe_audio_file(recorded_audio_path)
                if wake_word.lower() in transcribed_text.lower():
                    prompt = transcribed_text.lower().split(wake_word.lower(), 1)[-1].strip()
                    if prompt:
                        print(f"Heard prompt: '{prompt}'")
                        conversation_logger.info(f"USER: {prompt}")
                        thinking_phrase = random.choice(config['thinking_indicator_texts'])
                        print(f"Playing thinking indicator: '{thinking_phrase}'")
                        await asyncio.to_thread(voice_client.synthesize_speech, thinking_phrase, THINKING_INDICATOR_PATH)
                        await asyncio.to_thread(audio_handler.play_audio, THINKING_INDICATOR_PATH)
                        
                        ai_response_text = await ai_brain.get_response(prompt)
                        
                        if ai_response_text:
                            cleaned_response_text = ai_response_text.replace('*', '')
                            print(f"AI: '{cleaned_response_text}'")
                            conversation_logger.info(f"ASSISTANT: {cleaned_response_text}")
                            conversation_logger.info("-" * 20)
                            log_handler.flush()
                            
                            synthesized_audio_path = voice_client.synthesize_speech(cleaned_response_text, RESPONSE_PATH)
                            if synthesized_audio_path:
                                await asyncio.to_thread(audio_handler.play_audio, synthesized_audio_path)
    except KeyboardInterrupt:
        print("\nShutting down the bot...")
    finally:
        audio_handler.cleanup()
        logging.shutdown()
        print("Bot has shut down.")

if __name__ == "__main__":
    asyncio.run(main())
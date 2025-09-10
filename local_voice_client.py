import os
import wave
import whisper
import torch
import traceback
from TTS.api import TTS

class LocalVoiceClient:
    """
    Handles STT and TTS. Accepts a speaker ID for dynamic voice changes.
    """
    def __init__(self, whisper_model="base.en", speaker_id="p228"):
        print("Initializing local voice clients...")
        print(f"Loading Whisper STT model: {whisper_model}")
        self.stt_model = whisper.load_model(whisper_model)
        print("Whisper model loaded.")
        print("Loading Coqui TTS model...")
        try:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Using device for TTS: {self.device}")
            self.tts_engine = TTS(model_name="tts_models/en/vctk/vits", progress_bar=True).to(self.device)
            self.speaker_id = speaker_id
            print(f"Coqui TTS model loaded successfully. Using speaker: {self.speaker_id}")
        except Exception:
            print("\n--- FATAL ERROR DURING TTS INITIALIZATION ---")
            traceback.print_exc()
            raise
        print("--- Local voice clients are ready. ---")

    def transcribe_audio_file(self, audio_path="user_speech.wav"):
        if not os.path.exists(audio_path): return ""
        print(f"Transcribing audio file: {audio_path}")
        try:
            result = self.stt_model.transcribe(audio_path, fp16=False)
            transcribed_text = result.get('text', '')
            print(f"Transcription result: '{transcribed_text}'")
            return transcribed_text
        except Exception:
            traceback.print_exc()
            return ""

    def synthesize_speech(self, text, output_path="ai_response.wav"):
        print(f"Synthesizing speech for text: '{text}'")
        try:
            self.tts_engine.tts_to_file(text=text, speaker=self.speaker_id, file_path=output_path)
            print(f"Speech synthesized and saved to: {output_path}")
            return output_path
        except Exception:
            traceback.print_exc()
            return None
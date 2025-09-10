# Multi-Brain AI Voice Companion for TeamSpeak

This project is a sophisticated, real-time, voice-activated AI assistant designed to run as a companion in a TeamSpeak voice channel. It features a modular, "pluggable brain" architecture, allowing you to switch between cloud-based models like Google Gemini and OpenAI's GPT-4, or a completely private, self-hosted model running on Ollama.

This guide provides the complete, verified steps to set up the AI companion on a Windows system.

## Features

* 🗣️ Real-Time Voice Interaction: Natural, hands-free conversation with a configurable wake word.
* 🧠 Pluggable AI Brains: Switch between Gemini (internet-connected), GPT-4 (creative), and Ollama (private) at startup.
* 🎤 Local Voice Processing: Utilizes local Whisper for STT and Coqui TTS for a high-quality male voice, ensuring privacy and zero audio processing costs.
* ⚙️ Fully Configurable: A central config.json file controls the AI's name, voice, personality, wake word, and API keys.
* 💡 Dynamic "Thinking" Indicator: Provides instant audio feedback when a command is heard.
* 📝 Conversation Logging: Automatically saves a "memory" of all interactions to conversation_log.txt.
* 🚀 One-Click Launch: A simple start_assistant.bat script automates the entire startup sequence.

## How It Works

The system uses a robust dual virtual cable setup on Windows to create a stable, echo-free audio pipeline between the TeamSpeak client and the Python AI script. The AI listens to the channel audio, transcribes it, sends it to the chosen LLM, synthesizes the response, and speaks it back into the channel.

## Prerequisites

* A Windows machine (10, 11, or Server).
* An NVIDIA GPU (required for local voice models).
* A TeamSpeak 3 account and a server to use the bot on.

## Installation Guide

### Phase 1: System Foundation

1. NVIDIA Drivers: Install the latest drivers for your GPU from the NVIDIA website. Reboot after installation.
2. Python 3.11: Download and install Python 3.11 from the official website. CRITICAL: On the first screen of the installer, check the box "Add python.exe to PATH".
3. Git for Windows: Download and install from the official website.
4. Microsoft C++ Build Tools: This is required to build the TTS engine.
   * Download the "Build Tools for Visual Studio 2022" from the Visual Studio website.
   * Run the installer. In the "Workloads" tab, check the box for "Desktop development with C++".
   * Click "Install". Reboot your computer when it's finished.
5. eSpeak-ng: This is a dependency for the advanced TTS voice model.
   * Download the ...x64.msi installer from the eSpeak-ng GitHub releases page.
   * Run the installer with default options. Reboot your computer.

### Phase 2: Project Setup

1. Clone This Repository: Open a Command Prompt (cmd.exe) and run the following commands:

   ```cmd
   cd C:\
   git clone [[https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME](https://github.com/E2cD3s/Teamspeak-AI-Assistant).git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git) tsai
   cd tsai
   ```
2. Set Up Python Environment:

   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install Python Packages: This will install all required libraries from the requirements.txt file.

   ```cmd
   pip install -r requirements.txt
   ```
4. Download TTS Voice Models: This will download the voice library and may take some time.

   ```cmd
   git clone [https://huggingface.co/rhasspy/piper-voices](https://huggingface.co/rhasspy/piper-voices)
   ```

### Phase 3: Audio Plumbing

1. Install VB-CABLE A & B: 
   * Download the "VBCABLE_Driver\_PackXX.zip" from VB-Audio's website (the main, free one).
   * Download the "VBCABLE_A&B_Driver\_PackXX.zip" from the same page (this is donationware).
   * Unzip both files.
   * For both, find the ...\_Setup_x64.exe file, right-click it, and choose "Run as administrator".
   * Reboot your computer after both are installed.

### Phase 4: Configuration

1. Rename the Config File: In your C:\\tsai folder, rename config.json.example to config.json.
2. Edit config.json: Open the new config.json file in a text editor and fill in your details:
   * gemini_api_key: Your API key from Google AI Studio.
   * openai_api_key: Your API key from the OpenAI Platform.
   * You can also customize the wake word, voice, Ollama model, and personality prompt here.

### Phase 5: One-Time TeamSpeak Setup

You must do this once to save the audio settings.

1. Install TeamSpeak 3.5.6: Download and install the 64-bit Windows client.
2. Configure Windows Sound:
   * Right-click the speaker icon in your system tray and choose "Sounds".
   * Playback Tab: Right-click CABLE-A Input and "Set as Default Device".
   * Recording Tab: Right-click in the empty space, check "Show Disabled Devices", then right-click "Stereo Mix" and Disable it to prevent echos.
3. Configure TeamSpeak Audio:
   * Open TeamSpeak and go to Tools -> Options.
   * Playback Tab: Set Playback Device to Default.
   * Capture Tab: Set Capture Device to CABLE-B Output (VB-Audio CABLE-B).
   * Uncheck all audio processing boxes (echo cancellation, etc.).
   * Click Apply and OK.

## Running the Assistant

1. Make sure the Ollama application (if you plan to use it) and the TeamSpeak 3 client are running and connected to your server.
2. In your C:\\tsai folder, simply double-click the start_assistant.bat file.
3. A new terminal window will open. Choose the AI brain you want to use for the session.
4. The assistant is now live!

## License

This project is licensed under the MIT License.

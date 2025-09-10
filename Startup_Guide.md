# AI Companion Startup Guide

This guide covers the two methods for launching your AI assistant.

### Prerequisites

Before starting, ensure the following are running:

1. Ollama Application: The Ollama icon must be visible in your Windows system tray. If not, start the Ollama application from your Start Menu.
2. TeamSpeak 3 Client: The TeamSpeak client must be open and connected to your desired server and channel.

---

### Method 1: Manual Startup

This method is useful for debugging.

1. Open Command Prompt: Open a new cmd.exe window.
2. Navigate to Project Directory:

   ```cmd
   cd C:\tsai
   ```
3. Activate Virtual Environment:

   ```cmd
   .venv\Scripts\activate
   ```
4. Run the AI Script:

   ```cmd
   python teamspeak_ai.py
   ```
5. The script will now prompt you to choose an AI brain. After you make a selection, it will connect to the audio devices and begin listening.

---

### Method 2: Automatic Startup (Recommended)

This is the easiest way to launch the assistant for everyday use.

1. Navigate to your C:\\tsai folder in Windows File Explorer.
2. Find the file named start_assistant.bat.
3. Double-click the file.

A new command prompt window will open, check if Ollama is running, activate the environment, and launch the AI script for you. You will still need to choose the AI brain in the terminal window that opens.

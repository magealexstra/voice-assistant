# Offline Voice Assistant

This is an offline voice assistant that integrates Nerd Dictation, OpenVoice, and local LLM capabilities using LM-Studio. It provides voice-to-voice interaction while maintaining privacy by running everything locally.

## Prerequisites

- Python 3.9+
- Nerd Dictation installed
- LM-Studio running locally with API enabled
- Working microphone and speakers
- Git (for cloning repositories)

## Installation

1. Clone the OpenVoice repository (if not already done):
```bash
git clone https://github.com/myshell-ai/OpenVoice.git
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate
```

3. Install the required Python packages:
```bash
pip install -r requirements.txt
```

4. Install OpenVoice from the local repository:
```bash
cd OpenVoice
pip install -e .
cd ..
```

5. Make sure Nerd Dictation is installed and configured on your system
6. Ensure LM-Studio is running with the API server enabled (default port: 1234)

## Usage

1. Start LM-Studio and load your preferred model
2. Enable the API server in LM-Studio
3. Run the setup check to verify all components are working:
```bash
python setup_check.py
```

4. Run the voice assistant:
```bash
python voice_assistant.py
```

5. Speak your query when prompted
6. Say "exit" to quit the program

## Troubleshooting

- If OpenVoice fails to initialize or generate speech, the system will automatically fall back to using espeak for text-to-speech.
- If you encounter issues with Nerd Dictation, make sure it's properly installed and configured.
- If LM-Studio connection fails, verify that it's running and the API server is enabled on port 1234.

## Features

- Voice input using Nerd Dictation for accurate speech recognition
- Local LLM integration via LM-Studio for offline AI responses
- High-quality text-to-speech output using OpenVoice voice cloning technology
- Fallback to system text-to-speech (espeak) if OpenVoice encounters issues
- Fully offline operation for enhanced privacy

#!/usr/bin/env python3
import os
import json
import subprocess
import time
import sys

import torch
import torchaudio
import requests
import numpy as np
import soundfile as sf
from playsound import playsound

# Add the OpenVoice directory to the path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'OpenVoice'))
from openvoice.openvoice import OpenVoice

class VoiceAssistant:
    def __init__(self, lm_studio_url="http://localhost:1234/v1"):
        self.lm_studio_url = lm_studio_url
        self.nerd_dictation_path = os.path.expanduser("~/nerd-dictation")

        # Verify nerd-dictation installation
        if not os.path.exists(self.nerd_dictation_path):
            raise RuntimeError("Nerd Dictation not found. Please install it first.")
        
        # Initialize OpenVoice
        print("Initializing OpenVoice...")
        try:
            self.openvoice = OpenVoice()
            # Set default voice (you can change this to any speaker in the OpenVoice model)
            self.speaker_id = 0  # Default speaker
            self.sample_rate = 24000  # Default sample rate for OpenVoice
            print("OpenVoice initialized successfully!")
        except Exception as e:
            print(f"Error initializing OpenVoice: {e}")
            print("Will fall back to system text-to-speech if needed.")
            self.openvoice = None

    def start_nerd_dictation(self):
        """Start nerd-dictation in begin mode"""
        try:
            subprocess.Popen([
                os.path.join(self.nerd_dictation_path, "nerd-dictation"),
                "begin",
                "--timeout", "5"
            ])
        except Exception as e:
            print(f"Error starting nerd-dictation: {e}")
            return False
        return True

    def stop_nerd_dictation(self):
        """Stop nerd-dictation"""
        try:
            subprocess.run([
                os.path.join(self.nerd_dictation_path, "nerd-dictation"),
                "end"
            ])
        except Exception as e:
            print(f"Error stopping nerd-dictation: {e}")

    def listen(self):
        """Listen for voice input using Nerd Dictation"""
        print("Listening... (Speak your message)")

        # Start nerd-dictation and create a temporary file for output
        temp_file = "/tmp/nerd_dictation_output.txt"
        if os.path.exists(temp_file):
            os.remove(temp_file)

        try:
            # Start nerd-dictation in begin mode with output to file
            process = subprocess.Popen([
                os.path.join(self.nerd_dictation_path, "nerd-dictation"),
                "begin",
                "--output", temp_file,
                "--timeout", "5"
            ])

            # Wait for the timeout or until speech is detected and processed
            time.sleep(6)  # Wait slightly longer than the timeout

            # Stop nerd-dictation
            self.stop_nerd_dictation()

            # Read the output file if it exists
            if os.path.exists(temp_file):
                with open(temp_file, 'r') as f:
                    text = f.read().strip()

                os.remove(temp_file)
                return text.lower() if text else None
            return None

        except Exception as e:
            print(f"Error using Nerd Dictation: {e}")

            return None

    def query_local_llm(self, prompt):
        """Query the local LM-Studio instance"""
        try:
            response = requests.post(
                f"{self.lm_studio_url}/chat/completions",
                json={
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 150
                },
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error querying LLM: {e}")
            return "I'm sorry, I encountered an error while processing your request."

    def speak(self, text):
        """Convert text to speech using OpenVoice or fallback to system TTS"""
        if self.openvoice is not None:
            try:
                # Generate speech using OpenVoice
                print("Generating speech with OpenVoice...")
                output_wav = self.openvoice.inference(
                    text,
                    self.speaker_id,
                    language='en'
                )
                
                # Save and play the audio
                temp_file = "response.wav"
                sf.write(temp_file, output_wav, self.sample_rate)
                playsound(temp_file)
                os.remove(temp_file)
                return
            except Exception as e:
                print(f"Error in OpenVoice text-to-speech: {e}")
                print("Falling back to system text-to-speech...")
        
        # Fallback to system text-to-speech
        try:
            print("Using system text-to-speech...")
            os.system(f'espeak "{text}"')
        except Exception as e2:
            print(f"Error in fallback text-to-speech: {e2}")

    def run(self):
        """Main loop for the voice assistant"""
        print("Voice Assistant is ready! Say 'exit' to quit.")
        
        while True:
            text = self.listen()
            if text:
                print(f"You said: {text}")
                
                if text == "exit":
                    print("Goodbye!")
                    break
                
                # Get response from LLM
                response = self.query_local_llm(text)
                print(f"Assistant: {response}")
                
                # Convert response to speech
                self.speak(response)

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()

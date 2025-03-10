#!/usr/bin/env python3
import os
import sys
import subprocess
import requests
import torch
import torchaudio
from playsound import playsound
import soundfile as sf
import numpy as np

# Add the OpenVoice directory to the path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'OpenVoice'))
from openvoice.openvoice import OpenVoice

def check_nerd_dictation():
    print("\nChecking Nerd Dictation installation...")
    nerd_dictation_path = os.path.expanduser("~/nerd-dictation")
    if not os.path.exists(nerd_dictation_path):
        print("❌ Nerd Dictation not found at ~/nerd-dictation")
        print("Please install Nerd Dictation first:")
        print("git clone https://github.com/ideasman42/nerd-dictation.git ~/nerd-dictation")
        return False
    print("✓ Nerd Dictation found")
    return True

def check_lm_studio():
    print("\nChecking LM-Studio API connection...")
    try:
        response = requests.get("http://localhost:1234/v1/models")
        if response.status_code == 200:
            print("✓ LM-Studio API is running")
            return True
        else:
            print("❌ LM-Studio API returned unexpected status code:", response.status_code)
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to LM-Studio API")
        print("Please make sure LM-Studio is running with the API server enabled")
        return False

def check_openvoice():
    print("\nTesting OpenVoice setup...")
    try:
        # Check if OpenVoice directory exists
        openvoice_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'OpenVoice')
        if not os.path.exists(openvoice_dir):
            print("❌ OpenVoice directory not found")
            print("Please clone the OpenVoice repository:")
            print("git clone https://github.com/myshell-ai/OpenVoice.git")
            return False
            
        print("✓ OpenVoice directory found")
        
        # Initialize OpenVoice
        try:
            openvoice = OpenVoice()
            print("✓ OpenVoice model loaded successfully")

            # Test text-to-speech generation
            test_text = "Testing OpenVoice output"
            print("Generating test audio...")
            output_wav = openvoice.inference(test_text, speaker_id=0, language='en')
            
            # Save and play test audio
            temp_file = "test_audio.wav"
            sample_rate = 24000  # Default sample rate for OpenVoice
            sf.write(temp_file, output_wav, sample_rate)
            playsound(temp_file)
            os.remove(temp_file)
            
            print("✓ OpenVoice text-to-speech working")
            return True
        except Exception as e:
            print("❌ Error initializing or using OpenVoice:", str(e))
            print("Will try to use system text-to-speech as fallback")
            
            # Check if espeak is available as a fallback
            try:
                subprocess.run(['which', 'espeak'], check=True, stdout=subprocess.PIPE)
                print("✓ espeak found as fallback text-to-speech")
                return True
            except subprocess.CalledProcessError:
                print("❌ espeak not found. Please install it:")
                print("sudo apt-get install espeak")
                return False
    except Exception as e:
        print("❌ Error testing OpenVoice:", str(e))
        print("Make sure you have installed all required dependencies")
        return False

def main():
    print("Voice Assistant Setup Check")
    print("==========================")
    
    nerd_ok = check_nerd_dictation()
    lm_ok = check_lm_studio()
    openvoice_ok = check_openvoice()
    
    print("\nSummary:")
    print("========")
    if all([nerd_ok, lm_ok, openvoice_ok]):
        print("✓ All components are ready!")
        print("\nYou can now run the voice assistant:")
        print("python voice_assistant.py")
    else:
        print("❌ Some components need attention")
        print("Please fix the issues above before running the voice assistant")

if __name__ == "__main__":
    main()

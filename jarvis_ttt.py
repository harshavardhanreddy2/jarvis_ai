import os
import re
import subprocess
import ollama

MODEL = "llama3.2"  # Change to your installed model

def speak(text):
    # 1. Strip markdown artifacts (*, #, _, `, etc.)
    clean_text = re.sub(r'[*#_`>-]', '', text)
    # 2. Flatten all lines and whitespace into a continuous sentence
    clean_text = " ".join(clean_text.split())
    
    # Escape quotes for Windows shell
    safe_text = clean_text.replace('"', '""').replace("'", "''")
    
    # 3. Use Windows native SAPI voice directly (100% offline, never cuts off)
    ps_command = f'Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Rate = 1; $speak.Speak("{safe_text}");'
    subprocess.run(["powershell", "-Command", ps_command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("=== Ollama Voice Chatbot (Type 'quit' to exit) ===")

messages = [
    {"role": "system", "content": "You are a concise voice assistant. Keep all responses brief and under 2-3 sentences."}
]

while True:
    user_input = input("\nYou: ")
    if user_input.strip().lower() in ("quit", "exit"):
        speak("Goodbye!")
        print("Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})

    print("Assistant: ", end="", flush=True)
    full_reply = ""

    # Stream the reply token by token in real time
    stream = ollama.chat(model=MODEL, messages=messages, stream=True)
    for chunk in stream:
        token = chunk["message"]["content"]
        print(token, end="", flush=True)
        full_reply += token

    print()
    messages.append({"role": "assistant", "content": full_reply})

    # Speak the entire response back
    speak(full_reply)
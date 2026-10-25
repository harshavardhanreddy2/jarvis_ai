import ollama
import pyttsx3

MODEL = "llama3.2"  # Change to the model you pulled

# 1. Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 175)  # Speed of speech (words per minute)

# Optional: Adjust volume (0.0 to 1.0)
engine.setProperty("volume", 0.9)

def speak(text):
    engine.say(text)
    engine.runAndWait()

print("=== Ollama Voice Chatbot (Type 'quit' to exit) ===")

# Keep the answers short so it doesn't talk forever
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

    # Speak the response out loud
    speak(full_reply)
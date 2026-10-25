import ollama

MODEL = "llama3.2"  # Change to the model you pulled

print("=== Ollama Interactive Terminal (Type 'quit' to exit) ===")

messages = [
    {"role": "system", "content": "You are a concise, helpful assistant."}
]

while True:
    user_input = input("\nYou: ")
    if user_input.strip().lower() in ("quit", "exit"):
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
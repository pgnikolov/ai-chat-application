from groq import Groq
from datetime import datetime
from deep_translator import GoogleTranslator

client = Groq(
    api_key="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",
)

def get_ai_response(user_input):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"

def save_chat_history(user_input, response, filename="chat_history.txt"):
    with open(filename, "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp} - You: {user_input}\n{timestamp} - AI: {response}\n")

def load_chat_history(filename="chat_history.txt"):
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        return "No chat history found."

def clear_chat_history(filename="chat_history.txt"):
    with open(filename, "w") as file:
        file.write("")

def translate_to_language(text, dest_language):
    translated = GoogleTranslator(source='auto', target=dest_language).translate(text)
    return translated

def main():
    print("Welcome to the AI Chat! Type 'exit' to end the conversation.")
    print("Type '!history' to view chat history.")
    print("Type '!clear' to clear chat history.")
    print("Type '!lang [language_code]' to change the language.")
    print("Type '!langs' to display supported languages.")

    language = "en"

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        elif user_input.lower() == "!history":
            print(load_chat_history())
            continue
        elif user_input.lower() == "!clear":
            clear_chat_history()
            print("Chat history cleared.")
            continue
        elif user_input.lower().startswith("!lang"):
            language = user_input.split(" ", 1)[1]
            print(f"Language changed to {language}.")
            continue
        elif user_input.lower() == "!langs":
            print("Supported languages: en (English), bg (Bulgarian) and others.....")  # other langs acc to the needs

        translated_input = translate_to_language(user_input, language)
        response = get_ai_response(translated_input)
        translated_response = translate_to_language(response, language)

        print(f"AI: {translated_response}")

        save_chat_history(user_input, translated_response)

if __name__ == "__main__":
    main()

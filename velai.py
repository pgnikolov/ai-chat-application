from groq import Groq
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk

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

def send_message(event=None):
    user_input = user_entry.get()

    if user_input.strip() == "":
        return

    chat_history.insert(tk.END, 'You: ', 'user_label')
    chat_history.insert(tk.END, user_input + '\n', 'user_input')
    user_entry.delete(0, tk.END)

    response = get_ai_response(user_input)
    chat_history.insert(tk.END, 'Velai: ', 'ai_label')
    chat_history.insert(tk.END, response + '\n', 'ai_response')

    # Scroll to the bottom
    chat_history.yview(tk.END)


root = tk.Tk()
root.title("Velai Chat AI with Groq API")  # Updated title

window_width = 1024
window_height = 683
root.geometry(f"{window_width}x{window_height}")

bg_image = Image.open("img-ai.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)
background_label = tk.Label(root, image=bg_photo)
background_label.place(relwidth=1, relheight=1)

chat_frame = tk.Frame(root, bg="#f7f7f7", bd=5)
chat_frame.place(relwidth=0.7, relheight=0.6, relx=0.15, rely=0.1)

chat_history = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, state='normal')
chat_history.pack(fill=tk.BOTH, expand=True)

# Define tags for different fonts
chat_history.tag_config('user_input', font=("Helvetica", 12), foreground="green")
chat_history.tag_config('user_label', font=("Helvetica", 12, "bold"), foreground="darkgreen")
chat_history.tag_config('ai_response', font=("Helvetica", 12), foreground="blue")
chat_history.tag_config('ai_label', font=("Helvetica", 12, "bold"), foreground="red")

user_entry = tk.Entry(root, font=("Helvetica", 14))
user_entry.place(relwidth=0.7, relheight=0.07, relx=0.15, rely=0.75)

# Bind the Enter key to the send_message function
user_entry.bind("<Return>", send_message)

# Send button
send_button = tk.Button(root, text="Send", font=("Helvetica", 14), command=send_message)
send_button.place(relwidth=0.2, relheight=0.07, relx=0.65, rely=0.75)

root.mainloop()

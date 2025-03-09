import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from PIL import Image, ImageTk  # Requires Pillow installed (pip install Pillow)
import os

# For demo purposes, we simulate an AI response.
def simulate_ai_response(user_message):
    # In a real implementation, you would call your AI model here
    # e.g., response = ai_model.run_conversation(user_message)
    # For now, we simulate a response by echoing the message.
    return f"AI (EventElf): I received your message: '{user_message}'"

class ChatUI:
    def __init__(self, master):
        self.master = master
        master.title("EventElf Chat")
        master.geometry("600x500")
        master.configure(bg="#f0f0f0")  # light gray background for a modern look

        # Load images for UI components.
        # Replace 'triangle.png', 'elf.png', and 'stars.png' with your image file paths.
        try:
            self.triangle_image = ImageTk.PhotoImage(Image.open("triangle.jpg").resize((30, 30)))
        except Exception as e:
            messagebox.showwarning("Image Load Warning", "Could not load triangle.png. Button will be text-only.")
            self.triangle_image = None

        try:
            self.elf_image = ImageTk.PhotoImage(Image.open("elf.jpg").resize((30, 30)))
        except Exception as e:
            messagebox.showwarning("Image Load Warning", "Could not load elf.png.")
            self.elf_image = None

        try:
            self.stars_image = ImageTk.PhotoImage(Image.open("star.jpg").resize((100, 30)))
        except Exception as e:
            messagebox.showwarning("Image Load Warning", "Could not load stars.png.")
            self.stars_image = None

        # Create a frame for the chat feed.
        self.chat_frame = tk.Frame(master, bg="#f0f0f0")
        self.chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Use a scrolled text widget for the conversation area.
        self.chat_feed = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, state=tk.DISABLED, font=("Helvetica", 12))
        self.chat_feed.pack(fill=tk.BOTH, expand=True)

        # Optionally, add decorative stars image at the top (if available)
        if self.stars_image:
            self.stars_label = tk.Label(master, image=self.stars_image, bg="#f0f0f0")
            self.stars_label.pack(pady=(0, 5))

        # Create a frame for the input area.
        self.input_frame = tk.Frame(master, bg="#f0f0f0")
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)

        # Entry widget for user to type message.
        self.message_entry = tk.Entry(self.input_frame, font=("Helvetica", 12))
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))
        self.message_entry.bind("<Return>", self.send_message)

        # Button to send the message. Uses the triangle image if available.
        if self.triangle_image:
            self.send_button = tk.Button(self.input_frame, image=self.triangle_image, command=self.send_message, bd=0)
        else:
            self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

    def append_message(self, sender, message, icon=None):
        """Append a message to the chat feed."""
        self.chat_feed.configure(state=tk.NORMAL)
        if icon:
            # Insert icon if provided (this is a simplified approach; more complex layouts might use a canvas)
            self.chat_feed.image_create(tk.END, image=icon)
            self.chat_feed.insert(tk.END, " ")
        self.chat_feed.insert(tk.END, f"{sender}: {message}\n")
        self.chat_feed.configure(state=tk.DISABLED)
        self.chat_feed.see(tk.END)

    def send_message(self, event=None):
        """Retrieve user input, display it, and simulate an AI response."""
        user_message = self.message_entry.get().strip()
        if not user_message:
            return  # do nothing if message is empty

        # Append the user's message to the chat feed.
        self.append_message("You", user_message)

        # Clear the entry widget.
        self.message_entry.delete(0, tk.END)

        # Optionally, you can simulate a delay for AI "thinking" using after()
        self.master.after(500, self.process_ai_response, user_message)

    def process_ai_response(self, user_message):
        # Simulate getting an AI response.
        ai_response = simulate_ai_response(user_message)
        # Append the AI's message to the chat feed.
        # If available, we prepend an elf icon for the AI.
        self.append_message("", ai_response, icon=self.elf_image)

def main():
    root = tk.Tk()
    app = ChatUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

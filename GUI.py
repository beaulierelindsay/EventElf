import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
import ai_model
from main import create_event

class ChatUI:
    def __init__(self, master):
        self.master = master
        master.title("EventElf Chat")
        master.geometry("600x500")
        master.configure(bg="#f0f0f0")  # light gray background

        # Initialize images
        self.triangle_image = None
        self.elf_image = None
        self.stars_image = None
        
        # Try to load images, but continue if they aren't available
        try:
            self.triangle_image = ImageTk.PhotoImage(Image.open("triangle.png").resize((30, 30)))
            self.elf_image = ImageTk.PhotoImage(Image.open("elf.png").resize((30, 30)))
            self.stars_image = ImageTk.PhotoImage(Image.open("stars.png").resize((100, 30)))
            
            # Add decorative stars image at the top if available
            if self.stars_image:
                self.stars_label = tk.Label(master, image=self.stars_image, bg="#f0f0f0")
                self.stars_label.pack(pady=(10, 5))
        except Exception as e:
            print(f"Image loading error: {e}")
            # Continue without images

        # Create frame for the chat feed
        self.chat_frame = tk.Frame(master, bg="#f0f0f0")
        self.chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Scrollable text widget for displaying conversation
        self.chat_feed = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, state=tk.DISABLED, font=("Helvetica", 12))
        self.chat_feed.pack(fill=tk.BOTH, expand=True)

        # Input frame at the bottom
        self.input_frame = tk.Frame(master, bg="#f0f0f0")
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)

        # Entry widget for typing messages
        self.message_entry = tk.Entry(self.input_frame, font=("Helvetica", 12))
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.message_entry.bind("<Return>", self.send_message)

        # Button to send message
        if self.triangle_image:
            self.send_button = tk.Button(self.input_frame, image=self.triangle_image, command=self.send_message, bd=0)
        else:
            self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)
        
        # Variable to store pending events
        self.pending_events = None
        
        # Welcome message
        self.master.after(500, lambda: self.append_message("EventElf", "Hello! I can help you create calendar events. What event would you like to schedule?", self.elf_image))

    def append_message(self, sender, message, icon=None):
        """Append a message to the chat feed."""
        self.chat_feed.configure(state=tk.NORMAL)
        if sender:
            if icon:
                # Insert icon if provided
                self.chat_feed.image_create(tk.END, image=icon)
                self.chat_feed.insert(tk.END, " ")
            self.chat_feed.insert(tk.END, f"{sender}: ")
        self.chat_feed.insert(tk.END, f"{message}\n")
        self.chat_feed.configure(state=tk.DISABLED)
        self.chat_feed.see(tk.END)

    def send_message(self, event=None):
        """Handle sending a message when Enter is pressed or the send button is clicked."""
        user_message = self.message_entry.get().strip()
        if not user_message:
            return  # Do nothing if the input is empty
            
        # Check if we're waiting for a yes/no response to event confirmation
        if self.pending_events is not None:
            if user_message.lower() in ["yes", "y"]:
                self.create_pending_events()
            else:
                self.append_message("EventElf", "Event creation cancelled. What else would you like to schedule?", self.elf_image)
                self.pending_events = None
            self.message_entry.delete(0, tk.END)
            return

        # Append the user's message to the chat feed
        self.append_message("You", user_message)
        self.message_entry.delete(0, tk.END)

        # Show "thinking" indicator
        self.append_message("EventElf", "Thinking...", self.elf_image)
        
        # Process the AI response after a short delay to simulate thinking
        self.master.after(100, self.process_ai_response, user_message)

    def process_ai_response(self, user_message):
        """Process user message and get AI response"""
        # Remove the "thinking" message
        self.chat_feed.configure(state=tk.NORMAL)
        self.chat_feed.delete("end-2l", "end-1c")
        self.chat_feed.configure(state=tk.DISABLED)
        
        # Process the message using ai_model.py
        ai_model.run_conversation(user_message, self.handle_event_response)

    def handle_event_response(self, events, response_text):
        """Callback function to handle the parsed events and response"""
        self.pending_events = events
        self.append_message("EventElf", response_text, self.elf_image)

    def create_pending_events(self):
        """Create the pending events that were confirmed by the user"""
        try:
            for event in self.pending_events:
                create_calendar_event_result = create_event(event)
                # You might want to extract and display more info about the created event
            
            self.append_message("EventElf", f"Successfully created {len(self.pending_events)} event(s) in your calendar.", self.elf_image)
        except Exception as e:
            self.append_message("EventElf", f"Error creating event: {str(e)}", self.elf_image)
        
        # Reset pending events
        self.pending_events = None

def main():
    root = tk.Tk()
    app = ChatUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
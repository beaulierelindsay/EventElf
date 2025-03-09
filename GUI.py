import tkinter as tk
from tkinter import scrolledtext, messagebox, font
from PIL import Image, ImageTk, ImageDraw
import ai_model
from main import create_event
import os
import sys

class ModernChatUI:
    def __init__(self, master):
        self.master = master
        master.title("EventElf Chat")
        master.geometry("400x650")  # More phone-like dimensions
        
        # Color scheme with sage green background
        self.colors = {
            "bg": "#d4e0d0",           # Sage green background
            "user_bubble": "#5a8262",   # Darker sage for user messages
            "bot_bubble": "#f1f3f6",    # Light gray for bot messages
            "user_text": "#ffffff",     # White text for user messages
            "bot_text": "#212529",      # Dark text for bot messages
            "input_bg": "#ffffff",      # White input background
            "accent": "#5a8262"         # Accent color for buttons
        }
        
        master.configure(bg=self.colors["bg"])
        
        # Create custom fonts
        self.default_font = font.Font(family="Helvetica", size=10)
        self.message_font = font.Font(family="Helvetica", size=11)
        self.header_font = font.Font(family="Helvetica", size=14, weight="bold")

        # Initialize images
        self.triangle_image = None
        self.elf_image = None
        self.stars_image = None
        self.send_icon = None
        
        # Get the directory of the script
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle
            script_dir = os.path.dirname(sys.executable)
        else:
            # If run as a script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
        # Print current working directory for debugging
        print("Current working directory:", os.getcwd())
        print("Script directory:", script_dir)
        
        # Check if image files exist
        elf_path = os.path.join(script_dir, "elf.png")
        stars_path = os.path.join(script_dir, "stars.png")
        
        print(f"Looking for elf.png at: {elf_path}")
        print(f"File exists: {os.path.exists(elf_path)}")
        
        # Try to load images
        try:
            # If elf.png exists, use it, otherwise create default
            if os.path.exists(elf_path):
                self.elf_image = self.create_circular_avatar(elf_path, size=32)
            else:
                self.elf_image = self.create_default_avatar(size=32)
                
            # Create a send button icon (right-facing arrow)
            self.send_icon = self.create_send_icon()
            
            # Try to load stars image if it exists
            if os.path.exists(stars_path):
                self.stars_image = ImageTk.PhotoImage(Image.open(stars_path).resize((120, 36)))
        except Exception as e:
            print(f"Image loading error: {e}")
            self.elf_image = self.create_default_avatar(size=32)
            # Continue without other images

        # Header frame
        self.header_frame = tk.Frame(master, bg="#ffffff", height=60)
        self.header_frame.pack(fill=tk.X)
        self.header_frame.pack_propagate(False)
        
        # Header with app title and elf avatar
        if self.elf_image:
            self.avatar_label = tk.Label(self.header_frame, image=self.elf_image, bg="#ffffff")
            self.avatar_label.pack(side=tk.LEFT, padx=15)
        
        self.title_label = tk.Label(
            self.header_frame, 
            text="EventElf", 
            font=self.header_font, 
            bg="#ffffff", 
            fg="#5a8262"  # Match the accent color
        )
        self.title_label.pack(side=tk.LEFT, padx=5)
        
        # Add a separator line below the header
        self.separator = tk.Frame(master, height=1, bg="#e0e0e0")
        self.separator.pack(fill=tk.X)

        # Create frame for the chat feed
        self.chat_frame = tk.Frame(master, bg=self.colors["bg"])
        self.chat_frame.pack(padx=0, pady=0, fill=tk.BOTH, expand=True)

        # Custom scrolled text widget for displaying conversation
        self.chat_feed = tk.Canvas(self.chat_frame, bg=self.colors["bg"], highlightthickness=0)
        self.chat_feed.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Scrollbar for the canvas
        self.scrollbar = tk.Scrollbar(self.chat_feed, orient="vertical", command=self.chat_feed.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.chat_feed.configure(yscrollcommand=self.scrollbar.set)
        
        # Create a frame inside the canvas to hold messages
        self.messages_frame = tk.Frame(self.chat_feed, bg=self.colors["bg"])
        self.chat_feed.create_window((0, 0), window=self.messages_frame, anchor="nw", width=self.chat_feed.winfo_width())
        
        # Bind canvas resize to update the scrollable region
        self.chat_feed.bind("<Configure>", self.on_canvas_configure)
        self.messages_frame.bind("<Configure>", self.on_frame_configure)

        # Input area at the bottom
        self.input_area = tk.Frame(master, bg="#ffffff", height=60)
        self.input_area.pack(fill=tk.X, side=tk.BOTTOM)
        self.input_area.pack_propagate(False)
        
        # Add a separator line above the input area
        self.bottom_separator = tk.Frame(master, height=1, bg="#e0e0e0")
        self.bottom_separator.pack(fill=tk.X, side=tk.BOTTOM, before=self.input_area)

        # Create a rounded frame for the input field
        self.input_frame = tk.Frame(self.input_area, bg="#f1f3f6", bd=0)
        self.input_frame.pack(fill=tk.X, expand=True, padx=10, pady=10)
        
        # Make the input frame appear rounded by adding corners
        self.round_input_frame()

        # Entry widget for typing messages
        self.message_entry = tk.Entry(
            self.input_frame, 
            font=self.message_font,
            bd=0,
            bg="#f1f3f6",
            fg="#212529",
            insertbackground="#5a8262"  # Cursor color matching theme
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(15, 5), pady=8)
        self.message_entry.bind("<Return>", self.send_message)
        
        # Focus the entry field
        self.message_entry.focus_set()

        # Button to send message
        if self.send_icon:
            self.send_button = tk.Button(
                self.input_frame, 
                image=self.send_icon, 
                command=self.send_message, 
                bd=0,
                bg="#f1f3f6",
                activebackground="#f1f3f6",
                highlightthickness=0
            )
        else:
            self.send_button = tk.Button(
                self.input_frame, 
                text="Send", 
                command=self.send_message,
                bg=self.colors["accent"],
                fg="#ffffff",
                bd=0,
                padx=10,
                pady=5,
                font=self.default_font
            )
        self.send_button.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Variable to store pending events
        self.pending_events = None
        
        # Welcome message
        self.master.after(500, lambda: self.append_message("EventElf", "Hello! I can help you create calendar events. What event would you like to schedule?"))

    def create_default_avatar(self, size=40):
        """Create a default avatar when image files are missing"""
        try:
            img = Image.new('RGBA', (size, size), self.colors["accent"])
            draw = ImageDraw.Draw(img)
            
            # Add a text "EE" for EventElf in the center
            font_size = size // 2
            draw.text((size//2, size//2), "EE", fill="white", anchor="mm")
            
            # Create a mask for circular cropping
            mask = Image.new('L', (size, size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, size, size), fill=255)
            
            # Apply the mask to make it circular
            result = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            result.paste(img, (0, 0), mask)
            
            return ImageTk.PhotoImage(result)
        except Exception as e:
            print(f"Default avatar creation error: {e}")
            return None
    
    def create_circular_avatar(self, image_path, size=40):
        """Create a circular avatar image"""
        try:
            # Open the image
            img = Image.open(image_path)
            img = img.resize((size, size))
            
            # Create a mask for circular cropping
            mask = Image.new('L', (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)
            
            # Apply the mask
            result = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            result.paste(img, (0, 0), mask)
            
            return ImageTk.PhotoImage(result)
        except Exception as e:
            print(f"Avatar creation error: {e}")
            # Create a default avatar instead
            return self.create_default_avatar(size)

    def create_send_icon(self, size=20):
        """Create a send button icon"""
        try:
            # Create a new image with an arrow
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw an arrow pointing right
            arrow_color = self.colors["accent"]
            # Drawing a paper airplane style icon
            points = [
                (0, size//2),           # Left point
                (size//2, 0),           # Top point
                (size, size//2),        # Right point
                (size//2, size),        # Bottom point
                (size//2, size//3*2),   # Bottom-left indent
                (size//3*2, size//2)    # Middle-left indent
            ]
            draw.polygon(points, fill=arrow_color)
            
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Send icon creation error: {e}")
            return None

    def on_canvas_configure(self, event):
        """Update the scrollable region when the canvas is resized"""
        self.chat_feed.itemconfig(1, width=event.width)
        
    def on_frame_configure(self, event):
        """Update the scrollable region when the frame changes size"""
        self.chat_feed.configure(scrollregion=self.chat_feed.bbox("all"))
        self.chat_feed.yview_moveto(1.0)  # Scroll to bottom

    def create_round_bubble_image(self, width, height, color, radius=15):
        """Create a round rectangle image for message bubbles"""
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw a rounded rectangle
        draw.rounded_rectangle([(0, 0), (width, height)], radius, fill=color)
        
        return ImageTk.PhotoImage(image)
    
    def create_message_bubble(self, sender, message, is_user=False):
        """Create a message bubble in the chat feed with rounder corners"""
        # Frame for this message
        message_frame = tk.Frame(self.messages_frame, bg=self.colors["bg"])
        message_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Calculate appropriate width based on message length
        message_width = min(len(message) * 8 + 50, 220)  # Limit max width
        message_height = (len(message) // 30 + 1) * 20 + 16  # Estimate height
        
        if is_user:
            # User message (right-aligned)
            spacer = tk.Frame(message_frame, bg=self.colors["bg"], width=40)
            spacer.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Create rounded bubble background
            try:
                bubble_bg = self.create_round_bubble_image(
                    message_width, 
                    message_height, 
                    self.colors["user_bubble"],
                    radius=18  # More rounded corners
                )
                
                # Container for bubble
                bubble_container = tk.Label(
                    message_frame,
                    image=bubble_bg,
                    bg=self.colors["bg"],
                    bd=0
                )
                bubble_container.image = bubble_bg  # Keep reference
                bubble_container.pack(side=tk.RIGHT)
                
                # Text over the bubble
                bubble = tk.Label(
                    bubble_container,
                    text=message,
                    bg=self.colors["user_bubble"],
                    fg=self.colors["user_text"],
                    font=self.message_font,
                    justify=tk.LEFT,
                    anchor="w",
                    padx=12,
                    pady=8,
                    wraplength=message_width - 24
                )
                bubble.place(relx=0.5, rely=0.5, anchor="center")
            except Exception as e:
                # Fallback if image creation fails
                print(f"Bubble creation error: {e}")
                bubble = tk.Label(
                    message_frame,
                    text=message,
                    bg=self.colors["user_bubble"],
                    fg=self.colors["user_text"],
                    font=self.message_font,
                    justify=tk.LEFT,
                    anchor="w",
                    padx=12,
                    pady=8,
                    wraplength=200,
                    bd=0
                )
                bubble.pack(side=tk.RIGHT)
        else:
            # Bot message (left-aligned with avatar)
            if self.elf_image:
                avatar = tk.Label(message_frame, image=self.elf_image, bg=self.colors["bg"])
                avatar.pack(side=tk.LEFT, padx=(0, 8))
            
            # Create rounded bubble background
            try:
                bubble_bg = self.create_round_bubble_image(
                    message_width, 
                    message_height, 
                    self.colors["bot_bubble"],
                    radius=18  # More rounded corners
                )
                
                # Container for bubble
                bubble_container = tk.Label(
                    message_frame,
                    image=bubble_bg,
                    bg=self.colors["bg"],
                    bd=0
                )
                bubble_container.image = bubble_bg  # Keep reference
                bubble_container.pack(side=tk.LEFT)
                
                # Text over the bubble
                bubble = tk.Label(
                    bubble_container,
                    text=message,
                    bg=self.colors["bot_bubble"],
                    fg=self.colors["bot_text"],
                    font=self.message_font,
                    justify=tk.LEFT,
                    anchor="w",
                    padx=12,
                    pady=8,
                    wraplength=message_width - 24
                )
                bubble.place(relx=0.5, rely=0.5, anchor="center")
            except Exception as e:
                # Fallback if image creation fails
                print(f"Bubble creation error: {e}")
                bubble = tk.Label(
                    message_frame,
                    text=message,
                    bg=self.colors["bot_bubble"],
                    fg=self.colors["bot_text"],
                    font=self.message_font,
                    justify=tk.LEFT,
                    anchor="w",
                    padx=12,
                    pady=8,
                    wraplength=200,
                    bd=0
                )
                bubble.pack(side=tk.LEFT)
            
            # Add spacer to push the message to the left
            spacer = tk.Frame(message_frame, bg=self.colors["bg"], width=40)
            spacer.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        # Update scrollable region and scroll to bottom
        self.messages_frame.update_idletasks()
        self.chat_feed.configure(scrollregion=self.chat_feed.bbox("all"))
        self.chat_feed.yview_moveto(1.0)

    def append_message(self, sender, message, is_user=False):
        """Append a message to the chat feed."""
        # If sender is "You", it's a user message
        if sender == "You":
            is_user = True
            
        self.create_message_bubble(sender, message, is_user)

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
                self.append_message("EventElf", "Event creation cancelled. What else would you like to schedule?")
                self.pending_events = None
            self.message_entry.delete(0, tk.END)
            return

        # Append the user's message to the chat feed
        self.append_message("You", user_message, is_user=True)
        self.message_entry.delete(0, tk.END)

        # Create a temporary "thinking" message
        thinking_frame = tk.Frame(self.messages_frame, bg=self.colors["bg"])
        thinking_frame.pack(fill=tk.X, padx=10, pady=5)
        
        if self.elf_image:
            avatar = tk.Label(thinking_frame, image=self.elf_image, bg=self.colors["bg"])
            avatar.pack(side=tk.LEFT, padx=(0, 8))
        
        thinking_bubble = tk.Label(
            thinking_frame,
            text="Thinking...",
            bg=self.colors["bot_bubble"],
            fg=self.colors["bot_text"],
            font=self.message_font,
            padx=12,
            pady=8
        )
        thinking_bubble.pack(side=tk.LEFT)
        
        # Update scrollable region and scroll to bottom
        self.messages_frame.update_idletasks()
        self.chat_feed.configure(scrollregion=self.chat_feed.bbox("all"))
        self.chat_feed.yview_moveto(1.0)
        
        # Process the AI response after a short delay to simulate thinking
        self.master.after(100, lambda: self.process_ai_response(user_message, thinking_frame))

    def round_input_frame(self):
        """Apply rounded corners to the input frame"""
        try:
            # Get dimensions of the input frame
            self.input_frame.update_idletasks()
            width = self.input_frame.winfo_width()
            height = self.input_frame.winfo_height()
            
            if width <= 1 or height <= 1:  # Not yet properly sized
                self.master.after(100, self.round_input_frame)
                return
                
            # Create rounded rectangle background
            rounded_bg = self.create_round_bubble_image(
                width, 
                height, 
                "#f1f3f6",
                radius=20  # Very rounded corners
            )
            
            # Apply the rounded background
            bg_label = tk.Label(self.input_frame, image=rounded_bg, bg=self.colors["bg"])
            bg_label.image = rounded_bg  # Keep reference
            bg_label.place(x=0, y=0)
            
            # Bring entry and button to front
            self.message_entry.lift()
            self.send_button.lift()
        except Exception as e:
            print(f"Input frame rounding error: {e}")
    
    def process_ai_response(self, user_message, thinking_frame):
        """Process user message and get AI response"""
        # Remove the "thinking" message frame
        thinking_frame.destroy()
        
        # Process the message using ai_model.py
        ai_model.run_conversation(user_message, self.handle_event_response)

    def handle_event_response(self, events, response_text):
        """Callback function to handle the parsed events and response"""
        self.pending_events = events
        self.append_message("EventElf", response_text)

    def create_pending_events(self):
        """Create the pending events that were confirmed by the user"""
        try:
            for event in self.pending_events:
                create_calendar_event_result = create_event(event)
            
            self.append_message("EventElf", f"Successfully created {len(self.pending_events)} event(s) in your calendar.")
        except Exception as e:
            self.append_message("EventElf", f"Error creating event: {str(e)}")
        
        # Reset pending events
        self.pending_events = None

def main():
    root = tk.Tk()
    app = ModernChatUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
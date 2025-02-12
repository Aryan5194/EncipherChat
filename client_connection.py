import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

# Colors and fonts
BACKGROUND_COLOR = '#1F2833'  # New dark background color
TEXT_COLOR = '#C5C6C7'  # Light text color
BUTTON_COLOR = '#66FCF1'  # New button color (light cyan)
ENTRY_COLOR = '#4C566A'  # Dark grey for input fields
HIGHLIGHT_COLOR = '#45A29E'  # Light blue for highlights
MESSAGE_BG_COLOR = '#2B3A42'  # New dark grey for message field
MESSAGE_COLOR = '#A3BE8C'  # Green for messages (attractive color)
FONT = ("Arial", 12)
BUTTON_FONT = ("Arial", 12, "bold")
SMALL_FONT = ("Arial", 11)

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    """Add a message to the chat box"""
    message_box.config(state=tk.NORMAL)
    message_box.tag_config("message", foreground=MESSAGE_COLOR)  # Set message color
    message_box.insert(tk.END, message + '\n', "message")
    message_box.config(state=tk.DISABLED)
    message_box.yview(tk.END)  # Auto-scroll to the latest message

def connect():
    """Connect to the server"""
    # Get host and port from the input fields
    HOST = host_textbox.get()
    PORT = port_textbox.get()

    # Validate host and port
    if not HOST or not PORT:
        messagebox.showerror("Invalid Input", "Host and Port cannot be empty")
        return

    try:
        PORT = int(PORT)  # Convert port to integer
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
        
        # Enable username input after successful connection
        username_textbox.config(state=tk.NORMAL)
        username_button.config(state=tk.NORMAL)
        
        # Disable connection inputs
        host_textbox.config(state=tk.DISABLED)
        port_textbox.config(state=tk.DISABLED)
        connect_button.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST}:{PORT}\nError: {e}")

def join_chat():
    """Join the chat with username"""
    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
        print("SEND : ", username.encode())
        
        # Disable username inputs after joining
        username_textbox.config(state=tk.DISABLED)
        username_button.config(state=tk.DISABLED)
        
        # Update UI
        username_label.config(text=f"Welcome {username} to our secure room", fg=HIGHLIGHT_COLOR)
        
        # Start listening for messages
        threading.Thread(target=listen_for_messages_from_server).start()
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

def send_message():
    """Send a message to the server"""
    message = message_textbox.get()
    if message != '':
        message_textbox.delete(0, len(message))
        client.sendall(message.encode("utf-8"))
        print("SEND : ", message.encode())
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

def listen_for_messages_from_server():
    """Listen for messages from the server"""
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                # Extract username and message content (remove key-related data)
                if '~' in message:
                    parts = message.split('~')
                    username = parts[0]
                    message_content = parts[1]
                    add_message(f"{username}: {message_content}")
                else:
                    add_message(message)
            else:
                messagebox.showerror("Error", "Message received from server is empty")
                break
        except:
            print("Error receiving message from server")
            break

# GUI setup
root = tk.Tk()
root.geometry("600x600")
root.title("SECURE CHAT ROOM")
root.resizable(False, False)
root.configure(bg=BACKGROUND_COLOR)

# Configure grid layout
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# Top frame for connection details
top_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
top_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Host and port input
host_label = tk.Label(top_frame, text="Host:", font=FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
host_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

host_textbox = tk.Entry(top_frame, font=FONT, bg=ENTRY_COLOR, fg=TEXT_COLOR, width=15)
host_textbox.grid(row=0, column=1, padx=5, pady=5, sticky="w")

port_label = tk.Label(top_frame, text="Port:", font=FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
port_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

port_textbox = tk.Entry(top_frame, font=FONT, bg=ENTRY_COLOR, fg=TEXT_COLOR, width=10)
port_textbox.grid(row=0, column=3, padx=5, pady=5, sticky="w")

# Oval-shaped Connect button
connect_button = tk.Button(
    top_frame,
    text="Connect",
    font=BUTTON_FONT,
    bg=BUTTON_COLOR,
    fg=BACKGROUND_COLOR,  # Button text color matches background
    command=connect,
    relief=tk.FLAT,  # Remove button border
    bd=0,  # Remove border
    highlightthickness=0,  # Remove highlight
    padx=10,  # Add padding
    pady=5,  # Add padding
    borderwidth=0,  # Remove border
    highlightbackground=BACKGROUND_COLOR,  # Match background
    highlightcolor=BACKGROUND_COLOR,  # Match background
)
connect_button.grid(row=0, column=4, padx=5, pady=5, sticky="w")

# Username input (initially disabled)
username_label = tk.Label(top_frame, text="Username:", font=FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
username_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

username_textbox = tk.Entry(top_frame, font=FONT, bg=ENTRY_COLOR, fg=TEXT_COLOR, width=15, state=tk.DISABLED)
username_textbox.grid(row=1, column=1, padx=5, pady=5, sticky="w")

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=BUTTON_COLOR, fg=BACKGROUND_COLOR, command=join_chat, state=tk.DISABLED)
username_button.grid(row=1, column=2, padx=5, pady=5, sticky="w")

# Middle frame for chat messages
middle_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
middle_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

# Chat message box
message_box = scrolledtext.ScrolledText(
    middle_frame,
    font=SMALL_FONT,
    bg=MESSAGE_BG_COLOR,  # Attractive background color
    fg=TEXT_COLOR,
    width=67,
    height=26.5,
    wrap=tk.WORD,  # Wrap text by words
)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Bottom frame for sending messages
bottom_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
bottom_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

# Message input
message_textbox = tk.Entry(bottom_frame, font=FONT, bg=ENTRY_COLOR, fg=TEXT_COLOR, width=38)
message_textbox.pack(side=tk.LEFT, padx=10, pady=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=BUTTON_COLOR, fg=BACKGROUND_COLOR, command=send_message)
message_button.pack(side=tk.LEFT, padx=10, pady=10)

# Start the GUI
def main():
    root.mainloop()

if __name__ == '__main__':
    main()
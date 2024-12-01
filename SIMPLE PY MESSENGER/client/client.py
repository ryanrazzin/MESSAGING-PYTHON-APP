import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, filedialog, Toplevel
from PIL import Image, ImageTk
import pyautogui

# Function to handle login
def login(event=None):
    global nickname
    nickname = nickname_entry.get()
    login_window.destroy()
    start_chat()

# Function to start the chat
def start_chat():
    # Client setup
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('CHANGE ME IP', PORT))

    # Function to send message
    def send_message(event=None):
        message = message_entry.get()
        client.send(f'{nickname}: {message}'.encode('utf-8'))
        display_message(f'You: {message}', "right")
        message_entry.delete(0, tk.END)

    # Function to send image
    def send_image():
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as file:
                image_data = file.read()
            client.send(f'{nickname}:IMAGE'.encode('utf-8'))
            client.send(image_data)
            display_image(file_path, "right")

    # Function to receive messages from the server
    def receive():
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    client.send(nickname.encode('utf-8'))
                elif message.endswith(':IMAGE'):
                    image_data = client.recv(1024*1024)  # Adjust buffer size as needed
                    with open('received_image.png', 'wb') as file:
                        file.write(image_data)
                    display_image('received_image.png', "left")
                elif not message.startswith(f'{nickname}:'):
                    display_message(message, "left")
            except:
                print("An error occurred!")
                client.close()
                break

    # Function to display messages in text bubbles
    def display_message(message, align):
        if align == "right":
            bubble = tk.Frame(message_display, bg="#4CAF50", padx=10, pady=5)  # Green for your messages
            label = tk.Label(bubble, text=message, bg="#4CAF50", fg="#FFFFFF", font=("Arial", 12), wraplength=300)
        else:
            bubble = tk.Frame(message_display, bg="#2196F3", padx=10, pady=5)  # Blue for other messages
            label = tk.Label(bubble, text=message, bg="#2196F3", fg="#FFFFFF", font=("Arial", 12), wraplength=300)
        
        label.pack()
        message_display.window_create(tk.END, window=bubble)
        message_display.insert(tk.END, "\n")
        if align == "right":
            bubble.pack(anchor='e', padx=10, pady=5)
        else:
            bubble.pack(anchor='w', padx=10, pady=5)

    # Function to display images
    def display_image(file_path, align):
        img = Image.open(file_path)
        img.thumbnail((100, 100))
        img = ImageTk.PhotoImage(img)
        if align == "right":
            bubble = tk.Frame(message_display, bg="#4CAF50", padx=10, pady=5)  # Green for your messages
            label = tk.Label(bubble, image=img, bg="#4CAF50")
        else:
            bubble = tk.Frame(message_display, bg="#2196F3", padx=10, pady=5)  # Blue for other messages
            label = tk.Label(bubble, image=img, bg="#2196F3")
        
        label.image = img  # Keep a reference to avoid garbage collection
        label.pack()
        label.bind("<Button-1>", lambda e: open_fullscreen_image(file_path))
        message_display.window_create(tk.END, window=bubble)
        message_display.insert(tk.END, "\n")
        if align == "right":
            bubble.pack(anchor='e', padx=10, pady=5)
        else:
            bubble.pack(anchor='w', padx=10, pady=5)

    # Function to open image in full screen
    def open_fullscreen_image(file_path):
        top = Toplevel()
        top.title("Full Screen Image")
        img = Image.open(file_path)
        img = ImageTk.PhotoImage(img)
        label = tk.Label(top, image=img)
        label.image = img  # Keep a reference to avoid garbage collection
        label.pack()

    # Function to toggle dark mode
    def toggle_dark_mode():
        if root.cget("bg") == "#2C2F33":
            root.config(bg="#FFFFFF")
            message_display.config(bg="#FFFFFF", fg="#2C2F33")
            message_entry.config(bg="#FFFFFF", fg="#2C2F33")
            send_button.config(bg="#7289DA", fg="#FFFFFF")
            dark_mode_button.config(bg="#7289DA", fg="#FFFFFF", text="Dark Mode")
        else:
            root.config(bg="#2C2F33")
            message_display.config(bg="#2C2F33", fg="#FFFFFF")
            message_entry.config(bg="#2C2F33", fg="#FFFFFF")
            send_button.config(bg="#7289DA", fg="#FFFFFF")
            dark_mode_button.config(bg="#7289DA", fg="#FFFFFF", text="Light Mode")

    # Function to bring up the emoji keyboard
    def open_emoji_keyboard(event=None):
        pyautogui.hotkey('win', '.')

    # Create main window
    global root
    root = tk.Tk()
    root.title("Chat-OS")
    root.geometry("900x1000")
    root.config(bg="#2C2F33")

    # Add widgets
    global message_display, message_entry, send_button, dark_mode_button
    message_display = scrolledtext.ScrolledText(root, height=30, width=70, bg="#2C2F33", fg="#FFFFFF", font=("Arial", 12))
    message_display.pack(pady=10, fill=tk.BOTH, expand=True)

    message_entry = tk.Entry(root, width=70, bg="#2C2F33", fg="#FFFFFF", font=("Arial", 12))
    message_entry.pack(pady=10, fill=tk.X)
    message_entry.bind("<Return>", send_message)

    # Create a frame for the buttons
    button_frame = tk.Frame(root, bg="#2C2F33")
    button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    send_button = tk.Button(button_frame, text="Send", command=send_message, bg="#7289DA", fg="#FFFFFF", font=("Arial", 12), relief="flat", bd=0)
    send_button.pack(side=tk.LEFT, padx=5)
    send_button.config(highlightbackground="#7289DA", highlightcolor="#7289DA", highlightthickness=2, bd=0, padx=10, pady=5)

    image_button = tk.Button(button_frame, text="Send Image", command=send_image, bg="#7289DA", fg="#FFFFFF", font=("Arial", 12), relief="flat", bd=0)
    image_button.pack(side=tk.LEFT, padx=5)
    image_button.config(highlightbackground="#7289DA", highlightcolor="#7289DA", highlightthickness=2, bd=0, padx=10, pady=5)

    dark_mode_button = tk.Button(button_frame, text="Light Mode", command=toggle_dark_mode, bg="#7289DA", fg="#FFFFFF", font=("Arial", 12), relief="flat", bd=0)
    dark_mode_button.pack(side=tk.LEFT, padx=5)
    dark_mode_button.config(highlightbackground="#7289DA", highlightcolor="#7289DA", highlightthickness=2, bd=0, padx=10, pady=5)

    emoji_button = tk.Button(button_frame, text="😊", command=open_emoji_keyboard, bg="#7289DA", fg="#FFFFFF", font=("Arial", 12), relief="flat", bd=0)
    emoji_button.pack(side=tk.LEFT, padx=5)
    emoji_button.config(highlightbackground="#7289DA", highlightcolor="#7289DA", highlightthickness=2, bd=0, padx=10, pady=5)

    # Start threads for receiving and sending messages
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    # Run the application
    root.mainloop()

# Create login window
login_window = tk.Tk()
login_window.title("Login To Chat-OS")
login_window.geometry("300x200")
login_window.config(bg="#2C2F33")

tk.Label(login_window, text="Enter your nickname:", bg="#2C2F33", fg="#FFFFFF", font=("Arial", 12)).pack(pady=20)
nickname_entry = tk.Entry(login_window, width=30, bg="#2C2F33", fg="#FFFFFF", font=("Arial", 12))
nickname_entry.pack(pady=10)
nickname_entry.bind("<Return>", login)

login_button = tk.Button(login_window, text="Login", command=login, bg="#7289DA", fg="#FFFFFF", font=("Arial", 12), relief="flat", bd=0)
login_button.pack(pady=10)
login_button.config(highlightbackground="#7289DA", highlightcolor="#7289DA", highlightthickness=2, bd=0, padx=10, pady=5)

login_window.mainloop()

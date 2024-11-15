import tkinter as tk
from tkinter import simpledialog  
from tkinter import scrolledtext
import threading
import socket

HEADER = 64
PORT = 8000
IP_SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (IP_SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT = "!DISCONNECT"

class ChatClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        
        #gui
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=15, state="disabled")
        self.chat_area.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        self.msg_entry = tk.Entry(self.root, width=40)
        self.msg_entry.grid(column=0, row=1, padx=10, pady=10)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.grid(column=1, row=1, padx=10, pady=10)

        self.user_name = tk.simpledialog.askstring("Name", "Enter your name:")
        if self.user_name:
            self.send_name(self.user_name)
            self.start_receive_thread()
        else:
            self.root.destroy() 

    def send_name(self, name):
        name_msg = name.encode(FORMAT)
        name_length = len(name_msg)
        send_length = str(name_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(name_msg)

    def send_message(self):
        msg = self.msg_entry.get()
        if msg:
            message = msg.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            self.client.send(send_length)
            self.client.send(message)
            self.msg_entry.delete(0, tk.END)  # clearing entry

            if msg == DISCONNECT:
                self.root.quit()  

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(HEADER * 2).decode(FORMAT)
                self.display_message(message)
            except:
                print("An error occurred or connection closed.")
                self.client.close()
                break

    def display_message(self, message):
        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state="disabled")
        self.chat_area.yview(tk.END)

        if message.startswith("[SERVER] Online Members:"):
            pass

    def start_receive_thread(self):
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()

def main():
    root = tk.Tk()
    app = ChatClientGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

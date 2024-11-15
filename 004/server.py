import socket
import threading

HEADER = 64
PORT = 8000
IP_SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (IP_SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


clients = {}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} is connected")

    name_length = conn.recv(HEADER).decode(FORMAT)
    name = conn.recv(int(name_length)).decode(FORMAT)
    clients[conn] = name
    print(f"[{addr}] identified as {name}")

    broadcast(f"[SERVER] {name} has joined the chat.")
    broadcast_online_members()

    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)

                if msg == DISCONNECT:
                    print(f"[{addr}] {name} disconnected")
                    connected = False
                else:
                    formatted_msg = f"[{name}]: {msg}"
                    print(formatted_msg)
                    broadcast(formatted_msg)  
        except ConnectionResetError:
            print(f"[{addr}] {name} disconnected unexpectedly")
            connected = False

    remove_client(conn)
    conn.close()

def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode(FORMAT))
        except:
            remove_client(client)

def broadcast_online_members():
    online_members = ", ".join(clients.values())
    broadcast(f"[SERVER] Online Members: {online_members}")

def remove_client(client):
    if client in clients:
        print(f"[DISCONNECT] Removing {clients[client]} from active clients")
        del clients[client]
        broadcast_online_members()  

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {IP_SERVER}")
    while True:
        conn, addr = server.accept()
        print(f"[CONNECTION] {addr} connected.")
        
    
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Active Connections: {threading.active_count() - 1}")

print("Server has started...")
start()

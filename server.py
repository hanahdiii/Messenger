import socket
import threading

HOST = '127.0.0.1' 
PORT = 12345

clients = {}

def handle_client(conn, addr):
    username = conn.recv(1024).decode()
    clients[username] = conn
    print(f"{username} joined from {addr}")

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            receiver, msg = data.split(":", 1)
            if receiver in clients:
                clients[receiver].send(f"{username}:{msg}".encode())
        except:
            break

    conn.close()
    del clients[username]
    print(f"{username} disconnected.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server listening on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()

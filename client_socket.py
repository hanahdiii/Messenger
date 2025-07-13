import socket
import threading

class ChatClient:
    def __init__(self, username, on_message):
        self.username = username
        self.on_message = on_message  
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.connect(("127.0.0.1", 12345))  
            self.socket.send(self.username.encode())  
            print(f"[CLIENT] Connected to server as {self.username}")
        except Exception as e:
            print(f"[CLIENT ERROR] Could not connect: {e}")
            return

        self.running = True
        self.listen_thread = threading.Thread(target=self.listen, daemon=True)
        self.listen_thread.start()

    def listen(self):
        while self.running:
            try:
                data = self.socket.recv(1024).decode()
                if data:
                    print(f"[CLIENT] Received: {data}")
                    self.on_message(data)
            except Exception as e:
                print(f"[CLIENT ERROR] Listening stopped: {e}")
                break

    def send(self, receiver, message):
        try:
            full_data = f"{receiver}:{message}"
            self.socket.send(full_data.encode())
            print(f"[CLIENT] Sent: {full_data}")
        except Exception as e:
            print(f"[CLIENT ERROR] Sending failed: {e}")

    def close(self):
        self.running = False
        try:
            self.socket.close()
            print(f"[CLIENT] Disconnected from server")
        except:
            pass

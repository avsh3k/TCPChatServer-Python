import socket
import threading

class ChatClient:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.nickname = input("Enter your nickname: ")

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        self.send_messages()

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                print(message)
            except OSError:
                break

    def send_messages(self):
        while True:
            message = input()
            self.client.send("{}: {}".format(self.nickname, message).encode())

        self.client.close()


if __name__ == "__main__":
    host = "127.0.0.1"  # Change this to the server's IP address
    port = 55546  # Change this to the server's port
    chat_client = ChatClient(host, port)

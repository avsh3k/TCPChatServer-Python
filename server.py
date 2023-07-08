import socket
import threading

class ChatRoom:
    def __init__(self):
        self.host = "127.0.0.1"  # Change this to your desired host
        self.port = 55546  # Change this to your desired port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.nicknames = []

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()

        print("Chat server started on {}:{}".format(self.host, self.port))

        while True:
            client_socket, client_address = self.server.accept()
            print("New connection from {}:{}".format(client_address[0], client_address[1]))

            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle_client(self, client_socket):
        nickname = client_socket.recv(1024).decode()
        self.nicknames.append(nickname)
        self.clients.append(client_socket)

        print("Nickname of client {}:{} is {}".format(client_socket.getpeername()[0],
                                                      client_socket.getpeername()[1], nickname))
        self.broadcast("{} joined the chat!".format(nickname).encode())

        while True:
            try:
                message = client_socket.recv(1024)
                self.broadcast(message)
            except ConnectionResetError:
                index = self.clients.index(client_socket)
                self.clients.remove(client_socket)
                client_socket.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                self.broadcast("{} left the chat.".format(nickname).encode())
                break


if __name__ == "__main__":
    chat_room = ChatRoom()
    chat_room.start()

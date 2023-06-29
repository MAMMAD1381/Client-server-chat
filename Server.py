import socket
import threading


class Server:
    def __init__(self):
        self.host = '127.0.0.1'  # localhost
        self.port = 55555
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = {}   # new clients will be stored here
        self.talking_user_name = None
        print(f'Server listening on {self.host}:{self.port}')

    def handle_client(self, conn, addr):
        print(f'New connection from {addr}')
        previous_msg = ''
        client_name = ''
        talking_username = ''
        connected = True
        while connected:
            msg_length = conn.recv(64).decode('utf-8')
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode('utf-8')
                if msg == 'quit':  # quit
                    # client_name = msg
                    del self.clients[client_name]
                    connected = False
                elif previous_msg == 'new user':  # first time
                    client_name = msg
                    self.clients[client_name] = conn

                elif 'start message with' in msg:
                    receiver_name = msg.split(' ')[3]
                    print(receiver_name)
                    if receiver_name in self.clients:
                        talking_username = receiver_name
                        # self.send(self.clients[self.talking_user_name], f'from {client_name}: {msg}')
                        # self.clients[receiver_name].send(f'from {client_name}: {msg}'.encode('utf-8'))
                    else:
                        self.send(conn, "ERROR: user doesn't exists")
                        talking_username = ''
                elif talking_username:
                    try:
                        self.send(self.clients[talking_username], f'from {client_name}: {msg}')
                    except Exception as error:
                        talking_username = ''
                        self.send(conn, "ERROR: user doesn't exists")

                elif msg == 'stop':
                    talking_username = ''

                print(f'{client_name}:{addr} says: {msg}')
                print(self.clients)
                # conn.send('Message received'.encode('utf-8'))
                previous_msg = msg

        conn.close()

    def start(self):
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f'Active connections: {threading.activeCount() - 1}')

    def send(self, conn, msg):
        conn.send(msg.encode('utf-8'))


if __name__ == '__main__':
    server = Server()
    server.start()

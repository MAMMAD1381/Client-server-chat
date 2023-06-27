import socket
import threading


class Server:
    def __init__(self):
        self.host = '127.0.0.1'  # localhost
        self.port = 55555  # arbitrary non-privileged port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = {}
        print(f'Server listening on {self.host}:{self.port}')

    def handle_client(self, conn, addr):
        print(f'New connection from {addr}')
        previous_msg = ''
        client_name = ''
        connected = True
        while connected:
            msg_length = conn.recv(64).decode('utf-8')
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode('utf-8')
                if previous_msg == 'quit':  # quit
                    # client_name = msg
                    del self.clients[client_name]
                    connected = False
                elif previous_msg == 'new user':    # first time
                    client_name = msg
                    self.clients[client_name] = conn

                elif 'send to' in previous_msg:
                    receiver_name = previous_msg.split(' ')[2]
                    self.clients[receiver_name].send(f'from {client_name}: {msg}'.encode('utf-8'))


                print(f'{client_name}:{addr} says: {msg}')
                print(self.clients)
                conn.send('Message received'.encode('utf-8'))
                previous_msg = msg

        conn.close()

    def start(self):
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f'Active connections: {threading.activeCount() - 1}')


if __name__ == '__main__':
    server = Server()
    server.start()

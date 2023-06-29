import socket
import threading

import select


class Client:
    def __init__(self, name):
        self.name = name
        self.host = '127.0.0.1'  # localhost
        self.port = 55555  # arbitrary non-privileged port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

    def send_message(self, msg, client_name=None):
        if client_name is not None:
            self.send_message(f'start message with {client_name}')
            self.send_message(msg)
        else:
            message = msg.encode('utf-8')
            msg_length = len(message)
            send_length = str(msg_length).encode('utf-8')
            send_length += b' ' * (64 - len(send_length))
            self.client.send(send_length)
            self.client.send(message)

    def receiver(self, client):
        while True:
            try:
                # Check if there is data to read from the socket
                ready_to_read, _, _ = select.select([client], [], [], 0)

                # If there is data to read, receive it and print it
                if ready_to_read:
                    message = client.recv(1024).decode('utf-8')
                    if message:
                        print(f'\nnew message: {message}')
            except:
                print("An error occurred!")
                client.close()
                break

    def sender(self):
        while True:
            client_name = input('pls enter the receiver name: ')

            if client_name == 'close':
                break

            if client_name:
                client.send_message(f'start message with {client_name}')
            while True:
                msg = input('enter your message: ')
                if msg == '':
                    break
                client.send_message(msg)
        self.quit()

    def quit(self):
        self.send_message('quit')
        # self.send_message(self.name)
        self.client.close()

    def start(self):
        self.send_message('new user')
        self.send_message(self.name)


if __name__ == '__main__':
    name = input('pls enter your name:')
    client = Client(name)
    client.start()
    receiver = threading.Thread(target=client.receiver, args=(client.client,))
    sender = threading.Thread(target=client.sender, args=())
    receiver.start()
    sender.start()

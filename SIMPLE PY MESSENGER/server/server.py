import socket
import threading

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('CHANGE ME IP', PORT))
server.listen()

clients = []
nicknames = []

# Broadcast messages to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle individual client connections
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

# Accept new client connections
def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print('Server is listening...')
receive()

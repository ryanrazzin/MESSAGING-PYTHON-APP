import socket
import threading

# Choose a nickname
nickname = input("Choose your nickname: ")

# Client setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('CHANGE ME IP', PORT))

# Receive messages from the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

# Send messages to the server
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))

# Start threads for receiving and sending messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

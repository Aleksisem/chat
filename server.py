import socket
import threading

HOST = '127.0.0.1'
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(sender, message):
  for client in clients:
    if (client == sender):
      continue
    client.send(message)

def handle(client):
  while True:
    try:
      message = client.recv(1024)
      broadcast(client, message)
    except:
      index = clients.index(client)
      clients.remove(client)
      client.close()
      nickname = nicknames[index]
      broadcast('{} left'.format(nickname).encode('utf-8'))
      nicknames.remove(nickname)
      break

def receive():
  while True:
    client, address = server.accept()
    print('Подключение {}'.format(str(address)))

    client.send('NICKNAME'.encode('utf-8'))
    nickname = client.recv(1024).decode('utf-8')
    nicknames.append(nickname)
    clients.append(client)

    print('Никнейм: {}'.format(nickname))
    broadcast('{} подключен'.format(nickname).encode('utf-8'))
    client.send('Подключен к серверу'.encode('utf-8'))

    thread = threading.Thread(target = handle, args = (client, ))
    thread.start()

receive()

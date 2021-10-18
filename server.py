import socket
import threading

# Параметры соединения
HOST = '127.0.0.1'
PORT = 8080

# Запуск сервера
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Список клиентов и никнеймов
clients = []
nicknames = []

# Отправляет сообщения всем подключенным клиентам
def broadcast(sender, message):
  for client in clients:
    if (client == sender):
      continue
    client.send(message)

# Отлавливает сообщения, отправляемые клиентами
def handle(client):
  while True:
    try:
      # Рассылает сообщение всем клиентам
      message = client.recv(1024)
      broadcast(client, message)
    except:
      # Удаляет и закрывает соединение с клиентом
      index = clients.index(client)
      clients.remove(client)
      client.close()
      nickname = nicknames[index]
      broadcast('{} left'.format(nickname).encode('utf-8'))
      nicknames.remove(nickname)
      break

# Прослушивает соединения
def receive():
  while True:
    # Принимает соединение
    client, address = server.accept()
    print('Подключение {}'.format(str(address)))

    # Запрашивает и сохраняет никнейм клиента
    client.send('NICKNAME'.encode('utf-8'))
    nickname = client.recv(1024).decode('utf-8')
    nicknames.append(nickname)
    clients.append(client)

    # Уведломляет всех клиентов о подключении нового клиента
    print('Никнейм: {}'.format(nickname))
    broadcast(client, '{} подключен'.format(nickname).encode('utf-8'))
    client.send('Подключен к серверу'.encode('utf-8'))

    # Запуск потока по захвату сообщений
    thread = threading.Thread(target = handle, args = (client, ))
    thread.start()

receive()

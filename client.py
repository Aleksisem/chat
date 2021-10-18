import socket
import threading

# Прослушивает сервер и отправляет никнейм
def receive():
  while True:
    try:
      # Принимает сообщения с сервера
      # Если сообщение 'NICKNAME', отправляет никнейм
      message = client.recv(1024).decode('utf-8')
      if message == 'NICKNAME':
        client.send(nickname.encode('utf-8'))
      else:
        print(message)
    except:
      # Закрывает соединение
      print('Error!')
      client.close()
      break

# Отправляет сообщение на сервер
def write():
  while True:
    message = '{}: {}'.format(nickname, input(''))
    client.send(message.encode('utf-8'))

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080
server_address = (SERVER_HOST, SERVER_PORT)

# Выбор никнейма
nickname = input('Выберите никнейм: ')

# Подключение к серверу
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_address)

# Запускает поток для прослушивания сервера
receive_thread = threading.Thread(target = receive)
receive_thread.start()

# Запускает поток для отправления сообщений
write_thread = threading.Thread(target = write)
write_thread.start()
import socket
import threading

def receive():
  while True:
    try:
      message = client.recv(1024).decode('utf-8')
      if message == 'NICKNAME':
        client.send(nickname.encode('utf-8'))
      else:
        print(message)
    except:
      print('Error!')
      client.close()
      break

def write():
  while True:
    message = '{}: {}'.format(nickname, input(''))
    client.send(message.encode('utf-8'))

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080
server_address = (SERVER_HOST, SERVER_PORT)

nickname = input('Choose your nickname: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_address)

receive_thread = threading.Thread(target = receive)
receive_thread.start()

write_thread = threading.Thread(target = write)
write_thread.start()
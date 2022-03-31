import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

lock = allocate_lock()

server = 'localhost'
port = 5555

server_ip = socket.gethostbyname(server)

try:
	s.bind((server, port))

except socket.error as e:
	print(str(e))

s.listen(2)
print("Oczekiwanie na połączenia")

currentId = "0"
pos = ["0:-1,-1,3,0,-1", "1:-1,-1,3,0,-1"]
def threaded_client(conn):
	global currentId, pos, lock
	conn.send(str.encode(currentId))
	with lock:
		currentId = "1"
	reply = ''
	while True:
		try:
			data = conn.recv(2048)
			reply = data.decode('utf-8')
			if not data:
				conn.send(str.encode("Koniec przesyłania"))
				break
			else:
				print("Otrzymano: " + reply)
				arr = reply.split(":")
				id = int(arr[0])
				with lock:
					pos[id] = reply

				if id == 0: nid = 1
				if id == 1: nid = 0

				reply = pos[nid][:]
				print("Wysłano: " + reply)

			conn.sendall(str.encode(reply))
		except:
			break

	print("Zamknięto połączenie")
	with lock:
		currentId = "0"
	conn.close()

while True:
	conn, addr = s.accept()
	print("Połączono do: ", addr)

	start_new_thread(threaded_client, (conn,))
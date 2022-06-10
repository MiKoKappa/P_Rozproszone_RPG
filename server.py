from calendar import c
import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

lock_id = allocate_lock()
lock_coin = allocate_lock()

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
coinPositions = ["100,20", "275,45", "150,150"]
currCoinPos = 0
pos = ["0:-1,-1,3,0,-1", "1:-1,-1,3,0,-1"]
def threaded_client(conn):
	global currentId, pos, lock_id, lock_coin, coinPositions, currCoinPos
	conn.send(str.encode(currentId))
	with lock_id:
		currentId = "1"
	reply = ''
	while True:
		try:
			collected = 0
			data = conn.recv(2048)
			reply = data.decode('utf-8')
			if not data:
				conn.send(str.encode("Koniec przesyłania"))
				break
			else:
				print("Otrzymano: " + reply)
				arr = reply.split(":")
				if(int(arr[1][-1])==1):
					with lock_coin:
						currCoinPos = (currCoinPos + 1)%3
						collected = 1
				id = int(arr[0])
				with lock_id:
					pos[id] = reply[:len(reply)-2]
				if id == 0: nid = 1
				if id == 1: nid = 0
				sendString = str(pos[nid][:])+","+str(collected)+","+coinPositions[currCoinPos]
				
				

				print("Wysłano: " + sendString)

			conn.sendall(str.encode(sendString))
		except:
			break

	print("Zamknięto połączenie")
	with lock_id:
		currentId = "0"
	conn.close()

while True:
	conn, addr = s.accept()
	print("Połączono do: ", addr)

	start_new_thread(threaded_client, (conn,))
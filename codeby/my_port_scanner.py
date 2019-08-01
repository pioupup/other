
import socket

port = [20, 21 , 22, 23, 42, 43, 53, 67, 69, 80]

host = input("Enter hostname or IP adress:")
for i in port:
	try:
		scan = socket.socket()
		print("Scanning " + str(i) + " port on host " + host)
		scan.settimeout(0.5)
		scan.connect((host, i))
	except socket.error:
		print("Port -- ", i, " -- [CLOSED]")
	else:
		print("Port -- ", i, " -- [OPEN]")

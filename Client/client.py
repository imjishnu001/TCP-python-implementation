import socket
import pickle 
import string
import random 
import time

HEARDERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1',5002))

def name_generator(size=6, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))

def getFiles():
	full_msg = b''
	new_msg = True
	while True:
		msg = s.recv(16)
		if new_msg:
			msglen = int(msg[:HEARDERSIZE])
			new_msg = False

		full_msg += msg

		if len(full_msg)-HEARDERSIZE == msglen:
			d = pickle.loads(full_msg[HEARDERSIZE:])
			print("\nFiles avilable",d)
			menu()
			new_msg  = True
			full_msg = b''


def downloadFile():
	filename = name_generator(10, "1234567890ABCDEFGH")+'.txt'
	file = open(filename,'wb')
	file_data = s.recv(1000000)
	if file_data.decode("utf-8") == "File does not exist":
		print('\n\n',file_data.decode("utf-8"),'\n')
		menu()
	file.write(file_data)
	file.close()
	print(f"Data stored in {filename}")
	menu()

def menu():
	quit = 0
	while quit == 0:
		try:
			print("\n 1. List Files ")
			print("\n 2. Get File")
			print("\n 3. Quit")
			choice = int(input(str("\n\nEnter a number:")))
			if choice == 1:
				data = bytes(f'getFile{choice}','utf-8')
				s.send(data)
				getFiles()
			elif choice == 2:
				filename = input(str("\n\nEnter file name:"))
				data = bytes(f'{filename}{choice}','utf-8')
				s.send(data)
				downloadFile()
			elif choice == 3:
				quit = 1
				print("Good bye")
				time.sleep(3)
				data = bytes(f'Good Bye{choice}','utf-8')
				s.send(data)
				break
		except:
			exit()	
				
menu()
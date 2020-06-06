import socket 
import pickle
import os
import glob

HEARDERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1',5002))
s.listen(5) #number of connections that can be handled

def listner():
    client, address = s.accept()
    while True:
        try:
            print(f"connection from {address} has been established")
            data = client.recv(1024)
            decodedData = data.decode("utf-8")
            choice = int(decodedData[-1:])                   #Extracting user choice from decoded string        
            if choice == 1:
                arr = next(os.walk('.'))[2]
                msg = pickle.dumps(arr)
                msg = bytes(f'{len(msg):<{HEARDERSIZE}}','utf-8')+msg
                client.send(msg)
                
            elif choice ==2:
                try:
                    search = decodedData[:-1] 
                    file = open(search,'rb')
                    file_data = file.read(1000000)
                    client.send(file_data)
                    file.close()
                except:
                    client.send(b'File does not exist')
            elif choice ==3:
                print("Good bye")
                client.close()
                listner()
            else:
                print(0)
        except:
            print("Unexpected Error")
            client.close()
            listner()

listner()
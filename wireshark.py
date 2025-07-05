# Esse codigo é um modelo base de coomo o wireshark lê pacotes.
# Poderiamos por exemplo, montar isso aqui de uma maneira retorne apenas o tipo de pacote que precisamos
# É Bem mais facil utilizar o scapy e resolver isso.

import socket 

socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
print(socket.recvfrom(65535))
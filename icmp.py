from scapy.layers.inet import IP, ICMP
from scapy.layers.l2 import Ether
from scapy.sendrecv import srp1

packet = Ether()
packet /= IP(dst='www.google.com') # enviamos um pacote (fazendo ping)
packet /= ICMP()
packet.show()
result = srp1(packet)
result.show()
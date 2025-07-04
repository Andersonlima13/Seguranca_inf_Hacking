import socket 
import struct

s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
data = s.recvfrom(65535)



def ethernet_frame(data): 
    dst_mac , src_mac , ethernet_typ = struct.unpack("! 6s 6s H", data[:14])
    return dst_mac, src_mac, ethernet_typ, data[14:]



def ip_header(data):
    ipheader = struct.unpack("!BBHHHBBH4s4s", data[:20])
    ip_version = ipheader[0]
    ttl = ipheader[5]
    proto = ipheader[6]
    src_ip = ipheader[8]
    ip_dst = ipheader[9]
    return ip_version, ttl, proto, socket.inet_ntoa(src_ip), socket.inet_ntoa(ip_dst), data[20:].decode('latin-1', errors='ignore')




def translate_mac(bytes):   
    return ":".join(map('{:02x}'.format, bytes)).upper()





if __name__ == "__main__":
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    while 1:
        data, source = s.recvfrom(65535)
        dst_mac, src_mac, tp, ip_pkt = ethernet_frame(data)
        print(ip_header(ip_pkt))






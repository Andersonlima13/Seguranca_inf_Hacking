from scapy.all import sniff, IP, TCP, UDP, DNS, DNSQR, DNSRR
import socket
import datetime # Para registrar o horário

# --- Funções Auxiliares --- 1
# obtém o endereço de ip do local host 

"""def get_local_ip():
    # Tenta obter o endereço IP local do seu computador
    local = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Conecta a um IP público (não precisa ser real) para obter o IP da interface de saída
        local.connect(('8.8.8.8', 80)) # Usando o DNS do Google
        local_ip = local.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1' # Fallback para localhost se falhar
    finally:
        local.close()
       # print(f"Seu ip local é {local_ip} " )
    return local_ip
    
"""


def get_connected_hosts():
    "Obtem o endereço de todos os dispositivos conectados na rede (no gateway em questao)"
    pass
    








LOCAL_IP =  '10.0.0.63'       # Ip sendo monitorado
ip_to_hostname_cache = {}     # Cache para mapear IPs a nomes de hosts (resoluções DNS)
seen_destinations = set()    # Rastreia quais IP:Porta ja foram monitorados 
pending_dns_queries = {}

print(f"Monitoramento iniciado para o ip : {LOCAL_IP}")
print("Monitorando novas conexões SYN e tráfego DNS...")
print("Pressione Ctrl+C para encerrar a qualquer momento.\n")



# --- Função de Callback para Cada Pacote Capturado --- 2 

def packet_callback(packet):
    current_time = datetime.datetime.now().strftime('%H:%M:%S')

    # 1. Processar Tráfego DNS para Popular o Cache
    if UDP in packet and DNS in packet:
        # Consulta DNS (seu PC perguntando o IP de um domínio)
        if packet[UDP].dport == 53 and DNSQR in packet: # Se é uma consulta DNS de saída
            # Usamos o transaction ID (id) para parear consultas com respostas
            dns_query_id = packet[DNS].id
            query_name = packet[DNSQR].qname.decode('utf-8').rstrip('.')
            
            # Armazena a consulta pendente
            pending_dns_queries[(packet[IP].src, packet[IP].dst, dns_query_id)] = query_name
            # print(f"[{current_time}] DNS Consulta Registrada: ID {dns_query_id}, Query: {query_name}") # Depuração

        # Resposta DNS (o servidor DNS respondendo com o IP de um domínio)
        if packet[UDP].sport == 53 and DNSRR in packet: # Se é uma resposta DNS de entrada
            dns_response_id = packet[DNS].id
            
            # Tenta encontrar a consulta correspondente
            matching_query_name = None
            for (q_src, q_dst, q_id), q_name in list(pending_dns_queries.items()):
                if q_id == dns_response_id and q_dst == packet[IP].src and q_src == packet[IP].dst:
                    matching_query_name = q_name
                    del pending_dns_queries[(q_src, q_dst, q_id)] # Remove da lista de pendentes
                    break

            for i in range(packet[DNS].ancount):
                if isinstance(packet[DNS].an[i], DNSRR) and packet[DNS].an[i].type == 1: # A record (IPv4 address)
                    resolved_ip = packet[DNS].an[i].rdata
                    # Preferimos o query_name original se encontrarmos
                    hostname_to_cache = matching_query_name if matching_query_name else packet[DNS].an[i].rrname.decode('utf-8').rstrip('.')
                    
                    ip_to_hostname_cache[resolved_ip] = hostname_to_cache
                    # print(f"[{current_time}] DNS Resposta Processada: {hostname_to_cache} -> {resolved_ip}") # Depuração

    # 2. Processar Pacotes TCP SYN de Saída
    if IP in packet and TCP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        dst_port = packet[TCP].dport
        
        is_syn_initial = packet[TCP].flags.S and not packet[TCP].flags.A

        if src_ip == LOCAL_IP and dst_ip != LOCAL_IP and not dst_ip.startswith("127.") and is_syn_initial:
            destination_key = f"{dst_ip}:{dst_port}"

            if destination_key not in seen_destinations:
                seen_destinations.add(destination_key)
                
                # Tenta obter o nome do host do cache DNS
                # Se não encontrar, mostra o IP e tenta fazer uma resolução reversa (menos precisa)
                associated_hostname = ip_to_hostname_cache.get(dst_ip)
                
                if associated_hostname is None:
                    # Se não achou no cache DNS, tenta uma resolução DNS reversa (pode ser imprecisa)
                    try:
                        hostname_from_reverse_dns = socket.gethostbyaddr(dst_ip)[0]
                        associated_hostname = hostname_from_reverse_dns
                        # Opcional: Adiciona ao cache para futuras referências, mas com a ressalva da precisão
                        ip_to_hostname_cache[dst_ip] = associated_hostname 
                    except socket.herror:
                        associated_hostname = "Dominio Desconhecido" # Não foi possível resolver
                    except Exception as e:
                        # print(f"Erro ao tentar resolução reversa para {dst_ip}: {e}") # Depuração
                        associated_hostname = "Dominio Desconhecido"

                # Formato de saída desejado
                print(f"{src_ip} -> {associated_hostname} ({dst_ip}:{dst_port}) -> {current_time}")

# --- Iniciar o Sniffing ---
try:
    sniff(prn=packet_callback, store=0, count=0, 
          filter=f"src host {LOCAL_IP} and (tcp or (udp and port 53))")

except PermissionError:
    print("\nERRO: Permissão negada. Você precisa rodar este script como administrador/root.")
    print("No Linux/macOS: sudo python3 seu_script.py")
    print("No Windows: Execute o terminal como administrador e rode python seu_script.py")
except Exception as e:
    print(f"\nOcorreu um erro inesperado: {e}")
    print("Verifique se o Npcap (Windows) ou suas bibliotecas de rede (Linux/macOS) estão instaladas corretamente.")
finally:
    print("\nMonitoramento encerrado.")
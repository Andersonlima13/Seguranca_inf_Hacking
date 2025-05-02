#!/bin/bash

# Arquivo com a lista de subdomínios
input="subdominios.txt"

# Para cada subdomínio no arquivo
while IFS= read -r subdominio
do
    echo "Rodando Nmap para: $subdominio"
    
    # Rodando Nmap para identificar portas abertas, serviços e versões
    nmap -T4 -sC -sV -p- -Pn "$subdominio" -oN "${subdominio}_nmap_result.txt"
    
    # Rodando Nmap para uma varredura mais profunda, incluindo scripts NSE para detectar vulnerabilidades
    nmap -T4 -sC -sV --script=vuln -p- -Pn "$subdominio" -oN "${subdominio}_vuln_scan.txt"
    
    echo "---------------------------------------------"
done < "$input"
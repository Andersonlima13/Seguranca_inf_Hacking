from PyPDF2 import PdfWriter, PdfReader

# Cria um novo PDF com JavaScript
output = PdfWriter()
input_pdf = PdfReader(open("documento_limpo.pdf", "rb"))

# Adiciona o JavaScript ao PDF (ação ao abrir)
js_code = """
app.alert("JavaScript no PDF funcionou! ✅");
"""
output.add_js(js_code)

# Copia as páginas do PDF original
for page in input_pdf.pages:
    output.add_page(page)

# Salva o novo PDF
with open("documento_com_js.pdf", "wb") as f:
    output.write(f)

print("PDF com JS criado: documento_com_js.pdf")


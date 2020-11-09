import pdfplumber as pp
from tika import parser
#with pp.open("mm.pdf") as pdf:
#    page = pdf.pages[40]
#    print(page.extract_text())

file = 'mm.pdf'

file_data = parser.from_file(file)

text = file_data['content']

print(text)

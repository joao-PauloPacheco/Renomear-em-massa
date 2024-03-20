import fitz
from os import chdir, getcwd, rename
from glob import glob as glob
import re

# regex dos nomes "nota" e "empresa" geral e o "2" é para notas de SBC
failed_pdfs = []
count = 0
cr_regex_name = r'(?<=2-Não)[\r\n](.+)'
cr_regex_name2 = r'(?<=Compl:)[\r\n](.+)'
cr_regex_tipo = r'(?<=Cálculo do ISSQN devido no Município)[\r\n](.+)'
cr_regex_tipo2 = r'(?<=SECRETARIA DE FINANÇAS)[\r\n](.+)'
text = ""


#separação de diretório(pasta chamada "teste" na área de trabalho)
get_curr = getcwd()
directory = r'C:/Users/User/OneDrive - Probo Contabilidade/Área de Trabalho/renomear/'
chdir(directory)
pdf_list = glob('*.pdf')


# separar o nome e tipo do arquivo e renomear
for pdf in pdf_list:
    with fitz.open(pdf) as pdf_obj:
        for page in pdf_obj:
            text = page.get_text()
            try:
                new_file_name = re.search(cr_regex_name, text).group().strip()
                new_file_tipo = re.search(cr_regex_tipo, text).group().strip() + '.pdf'
            except:
                new_file_name = re.search(cr_regex_name2, text).group().strip()
                new_file_tipo = re.search(cr_regex_tipo2, text).group().strip() + '.pdf'


    # Tenta renomear um pdf. Se o nome do arquivo ainda não existir, então renomeie.
    # Se existir, gere um erro e adicione à lista de falhas
    try:
        rename(pdf, new_file_name + " - " + new_file_tipo)
    except WindowsError:
        count += 1
        failed_pdfs.append(str(count) + ' - FALHOU EM RENOMEAR: [' + pdf + " ----> " + str(new_file_name) + "]")


# Se houvesse PDFs que não pudessem ser renomeados (têm o mesmo nome)
# em seguida, imprima-os em um arquivo de texto na pasta junto aos outros PDFs
chdir(get_curr)
if len(failed_pdfs) > 0:
    with open(directory + 'PDF_FAILURES.txt', 'w') as f:
        for failure in failed_pdfs:
            f.writelines(failure + '\n')

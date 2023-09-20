import os
import pandas as pd
from langchain.embeddings import HuggingFaceEmbeddings
import PyPDF2
import re


# Método para convertir un PDF en texto plano
def extraer_texto_pdf(ruta_archivo):
    with open(ruta_archivo, 'rb') as archivo:
        lector_pdf = PyPDF2.PdfReader(archivo)
        texto = ''
        for pagina in lector_pdf.pages:
            texto += pagina.extract_text()
    return texto

# Método para extraer la información principal de un fondo
def get_info_fondo(NIF):
    ruta_archivo = "registroPDFs/" + NIF + ".pdf"
    informe = extraer_texto_pdf(ruta_archivo)

    texto = informe[:500].replace('\n', '')
    print("\n\n" + texto)
    
    # Extraer el nombre del fondo
    nombre_fondo = re.search(r'^(.*?)Nº', texto, re.DOTALL).group(1)
    nombre_fondo = re.sub(r'\d', '', nombre_fondo)
    print("\n\nNombre y tipo del fondo:", nombre_fondo)

    # Extraer el número de registro CNMV
    registro_cnmv = re.search(r'Nº Registro CNMV: (\d+)', texto).group(1)
    print("Nº Registro CNMV:", registro_cnmv)

    # Extraer la gestora
    gestora = re.search(r'Gestora:\s?(.+?)Depo', texto).group(1)
    print("Gestora:", gestora)

    # Extraer el depositario
    depositario = re.search(r'Depositario:\s?(.+?)Aud', texto).group(1)
    print("Depositario:", depositario)

    # Extraer el auditor
    auditor = re.search(r'Auditor:\s?(.+?)Grup', texto).group(1)
    print("Auditor:", auditor)

    info_fondo = {
        "nombre_fondo": nombre_fondo,
        "registro_cnmv": registro_cnmv,
        "gestora": gestora,
        "depositario": depositario,
        "auditor": auditor
    }

    return info_fondo

# Metodo para extraer el anexo explciativo de un informe partiendo de su NIF
def get_anexo(NIF):
    ruta_archivo = "registroPDFs/" + NIF + ".pdf"
    informe = extraer_texto_pdf(ruta_archivo)
    texto_split = informe.split('9. Anexo explicativo del informe periódico')
    texto_split = texto_split[1].split('10. Detalle de inversiones financieras')
    anexo_explicativo = texto_split[0]
    return anexo_explicativo

def mi_funcion():

    path_registro = os.path.join('data', 'registro.csv')
    registro = pd.read_csv(path_registro, sep=';', encoding='utf-8')
    print(registro)
    # guardarlos en un csv

# Metodo para obtener una lista con todos los NIFs explorando el directorio con los Informes periodicos
def get_NIFs_from_PDFs():
    NIFs = []
    files = os.listdir('registroPDFs')
    for doc_name in files:
        NIF = doc_name[:-4]
        NIFs.append(NIF)
    return NIFs

# metodo para obtener una lista con los NIFs que se encuentran en un CSV
def get_NIFs_from_CSV(filename):
    df = pd.read_csv(filename)
    NIFs = df['NIF']
    return NIFs

def get_max_tokens(model_id):
    #LLM = HuggingFaceEmbeddings(model_name="Helsinki-NLP/opus-mt-en-es")
    LLM = HuggingFaceEmbeddings(model_name=model_id)
    #print(f"Maximum embedded sequence length: {LLM.client.get_max_seq_length()}")
    return LLM.client.get_max_seq_length()
    

def testeo():
    path_registro_info_fondos = os.path.join('data', 'registro_main_data.csv')
    registro_info_fondos = pd.read_csv(path_registro_info_fondos, sep=';', encoding='utf-8')
    selected_NIF = "V-65433930"

    fondo_concreto = registro_info_fondos.loc[registro_info_fondos['NIF'] == selected_NIF]
    #print(fondo_concreto)

    
    nombre_fondo = fondo_concreto['NOMBRE FONDO'].values[0]
    registro_cnmv = fondo_concreto['NUMERO REGISTRO CNMV'].values[0]
    gestora = fondo_concreto['GESTORA'].values[0]
    depositario = fondo_concreto['DEPOSITARIO'].values[0]
    auditor = fondo_concreto['AUDITOR'].values[0]

    print("Nombre del fondo:", nombre_fondo)
    print("Registro CNMV:", registro_cnmv)
    print("Gestora:", gestora)
    print("Depositario:", depositario)
    print("Auditor:", auditor)

if __name__=="__main__":
    #get_info_fondo("V-65433930")
    mi_funcion()
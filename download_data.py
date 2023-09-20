# ESTE FICHERO DESCARGA LOS PDFs Y TODO DEBERIA ALMACENARLOS EN EL DIRECTORIO CORRESPONDIENTE

import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, SessionNotCreatedException
import time

# para ordenarPDFs()
import os

#para copiar_elemento()
from selenium.webdriver.chrome.service import Service


# Método para descarga el Informe Periódico de un fondo a partir del NIF que recibe por parámetro.
# Se descarga en formato PDF y con nombre 'NIF_de_fondo.pdf'
def descargar_pdf(NIF):
    driver = None
    while driver == None:
        try:
            # Inicializar el navegador controlado por Selenium
            driver = webdriver.Chrome(executable_path="C:/Users/gcanc/.cache/selenium/chromedriver/win32/114.0.5735.90/chromedriver.exe")
        except SessionNotCreatedException as e:
                # Handle the exception
                print("Error: Failed to create a session with Chrome WebDriver.")
                print(f"Exception details: {e}")
                driver = None
                time.sleep(2)  # Wait for a few seconds before retrying


    # Cargar la página web
    url = "https://www.cnmv.es/Portal/Consultas/IIC/Fondo.aspx?nif=" + NIF + "&vista=1"
    driver.get(url)

    # Esperar hasta que el elemento esté presente y visible
    enlace_element = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "ctl00_ContentPrincipal_wIPPS_gridIPPS_ctl02_lnkPDF"))
    )

    # Obtener la URL del enlace de descarga
    enlace_descarga = enlace_element.get_attribute("href")

    # Abrir el documento utilizando la URL del enlace de descarga
    driver.get(enlace_descarga)
    
    # Obtener el contenido del archivo PDF
    response = requests.get(driver.current_url)

    # Guardar el archivo PDF en disco
    nombre_archivo = NIF + '.pdf'
    with open(nombre_archivo, 'wb') as archivo:
        archivo.write(response.content)

    print("Archivo descargado:", nombre_archivo)

    #time.sleep(2)

    # Cerrar el navegador controlado por Selenium
    driver.quit()

# Método que accede a a páginca de la CNMV y encuentra el elemento HTML donde se encuentra un menú desplegable
# con todos los fondos registrados. Devuelve el elemento HTML completo
def copiar_elemento():
    # Configurar el controlador del navegador Chrome
    #service = Service('C:/Users/gcanc/.cache/selenium/chromedriver/win32/114.0.5735.90/chromedriver.exe')
    #driver = webdriver.Chrome(service=service)
    driver = webdriver.Chrome(executable_path="C:/Users/gcanc/.cache/selenium/chromedriver/win32/114.0.5735.90/chromedriver.exe")

    # Cargar la página web
    url = 'https://www.cnmv.es/Portal/consultas/busqueda.aspx?id=12'
    driver.get(url)

    # Encontrar el botón "Buscar"
    buscar_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ctl00_ContentPrincipal_btnOk"))
    )

    # Ejecutar JavaScript para hacer clic en el botón
    driver.execute_script("arguments[0].click();", buscar_button)

    # Esperar a que aparezca el elemento select
    select_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "ctl00_ContentPrincipal_wbusqueda_lstSeleccion"))
    )

    # Obtener el contenido HTML del elemento select
    select_html = select_element.get_attribute("innerHTML")

    # Cerrar el navegador controlado por Selenium
    driver.quit()

    return select_html

# Método para extraer en un array los NIFs de los fondos que hay en el elemento HTML.
# Devuelve un array con los NIFs
def extraer_NIFs(elemento):
    # Dividimos el elemento (str) por las comillas para separar los NIFs del resto del contenido
    splitted = elemento.split('"')

    # Tomamos los valores impares de splitted, ya que contienen los NIFs
    NIFs = []
    for i in range(1, len(splitted), 2):
        NIFs.append(splitted[i])

    # Quitamos el primer elemento que corresponde a "selected"
    NIFs.pop(0)

    return NIFs

# Método para meter los PDFs de los Informes Periódicos en un subdirectorio PDF con el propósito
# de ordenar el directorio principal. (Puede integrarse en la función descrgar_pdf para que 
# se guarde directamente en el subdirectorio)
def ordenarPDFs():
    ficheros = os.listdir()
    for fichero in ficheros:
        if fichero.endswith(".pdf"):
            ruta_destino = os.path.join("PDFs", fichero)
            os.rename(fichero, ruta_destino)

def main():
    elemento = copiar_elemento()
    NIFs = extraer_NIFs(elemento)
    NIFs_error = [] # Para almacenar los NIFs que den fallo y volverlo a intentar en otro momento

    # Descargamos los PDFs gracias a la lista de NIFs
    i_error = 0
    for i in range(1 , len(NIFs)):
    #for i in range(1, 10):
        try:
            descargar_pdf(NIFs[i])
            print(str(i) + " / " + str(len(NIFs)) + " ficheros procesados")
            if i_error!=0: print(str(i_error) + "errores en descarga")
        except TimeoutException:
            print("Error al descargar el archivo PDF del fondo con NIF ", NIFs[i])
            NIFs_error.append(NIFs[i]) #TODO: Y con esto qué hago?
            i_error+=1
            
    #ordenarPDFs()

if __name__ == '__main__':
    main()

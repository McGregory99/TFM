# ESTE FICHERO TOMA LOS PDFS, EXTRAE EL ANEXO EXPLICATIVO, LO DESGLOSA Y LO GUARDA EN UN CSV
import os
import pandas as pd
import re
import defs
import inference_HF
 
# Método para extraer los anexos de los Informes Periodicos, desglosarlos y almacenarlos en un CSV
def save_anexos():
    ficheros = os.listdir('registroPDFs')

    i = 1

    NIFs = []
    anexos_explicativos = []
    situacion_mercados_evolucion_fondo = []
    informacion_sobre_inversiones = []
    evolucion_objetivo_rentabilidad = []
    riesgo_asumido_por_fondo = []
    perspectiva_mercado = []
    otra_informacion = []

    for doc_name in ficheros:
        NIF = doc_name[:-4]
        print("\n\n" + str(NIF))

        # Extraermos el anexo y lo guardamos para almacenarlo en el CSV
        anexo_explicativo = defs.get_anexo(NIF)
        anexos_explicativos.append(anexo_explicativo)
        
        # Quitamos los '\n' para que el REGEX sea más sencillo
        anexo_explicativo = anexo_explicativo.replace('\n', ' ')
        anexo_explicativo = anexo_explicativo.replace('  ', ' ')

        # Analizazmos el texto empleando REGEX para extraer los fragmentos del Anexo Explicativo
        patron = r"SITUACI[OÓ]N DE LOS MERCADOS Y EVOLUCI[OÓ]N DEL FONDO"
        if re.search(patron, anexo_explicativo, flags=re.IGNORECASE)==None:
            patron = r"SITUACI[OÓ]N DE LOS MERCADOS Y EVOLUCI[OÓ]N DE LA IIC"
            if re.search(patron, anexo_explicativo, flags=re.IGNORECASE)==None:
                patron = r"SITUACI[OÓ]N DE LOS MERCADOS"
        partes = re.split(patron, anexo_explicativo, flags=re.IGNORECASE)

        patron = r"INFORMACI[OÓ]N SOBRE LAS INVERSIONES"
        if re.search(patron, partes[1], flags=re.IGNORECASE)==None:
            patron = r"INFORMACI[OÓ]N SOBRE INVERSIONES"
            if re.search(patron, partes[1], flags=re.IGNORECASE)==None:
                patron = r"INVERSIONES Y DESINVERSIONES EN EL PERIODO"
        partes = re.split(patron, partes[1], flags=re.IGNORECASE)
        #print("\n1. SITUACIÓN DE LOS MERCADOS Y EVOLUCIÓN DEL FONDO: ")
        #print(partes[0][:100])
        situacion_mercados_evolucion_fondo.append(partes[0])
        resto_texto = ''.join(partes[1:])

        patron = r"EVOLUCI[OÓ]N DEL OBJETIVO CONCRETO DE RENTABILIDAD"
        if re.search(patron, anexo_explicativo, flags=re.IGNORECASE)==None:
            patron = r"EVOLUCI[OÓ]N DEL OBJETIVO CONCRETO DE VOLATILIDAD"
        partes = re.split(patron, resto_texto, flags=re.IGNORECASE)
        #print("2. INFORMACIÓN SOBRE LAS INVERSIONES: ")
        #print(partes[0][:100])
        informacion_sobre_inversiones.append(partes[0])
        resto_texto = ''.join(partes[1:])

        patron = r"4.\sRIESGO ASUMIDO POR LA IIC"
        if re.search(patron, resto_texto[:100], flags=re.IGNORECASE)==None:
            patron = r"4.\sRIESGO ASUMIDOS POR EL FONDO"
            if re.search(patron, resto_texto[:100], flags=re.IGNORECASE)==None:
                patron = r"4.\sRIESGO ASUMIDOS POR LA IIC"
                if re.search(patron, resto_texto[:100], flags=re.IGNORECASE)==None:
                    patron = r"4.\sRIESGO ASUMIDO POR EL FONDO"
                    if re.search(patron, resto_texto[:100], flags=re.IGNORECASE)==None:
                        patron = r"4.?\sRIESGO ACUMULADO DEL FONDO"
                        if re.search(patron, resto_texto[:100], flags=re.IGNORECASE)==None:
                            patron = r"4.RIESGO ASUMIDO POR EL FONDO"
        partes = re.split(patron, partes[1], flags=re.IGNORECASE)
        #print("3. EVOLUCIÓN DEL OBJETIVO CONCRETO DE RENTABILIDAD: ")
        #print(partes[0][:100])
        evolucion_objetivo_rentabilidad.append(partes[0])
        resto_texto = ''.join(partes[1:])

        patron = r"EJERCICIO DE DERECHOS POL[IÍ]TICOS"
        if re.search(patron, resto_texto, flags=re.IGNORECASE)==None:
            patron = r"EJERCICIO DERECHOS POL[IÍ]TICOS"
            if re.search(patron, resto_texto, flags=re.IGNORECASE)==None:
                patron = r"EJERCICIO DE LOS DERECHOS POL[IÍ]TICOS"
        partes = re.split(patron, resto_texto, flags=re.IGNORECASE)
        #print("4. RIESGO ASUMIDO POR EL FONDO: ")
        #print(partes[0][:100])
        riesgo_asumido_por_fondo.append(partes[0])
        resto_texto = ''.join(partes[1:])     

        patron = r"PERSPECTIVAS DE MERCADO Y ACTUACI[OÓ]N PREVISIBLE DEL FONDO"
        partes = re.split(patron, resto_texto, flags=re.IGNORECASE)
        #print("10. PERSPECTIVAS DE MERCADO Y ACTUACIÓN PREVISIBLE DEL FONDO: ")
        #print(partes[1])
        perspectiva_mercado.append(partes[1])
        resto_texto = resto_texto.replace(partes[1], "")

        otra_informacion.append(resto_texto)
        NIFs.append(NIF)   

        print(f'{i}/{len(ficheros)} ficheros procesados\n\n')
        i+=1
        if i==20: break

        '''except IndexError:
            ruta_origen = os.path.join("registroPDFs", doc_name)
            ruta_destino = os.path.join("PDF_malformato", doc_name)
            try:
                os.rename(ruta_origen, ruta_destino)
                print(f"Archivo '{doc_name}' movido exitosamente a 'PDF_malformato'.")
            except FileNotFoundError:
                print(f"El archivo '{doc_name}' no se encontró en 'registroPDFs'.")
            except Exception as e:
                print(f"Ocurrió un error al mover el archivo: {e}")

        respuesta = input("¿Formato correcto? [s/n]")
        if respuesta== "s":
            ruta_origen = os.path.join("registroPDFs", doc_name)
            ruta_destino = os.path.join("buenosPDFs", doc_name)
            try:
                os.rename(ruta_origen, ruta_destino)
                print(f"Archivo '{doc_name}' movido exitosamente a 'buenosPDFs'.")
            except FileNotFoundError:
                print(f"El archivo '{doc_name}' no se encontró en 'registroPDFs'.")
            except Exception as e:
                print(f"Ocurrió un error al mover el archivo: {e}")
        if respuesta== "n":
            ruta_origen = os.path.join("registroPDFs", doc_name)
            ruta_destino = os.path.join("PDF_malformato", doc_name)
            try:
                os.rename(ruta_origen, ruta_destino)
                print(f"Archivo '{doc_name}' movido exitosamente a 'PDF_malformato'.")
            except FileNotFoundError:
                print(f"El archivo '{doc_name}' no se encontró en 'registroPDFs'.")
            except Exception as e:
                print(f"Ocurrió un error al mover el archivo: {e}")'''
        


    data = {
    'NIF': NIFs,
    'SITUACIÓN MERCADOS. EVOLUCION FONDO': situacion_mercados_evolucion_fondo,
    'INFORMACIÓN SOBRE INVERSIONES': informacion_sobre_inversiones,
    'EVOLUCIÓN OBJETIVO RENTABILIDAD': evolucion_objetivo_rentabilidad,
    'RIESGO ASUMIDO': riesgo_asumido_por_fondo,
    'PERSPECTIVA DE MERCADO' : perspectiva_mercado,
    'MÁS INFORMACIÓN': otra_informacion,
    'ANEXO COMPLETO': anexos_explicativos
    }

    df = pd.DataFrame(data)
    path_registro = os.path.join('data', 'registro.csv')
    df.to_csv(path_registro, sep=';', encoding='utf-8', index=False)
     
# Método para extraer información (nombre, gestora, depositario...) de los Informes Periódicos. Se almacena en un CSV
def save_main_data():
    ficheros = os.listdir('registroPDFs')

    nombre_fondo = []
    registro_cnmv = []
    gestora = []
    depositario = []
    auditor = []
    NIFs = []

    for doc_name in ficheros:
        NIF = doc_name[:-4]
        NIFs.append(NIF)
        print("\n\n" + str(NIF))

        info_fondo = defs.get_info_fondo(NIF)
        
        nombre_fondo.append(info_fondo["nombre_fondo"])
        registro_cnmv.append(info_fondo["registro_cnmv"])
        gestora.append(info_fondo["gestora"])
        depositario.append(info_fondo["depositario"])
        auditor.append(info_fondo["auditor"])

    data = {
    'NIF': NIFs,
    'NOMBRE FONDO': nombre_fondo,
    'NUMERO REGISTRO CNMV': registro_cnmv,
    'GESTORA': gestora,
    'DEPOSITARIO': depositario,
    'AUDITOR': auditor,
    }

    df = pd.DataFrame(data)
    path_registro_main_data = os.path.join('data', 'registro_main_data.csv')
    df.to_csv(path_registro_main_data, sep=';', encoding='utf-8', index=False)

# Método para traducir registro.csv y generar registro_ENG.csv
def traducir_anexos_ES_EN():

    path_registro = os.path.join('data', 'registro.csv')
    df = pd.read_csv(path_registro, sep=';', encoding='utf-8')

    # guardar las columnas de df en arrays
    NIFs = df['NIF']
    situacion_mercados_evolucion_fondo = df['SITUACIÓN MERCADOS. EVOLUCION FONDO']
    informacion_sobre_inversiones = df['INFORMACIÓN SOBRE INVERSIONES']
    evolucion_objetivo_rentabilidad = df['EVOLUCIÓN OBJETIVO RENTABILIDAD']
    riesgo_asumido_por_fondo = df['RIESGO ASUMIDO']
    perspectiva_mercado = df['PERSPECTIVA DE MERCADO']
    
    print("\n\nTRADUCIENDO ANEXOS DE ESPAÑOL A INGLES...")
    # recorrer cada array e ir llamando al metodo traducir
    i=1
    situacion_mercados_evolucion_fondo_ENG = []
    for elemento in situacion_mercados_evolucion_fondo:
        elemento_ENG = inference_HF.translate_text_ES_EN(elemento)
        situacion_mercados_evolucion_fondo_ENG.append(elemento_ENG)
        print(f'{i}/{len(situacion_mercados_evolucion_fondo)} [situacion_mercados_evolucion_fondo] traducido\n')
        i+=1

    i=1
    informacion_sobre_inversiones_ENG = []
    for elemento in informacion_sobre_inversiones:
        elemento_ENG = inference_HF.translate_text_ES_EN(elemento)
        informacion_sobre_inversiones_ENG.append(elemento_ENG)
        print(f'{i}/{len(informacion_sobre_inversiones)} [informacion_sobre_inversiones] traducido\n')
        i+=1

    i=1
    evolucion_objetivo_rentabilidad_ENG = []
    for elemento in evolucion_objetivo_rentabilidad:
        elemento_ENG = inference_HF.translate_text_ES_EN(elemento)
        evolucion_objetivo_rentabilidad_ENG.append(elemento_ENG)
        print(f'{i}/{len(evolucion_objetivo_rentabilidad)} [evolucion_objetivo_rentabilidad] traducido\n')
        i+=1
    
    i=1
    riesgo_asumido_por_fondo_ENG = []
    for elemento in riesgo_asumido_por_fondo:
        elemento_ENG = inference_HF.translate_text_ES_EN(elemento)
        riesgo_asumido_por_fondo_ENG.append(elemento_ENG)
        print(f'{i}/{len(riesgo_asumido_por_fondo)} [riesgo_asumido_por_fondo] traducido\n')
        i+=1

    i=1
    perspectiva_mercado_ENG = []
    for elemento in perspectiva_mercado:
        elemento_ENG = inference_HF.translate_text_ES_EN(elemento)
        perspectiva_mercado_ENG.append(elemento_ENG)
        print(f'{i}/{len(perspectiva_mercado)} [perspectiva_mercado] traducido\n')
        i+=1

    # juntamos los que ya tenemos con los nuevos y lo almacenamos en los arrays nuevos
    #df_ENG = pd.read_csv('test_registro_final_ENG.csv', sep=';', encoding='utf-8')
    #NIFs = pd.concat([df_ENG['NIF'], pd.Series(NIFs)], ignore_index=True)
    #situacion_mercados_evolucion_fondo_ENG = pd.concat([df_ENG['SITUACIÓN MERCADOS. EVOLUCION FONDO'], pd.Series(situacion_mercados_evolucion_fondo_ENG)], ignore_index=True)
    
    
    data = {
    'NIF': NIFs,
    'SITUACIÓN MERCADOS. EVOLUCION FONDO': situacion_mercados_evolucion_fondo_ENG,
    'INFORMACIÓN SOBRE INVERSIONES': informacion_sobre_inversiones_ENG,
    'EVOLUCIÓN OBJETIVO RENTABILIDAD': evolucion_objetivo_rentabilidad_ENG,
    'RIESGO ASUMIDO': riesgo_asumido_por_fondo_ENG,
    'PERSPECTIVA DE MERCADO' : perspectiva_mercado_ENG,
    }

    df_ENG = pd.DataFrame(data)
    path_registro_ENG = os.path.join('data', 'registro_ENG.csv')
    df_ENG.to_csv(path_registro_ENG, sep=';', encoding='utf-8', index=False)

############################################################

# Metodo para abrir CSV registro, resumir el texto de cada celda con META/BART (en ingles) y guardarlo en un nuevo CSV
def save_summarization_bart():
    path_registro_ENG = os.path.join('data', 'registro_ENG.csv')
    df = pd.read_csv(path_registro_ENG, sep=';', encoding='utf-8')

    # Abrimos las columnas para realizar el analisis de sentimientos
    NIFs = df['NIF']
    situacion_mercados_evolucion_fondo = df['SITUACIÓN MERCADOS. EVOLUCION FONDO']
    informacion_sobre_inversiones = df['INFORMACIÓN SOBRE INVERSIONES']
    riesgo_asumido_por_fondo = df['RIESGO ASUMIDO']
    perspectiva_mercado = df['PERSPECTIVA DE MERCADO']

    print("\n\nRESUMIENDO TEXTOS CON BART...")
    # Recorremos columna a columna y celda a celda llamando al modelo
    i=1
    situacion_mercados_evolucion_fondo_SUMMARY = []
    for elemento in situacion_mercados_evolucion_fondo:
        elemento_SUMMARY = inference_HF.summarize_BART(elemento)
        situacion_mercados_evolucion_fondo_SUMMARY.append(elemento_SUMMARY)
        print(f'{i}/{len(situacion_mercados_evolucion_fondo)} [situacion_mercados_evolucion_fondo] resumido\n')
        i+=1
    
    i=1
    informacion_sobre_inversiones_SUMMARY = []
    for elemento in informacion_sobre_inversiones:
        elemento_SUMMARY = inference_HF.summarize_BART(elemento)
        informacion_sobre_inversiones_SUMMARY.append(elemento_SUMMARY)
        print(f'{i}/{len(informacion_sobre_inversiones)} [informacion_sobre_inversiones] resumido\n')
        i+=1

    i=1
    riesgo_asumido_por_fondo_SUMMARY = []
    for elemento in riesgo_asumido_por_fondo:
        elemento_SUMMARY = inference_HF.summarize_BART(elemento)
        riesgo_asumido_por_fondo_SUMMARY.append(elemento_SUMMARY)
        print(f'{i}/{len(riesgo_asumido_por_fondo)} [riesgo_asumido_por_fondo] resumido\n')
        i+=1

    i=1
    perspectiva_mercado_SUMMARY = []
    for elemento in perspectiva_mercado:
        elemento_SUMMARY = inference_HF.summarize_BART(elemento)
        perspectiva_mercado_SUMMARY.append(elemento_SUMMARY)
        print(f'{i}/{len(perspectiva_mercado)} [perspectiva_mercado] resumido\n')
        i+=1
    
    # Almacenamos en un dataframe los arrays para convertislo en un CSV
    data = {
    'NIF': NIFs,
    'SITUACIÓN MERCADOS. EVOLUCION FONDO': situacion_mercados_evolucion_fondo_SUMMARY,
    'INFORMACIÓN SOBRE INVERSIONES': informacion_sobre_inversiones_SUMMARY,
    'RIESGO ASUMIDO': riesgo_asumido_por_fondo_SUMMARY,
    'PERSPECTIVA DE MERCADO': perspectiva_mercado_SUMMARY
    }

    df_SUMMARY = pd.DataFrame(data)
    path_resumen_BART_ENG = os.path.join('data', 'resumen_BART_ENG.csv')
    df_SUMMARY.to_csv(path_resumen_BART_ENG, sep=';', encoding='utf-8', index=False)

# Metodo para abrir CSV registro, resumir el texto de cada celda con GOOGLE/PEGASUS (en ingles) y guardarlo en un nuevo CSV
def save_summarization_pegasus():
    path_registro_ENG = os.path.join('data', 'registro_ENG.csv')
    df = pd.read_csv(path_registro_ENG, sep=';', encoding='utf-8')

    # Abrimos las columnas para realizar el analisis de sentimientos
    NIFs = df['NIF']
    situacion_mercados_evolucion_fondo = df['SITUACIÓN MERCADOS. EVOLUCION FONDO']
    informacion_sobre_inversiones = df['INFORMACIÓN SOBRE INVERSIONES']
    riesgo_asumido_por_fondo = df['RIESGO ASUMIDO']
    perspectiva_mercado = df['PERSPECTIVA DE MERCADO']

    print("\n\nRESUMIENDO TEXTOS CON PEGASUS...")
    # Recorremos columna a columna y celda a celda llamando al modelo
    i=1
    situacion_mercados_evolucion_fondo_SUMMARY = []
    for elemento in situacion_mercados_evolucion_fondo:
        elemento_SUMMARY = inference_HF.summarize_PEGASUS(elemento)
        situacion_mercados_evolucion_fondo_SUMMARY.append(elemento_SUMMARY)
        print(f'{i}/{len(situacion_mercados_evolucion_fondo)} [situacion_mercados_evolucion_fondo] resumido')
        i+=1

    i=1
    informacion_sobre_inversiones_SUMMARY = []
    for elemento in informacion_sobre_inversiones:
        elemento_SUMMARY = inference_HF.summarize_PEGASUS(elemento)
        informacion_sobre_inversiones_SUMMARY.append(elemento_SUMMARY)
        print(f'{i}/{len(informacion_sobre_inversiones)} [informacion_sobre_inversiones] resumido')
        i+=1

    i=1
    riesgo_asumido_por_fondo_SUMMARY = []
    for elemento in riesgo_asumido_por_fondo:
        elemento_SUMMARY = inference_HF.summarize_PEGASUS(elemento)
        riesgo_asumido_por_fondo_SUMMARY.append(elemento_SUMMARY)
        print(f'{i}/{len(riesgo_asumido_por_fondo)} [riesgo_asumido_por_fondo] resumido')
        i+=1

    i=1
    perspectiva_mercado_SUMMARY = []
    for elemento in perspectiva_mercado:
        elemento_SUMMARY = inference_HF.summarize_PEGASUS(elemento)
        perspectiva_mercado_SUMMARY.append(elemento_SUMMARY)
        print(f'{i}/{len(perspectiva_mercado)} [perspectiva_mercado] resumido')
        i+=1
    
    # Almacenamos en un dataframe los arrays para convertislo en un CSV
    data = {
    'NIF': NIFs,
    'SITUACIÓN MERCADOS. EVOLUCION FONDO': situacion_mercados_evolucion_fondo_SUMMARY,
    'INFORMACIÓN SOBRE INVERSIONES': informacion_sobre_inversiones_SUMMARY,
    'RIESGO ASUMIDO': riesgo_asumido_por_fondo_SUMMARY,
    'PERSPECTIVA DE MERCADO': perspectiva_mercado_SUMMARY
    }

    df_SUMMARY = pd.DataFrame(data)
    path_resumen_PEGASUS_ENG = os.path.join('data', 'resumen_PEGASUS_ENG.csv')
    df_SUMMARY.to_csv(path_resumen_PEGASUS_ENG, sep=';', encoding='utf-8', index=False)
    
# Taducir el resumen de pegasus del ingles al español
def save_resumen_pegasus():
    path_resumen_PEGASUS_ENG = os.path.join('data', 'resumen_PEGASUS_ENG.csv')
    df = pd.read_csv(path_resumen_PEGASUS_ENG, sep=';', encoding='utf-8')

    NIFs = df['NIF']
    situacion_mercados_evolucion_fondo_SUMMARY = df['SITUACIÓN MERCADOS. EVOLUCION FONDO']
    informacion_sobre_inversiones_SUMMARY =  df['INFORMACIÓN SOBRE INVERSIONES']
    riesgo_asumido_por_fondo_SUMMARY = df['RIESGO ASUMIDO']
    perspectiva_mercado_SUMMARY = df['PERSPECTIVA DE MERCADO']
    
    print("\n\nTRADUCIENDO RESUMENES DE PEGASUS AL ESPAÑOL...")
    # Recorremos columna a columna y celda a celda llamando al modelo
    i=1
    situacion_mercados_evolucion_fondo_SUMMARY_ESP = []
    for resumen_ENG in situacion_mercados_evolucion_fondo_SUMMARY:
        resumen_ESP = inference_HF.translate_text_EN_ES(resumen_ENG)
        situacion_mercados_evolucion_fondo_SUMMARY_ESP.append(resumen_ESP)
        print(f'{i}/{len(situacion_mercados_evolucion_fondo_SUMMARY)} [situacion_mercados_evolucion_fondo] resumen traducidon')
        i+=1

    i=1
    informacion_sobre_inversiones_SUMMARY_ESP = []
    for resumen_ENG in informacion_sobre_inversiones_SUMMARY:
        resumen_ESP = inference_HF.translate_text_EN_ES(resumen_ENG)
        informacion_sobre_inversiones_SUMMARY_ESP.append(resumen_ESP)
        print(f'{i}/{len(informacion_sobre_inversiones_SUMMARY)} [informacion_sobre_inversiones] resumen traducido')
        i+=1

    i=1
    riesgo_asumido_por_fondo_SUMMARY_ESP = []
    for resumen_ENG in riesgo_asumido_por_fondo_SUMMARY:
        resumen_ESP = inference_HF.translate_text_EN_ES(resumen_ENG)
        riesgo_asumido_por_fondo_SUMMARY_ESP.append(resumen_ESP)
        print(f'{i}/{len(riesgo_asumido_por_fondo_SUMMARY)} [riesgo_asumido_por_fondo] resumen traducido')
        i+=1

    i=1
    perspectiva_mercado_SUMMARY_ESP = []
    for resumen_ENG in perspectiva_mercado_SUMMARY:
        resumen_ESP = inference_HF.translate_text_EN_ES(resumen_ENG)
        perspectiva_mercado_SUMMARY_ESP.append(resumen_ESP)
        print(f'{i}/{len(perspectiva_mercado_SUMMARY)} [perspectiva_mercado] resumen traducido')
        i+=1
    
    # Almacenamos en un dataframe los arrays para convertislo en un CSV
    data = {
    'NIF': NIFs,
    'SITUACIÓN MERCADOS. EVOLUCION FONDO': situacion_mercados_evolucion_fondo_SUMMARY_ESP,
    'INFORMACIÓN SOBRE INVERSIONES': informacion_sobre_inversiones_SUMMARY_ESP,
    'RIESGO ASUMIDO': riesgo_asumido_por_fondo_SUMMARY_ESP,
    'PERSPECTIVA DE MERCADO': perspectiva_mercado_SUMMARY_ESP
    }

    df_SUMMARY_ESP = pd.DataFrame(data)
    path_resumen_PEGASUS = os.path.join('data', 'resumen_PEGASUS.csv')
    df_SUMMARY_ESP.to_csv(path_resumen_PEGASUS, sep=';', encoding='utf-8', index=False)

# traducir el resumen de bart de epañol a ingles
def save_resumen_bart():
    path_resumen_BART_ENG = os.path.join('data', 'resumen_BART_ENG.csv')
    df = pd.read_csv(path_resumen_BART_ENG, sep=';', encoding='utf-8')

    NIFs = df['NIF']
    situacion_mercados_evolucion_fondo_SUMMARY = df['SITUACIÓN MERCADOS. EVOLUCION FONDO']
    informacion_sobre_inversiones_SUMMARY =  df['INFORMACIÓN SOBRE INVERSIONES']
    riesgo_asumido_por_fondo_SUMMARY = df['RIESGO ASUMIDO']
    perspectiva_mercado_SUMMARY = df['PERSPECTIVA DE MERCADO']
    
    print("\n\nTRADUCIENDO RESUMENES DE PEGASUS AL ESPAÑOL...")
    # Recorremos columna a columna y celda a celda llamando al modelo
    i=1
    situacion_mercados_evolucion_fondo_SUMMARY_ESP = []
    for resumen_ENG in situacion_mercados_evolucion_fondo_SUMMARY:
        resumen_ESP = inference_HF.translate_text_EN_ES(resumen_ENG)
        situacion_mercados_evolucion_fondo_SUMMARY_ESP.append(resumen_ESP)
        print(f'{i}/{len(situacion_mercados_evolucion_fondo_SUMMARY)} [situacion_mercados_evolucion_fondo] resumen traducidon')
        i+=1

    i=1
    informacion_sobre_inversiones_SUMMARY_ESP = []
    for resumen_ENG in informacion_sobre_inversiones_SUMMARY:
        resumen_ESP = inference_HF.translate_text_EN_ES(resumen_ENG)
        informacion_sobre_inversiones_SUMMARY_ESP.append(resumen_ESP)
        print(f'{i}/{len(informacion_sobre_inversiones_SUMMARY)} [informacion_sobre_inversiones] resumen traducido')
        i+=1

    i=1
    riesgo_asumido_por_fondo_SUMMARY_ESP = []
    for resumen_ENG in riesgo_asumido_por_fondo_SUMMARY:
        resumen_ESP = inference_HF.translate_text_EN_ES(resumen_ENG)
        riesgo_asumido_por_fondo_SUMMARY_ESP.append(resumen_ESP)
        print(f'{i}/{len(riesgo_asumido_por_fondo_SUMMARY)} [riesgo_asumido_por_fondo] resumen traducido')
        i+=1

    i=1
    perspectiva_mercado_SUMMARY_ESP = []
    for resumen_ENG in perspectiva_mercado_SUMMARY:
        resumen_ESP = inference_HF.translate_text_EN_ES(resumen_ENG)
        perspectiva_mercado_SUMMARY_ESP.append(resumen_ESP)
        print(f'{i}/{len(perspectiva_mercado_SUMMARY)} [perspectiva_mercado] resumen traducido')
        i+=1
    
    # Almacenamos en un dataframe los arrays para convertislo en un CSV
    data = {
    'NIF': NIFs,
    'SITUACIÓN MERCADOS. EVOLUCION FONDO': situacion_mercados_evolucion_fondo_SUMMARY_ESP,
    'INFORMACIÓN SOBRE INVERSIONES': informacion_sobre_inversiones_SUMMARY_ESP,
    'RIESGO ASUMIDO': riesgo_asumido_por_fondo_SUMMARY_ESP,
    'PERSPECTIVA DE MERCADO': perspectiva_mercado_SUMMARY_ESP
    }

    df_SUMMARY_ESP = pd.DataFrame(data)
    path_resumen_BART = os.path.join('data', 'resumen_BART.csv')
    df_SUMMARY_ESP.to_csv(path_resumen_BART, sep=';', encoding='utf-8', index=False)
    
####################################################################

# Metodo para abrir CSV registro, analizar sentimientos de cada celda y guardarlos en un nuevo CSV
def save_sentiment_analysis_full_text():
    path_registro_ENG = os.path.join('data', 'registro_ENG.csv')
    df = pd.read_csv(path_registro_ENG, sep=';', encoding='utf-8')

    # Abrimos las columnas para realizar el analisis de sentimientos
    NIFs = df['NIF']
    situacion_mercados_evolucion_fondo = df['SITUACIÓN MERCADOS. EVOLUCION FONDO']
    informacion_sobre_inversiones = df['INFORMACIÓN SOBRE INVERSIONES']
    riesgo_asumido_por_fondo = df['RIESGO ASUMIDO']
    perspectiva_mercado = df['PERSPECTIVA DE MERCADO']

    print("PROCESANDO SENTIMIENTOS DEL TEXTO COMPLETO...")
    # Recorremos columna a columna y celda a celda llamando al modelo
    i=1
    situacion_mercados_evolucion_fondo_SENTIMENT = []
    for elemento in situacion_mercados_evolucion_fondo:
        elemento_SENTIMENT = inference_HF.analize_sentiment_full_text(elemento)
        situacion_mercados_evolucion_fondo_SENTIMENT.append(elemento_SENTIMENT)
        
        print(f'{i}/{len(situacion_mercados_evolucion_fondo)} [situacion_mercados_evolucion_fondo] sentimiento analizado')
        i+=1

    i=1
    informacion_sobre_inversiones_SENTIMENT = []
    for elemento in informacion_sobre_inversiones:
        elemento_SENTIMENT = inference_HF.analize_sentiment_full_text(elemento)
        informacion_sobre_inversiones_SENTIMENT.append(elemento_SENTIMENT)
        print(f'{i}/{len(informacion_sobre_inversiones)} [informacion_sobre_inversiones] sentimiento analizado')
        i+=1

    i=1
    riesgo_asumido_por_fondo_SENTIMENT = []
    for elemento in riesgo_asumido_por_fondo:
        elemento_SENTIMENT = inference_HF.analize_sentiment_full_text(elemento)
        riesgo_asumido_por_fondo_SENTIMENT.append(elemento_SENTIMENT)
        print(f'{i}/{len(riesgo_asumido_por_fondo)} [riesgo_asumido_por_fondo] sentimiento analizado')
        i+=1

    i=1
    perspectiva_mercado_SENTIMENT = []
    for elemento in perspectiva_mercado:
        elemento_SENTIMENT = inference_HF.analize_sentiment_full_text(elemento)
        perspectiva_mercado_SENTIMENT.append(elemento_SENTIMENT)
        print(f'{i}/{len(perspectiva_mercado)} [perspectiva_mercado] sentimiento analizado')
        i+=1
    
    # Almacenamos en un dataframe los arrays para convertislo en un CSV
    data = {
    'NIF': NIFs,
    'SITUACIÓN MERCADOS. EVOLUCION FONDO': situacion_mercados_evolucion_fondo_SENTIMENT,
    'INFORMACIÓN SOBRE INVERSIONES': informacion_sobre_inversiones_SENTIMENT,
    'RIESGO ASUMIDO': riesgo_asumido_por_fondo_SENTIMENT,
    'PERSPECTIVA DE MERCADO': perspectiva_mercado_SENTIMENT
    }

    df_SENTIMENT = pd.DataFrame(data)
    df_SENTIMENT.to_csv('sentimientos.csv', sep=';', encoding='utf-8', index=False)

# Metodo para abrir CSV registro, analizar sentimientos de cada celda y guardarlos en un nuevo CSV
def save_sentiment_analysis_bart():
    path_resumen_BART_ENG = os.path.join('data', 'resumen_BART_ENG.csv')
    df = pd.read_csv(path_resumen_BART_ENG, sep=';', encoding='utf-8')

    # Abrimos las columnas para realizar el analisis de sentimientos
    NIFs = df['NIF']
    situacion_mercados_evolucion_fondo = df['SITUACIÓN MERCADOS. EVOLUCION FONDO']
    informacion_sobre_inversiones = df['INFORMACIÓN SOBRE INVERSIONES']
    riesgo_asumido_por_fondo = df['RIESGO ASUMIDO']
    perspectiva_mercado = df['PERSPECTIVA DE MERCADO']
    
    print("PROCESANDO SENTIMIENTOS DEL RESUMEN DE BART...")
    # Recorremos columna a columna y celda a celda llamando al modelo
    i=1
    situacion_mercados_evolucion_fondo_SENTIMENT = []
    for elemento in situacion_mercados_evolucion_fondo:
        elemento_SENTIMENT = inference_HF.analize_sentiment_summary(elemento)
        situacion_mercados_evolucion_fondo_SENTIMENT.append(elemento_SENTIMENT)
        
        print(f'{i}/{len(situacion_mercados_evolucion_fondo)} [situacion_mercados_evolucion_fondo] sentimiento analizado')
        i+=1

    i=1
    informacion_sobre_inversiones_SENTIMENT = []
    for elemento in informacion_sobre_inversiones:
        elemento_SENTIMENT = inference_HF.analize_sentiment_summary(elemento)
        informacion_sobre_inversiones_SENTIMENT.append(elemento_SENTIMENT)
        print(f'{i}/{len(informacion_sobre_inversiones)} [informacion_sobre_inversiones] sentimiento analizado')
        i+=1

    i=1
    riesgo_asumido_por_fondo_SENTIMENT = []
    for elemento in riesgo_asumido_por_fondo:
        elemento_SENTIMENT = inference_HF.analize_sentiment_summary(elemento)
        riesgo_asumido_por_fondo_SENTIMENT.append(elemento_SENTIMENT)
        print(f'{i}/{len(riesgo_asumido_por_fondo)} [riesgo_asumido_por_fondo] sentimiento analizado')
        i+=1

    i=1
    perspectiva_mercado_SENTIMENT = []
    for elemento in perspectiva_mercado:
        elemento_SENTIMENT = inference_HF.analize_sentiment_summary(elemento)
        perspectiva_mercado_SENTIMENT.append(elemento_SENTIMENT)
        print(f'{i}/{len(perspectiva_mercado)} [perspectiva_mercado] sentimiento analizado')
        i+=1
    
    # Almacenamos en un dataframe los arrays para convertislo en un CSV
    data = {
    'NIF': NIFs,
    'SITUACIÓN MERCADOS. EVOLUCION FONDO': situacion_mercados_evolucion_fondo_SENTIMENT,
    'INFORMACIÓN SOBRE INVERSIONES': informacion_sobre_inversiones_SENTIMENT,
    'RIESGO ASUMIDO': riesgo_asumido_por_fondo_SENTIMENT,
    'PERSPECTIVA DE MERCADO': perspectiva_mercado_SENTIMENT
    }

    df_SENTIMENT = pd.DataFrame(data)
    df_SENTIMENT.to_csv('sentimientos_BART.csv', sep=';', encoding='utf-8', index=False)

# Metodo para abrir CSV registro, analizar sentimientos de cada celda y guardarlos en un nuevo CSV
def save_sentiment_analysis_pegasus():
    path_resumen_PEGASUS_ENG = os.path.join('data', 'resumen_PEGASUS_ENG.csv')
    df = pd.read_csv(path_resumen_PEGASUS_ENG, sep=';', encoding='utf-8')

    # Abrimos las columnas para realizar el analisis de sentimientos
    NIFs = df['NIF']
    situacion_mercados_evolucion_fondo = df['SITUACIÓN MERCADOS. EVOLUCION FONDO']
    informacion_sobre_inversiones = df['INFORMACIÓN SOBRE INVERSIONES']
    riesgo_asumido_por_fondo = df['RIESGO ASUMIDO']
    perspectiva_mercado = df['PERSPECTIVA DE MERCADO']
    
    print("PROCESANDO SENTIMIENTOS DEL RESUMEN DE PEGASUS...")
    # Recorremos columna a columna y celda a celda llamando al modelo
    i=1
    situacion_mercados_evolucion_fondo_SENTIMENT = []
    for elemento in situacion_mercados_evolucion_fondo:
        elemento_SENTIMENT = inference_HF.analize_sentiment_summary(elemento)
        situacion_mercados_evolucion_fondo_SENTIMENT.append(elemento_SENTIMENT)
        
        print(f'{i}/{len(situacion_mercados_evolucion_fondo)} [situacion_mercados_evolucion_fondo] sentimiento analizado')
        i+=1

    i=1
    informacion_sobre_inversiones_SENTIMENT = []
    for elemento in informacion_sobre_inversiones:
        elemento_SENTIMENT = inference_HF.analize_sentiment_summary(elemento)
        informacion_sobre_inversiones_SENTIMENT.append(elemento_SENTIMENT)
        print(f'{i}/{len(informacion_sobre_inversiones)} [informacion_sobre_inversiones] sentimiento analizado')
        i+=1

    i=1
    riesgo_asumido_por_fondo_SENTIMENT = []
    for elemento in riesgo_asumido_por_fondo:
        elemento_SENTIMENT = inference_HF.analize_sentiment_summary(elemento)
        riesgo_asumido_por_fondo_SENTIMENT.append(elemento_SENTIMENT)
        print(f'{i}/{len(riesgo_asumido_por_fondo)} [riesgo_asumido_por_fondo] sentimiento analizado')
        i+=1

    i=1
    perspectiva_mercado_SENTIMENT = []
    for elemento in perspectiva_mercado:
        elemento_SENTIMENT = inference_HF.analize_sentiment_summary(elemento)
        perspectiva_mercado_SENTIMENT.append(elemento_SENTIMENT)
        print(f'{i}/{len(perspectiva_mercado)} [perspectiva_mercado] sentimiento analizado')
        i+=1
    
    # Almacenamos en un dataframe los arrays para convertislo en un CSV
    data = {
    'NIF': NIFs,
    'SITUACIÓN MERCADOS. EVOLUCION FONDO': situacion_mercados_evolucion_fondo_SENTIMENT,
    'INFORMACIÓN SOBRE INVERSIONES': informacion_sobre_inversiones_SENTIMENT,
    'RIESGO ASUMIDO': riesgo_asumido_por_fondo_SENTIMENT,
    'PERSPECTIVA DE MERCADO': perspectiva_mercado_SENTIMENT
    }

    df_SENTIMENT = pd.DataFrame(data)
    df_SENTIMENT.to_csv('sentimientos_PEGASUS.csv', sep=';', encoding='utf-8', index=False)

####################################################################

# Esto es para procesar el texto traducido que lo habia hecho en un formato raro
def esta_la_borro():
    path_registro_ENG = os.path.join('data', 'registro_ENG.csv')
    df_ENG = pd.read_csv(path_registro_ENG, sep=';', encoding='utf-8')
    path_registro = os.path.join('data', 'registro.csv')
    df = pd.read_csv(path_registro, sep=';', encoding='utf-8')

    NIFs = df['NIF']
    situacion_mercados_evolucion_fondo = df_ENG['SITUACIÓN MERCADOS. EVOLUCION FONDO']
    informacion_sobre_inversiones = df_ENG['INFORMACIÓN SOBRE INVERSIONES']
    evolucion_objetivo_rentabilidad = df_ENG['EVOLUCIÓN OBJETIVO RENTABILIDAD']
    riesgo_asumido_por_fondo = df_ENG['RIESGO ASUMIDO']

    perspectiva_mercado = df['PERSPECTIVA DE MERCADO']


    i=1
    perspectiva_mercado_ENG = []
    for elemento in perspectiva_mercado:
        elemento_ENG = inference_HF.translate_text_ES_EN(elemento)
        perspectiva_mercado_ENG.append(elemento_ENG)
        print(f'{i}/{len(perspectiva_mercado)} [perspectiva_mercado] traducido')
        i+=1

    '''for output in situacion_mercados_evolucion_fondo:
        text = output.replace("{'translation_text': '", "")
        text = text.replace("[", "")
        text = text.replace("]", "")
        text = text.replace("'}", "")
        situacion_mercados_evolucion_fondo_v2.append(text)
    for output in informacion_sobre_inversiones:
        text = output.replace("{'translation_text': '", "")
        text = text.replace("[", "")
        text = text.replace("]", "")
        text = text.replace("'}", "")
        informacion_sobre_inversiones_v2.append(text)
    for output in evolucion_objetivo_rentabilidad:
        text = output.replace("{'translation_text': '", "")
        text = text.replace("[", "")
        text = text.replace("]", "")
        text = text.replace("'}", "")
        evolucion_objetivo_rentabilidad_v2.append(text)
    for output in riesgo_asumido_por_fondo:
        text = output.replace("{'translation_text': '", "")
        text = text.replace("[", "")
        text = text.replace("]", "")
        text = text.replace("'}", "")
        riesgo_asumido_por_fondo_v2.append(text)'''
    
    data = {
    'NIF': NIFs,
    'SITUACIÓN MERCADOS. EVOLUCION FONDO': situacion_mercados_evolucion_fondo,
    'INFORMACIÓN SOBRE INVERSIONES': informacion_sobre_inversiones,
    'EVOLUCIÓN OBJETIVO RENTABILIDAD': evolucion_objetivo_rentabilidad,
    'RIESGO ASUMIDO': riesgo_asumido_por_fondo,
    'PERSPECTIVA DE MERCADO': perspectiva_mercado_ENG
    }

    df_ENG = pd.DataFrame(data)
    path_registro_ENG = os.path.join('data', 'registro_ENG.csv')
    df_ENG.to_csv(path_registro_ENG, sep=';', encoding='utf-8', index=False)

# Voy a ver si consigo meter en el CSV un diccionario y si no pues vuelvo a pegarme con esta funcion
def test_open_sentmimientos():
    sentiments = pd.read_csv('sentiments_mini.csv', sep=';', encoding='utf-8')
    sentimiento_concreto = sentiments.loc[sentiments['NIF'] == "V01769819"]

    array_str = sentimiento_concreto['SITUACIÓN MERCADOS. EVOLUCION FONDO'].iloc[0]

    array = array_str[1:-1].split(', ') 

    # Extraer los tres valores del array
    valor_positive = array[0]
    valor_neutral = array[1]
    valor_negative = array[2]

    # Imprimir los valores
    print("Valor de 'positive':", valor_positive)
    print("Valor de 'neutral':", valor_neutral)
    print("Valor de 'negative':", valor_negative)


    #print(type(text))
    #print(text['positive'].values)



######################################
#        FUNCIONES PRINCIPALES       #
######################################
def generar_corpus():
    save_anexos()
    save_main_data()
    traducir_anexos_ES_EN()

def generar_resumenes():
    save_summarization_bart()
    save_resumen_bart()
    save_summarization_pegasus()
    save_resumen_pegasus()

def generar_analisis_sentimientos():
    save_sentiment_analysis_full_text()
    save_sentiment_analysis_bart()
    save_sentiment_analysis_pegasus()

if __name__ == '__main__':
    generar_corpus()
    generar_resumenes()
    generar_analisis_sentimientos()
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import os


def menu_principal():
    with st.container():
        st.title("RESUMENES FINANCIEROS")
        st.subheader("Realizado por Gregorio Cancio Ramírez")
        st.text("Esta aplicación aborda la necesidad de analizar informes periódicos, que a menudo tienen una extensión considerable, junto con sus Anexos Explicativos más concisos. \nLa estrategia propuesta consiste en priorizar la lectura del breve Anexo Explicativo para obtener una visión general rápida de todo el informe. \nSin embargo, dado que el análisis de múltiples informes puede ser laborioso, el propósito fundamental de este Trabajo Final de Máster es simplificar aún más el proceso \nmediante la generación de resúmenes concisos del Anexo Explicativo. ")


def ver_informacion_fondo():
    
    columns = st.columns([1,2])

    path_registro = os.path.join('data', 'registro.csv')
    path_main_data = os.path.join('data', 'registro_main_data.csv')
    registro = pd.read_csv(path_registro, sep=';', encoding='utf-8')
    registro_info_fondos = pd.read_csv(path_main_data, sep=';', encoding='utf-8')
    
    # Columna de la izquierda
    with columns[0]:
        with st.container():
            st.header("INFORMACIÓN CONCRETA")
            st.divider()
            options = registro['NIF']
            selected_NIF = st.selectbox(label="Selección de NIF", options=options, index=0,  placeholder="Selección de NIF...", key="nif_select")
        
        with st.container(): # CONTAINER CON DESPLEGABLE PARA NIF Y BOTON DE DESCARGAR
            with open("registroPDFs/" + selected_NIF + ".pdf", "rb") as pdf_file:
                anexoPDF = pdf_file.read()

            st.download_button(
                label = "Descargar el informe completo",
                data = anexoPDF,
                file_name = "Informe_" + selected_NIF + ".pdf",
                mime = 'application/octet-stream'
                )
            st.divider()


        with st.container(): #CONTAINER CON DATOS PRINCIPALES DEL FONDO

            fondo_concreto = registro_info_fondos.loc[registro_info_fondos['NIF'] == selected_NIF]

            nombre_fondo = fondo_concreto['NOMBRE FONDO'].values[0]
            registro_cnmv = fondo_concreto['NUMERO REGISTRO CNMV'].values[0]
            gestora = fondo_concreto['GESTORA'].values[0]
            depositario = fondo_concreto['DEPOSITARIO'].values[0]
            auditor = fondo_concreto['AUDITOR'].values[0]

            st.text("Nombre del fondo: " + str(nombre_fondo))
            st.text("Registro CNMV: " + str(registro_cnmv))
            st.text("Gestora: " + str(gestora))
            st.text("Depositario: " + str(depositario))
            st.text("Auditor: " + str(auditor))

            st.divider()

    # Columna de la derecha            
    with columns[1]: 
        st.header("ANEXO EXPLICATIVO")
        fondo_concreto = registro.loc[registro['NIF'] == selected_NIF]
        anexo = fondo_concreto['ANEXO COMPLETO'].values[0]

        st.text(anexo)

def ver_resumen_fondo():

    path_registro = os.path.join('data', 'registro.csv')
    registro = pd.read_csv(path_registro, sep=';', encoding='utf-8')
    
    path_resumen_BART = os.path.join('data', 'resumen_BART.csv')
    resumen_BART = pd.read_csv(path_resumen_BART, sep=';', encoding='utf-8')  
    path_resumen_PEGASUS = os.path.join('data', 'resumen_PEGASUS.csv')
    resumen_PEGASUS = pd.read_csv(path_resumen_PEGASUS, sep=';', encoding='utf-8')  

    path_sentimientos = os.path.join('data', 'sentimientos.csv')
    sentimientos_TEXTO = pd.read_csv(path_sentimientos, sep=';', encoding='utf-8') 
    path_sentimientos_BART = os.path.join('data', 'sentimientos_BART.csv')
    sentimientos_BART = pd.read_csv(path_sentimientos_BART, sep=';', encoding='utf-8')
    path_sentimientos_PEGASUS = os.path.join('data', 'sentimientos_PEGASUS.csv')
    sentimientos_PEGASUS = pd.read_csv(path_sentimientos_PEGASUS, sep=';', encoding='utf-8')

         
      
    with st.container():

        st.divider()  
        options = registro['NIF']
        selected_NIF = st.selectbox(label="Selección de NIF", options=options, index=0,  placeholder="Selección de NIF...", key="nif_select")
        
        options_LLM = ["PEGASUS", "BART"]
        selected_LLM = st.selectbox(label="Selección de modelo de lenguaje", options=options_LLM, index=0,  placeholder="Selección de modelo de lenguaje...", key="llm_select")
        st.divider()

        anexo_concreto = registro.loc[registro['NIF'] == selected_NIF]
        sentimiento_concreto = sentimientos_TEXTO.loc[sentimientos_TEXTO['NIF'] == selected_NIF]
        sentimiento_BART_concreto = sentimientos_BART.loc[sentimientos_BART['NIF'] == selected_NIF]
        sentimiento_PEGASUS_concreto = sentimientos_PEGASUS.loc[sentimientos_PEGASUS['NIF'] == selected_NIF]
        resumen_BART_concreto = resumen_BART.loc[resumen_BART['NIF'] == selected_NIF]
        resumen_PEGASUS_concreto = resumen_PEGASUS.loc[resumen_PEGASUS['NIF'] == selected_NIF]

        # FILA 1: SITUACIÓN DE LOS MERCADOS Y EVOLUCIÓN DEL FONDO
        row1 = st.columns([2,1,1], gap="large")
        with row1[0]:
            st.subheader("1. SITUACIÓN DE LOS MERCADOS Y EVOLUCIÓN DEL FONDO")
            if(selected_LLM=="PEGASUS"): resumen = resumen_PEGASUS_concreto['SITUACIÓN MERCADOS. EVOLUCION FONDO'].iloc[0]
            if(selected_LLM=="BART"): resumen = resumen_BART_concreto['SITUACIÓN MERCADOS. EVOLUCION FONDO'].iloc[0]
            st.write(resumen.replace("< n>", "\n").replace("<n>", "\n"))
        with row1[1]:
            st.subheader("SENTIMIENTOS \n(RESUMEN)")

            # Extraccion de sentimientos del CSV
            if(selected_LLM=="PEGASUS"): array_str = sentimiento_PEGASUS_concreto['SITUACIÓN MERCADOS. EVOLUCION FONDO'].iloc[0]
            if(selected_LLM=="BART"): array_str = sentimiento_BART_concreto['SITUACIÓN MERCADOS. EVOLUCION FONDO'].iloc[0]
            
            array = array_str[1:-1].split(', ') 
            valor_positive = array[0]
            valor_neutral = array[1]
            valor_negative = array[2]

            # Datos para el diagrama de pastel
            etiquetas = ['Positivo', 'Neutro', 'Negativo']
            valores = [valor_positive, valor_neutral, valor_negative]

            # Crear el diagrama de pastel
            fig, ax = plt.subplots(figsize=(6, 6), facecolor='none')
            colores = ['#00ff00', '#ffff00', '#ff0000']
            ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=colores, textprops={'color':'#000000', "fontsize":10})
            ax.legend(labels=etiquetas, loc="upper center", bbox_to_anchor=(0.5, -0.04), ncol=3)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Mostrar el diagrama de pastel en Streamlit
            st.pyplot(fig)
                
        with row1[2]:
            st.subheader("SENTIMIENTOS \n(TEXTO COMPLETO)")

            # Extraccion de valores del CSV
            array_str = sentimiento_concreto['SITUACIÓN MERCADOS. EVOLUCION FONDO'].iloc[0]
            array = array_str[1:-1].split(', ') 
            valor_positive = array[0]
            valor_neutral = array[1]
            valor_negative = array[2]

            # Datos para el diagrama de pastel
            etiquetas = ['Positivo', 'Neutro', 'Negativo']
            valores = [valor_positive, valor_neutral, valor_negative]

            # Crear el diagrama de pastel
            fig, ax = plt.subplots(figsize=(6, 6), facecolor='none')
            colores = ['#00ff00', '#ffff00', '#ff0000']
            ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=colores, textprops={'color':'#000000', "fontsize":10})
            ax.legend(labels=etiquetas, loc="upper center", bbox_to_anchor=(0.5, -0.04), ncol=3)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Mostrar el diagrama de pastel en Streamlit
            st.pyplot(fig)

        # FILA 2: INFORMACIÓN SOBRE INVERSIONES
        st.divider()
        row2 = st.columns([2,1,1], gap="large")
        with row2[0]:
            st.subheader("2. INFORMACIÓN SOBRE INVERSIONES")
            if(selected_LLM=="PEGASUS"): resumen = resumen_PEGASUS_concreto['INFORMACIÓN SOBRE INVERSIONES'].iloc[0]
            if(selected_LLM=="BART"): resumen = resumen_BART_concreto['INFORMACIÓN SOBRE INVERSIONES'].iloc[0]
            st.write(resumen.replace("< n>", "\n").replace("<n>", "\n"))

        with row2[1]:
            st.subheader("SENTIMIENTOS \n(RESUMEN)")
            # Extraccion de valores del CSV
            if(selected_LLM=="PEGASUS"): array_str = sentimiento_PEGASUS_concreto['INFORMACIÓN SOBRE INVERSIONES'].iloc[0]
            if(selected_LLM=="BART"): array_str = sentimiento_BART_concreto['INFORMACIÓN SOBRE INVERSIONES'].iloc[0]
            array_str = sentimiento_BART_concreto['INFORMACIÓN SOBRE INVERSIONES'].iloc[0]
            array = array_str[1:-1].split(', ') 
            valor_positive = array[0]
            valor_neutral = array[1]
            valor_negative = array[2]

            # Datos para el diagrama de pastel
            etiquetas = ['Positivo', 'Neutro', 'Negativo']
            valores = [valor_positive, valor_neutral, valor_negative]

            # Crear el diagrama de pastel
            fig, ax = plt.subplots(figsize=(6, 6), facecolor='none')
            colores = ['#00ff00', '#ffff00', '#ff0000']
            ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=colores, textprops={'color':'#000000', "fontsize":10})
            ax.legend(labels=etiquetas, loc="upper center", bbox_to_anchor=(0.5, -0.04), ncol=3)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Mostrar el diagrama de pastel en Streamlit
            st.pyplot(fig)
                
        with row2[2]:
            st.subheader("SENTIMIENTOS \n(TEXTO COMPLETO)")

            # Extraccion de valores del CSV
            array_str = sentimiento_concreto['INFORMACIÓN SOBRE INVERSIONES'].iloc[0]
            array = array_str[1:-1].split(', ') 
            valor_positive = array[0]
            valor_neutral = array[1]
            valor_negative = array[2]

            # Datos para el diagrama de pastel
            etiquetas = ['Positivo', 'Neutro', 'Negativo']
            valores = [valor_positive, valor_neutral, valor_negative]

            # Crear el diagrama de pastel
            fig, ax = plt.subplots(figsize=(6, 6), facecolor='none')
            colores = ['#00ff00', '#ffff00', '#ff0000']
            ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=colores, textprops={'color':'#000000', "fontsize":10})
            ax.legend(labels=etiquetas, loc="upper center", bbox_to_anchor=(0.5, -0.04), ncol=3)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Mostrar el diagrama de pastel en Streamlit
            st.pyplot(fig)
        
        # FILA 3: RIESGO ASUMIDO
        st.divider()
        row3 = st.columns([2,1,1], gap="large")
        with row3[0]:
            st.subheader("4. RIESGO ASUMIDO")
            if(selected_LLM=="PEGASUS"): resumen = resumen_PEGASUS_concreto['RIESGO ASUMIDO'].iloc[0]
            if(selected_LLM=="BART"): resumen = resumen_BART_concreto['RIESGO ASUMIDO'].iloc[0]
            st.write(resumen.replace("< n>", "\n").replace("<n>", "\n"))

        with row3[1]:
            st.subheader("SENTIMIENTOS \n(RESUMEN)")
            # Extraccion de valores del CSV
            if(selected_LLM=="PEGASUS"): array_str = sentimiento_PEGASUS_concreto['RIESGO ASUMIDO'].iloc[0]
            if(selected_LLM=="BART"): array_str = sentimiento_BART_concreto['RIESGO ASUMIDO'].iloc[0]
            
            array = array_str[1:-1].split(', ') 
            valor_positive = array[0]
            valor_neutral = array[1]
            valor_negative = array[2]

            # Datos para el diagrama de pastel
            etiquetas = ['Positivo', 'Neutro', 'Negativo']
            valores = [valor_positive, valor_neutral, valor_negative]

            # Crear el diagrama de pastel
            fig, ax = plt.subplots(figsize=(6, 6), facecolor='none')
            colores = ['#00ff00', '#ffff00', '#ff0000']
            ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=colores, textprops={'color':'#000000', "fontsize":10})
            ax.legend(labels=etiquetas, loc="upper center", bbox_to_anchor=(0.5, -0.04), ncol=3)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Mostrar el diagrama de pastel en Streamlit
            st.pyplot(fig)

                
        with row3[2]:
            st.subheader("SENTIMIENTOS \n(TEXTO COMPLETO)")

            # Extraccion de valores del CSV
            array_str = sentimiento_concreto['INFORMACIÓN SOBRE INVERSIONES'].iloc[0]
            array = array_str[1:-1].split(', ') 
            valor_positive = array[0]
            valor_neutral = array[1]
            valor_negative = array[2]

            # Datos para el diagrama de pastel
            etiquetas = ['Positivo', 'Neutro', 'Negativo']
            valores = [valor_positive, valor_neutral, valor_negative]

            # Crear el diagrama de pastel
            fig, ax = plt.subplots(figsize=(6, 6), facecolor='none')
            colores = ['#00ff00', '#ffff00', '#ff0000']
            ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=colores, textprops={'color':'#000000', "fontsize":10})
            ax.legend(labels=etiquetas, loc="upper center", bbox_to_anchor=(0.5, -0.04), ncol=3)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Mostrar el diagrama de pastel en Streamlit
            st.pyplot(fig)
    
        # FILA 4: PERSPECTIVA DE MERCADO
        st.divider()
        row4 = st.columns([2,1,1], gap="large")
        with row4[0]:
            st.subheader("10. PERSPECTIVA DE MERCADO")
            if(selected_LLM=="PEGASUS"): resumen = resumen_PEGASUS_concreto['PERSPECTIVA DE MERCADO'].iloc[0]
            if(selected_LLM=="BART"): resumen = resumen_BART_concreto['PERSPECTIVA DE MERCADO'].iloc[0]
            st.write(resumen.replace("< n>", "\n").replace("<n>", "\n"))

        with row4[1]:
            st.subheader("SENTIMIENTOS \n(RESUMEN)")
            # Extraccion de valores del CSV
            if(selected_LLM=="PEGASUS"): array_str = sentimiento_PEGASUS_concreto['PERSPECTIVA DE MERCADO'].iloc[0]
            if(selected_LLM=="BART"): array_str = sentimiento_BART_concreto['PERSPECTIVA DE MERCADO'].iloc[0]
            
            array = array_str[1:-1].split(', ') 
            valor_positive = array[0]
            valor_neutral = array[1]
            valor_negative = array[2]

            # Datos para el diagrama de pastel
            etiquetas = ['Positivo', 'Neutro', 'Negativo']
            valores = [valor_positive, valor_neutral, valor_negative]

            # Crear el diagrama de pastel
            fig, ax = plt.subplots(figsize=(6, 6), facecolor='none')
            colores = ['#00ff00', '#ffff00', '#ff0000']
            ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=colores, textprops={'color':'#000000', "fontsize":10})
            ax.legend(labels=etiquetas, loc="upper center", bbox_to_anchor=(0.5, -0.04), ncol=3)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Mostrar el diagrama de pastel en Streamlit
            st.pyplot(fig)

                
        with row4[2]:
            st.subheader("SENTIMIENTOS \n(TEXTO COMPLETO)")

            # Extraccion de valores del CSV
            array_str = sentimiento_concreto['PERSPECTIVA DE MERCADO'].iloc[0]
            array = array_str[1:-1].split(', ') 
            valor_positive = array[0]
            valor_neutral = array[1]
            valor_negative = array[2]

            # Datos para el diagrama de pastel
            etiquetas = ['Positivo', 'Neutro', 'Negativo']
            valores = [valor_positive, valor_neutral, valor_negative]

            # Crear el diagrama de pastel
            fig, ax = plt.subplots(figsize=(6, 6), facecolor='none')
            colores = ['#00ff00', '#ffff00', '#ff0000']
            ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=colores, textprops={'color':'#000000', "fontsize":10})
            ax.legend(labels=etiquetas, loc="upper center", bbox_to_anchor=(0.5, -0.04), ncol=3)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Mostrar el diagrama de pastel en Streamlit
            st.pyplot(fig)

st.set_page_config(
    page_title="Resumenes financieros", 
    page_icon="robot.png", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)


selected = option_menu(
    menu_title=None,
    options=["Página Principal", " Información concreta del Fondo", "Resumen financiero del Fondo"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

if selected == "Página Principal":
    menu_principal()

if selected == " Información concreta del Fondo":
    ver_informacion_fondo()

if selected == "Resumen financiero del Fondo":
    ver_resumen_fondo()

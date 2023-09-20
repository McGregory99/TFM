# FICHERO DESDE DONDE SE REALIZAN LAS LLAMADAS A TODOS LOS MODELOS A TRAVES DE LA API DE HUGGINGFACE
import requests
from langchain import HuggingFaceHub
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd


# Metodo para hacer la llamada a la API de inferencia de HuggingFace
def query(payload, API_URL, headers):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()



def translate_text_EN_ES(text_ENG):
    API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-es"
    headers = {"Authorization": "Bearer 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"}

    output = query(
        {"inputs": text_ENG,},
        API_URL, 
        headers)
    try:
        translated = output[0]['translation_text']
    except KeyError:
        print(output)
        exit()
    return translated

# Metodo que traduce un texto de español (ES) a inglés (EN)
def translate_text_ES_EN(text_ES):
    API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-es-en"
    headers = {"Authorization": "Bearer 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"}

    text_splitter = RecursiveCharacterTextSplitter(separators=[","], 
                                                chunk_size = 2000,
                                                chunk_overlap  = 20)
    docs = text_splitter.create_documents([text_ES])

    # Pasamos los docs a formato str
    translated = []
    for doc in docs:
        output = query(
            {"inputs": doc.page_content,},
            API_URL, 
            headers)
        try:
            translated.append(output[0]['translation_text'])
        except KeyError:
            print(output)
            exit()

    translated_str = ''.join(translated)
    return translated_str

# Metodo para llamar a la API y analizar los sentimientos
def analize_sentiment_full_text(text):
    API_URL = "https://api-inference.huggingface.co/models/ProsusAI/finbert"
    headers = {"Authorization": "Bearer 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"}

    # Dividimos el texto de entrada en fragmentos para cumplir el maximo de 512 tokens
    text_splitter = RecursiveCharacterTextSplitter(separators=[","], 
                                                chunk_size = 2000,
                                                chunk_overlap  = 20)
    docs = text_splitter.create_documents([text])
    
    # Como son varios documentos, hacemos una suma de los valores de cada sentimiento
    positive = 0
    neutral = 0
    negative = 0
    for doc in docs:
        json_sentiment = query(
            {"inputs": doc.page_content,},
            API_URL, 
            headers)
        try:
            for dict in json_sentiment[0]:
                if dict['label'] == "positive" : positive += dict['score']
                if dict['label'] == "neutral" : neutral += dict['score']
                if dict['label'] == "negative" : negative += dict['score']
        except KeyError:
            print(json_sentiment)
            exit()

    # Nomalizamos los valores para que el resultado se muestre sobre 1
    total = positive + neutral + negative
    positive = positive / total
    neutral = neutral / total
    negative = negative / total

    sentiment_array = [positive, neutral, negative]
    return sentiment_array

# Metodo para llamar a la API y analizar los sentimientos A PARTIR DEL RESUMEN GENERADO
def analize_sentiment_summary(summary):
    API_URL = "https://api-inference.huggingface.co/models/ProsusAI/finbert"
    headers = {"Authorization": "Bearer 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"}

    json_sentiment = query(
        {"inputs": summary,},
        API_URL, 
        headers)
    try:
        for dict in json_sentiment[0]:
            if dict['label'] == "positive" : positive = dict['score']
            if dict['label'] == "neutral" : neutral = dict['score']
            if dict['label'] == "negative" : negative = dict['score']

    except KeyError:
        print(json_sentiment)
        exit()

    sentiment_array = [positive, neutral, negative]
    return sentiment_array

# Metodo que toma un texto entero en ingles y lo resume con BART-LARGE-CNN. Devuelve el texto resumen
def summarize_BART(text_ENG):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": "Bearer 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"}
        
    resumen_ENG = query(
        {"inputs": text_ENG,},
        API_URL, 
        headers)

    try:
        summary_BART = resumen_ENG[0]['summary_text']
    except KeyError:
        print(resumen_ENG)
        exit()
    return summary_BART

# Metodo que toma un texto entero en ingles y lo resume con PEGASUS. Devuelve el texto resumen
def summarize_PEGASUS(text_ENG):
    API_URL = "https://api-inference.huggingface.co/models/google/pegasus-cnn_dailymail"
    headers = {"Authorization": "Bearer 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"}
        
    resumen_ENG = query(
        {"inputs": text_ENG,},
        API_URL, 
        headers)

    #print(resumen_ENG)
    try:
        summary_PEGASUS = resumen_ENG[0]['summary_text']
    except KeyError:
        print(resumen_ENG)
        exit()
    return summary_PEGASUS

# TODO: YA NO SE USA?
# Metodo que toma un texto entero en ingles y lo resume con BART-LARGE-CNN. Devuelve el texto resumen
def summarize_DEMO(text_ENG):
    API_URL = "https://api-inference.huggingface.co/models/mrm8488/bert2bert_shared-spanish-finetuned-summarization"
    headers = {"Authorization": "Bearer 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"}
        
    resumen_ENG = query(
        {"inputs": text_ENG,},
        API_URL, 
        headers)

    #print(resumen_ENG)
    try:
        summary = resumen_ENG[0]['summary_text']
    except KeyError:
        print(resumen_ENG)
        exit()
    return summary




if __name__ == '__main__':
    # Traducir registro de español a ingles
    #translate_text_ES_EN("Me gusta la tortilla de chipirones acompañada de un batido de chocolate cuando cae la noche en la ultima semana de agosto")

    # Sacar analisis de sentimientos
    #analize_sentiment_v2("This is very bad for all the economy experts. This is a disaster for the world economy. It also surprised the Japanese Nikkei Nikkei with an increase of 27%. On the European side, highlights the Italian Ftse MIB with an increase of 19%, the Eurostoxx 50 (16%) or the Ibex-35 (16.6%). They were slightly more backward the CAC 40 French (14%), the PSI 20 (3.4%), the Swiss market (5%), like the United Kingdom (1%) or the Emerging MSCI (3.5%). Analyzing the sectoral evolution, they highlight the good behavior of leisure and tourism (26.3%), retail (25.8%) and technology (25.3%). On the contrary, the field of basic resources (-13.8%), real estate (-11%) and energy (-4.3%) have been the ones that have behaved the worst after the good 2022 fall, except the real estate that follows the pandemic before the changes of habit in the work and the hardening of the cost of financing.In the currency, the volatility has persisted in the euro that has evolved in the period of 1.052-1 year,106, according to the central and declarations 1,9 % of the interest in the case of the euro has been reduced in the first place of the first place and the first year")
    print("HOLA")

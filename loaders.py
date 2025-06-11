import os
import streamlit as st
from fake_useragent import UserAgent
from time import sleep
from langchain_community.document_loaders import WebBaseLoader, YoutubeLoader, CSVLoader, PyPDFLoader, TextLoader

def carrega_site(url):
    documento = ''
    if not url == '':
        for i in range(5):
            try:
                os.environ['USER_AGENT'] = UserAgent().random
                loader = WebBaseLoader(url, raise_for_status=True)
                lista_documentos = loader.load()
                documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
                break
            except:
                print(f'Erro ao carregar o site{i+1}')
                sleep(2)
        if documento == '':
            st.error('Não foi possível carregar o site...')
            st.stop()
    return documento

def carrega_youtube(video_id):
    documento = ''
    try:
        loader = YoutubeLoader(video_id, add_video_info=False, language=['pt'])
        lista_documentos = loader.load()
        documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    except:
        st.error('Não foi possível carregar as legendas do vídeo :( Por favor baixe as legendas manualmente no formato **.txt** e envie o arquivo escolhendo o formato TXT.')
    return documento

def carrega_csv(caminho):
    documento = '' 
    try:
        if not caminho == '':
            loader = CSVLoader(caminho)
            lista_documentos = loader.load()
            documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    except:
        st.error('Ocorreu um erro ao carregar o arquivo :( Por favor recarregue a página.')
    return documento

def carrega_pdf(caminho):
    documento = '' 
    try:
        if not caminho == '':
            loader = PyPDFLoader(caminho)
            lista_documentos = loader.load()
            documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    except:
        st.error('Ocorreu um erro ao carregar o arquivo :( Por favor recarregue a página.')
    return documento

def carrega_txt(caminho):
    documento = '' 
    try:
        if not caminho == '':
            loader = TextLoader(caminho)
            lista_documentos = loader.load()
            documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    except:
        st.error('Ocorreu um erro ao carregar o arquivo :( Por favor recarregue a página.')
    return documento

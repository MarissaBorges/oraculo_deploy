import os
import streamlit as st
from fake_useragent import UserAgent
from time import sleep
from langchain_community.document_loaders import WebBaseLoader, YoutubeLoader, CSVLoader, PyPDFLoader, TextLoader

def carrega_site(url):
    documento = []
    if not url == '':
        for i in range(5):
            try:
                os.environ['USER_AGENT'] = UserAgent().random
                loader = WebBaseLoader(url, raise_for_status=True)
                lista_documentos = loader.load()
                documento = lista_documentos
                # documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
                break
            except Exception as e:
                print(f'Erro na tentativa {i+1} ao carregar o site.')
                print(f'URL: {url}')
                print(f'Tipo de erro: {type(e).__name__}')
                print(f'Detalhes do erro: {e}')
                sleep(3)
        if documento == '':
            st.error('Não foi possível carregar o site...')
            st.stop()
    return documento

def carrega_youtube(video_id):
    documento = []
    try:
        loader = YoutubeLoader(video_id, add_video_info=False, language=['pt'])
        lista_documentos = loader.load()
        documento = lista_documentos
        # documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    except Exception as e:
        print(f"Erro detalhado ao carregar YouTube: {e}")
        st.error('Não foi possível carregar as legendas do vídeo :( Por favor baixe as legendas manualmente no formato **.txt** e envie o arquivo escolhendo o formato TXT.')
        st.stop()
    return documento

def carrega_csv(caminho):
    documento = [] 
    try:
        if not caminho == '':
            loader = CSVLoader(caminho)
            lista_documentos = loader.load()
            documento = lista_documentos
            # documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    except Exception as e:
        print(f"Erro detalhado ao carregar YouTube: {e}")
        st.error('Ocorreu um erro ao carregar o arquivo :( Por favor recarregue a página.')
        st.stop()
    return documento

def carrega_pdf(caminho):
    documento = [] 
    try:
        if not caminho == '':
            loader = PyPDFLoader(caminho)
            lista_documentos = loader.load()
            documento = lista_documentos
            # documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    except Exception as e:
        print(f"Erro detalhado ao carregar YouTube: {e}")
        st.error('Ocorreu um erro ao carregar o arquivo :( Por favor recarregue a página.')
        st.stop()
    return documento

def carrega_txt(caminho):
    documento = [] 
    try:
        if not caminho == '':
            loader = TextLoader(caminho)
            lista_documentos = loader.load()
            documento = lista_documentos
            # documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    except Exception as e:
        print(f"Erro detalhado ao carregar YouTube: {e}")
        st.error('Ocorreu um erro ao carregar o arquivo :( Por favor recarregue a página.')
        st.stop()
    return documento

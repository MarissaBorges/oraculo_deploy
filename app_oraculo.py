import re
import tempfile
import os
import streamlit as st
from itertools import tee
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate as cpt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessageChunk
from loaders import *
from operator import itemgetter

TIPOS_DADOS_VALIDOS = [
    'Site', 'Youtube', 'PDF', 'CSV', 'TXT'
]

CONFIG_MODELOS = {
    "Groq": {"modelos": ["llama3-70b-8192","mistral-saba-24b", "deepseek-r1-distill-llama-70b", "allam-2-7b"],
             'chat': ChatGroq, 'secret_name': 'GROQ_API_KEY'}, 
}

msgs = StreamlitChatMessageHistory(key="mensagens_da_conversa")
MEMORIA = ConversationBufferMemory(chat_memory=msgs)

def carrega_arquivos(tipo_arquivo, arquivo):
    if not arquivo:
        return []
    
    documento = []

    if tipo_arquivo == 'Site':
        documento = carrega_site(arquivo)

    elif tipo_arquivo == 'Youtube':
        match = re.search(r"(?<=v=)[^&#]+", arquivo) or re.search(r"(?<=be/)[^&#]+", arquivo)
        video_id = match.group(0) if match else None

        if video_id:
            documento = carrega_youtube(video_id)
        else:
            st.error("URL do YouTube inválida. Não foi possível extrair o ID do vídeo.")
            st.stop()
            return None

    elif tipo_arquivo in ['PDF', 'CSV', 'TXT']:
        sufixo = f".{tipo_arquivo.lower()}"
        with tempfile.NamedTemporaryFile(suffix=sufixo, delete=False) as temp:
            temp.write(arquivo.read())
            caminho_temp = temp.name

        if tipo_arquivo == 'PDF':
            documento = carrega_pdf(caminho_temp)
        elif tipo_arquivo == 'CSV':
            documento = carrega_csv(caminho_temp)
        elif tipo_arquivo == 'TXT':
            documento = carrega_txt(caminho_temp)

        os.remove(caminho_temp)
    return documento


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


@st.cache_resource(show_spinner=False)
def funcao_rag(tipo_arquivo, arquivo, provedor, modelo):

    config_provedor = CONFIG_MODELOS.get(provedor)
    if not config_provedor:
        st.error(f"Provedor '{provedor}' não reconhecido ou configurado.")
        return None
    
    secret_name = config_provedor.get('secret_name')
    if not secret_name:
        st.error(f"Nome da chave secreta não configurado para o provedor '{provedor}'. Entre em contato com o administrador")
        st.markdown("[Entre em contato com o desenvolvedor](mailto:marissaborges2006@gmail.com)")
        st.stop()
        return None
    
    api_key = st.secrets.get(secret_name)
    if not api_key:
        st.error(f"A chave de API para {provedor} não foi encontrada. Entre em contato com o administrador.")
        st.markdown("[Entre em contato com o desenvolvedor](mailto:marissaborges2006@gmail.com)")
        st.stop()
        return None

    chat_class = config_provedor['chat']
    chat_instance = chat_class(model_name=modelo, groq_api_key=api_key)
    
    docs = carrega_arquivos(tipo_arquivo, arquivo)

    if not docs:
        system_message = """Você é um assistente amigável chamado Mimir, seu nome foi inspirado no jogo God Of War 4.
        Você é um deus da sabedoria e do conhecimento, então responda às perguntas da forma mais completa e útil possível.
        Responda sempre em português do Brasil, a menos que o usuário solicite outro idioma.
        """
        prompt = cpt.from_messages([
            ('system', system_message),
            ('placeholder', '{chat_history}'),
            ('user', '{input}')
        ])
        
        chain = prompt | chat_instance | StrOutputParser()
        return chain

    else:
        with st.spinner("Modelo esta carregando o documento, isso pode levar alguns minutos..."):
            text_spliter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
            chunks = text_spliter.split_documents(docs)

            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            vectorstore = Chroma.from_documents(chunks, embeddings)

            retriever = vectorstore.as_retriever(search_kwargs={'k': 5})

        system_message_rag = """Você é um assistente amigável chamado Mimir, seu nome foi inspirado no jogo God Of War 4. Você é um deus da sabedoria e do conhecimento, então responda às perguntas da forma mais completa e útil possível.

        Utilize o CONTEXTO fornecido abaixo para basear as suas respostas. Se a resposta não estiver no contexto, diga que você não possui informação sobre o assunto.
        Responda sempre em português do Brasil.
        CONTEXTO:
        {context}
        """
        prompt = cpt.from_messages([
            ('system', system_message_rag),
            ('placeholder', '{chat_history}'),
            ('user', '{input}')
        ])

        chain_rag = (
            {
                "context": itemgetter("input") | retriever | format_docs,
                "chat_history": itemgetter("chat_history"),
                "input": itemgetter("input"),
            }
            | prompt
            | chat_instance
            | StrOutputParser()
        )
        return chain_rag

def filtra_stream(stream):
    buffer = ""
    pensamento_removido = False
    primeiro_chunk_enviado = False
    regex_bloco_think = re.compile(r"<think>.*?</think>", re.DOTALL)

    for chunk in stream:
        content = ""
        if isinstance(chunk, dict):
            keys_comuns = ['answer', 'output', 'result', 'text']
            for key in keys_comuns:
                if key in chunk:
                    content = chunk[key]
                    break
        elif isinstance(chunk, AIMessageChunk):
            content = chunk.content
        elif isinstance(chunk, str):
            content = chunk
        
        if not isinstance(content, str):
            content = str(content)

        buffer += content

        if not pensamento_removido:
            match = regex_bloco_think.search(buffer)
            if match:
                buffer = regex_bloco_think.sub("", buffer)
                pensamento_removido = True
            elif "<think>" in buffer:
                continue
        
        if buffer:
            if not primeiro_chunk_enviado:
                buffer = buffer.lstrip()
                primeiro_chunk_enviado = True

            if buffer:
                yield buffer
                buffer = ""


def pagina_inicial():
    st.header('🤖 Bem-Vindo ao Oráculo Mimir', divider=True)

    chain = st.session_state.get('chain')

    if chain is None:
        st.error('O Oráculo não foi inicializado, por favor clique em **Inicializar Mimir...**')
        st.stop()

    memoria = st.session_state.get('memoria', MEMORIA)
    for mensagem in memoria.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)
    
    input_user = st.chat_input('Fale com o Mimir...')

    if input_user:
        chat = st.chat_message('human')
        chat.markdown(input_user)

        with st.chat_message('ai'):
                stream_original = chain.stream({
                    'input': input_user,
                    'chat_history': memoria.buffer_as_messages
                })

                stream_filtrada = filtra_stream(stream_original)

                stream_para_exibir, stream_para_capturar = tee(stream_filtrada)

                st.write_stream(stream_para_exibir)

                resposta_completa = "".join(list(stream_para_capturar))

        memoria.chat_memory.add_user_message(input_user)
        memoria.chat_memory.add_ai_message(resposta_completa)
        st.session_state['memoria'] = memoria


def sidebar():
    tabs = st.tabs(['Upload de Dados', 'Seleção de Modelos'])
    with tabs[0]:
        tipo_arquivo = st.selectbox('Selecione o tipo de arquivo', TIPOS_DADOS_VALIDOS)

        arquivo_key = f"arquivo_{tipo_arquivo}"

        if tipo_arquivo == 'Site' or tipo_arquivo == 'Youtube':
            arquivo = st.text_input(f'Informe a URL do {tipo_arquivo}...', key=arquivo_key)
        else:
            arquivo = st.file_uploader(f'Faça o upload do arquivo {tipo_arquivo}...', type=['.pdf', '.csv', '.txt'], key=arquivo_key)

    with tabs[1]:
        provedor = st.selectbox('Selecione o provedor do modelo...', CONFIG_MODELOS.keys())
        modelo = st.selectbox('Selecione o modelo...', CONFIG_MODELOS[provedor]['modelos'])

    if st.button('Inicializar Mimir', use_container_width=True):
        if "mensagens_da_conversa" in st.session_state:
            st.session_state.mensagens_da_conversa.clear()

        st.cache_resource.clear()

        if 'chain' in st.session_state:
            del st.session_state['chain']
        chain = funcao_rag(tipo_arquivo, arquivo, provedor, modelo)

        if chain:
            st.session_state['chain'] = chain
            st.success("Mimir inicializado com sucesso!")
        else:
            st.error("Falha ao inicializar Mimir.")
            st.stop()

def main():
    with st.sidebar:
        sidebar()
    pagina_inicial()

if __name__ == '__main__':
    main()

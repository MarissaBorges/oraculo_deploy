import re
import tempfile
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate as cpt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessageChunk
from loaders import *

TIPOS_DADOS_VALIDOS = [
    'Site', 'Youtube', 'PDF', 'CSV', 'TXT'
]

CONFIG_MODELOS = {
    "Groq": {"modelos": ["llama3-70b-8192","mistral-saba-24b", "deepseek-r1-distill-llama-70b", "allam-2-7b"],
             'chat': ChatGroq, 'secret_name': 'GROQ_API_KEY'}, 
}

MEMORIA = ConversationBufferMemory()

def carrega_arquivos(tipo_arquivo, arquivo):
    if tipo_arquivo == 'Site':
            documento = carrega_site(arquivo)
    elif tipo_arquivo == 'Youtube':
        documento = carrega_youtube(arquivo)
    elif tipo_arquivo == 'PDF':
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_pdf(nome_temp)
    elif tipo_arquivo == 'CSV':
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_csv(nome_temp)
    elif tipo_arquivo == 'TXT':
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_txt(nome_temp)
    return documento

def carrega_modelo(provedor, modelo, tipo_arquivo, arquivo):
    documento = carrega_arquivos(tipo_arquivo, arquivo)
    
    system_message = '''Você é um assistente amigável chamado Mimir, seu nome foi inspirado no jogo God Of War 4, onde Kratos e Atreus encontram o Deus da sabedoria e do conhecimento chamado Mimir e o levam consigo.
    Você possui acesso às seguintes informações vindas 
    de um documento {}: 

    ####
    {}
    ####

    Utilize as informações fornecidas para basear as suas respostas. Responda sempre em português Brasil a menos que o usuário solicite outro idioma. Não utilize tags de pensamento como <think> ou <reflection>. Forneça apenas a resposta final e direta.

    Sempre que houver $ na sua saída, substita por S.

    Se a informação do documento for algo como "Just a moment...Enable JavaScript and cookies to continue" 
    sugira ao usuário carregar novamente o Oráculo!'''.format(tipo_arquivo, documento)

    template = cpt.from_messages([
        ('system', system_message),
        ('placeholder', '{chat_history}'),
        ('user', '{input}')
    ])

    config_provedor = CONFIG_MODELOS.get(provedor)

    secret_name = config_provedor.get('secret_name')
    if not secret_name:
        st.error(f"Nome da chave secreta não configurado para o provedor '{provedor}'.")
        return False

    api_key = st.secrets.get(secret_name)

    if not api_key: # Verifica se a chave é None ou vazia
        st.error(f"Chave API para {provedor} ({secret_name}) não encontrada ou está vazia. "
                f"Por favor, entre em contato com o desenvolvedor para corrigir o erro")
        st.markdown('[email do desenvolvedor](marissaborges2006@gmail.com)')
        return False

    chat_class = config_provedor['chat']

    if provedor == "Groq":
        chat_instance = chat_class(model_name=modelo, groq_api_key=api_key)
    else: # Fallback, pode não funcionar para todos os provedores
        chat_instance = chat_class(model=modelo, api_key=api_key)
    
    chain = template | chat_instance | StrOutputParser()
    st.session_state['chain'] = chain

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
                stream_da_chain = chain.stream({
                    'input': input_user,
                    'chat_history': memoria.buffer_as_messages
                })
                resposta_filtrada = filtra_stream(stream_da_chain)
                resposta = st.write_stream(resposta_filtrada)

        memoria.chat_memory.add_user_message(input_user)
        memoria.chat_memory.add_ai_message(resposta)
        st.session_state['memoria'] = memoria


def sidebar():
    tabs = st.tabs(['Upload de Dados', 'Seleção de Modelos'])
    with tabs[0]:
        tipo_arquivo = st.selectbox('Selecione o tipo de arquivo', TIPOS_DADOS_VALIDOS)
        if tipo_arquivo == 'Site':
            arquivo = st.text_input('Informe a URL do Site...')
        if tipo_arquivo == 'Youtube':
            arquivo = st.text_input('Informe o link do vídeo...')
        if tipo_arquivo == 'PDF':
            arquivo = st.file_uploader('Faça o upload do arquivo PDF...', type=['.pdf'])
        if tipo_arquivo == 'CSV':
            arquivo = st.file_uploader('Faça o upload do arquivo CSV...', type=['.csv'])
        if tipo_arquivo == 'TXT':
            arquivo = st.file_uploader('Faça o upload do arquivo TXT...', type=['.txt'])


    with tabs[1]:
        provedor = st.selectbox('Selecione o provedor dos modelo...', CONFIG_MODELOS.keys())
        modelo = st.selectbox('Selecione o modelo...', CONFIG_MODELOS[provedor]['modelos'])
        
        # api_key = st.text_input(f'Adicione a api key para o provedor {provedor}',
        #                         value=st.session_state.get(f'api_key_{provedor}'))
        # st.session_state[f'api_key_{provedor}'] = api_key

    if st.button('Inicializar Mimir', use_container_width=True):
        carrega_modelo(provedor, modelo, tipo_arquivo, arquivo)
    
    if st.button('Apagar Histórico...', use_container_width=True):
        st.session_state['memoria'] = MEMORIA

def main():
    try:
        with st.sidebar:
            sidebar()
        pagina_inicial()
    except:
        st.error('Ocorreu um erro na aplicação, por favor recarregue a página e tente novamente...')

if __name__ == '__main__':
    main()

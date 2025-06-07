import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

TIPOS_DADOS_VALIDOS = [
    'Site', 'Youtube', 'PDF', 'CSV', 'TXT'
]

CONFIG_MODELOS = {
    "Groq": {"modelos": ["llama3-70b-8192","mistral-saba-24b","gemma-2b-it", "deepseek-r1-distill-llama-70b", "allam-2-7b", "whisper-large-v3-turbo"],
             'chat': ChatGroq, 'api_key': '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'},
    "Google": {"modelos": ["gemma-3-27b-it", "gemma-3n-e4b-it"], 
               'chat': ChatGoogleGenerativeAI, 'api_key': 'AIzaSyAyxXDdUZiuPlHnaTaQDwkrh7nafxRflNE'},
}

MEMORIA = ConversationBufferMemory()
def carrega_modelo(provedor, modelo):
    api_key = CONFIG_MODELOS[provedor]['api_key']
    chat = CONFIG_MODELOS[provedor]['chat'](model=modelo, api_key=api_key)
    st.session_state['chat'] = chat


def pagina_inicial():
    st.header('🤖 Bem-Vindo ao Oráculo Mimir', divider=True)

    chat_model = st.session_state.get('chat')
    memoria = st.session_state.get('memoria', MEMORIA)
    for mensagem in memoria.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)
    
    input_user = st.chat_input('Fale com o Mimir...')

    if input_user:
        chat = st.chat_message('human')
        chat.markdown(input_user)

        memoria.chat_memory.add_user_message(input_user)

        if chat_model is None:
            chat = st.chat_message('ai')
            chat.error("🤖 Mimir não foi inicializado. Por favor, selecione um modelo e clique em 'Inicializar Mimir' na barra lateral.")
        else:
            chat = st.chat_message('ai')
            resposta = chat.write_stream(chat_model.stream(input_user))

            memoria.chat_memory.add_user_message(input_user)
            memoria.chat_memory.add_ai_message(resposta)

        st.session_state['memoria'] = memoria
        print(st.session_state['memoria'])


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
        provedores_disponiveis = list(CONFIG_MODELOS.keys())
        provedor_default = st.session_state.get("provedor", provedores_disponiveis[0])
        provedor = st.selectbox('Selecione o provedor do modelo...',    
            provedores_disponiveis,
            index=provedores_disponiveis.index(provedor_default)
        )
        provedor = st.session_state["provedor"] = provedor

        modelos_disponiveis = CONFIG_MODELOS[provedor]['modelos']
        modelo_default = st.session_state.get(f"modelo_{provedor}", modelos_disponiveis[0])
        modelo = st.selectbox(
            'Escolha o modelo...',
            modelos_disponiveis,
            index=modelos_disponiveis.index(modelo_default)
        )
        modelo = st.session_state[f"modelo_{provedor}"] = modelo
        # api_key = st.text_input(f'Adicione a api key para o provedor {provedor}',
        #                         value=st.session_state.get(f'api_key_{provedor}'))
        # st.session_state[f'api_key_{provedor}'] = api_key

    if st.button('Inicializar Mimir', use_container_width=True):
        carrega_modelo(provedor, modelo)

def main():
    pagina_inicial()
    with st.sidebar:
        sidebar()

if __name__ == '__main__':
    main()

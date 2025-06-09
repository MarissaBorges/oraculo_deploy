import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

TIPOS_DADOS_VALIDOS = [
    'Site', 'Youtube', 'PDF', 'CSV', 'TXT'
]

CONFIG_MODELOS = {
    "Groq": {"modelos": ["llama3-70b-8192","mistral-saba-24b", "deepseek-r1-distill-llama-70b", "allam-2-7b"],
             'chat': ChatGroq, 'secret_name': 'GROQ_API_KEY'}, 
    "Google": {"modelos": ["gemma-3-1b-it", "gemma-3-4b-it", "gemma-3-12b-it", "gemma-3n-e4b-it"],
               'chat': ChatGoogleGenerativeAI, 'secret_name': 'GOOGLE_API_KEY'},
}

MEMORIA = ConversationBufferMemory()
def carrega_modelo(provedor, modelo):
        config_provedor = CONFIG_MODELOS.get(provedor)

        secret_name = config_provedor.get('secret_name')
        if not secret_name:
            st.error(f"Nome da chave secreta não configurado para o provedor '{provedor}'.")
            return False

        api_key = st.secrets.get(secret_name)

        if not api_key: # Verifica se a chave é None ou vazia
            st.error(f"Chave API para {provedor} ({secret_name}) não encontrada ou está vazia. "
                    f"Por favor, configure-a corretamente em st.secrets.")
            return False

        chat_class = config_provedor['chat']
        try:
            if provedor == "Groq":
                chat_instance = chat_class(model_name=modelo, groq_api_key=api_key)
            elif provedor == "Google":
                chat_instance = chat_class(model=modelo, google_api_key=api_key)
            else: # Fallback, pode não funcionar para todos os provedores
                chat_instance = chat_class(model=modelo, api_key=api_key)
            
            st.session_state['chat'] = chat_instance
            st.success(f"Modelo {provedor} - {modelo} carregado com sucesso!")
            return True
        except Exception as e: # Captura erros ao tentar usar a chave (ex: chave incorreta)
            st.error(f"Erro ao carregar o modelo {provedor} - {modelo}. "
                    f"Verifique se a chave API está correta e tem as permissões necessárias. Detalhes: {e}")
            if 'chat' in st.session_state: # Limpa se houve tentativa de definir
                del st.session_state['chat']
            return False

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

        if chat_model is None:
            chat = st.chat_message('ai')
            chat.error("🤖 Mimir não foi inicializado. Por favor, selecione um modelo e clique em 'Inicializar Mimir' na barra lateral.")
        else:
            chat = st.chat_message('ai')
            resposta = chat.write_stream(chat_model.stream(input_user))

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

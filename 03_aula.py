import streamlit as st

TIPOS_DADOS_VALIDOS = [
    'Site', 'Youtube', 'PDF', 'CSV', 'TXT'
]

CONFIG_MODELOS = {
    "Groq": {"modelos": ["llama3-70b-8192","mixtral-8x7b-32768","gemma-2b-it"]},
    "Google": {"modelos": ["models/gemini-1.5-pro-latest"]},
    "Hugging Face": {"modelos": ["deepseek-ai/deepseek-llm-7b-instruct","HuggingFaceH4/zephyr-7b-alpha"]}
}

MENSAGENS_EXEMPLO = [
    ('user', 'Olá'),
    ('assistent', 'Tudo bem?'),
    ('user', 'Tudo bem!')
]

def pagina_inicial():
    st.header('🤖 Bem-Vindo ao Oráculo Mimir', divider=True)

    mensagens = st.session_state.get('mensagens', MENSAGENS_EXEMPLO)
    for mensagem in mensagens:
        chat = st.chat_message(mensagem[0])
        chat.markdown(mensagem[1])
    
    input_user = st.chat_input('Fale com o Mimir...')

    if input_user:
        mensagens.append(('user', input_user))
        st.session_state['mensagens'] = mensagens
        st.rerun()

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
        provedor = st.selectbox('Selecione o provedor do modelo...', CONFIG_MODELOS.keys())
        modelo = st.selectbox('Escolha o modelo...', CONFIG_MODELOS[provedor]['modelos'])
        # api_key = st.text_input(f'Adicione a api key para o provedor {provedor}',
        #                         value=st.session_state.get(f'api_key_{provedor}'))
        # st.session_state[f'api_key_{provedor}'] = api_key

def main():
    pagina_inicial()
    with st.sidebar:
        sidebar()

if __name__ == '__main__':
    main()

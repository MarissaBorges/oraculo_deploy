import streamlit as st

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

def main():
    pagina_inicial()

if __name__ == '__main__':
    main()

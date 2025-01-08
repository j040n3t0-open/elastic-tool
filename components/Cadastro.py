import streamlit as st
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx
from components import TituloCadastro, BotaoSubmitStyle
import time, requests

def get_ip_address():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        return data['ip']
    except Exception as e:
        return str(e)

def salvaCadastro(ip_address,name,last_name,email,accept_contact):
    with open('./user_database/users.csv', 'a') as arquivo:
        # Escrever conteúdo incrementalmente
        arquivo.write(ip_address+','+name+','+last_name+','+email+','+str(accept_contact))
        arquivo.write('\n')
        st.session_state['cadastro'] = True
        st.success('Cadastro Finalizado! Navegue pelos menus...', icon="✅")

def cadastroUsuario():
    ip_address = get_ip_address()
    st.header(TituloCadastro.random_message())

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input('Primeiro Nome', '', key='name')
    with col2:
        last_name = st.text_input('Último Nome', '', key='last_name')
    
    email = st.text_input('Melhor e-mail', '', key='nome')
    accept_contact = st.checkbox('Aceito receber novidades nesse email', value=True )
    
    BotaoSubmitStyle.botaoSubmit()
    if st.button("Enviar", key='cadastroSubmit', use_container_width=True, type="primary"):
        if name and last_name and email:
            salvaCadastro(ip_address,name,last_name,email,accept_contact)
        else:
            st.warning("Preencha o cadastro primeiro!")
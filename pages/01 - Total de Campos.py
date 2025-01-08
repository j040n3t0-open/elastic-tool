import streamlit as st
#from streamlit_extras.app_logo import add_logo
from components import Header, Cadastro, BotaoSubmitStyle
import random, json
import pandas as pd

## Running project
##### streamlit run Home.py --theme.base dark --server.port 8502
 
def countFields(field_caps):
    count = 1
    type_list = []

    
    # Ler o arquivo JSON
    dados_json = json.loads(field_caps)

    for field in dados_json['fields']:
        count = count + 1        
        for field_type in dados_json['fields'][field]:
            type_list.append(field_type)

    contagem = {}
    for elemento in type_list:
        if elemento in contagem:
            contagem[elemento] += 1
        else:
            contagem[elemento] = 1

    # Ordenar o dicionário com base na quantidade
    ordenado_por_quantidade = sorted(contagem.items(), key=lambda x: x[1], reverse=True)

    return count,ordenado_por_quantidade

Header.add_logo()

if not "cadastro" in st.session_state:
    Cadastro.cadastroUsuario()
else:
    st.title("Total de Campos 🧮")
    st.subheader("Cole abaixo o resultado do seguinte comando:")

    st.write("**Modelo de busca:**")
    code = '''GET nome-indice/_field_caps?fields=*'''
    st.code(code, language='php')

    field_caps = st.text_area('Cole o retorno da busca acima:')

    def thatsFine(field_caps):
        try:
            total_campos,info_campos = countFields(field_caps)
            print(type(info_campos))
            print(info_campos)
            st.success('Done!', icon="✅")        
            st.subheader("Total de campos: %d" % total_campos)

            df = pd.DataFrame(info_campos, columns=['tipo', 'quantidade'])

            st.dataframe(df, use_container_width=True)
        except:
            st.error('Valide se colou o arquivo corretamente!', icon="🚨")

    try:
        BotaoSubmitStyle.botaoSubmit()
        if st.button("Obter análise", type="primary"):
            thatsFine(field_caps)
    except:
        st.error('Valide se colou o arquivo corretamente!', icon="🚨")

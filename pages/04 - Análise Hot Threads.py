import streamlit as st
#from streamlit_extras.app_logo import add_logo
from components import Header, Cadastro, BotaoSubmitStyle
import random, json
import pandas as pd
import re, os

## Running project
##### streamlit run Home.py --theme.base dark --server.port 8502
 
def geradorDF(field_caps):
    texto = field_caps

    def extrair_informacoes(entrada):
        
        try:
            data_hora = re.search(r'Hot threads at (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z)', entrada).group(1)
        except:
            data_hora = '-'
        try:
            intervalo = re.search(r'interval=(\d+)ms', entrada).group(1)
        except:
            intervalo = '-'
        try:
            busiest_threads = re.search(r'busiestThreads=(\d+)', entrada).group(1)
        except:
            busiest_threads = '-'
        try:
            data_type = re.search(r' data=(.+?)(,|})', entrada).group(1)
        except:
            data_type = '-'

        # Encontrar todas as informações da CPU
        cpu_info = re.findall(r'cpu=([\d.]+)%', entrada)
        if not cpu_info:
            cpu_info = re.findall(r'% ', entrada)
        
        cpu_other = re.findall(r'(other|idle)=([\d.]+)%', entrada)
        if not cpu_other:
            cpu_other = re.findall(r'% ', entrada)
        
        #cpu_total = [float(a) + float(b) for a, b in zip(cpu_info, cpu_other)]
        cpu_total = re.findall(r' ([\d.]+)%', entrada)
        #if not cpu_total:
        #    cpu_total.append(('other','0.0'))

        print(type(cpu_info),type(cpu_other),type(cpu_total))
        print(cpu_info,cpu_other,cpu_total)
        
        # Encontrar informações de threads
        #thread_info = re.findall(r'cpu usage by thread \'(.+?)\'', entrada)
        thread_info = re.findall(r'cpu usage by thread \'elasticsearch\[(.*?)\]\[(.*?)\]\[(.*?)\]\'', entrada)
        if not thread_info:
            thread_info = re.findall(r'cpu usage by thread \'(.*?)\'', entrada)
            new_thread_info = []
            for thread in thread_info:
                new_thread_info.append(thread)
            
            if not thread_info:
                new_thread_info.append("-")
        else:
            new_thread_info = []
            for thread in thread_info:
                new_thread_info.append(thread[1]+"["+thread[2]+"]")

        #print(new_thread_info)
        #print("Correspondências dentro de colchetes:", correspondencias_colchetes)
        #print("Correspondências dentro de parênteses:", correspondencias_parenteses)
        node_name = re.findall(r'cpu usage by thread \'elasticsearch\[(.+?)\]', entrada)
        if not node_name:
            node_name = re.findall(r' \{(.+?)\}', entrada)
         
        # Criar um DataFrame para as informações das threads
        df_threads = pd.DataFrame(new_thread_info, columns=["Thread Name"])
        df_nodes = pd.DataFrame(node_name, columns=["Node Name"])
        # Remover coluna 'Thread Details'
        #df_threads.pop('Thread Details')

        #print(cpu_total)
    
        df_principal = pd.DataFrame({
        "Data Type": data_type,
        "CPU Total %": cpu_total,
        "CPU Info %": cpu_info,
        "CPU Other %": cpu_other,
        "Data e Hora": data_hora,
        "Intervalo (ms)": intervalo,
        "Busiest Threads": busiest_threads,
        })
        
        
        return pd.concat([df_nodes, df_threads, df_principal], axis=1)

    # Extrair informações de cada entrada
    entradas = texto.strip().split(":::")
    clean_entradas = []
    for entrada in entradas:
        if "cpu usage by " in entrada:
            clean_entradas.append(entrada)
    entradas = clean_entradas
    #st.write(entradas)
    dados = [extrair_informacoes(entrada) for entrada in entradas if "Hot threads" in entrada]

    # Concatenar todos os DataFrames em um único DataFrame
    try:
        df_final = pd.concat(dados, ignore_index=True)

        print("Antes do Lambda")
        
        df_final['CPU Total %'] = df_final['CPU Total %'].astype(float)

        try:
            df_final['CPU Info %'] = df_final['CPU Info %'].astype(float)
        except:
            pass

        try:
            df_final['CPU Other %'] = df_final['CPU Other %'].apply(lambda x: x[1])
        except:
            pass
        #df_final['CPU Other %'] = df_final['CPU Other %'].astype(float)
        
        print(df_final['CPU Other %'])

        sorted_df = df_final.sort_values(by='CPU Total %', ascending=False)
        sorted_df = df_final

        return sorted_df
    except:
        return pd.DataFrame({})

Header.add_logo()

if not "cadastro" in st.session_state:
    Cadastro.cadastroUsuario()
else:
    st.title("Análise HOT Threads 🔥")
    st.subheader("Aqui você terá o resumo de algumas informações do Hot Threads")

    st.write("**Modelo de busca:**")
    code = '''GET _nodes/hot_threads'''
    st.code(code, language='php')

    field_caps = st.text_area('Cole o retorno da busca acima:')

    if "btn_click_hot_threads" not in st.session_state:
        st.session_state['btn_click_hot_threads'] = False

    try:
        BotaoSubmitStyle.botaoSubmit()
        if st.button("Obter análise", type="primary"):
            #with open('/home/joaoneto/projetos/scripts/elastic-tool-bkp/file.txt', 'a') as arquivo:
                # Escrever conteúdo incrementalmente
                #arquivo.write(field_caps)
                #arquivo.write('\n')
            # Função para extrair informações de uma entrada
            # Função para extrair informações de uma entrada
            df = geradorDF(field_caps)

            st.divider()

            st.session_state.df = df
            st.session_state.field_caps = field_caps
            st.session_state.btn_click_hot_threads  = True

        if st.session_state.btn_click_hot_threads:
            ## CONVERTENDO VALORES NUMERICOS
            df = st.session_state.df
            field_caps = st.session_state.field_caps

            if not df.empty:
                filtrar_node_name = st.multiselect("Selecione um Node para filtrar:", st.session_state.df['Node Name'].unique(), key='multi_hot')

                if filtrar_node_name:
                    node_list = []
                    for node in filtrar_node_name:
                        node_list.append(node)
                    dados_filtrados =  st.session_state.df[ st.session_state.df['Node Name'].isin(node_list)]

                    st.markdown(f'<br />',unsafe_allow_html=True)
                    # Ordenar o DataFrame filtrado pela coluna 'store' em ordem decrescente
                    sorted_df = dados_filtrados.sort_values(by='CPU Total %', ascending=False)
                    st.dataframe(sorted_df, use_container_width=True)
                else:
                    
                    st.markdown(f'<br />',unsafe_allow_html=True)
                    sorted_df = st.session_state.df.sort_values(by='CPU Total %', ascending=False)
                    st.dataframe(sorted_df, use_container_width=True)
            else:
                st.success("Nenhuma Thread identificada!", icon="🤷🏻‍♂️")
            
            st.divider()
            st.write("Referência: [HOT THREADS](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-nodes-hot-threads.html)")

    except Exception as e:
        st.error('Valide se colou o arquivo corretamente!', icon="🚨")
        st.write(e)

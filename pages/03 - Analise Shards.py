import streamlit as st
#from streamlit_extras.app_logo import add_logo
from components import Header, PrintInfo, Cadastro, BotaoSubmitStyle
import random, json, re
import pandas as pd
import numpy as np


st.cache_data.clear()
## Running project
##### streamlit run Home.py --theme.base dark --server.port 8502

Header.add_logo()

def set_node_roles(data):
    data_hot_list = []
    data_warm_list = []
    data_cold_list = []
    data_frozen_list = []
    data = json.loads(data)
    for node in data:
        if "h" in node['node.role']:
            data_hot_list.append(node)
        if "w" in node['node.role']:
            data_warm_list.append(node)
        if "c" in node['node.role']:
            data_cold_list.append(node)
        if "f" in node['node.role']:
            data_frozen_list.append(node)

    return data_hot_list,data_warm_list,data_cold_list,data_frozen_list

def printTotalNodes(data_hot_list,data_warm_list,data_cold_list,data_frozen_list):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        style = f"background-color: {'red'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">QTD HOT<br /> {len(data_hot_list)}',unsafe_allow_html=True)

    with col2:
        style = f"background-color: {'orange'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">QTD WARM<br /> {len(data_warm_list)}',unsafe_allow_html=True)

    with col3:
        style = f"background-color: {'RoyalBlue'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">QTD COLD<br /> {len(data_cold_list)}',unsafe_allow_html=True)

    with col4:
        style = f"background-color: {'DeepSkyBlue'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">QTD FROZEN<br /> {len(data_frozen_list)}',unsafe_allow_html=True)

@st.cache_data()
def processar_dados_hot(dados):
    dados['store'] = pd.to_numeric(dados['store'])
    dados['docs'] = pd.to_numeric(dados['docs'])
    return dados.copy()

@st.cache_data()
def processar_dados_warm(dados):
    dados['store'] = pd.to_numeric(dados['store'])
    dados['docs'] = pd.to_numeric(dados['docs'])
    return dados.copy()

@st.cache_data()
def processar_dados_cold(dados):
    dados['store'] = pd.to_numeric(dados['store'])
    dados['docs'] = pd.to_numeric(dados['docs'])
    return dados.copy()

@st.cache_data()
def processar_dados_frozen(dados):
    dados['store'] = pd.to_numeric(dados['store'])
    dados['docs'] = pd.to_numeric(dados['docs'])
    return dados.copy()


st.title("Análise de Shards 🔎")
st.subheader("Espaço destinado para análise de shards!")

st.markdown("Vamos pegar informações dos Nodes")
code = '''GET _cat/nodes?v&h=name,node.role&format=json'''
st.code(code, language='php')

data = st.text_area('Cole aqui o retorno da consulta dos nodes:')

st.markdown("Agora vamos pegar informações das shards")
code = '''GET _cat/shards?h=index,node,docs,store,shard,prirep,state,ip&bytes=mb&format=json'''
st.code(code, language='php')

data_shard = st.text_area('Cole aqui o retorno da consulta de shards:',key='shard')

st.markdown("Por último precisamos pegar a data de criação:")
code = '''GET _cat/indices?h=index,cds&expand_wildcards=all&format=json'''
st.code(code, language='php')

data_index_creation = st.text_area('Cole aqui o retorno da consulta dos indices:',key='indices')

# checagem de botao
if "btn_click" not in st.session_state:
    st.session_state['btn_click'] = False

BotaoSubmitStyle.botaoSubmit()
if st.button("Obter análise", key='shardSubmit', type="primary"):
    if data and data_shard and data_index_creation:
        try:
            data_hot_list, data_warm_list,data_cold_list,data_frozen_list = set_node_roles(data)
            data_shard = json.loads(data_shard)
            df = pd.DataFrame(data_shard)
            data_index_creation = json.loads(data_index_creation)
            df_index_creation = pd.DataFrame(data_index_creation)

            # Adicionar informação de data de criação no Shard com base no índice
            df = df.merge(df_index_creation, on='index', how='left')
            # Renomear o nome da coluna
            df = df.rename(columns={'cds': 'creation_date'})

            st.session_state.dados_processados_total = df
            st.session_state.data = data
            st.session_state.data_shard = data_shard
            st.session_state.data_index_creation = data_index_creation
            
            data_hot_node = []
            for node in data_hot_list:
                data_hot_node.append(node['name'])
            filtered_data_hot= df[df['node'].isin(data_hot_node)]
            st.session_state.dados_processados_hot = processar_dados_hot(filtered_data_hot)

            data_warm_node = []
            for node in data_warm_list:
                data_warm_node.append(node['name'])
            filtered_data_warm= df[df['node'].isin(data_warm_node)]
            st.session_state.dados_processados_warm = processar_dados_warm(filtered_data_warm)

            data_cold_node = []
            for node in data_cold_list:
                data_cold_node.append(node['name'])
            filtered_data_cold= df[df['node'].isin(data_cold_node)]
            st.session_state.dados_processados_cold = processar_dados_cold(filtered_data_cold)

            data_frozen_node = []
            for node in data_frozen_list:
                data_frozen_node.append(node['name'])
            filtered_data_frozen= df[df['node'].isin(data_frozen_node)]
            st.session_state.dados_processados_frozen = processar_dados_frozen(filtered_data_frozen)


            st.session_state.btn_click  = True
        except KeyError:
            st.warning('Valide se inseriu o cabeçalho correto na consulta!!!\n\n', icon="⚠️")
        except Exception as e:
            st.error('Valide se colou o arquivo corretamente!!!', icon="🚨")
    else:
        st.warning('Preencha os dados!', icon="⚠️")

if st.session_state.btn_click:
    try:
        ### CONVERTENDO VALORES NUMERICOS
        df = st.session_state.dados_processados_total
        data = st.session_state.data
        data_shard = st.session_state.data_shard
        data_index_creation = st.session_state.data_index_creation

        data_hot_list, data_warm_list,data_cold_list,data_frozen_list = set_node_roles(data)

        df['store'] = pd.to_numeric(df['store'])
        df['docs'] = pd.to_numeric(df['docs'])

        st.subheader("VISÃO GERAL")

        st.markdown("#### Total de Nodes")

        printTotalNodes(data_hot_list,data_warm_list,data_cold_list,data_frozen_list)
        
        st.markdown("#### Análise índice/shards")
        
        PrintInfo.printIndexInformations(df)

        st.divider()

        st.subheader("VISÃO POR NODE")
        
        if len(data_hot_list) > 0:
            st.subheader("HOT > TOP 10 SHARDS")

            data_hot_node = []
            for node in data_hot_list:
                data_hot_node.append(node['name'])
            filtered_data_hot= df[df['node'].isin(data_hot_node)]

            # Filtrando o DataFrame com base nas seleções

            filtrar_node_name = st.multiselect("Selecione um Node para filtrar:", st.session_state.dados_processados_hot['node'].unique(), key='multi_hot')

            if filtrar_node_name:
                node_list = []
                for node in filtrar_node_name:
                    node_list.append(node)
                dados_filtrados_hot =  st.session_state.dados_processados_hot[ st.session_state.dados_processados_hot['node'].isin(node_list)]

                PrintInfo.printIndexInformations(dados_filtrados_hot)
                st.markdown(f'<br />',unsafe_allow_html=True)
                st.write("Dados filtrados:")
                # Ordenar o DataFrame filtrado pela coluna 'store' em ordem decrescente
                sorted_df = dados_filtrados_hot.sort_values(by='store', ascending=False)
                # Exibir os 10 maiores valores
                top_10 = sorted_df.head(10)
                st.write(top_10, use_container_width=True)
            else:

                PrintInfo.printIndexInformations(filtered_data_hot)
                st.markdown(f'<br />',unsafe_allow_html=True)
                sorted_df = st.session_state.dados_processados_hot.sort_values(by='store', ascending=False)
                # Exibir os 10 maiores valores
                top_10 = sorted_df.head(10)
                st.write(top_10, use_container_width=True)

        if len(data_warm_list) > 0:
            st.subheader("WARM > TOP 10 SHARDS")
            data_warm_node = []
            for node in data_warm_list:
                data_warm_node.append(node['name'])
            filtered_data_warm= df[df['node'].isin(data_warm_node)]

            filtrar_node_name = st.multiselect("Selecione um Node para filtrar:", st.session_state.dados_processados_warm['node'].unique(), key='multi_warm')

            if filtrar_node_name:
                node_list = []
                for node in filtrar_node_name:
                    node_list.append(node)
                dados_filtrados_warm =  st.session_state.dados_processados_warm[ st.session_state.dados_processados_warm['node'].isin(node_list)]
                
                PrintInfo.printIndexInformations(dados_filtrados_warm)
                st.markdown(f'<br />',unsafe_allow_html=True)
                st.write("Dados filtrados:")
                # Ordenar o DataFrame filtrado pela coluna 'store' em ordem decrescente
                sorted_df = dados_filtrados_warm.sort_values(by='store', ascending=False)
                # Exibir os 10 maiores valores
                top_10 = sorted_df.head(10)
                st.write(top_10, use_container_width=True)
            else:
                PrintInfo.printIndexInformations(filtered_data_warm)
                st.markdown(f'<br />',unsafe_allow_html=True)
                sorted_df = st.session_state.dados_processados_warm.sort_values(by='store', ascending=False)
                # Exibir os 10 maiores valores
                top_10 = sorted_df.head(10)
                st.write(top_10, use_container_width=True)

        if len(data_cold_list) > 0:
            st.subheader("COLD > TOP 10 SHARDS")
            data_cold_node = []
            for node in data_cold_list:
                data_cold_node.append(node['name'])
            filtered_data_cold = df[df['node'].isin(data_cold_node)]

            
            filtrar_node_name = st.multiselect("Selecione um Node para filtrar:", st.session_state.dados_processados_cold['node'].unique(), key='multi_cold')

            if filtrar_node_name:
                node_list = []
                for node in filtrar_node_name:
                    node_list.append(node)
                dados_filtrados_cold =  st.session_state.dados_processados_cold[ st.session_state.dados_processados_cold['node'].isin(node_list)]

                PrintInfo.printIndexInformations(dados_filtrados_cold)
                st.markdown(f'<br />',unsafe_allow_html=True)
                st.write("Dados filtrados:")
                # Ordenar o DataFrame filtrado pela coluna 'store' em ordem decrescente
                sorted_df = dados_filtrados_cold.sort_values(by='store', ascending=False)
                # Exibir os 10 maiores valores
                top_10 = sorted_df.head(10)
                st.write(top_10, use_container_width=True)
            else:
                PrintInfo.printIndexInformations(filtered_data_cold)
                st.markdown(f'<br />',unsafe_allow_html=True)
                sorted_df = st.session_state.dados_processados_cold.sort_values(by='store', ascending=False)
                # Exibir os 10 maiores valores
                top_10 = sorted_df.head(10)
                st.write(top_10, use_container_width=True)

        if len(data_frozen_list) > 0:
            st.subheader("FROZEN > TOP 10 SHARDS")
            data_frozen_node = []
            for node in data_frozen_list:
                data_frozen_node.append(node['name'])
            filtered_data_frozen = df[df['node'].isin(data_frozen_node)]

            

            filtrar_node_name = st.multiselect("Selecione um Node para filtrar:", st.session_state.dados_processados_frozen['node'].unique(), key='multi_frozen')

            if filtrar_node_name:
                node_list = []
                for node in filtrar_node_name:
                    node_list.append(node)
                dados_filtrados_frozen =  st.session_state.dados_processados_frozen[ st.session_state.dados_processados_frozen['node'].isin(node_list)]
                st.write("Dados filtrados:")

                PrintInfo.printIndexInformations(dados_filtrados_frozen)
                st.markdown(f'<br />',unsafe_allow_html=True)
                # Ordenar o DataFrame filtrado pela coluna 'docs' em ordem decrescente
                sorted_df = dados_filtrados_frozen.sort_values(by='docs', ascending=False)
                # Exibir os 10 maiores valores
                top_10 = sorted_df.head(10)
                st.write(top_10, use_container_width=True)
            else:
                PrintInfo.printIndexInformations(filtered_data_frozen)
                st.markdown(f'<br />',unsafe_allow_html=True)
                sorted_df = st.session_state.dados_processados_frozen.sort_values(by='docs', ascending=False)
                # Exibir os 10 maiores valores
                top_10 = sorted_df.head(10)
                st.write(top_10, use_container_width=True)
        
        st.divider()
        st.subheader("PLAYGROUND (Todos os dados)")

        st.markdown(f'<br />',unsafe_allow_html=True)

        filtrar_node_name = st.multiselect("Selecione um Node para filtrar:", df['node'].unique())

        if filtrar_node_name:
            node_list = []
            for node in filtrar_node_name:
                node_list.append(node)
            df_filtered =  df[ df['node'].isin(node_list)]

            PrintInfo.printIndexInformations(df_filtered)
            st.markdown(f'<br />',unsafe_allow_html=True)
            st.write("Dados filtrados:")
            # Ordenar o DataFrame filtrado pela coluna 'store' em ordem decrescente
            sorted_df = df_filtered.sort_values(by='store', ascending=False)
            st.write(sorted_df, use_container_width=True)
        else:
            PrintInfo.printIndexInformations(df)
            st.markdown(f'<br />',unsafe_allow_html=True)
            sorted_df = df.sort_values(by='store', ascending=False)
            st.write(sorted_df, use_container_width=True)
    except KeyError:
        st.warning('Valide se inseriu o cabeçalho correto na consulta!!!\n\n', icon="⚠️")
    except Exception as e:
        st.error('Valide se colou o arquivo corretamente!!!', icon="🚨")
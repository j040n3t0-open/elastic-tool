import streamlit as st
#from streamlit_extras.app_logo import add_logo
from components import Header, Cadastro, BotaoSubmitStyle
import random, json, re
import pandas as pd
import numpy as np
import time


## Running project
##### streamlit run Home.py --theme.base dark --server.port 8502

Header.add_logo()

if not "cadastro" in st.session_state:
    Cadastro.cadastroUsuario()
else:
    st.title("Tempo de Consulta ⌛")
    st.subheader("Espaço destinado para análise de tempo gasto em uma consulta!")

    st.write("**Modelo de busca:**")
    code = '''GET index_name/_search?filter_path=took,profile&request_cache=false&human=true
    {
    "profile":true,
    "query":{"bool":{"filter":[{"term":{"foo":"bar"}}]}},
    "aggs":{"NAME":{"terms":{"field":"xpto"}}}
    }'''
    st.code(code, language='json')


    data = st.text_area('Cole abaixo o resultado da consulta e clique em Obter análise:')

    #json_file_path = "/home/joaoneto/projetos/scripts/elastic-tool/pages/explain.json"

    # Open the JSON file for reading
    #with open(json_file_path, "r") as json_file:
        # Load the JSON data from the file
        #data = json.load(json_file)

    def modify_data(data):
        data = data.split('"""')
        new_data = []
        for part in data:
            if not "{" in part:
                part = part.replace('"',"'")
                new_data.append(part)
            else:
                new_data.append(part)
        data = "\"".join(new_data)
        return data


    def mainProgram(data):

        # Ler o arquivo JSON
        data = modify_data(data)
        data = json.loads(data)
        time_took_sec = int(data['took']) / 1000
        total_time_per_shard_query = 0
        total_time_per_shard_aggs = 0

        time_query_list = []
        time_shard = []


        for shard in data['profile']['shards']:
            for search in shard['searches']:
                for query in search['query']:
                    total_time_per_shard_query = total_time_per_shard_query + query['time_in_nanos']
            for aggs in shard['aggregations']:
                total_time_per_shard_aggs = total_time_per_shard_aggs + aggs['time_in_nanos']
            # Encontrar todos os padrões na string
            padrao = r"\[([^\]]+)\]"
            resultados = re.findall(padrao, shard['id'])
            total_time_per_shard_query = total_time_per_shard_query / 1000000000
            total_time_per_shard_aggs = total_time_per_shard_aggs / 1000000000
            total_time = "Search %.2f/sec | Aggs %.2f/sec" % (total_time_per_shard_query,total_time_per_shard_aggs)
            time_shard.append({resultados[2]:total_time})


        # Usando a função sorted com uma expressão lambda para extrair o segundo valor de cada dicionário
        #time_shard_sorted = sorted(time_shard, key=lambda x: list(x.values())[0], reverse=True)
        # Imprimindo a lista ordenada
        #for value in time_shard_sorted:
            #for shard, time in value.items():
                #print(f'Chave: {chave}, Valor: {valor}')
                #print("Shard: %s / Time: %.2f/s" % (shard,time))
        #    

        try:
            st.success('Done!', icon="✅")
            st.subheader("**TEMPO DE PROCESSAMENTO ELASTICSEARCH**")
            st.write("**TOOK:** %.2f/sec" % time_took_sec)
            # Imprimir os resultados ordenados
            #style = f"padding: 5px; border-radius: 5px; font-weight: bold;font-size: 20px; height: 80px; display: flex;"
            #st.markdown(f'<div id="1" style="{style}"> ## Total por tipo de campo ##',unsafe_allow_html=True)
            for value in time_shard:
                for shard, time in value.items():
                    #time = "%.2f" % time
                    style = f"padding: 1px; border-radius: 1px; line-height: 0.1; font-size: 16px; height: 30px;"
                    st.markdown(f'<div id="1" style="{style}"> <b>Shard {shard}:</b> {time}',unsafe_allow_html=True)

            st.divider()
            st.subheader("**DETALHAMENTO ANALÍTICO POR SHARD**")

            query_list = []
            query_children_list = []
            query_granddaughter_list = []

            for shard in data['profile']['shards']:
                shard_id = shard['id']
                style = f"padding: 1px; border-radius: 1px; line-height: 1; font-size: 18px; height: 30px;"
                st.markdown(f'<div id="1" style="{style}"> <mark style="background: green"><b>{shard_id}</b></mark>',unsafe_allow_html=True)

                for search in shard['searches']:
                    for query in search['query']:
                        query_list.append({"type":query['type'],"time":query['time'],"time_in_nanos":query['time_in_nanos'],"description":query['description']})
                        try:
                            if len(query['children']) > 0:
                                #st.write("Detectado %i consultas filhas! Analisando tempo de search delas..." % len(query['children']))
                                for search_children in query['children']:
                                    query_children_list.append({"type":search_children['type'],"time_in_nanos":search_children['time_in_nanos'],"time":search_children['time'],"description":search_children['description']})
                                    try:
                                        if len(search_children['children']) > 0:
                                            #st.write("Detectado %i search filhas da filha! Analisando tempo de search delas..." % len(search_children['children']))
                                            for search_children_of_children in search_children['children']:
                                                query_granddaughter_list.append({"type":search_children_of_children['type'],"time":search_children_of_children['time'],"time_in_nanos":search_children_of_children['time_in_nanos'],"description":search_children_of_children['description']})
                                    except:
                                        pass
                        except:
                            pass


                if len(query_list) > 0:
                    st.write("**ANÁLISE DE QUERIES [PAI] 🔎**")
                    df = pd.DataFrame(query_list)
                    df = df.sort_values(by='time_in_nanos', ascending=False)
                    df = df.drop(columns=['time_in_nanos'])
                    st.table(df)

                if len(query_children_list) > 0:
                    st.write("**ANÁLISE DE QUERIES [FILHA] 🔎**")
                    df = pd.DataFrame(query_children_list)
                    df = df.sort_values(by='time_in_nanos', ascending=False)
                    df = df.drop(columns=['time_in_nanos'])
                    st.table(df)

                if len(query_granddaughter_list) > 0:
                    st.write("**ANÁLISE DE QUERIES [FILHA DA FILHA] 🔎**")
                    df = pd.DataFrame(query_granddaughter_list)
                    df = df.sort_values(by='time_in_nanos', ascending=False)
                    df = df.drop(columns=['time_in_nanos'])
                    st.table(df)


                aggs_list = []
                aggs_children_list = []

                for aggs in shard['aggregations']:
                    aggs_list.append({"type":aggs['type'],"time":aggs['time'],"time_in_nanos":aggs['time_in_nanos'],"description":aggs['description']})
                    try:
                        if len(aggs['children']) > 0:
                            for aggs_children in aggs['children']:
                                aggs_children_list.append({"type":aggs_children['type'],"time":aggs_children['time'],"time_in_nanos":aggs_children['time_in_nanos'],"description":aggs_children['description']})
                    except:
                        pass

                if len(aggs_list) > 0:
                    st.write("Analise de Agregações [PAI] 📊")
                    df = pd.DataFrame(aggs_list)
                    df = df.sort_values(by='time_in_nanos', ascending=False)
                    df = df.drop(columns=['time_in_nanos'])
                    st.table(df)

                if len(aggs_children_list) > 0:
                    st.write("Analise de Agregações [FILHA] 📊")
                    df = pd.DataFrame(aggs_children_list)
                    df = df.sort_values(by='time_in_nanos', ascending=False)
                    df = df.drop(columns=['time_in_nanos'])
                    st.table(df)
        except KeyError:
            st.warning('Valide se inseriu o cabeçalho correto na consulta!!!\n\n*?filter_path=took,profile&request_cache=false&human=true*', icon="⚠️")
        except Exception as e:
            st.write(e)
            st.error('Valide se colou o arquivo corretamente!!!', icon="🚨")

    try:
        control = 0
        BotaoSubmitStyle.botaoSubmit()
        if st.button("Obter análise", type="primary"):
            with st.spinner('Processando...'):
                time.sleep(5)
                control = 1
        if control > 0:
            mainProgram(data)
    except KeyError as e:
            st.write(e)
            st.warning('Valide se inserir o cabeçalho correto na consulta!!!\n\n*?filter_path=took,profile&request_cache=false&human=true*', icon="⚠️")    
    except:
        st.error('Valide se colou o arquivo corretamente!', icon="🚨")
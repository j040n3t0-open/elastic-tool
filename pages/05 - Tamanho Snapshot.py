import streamlit as st
#from streamlit_extras.app_logo import add_logo
from components import Header, PrintInfo, Cadastro, BotaoSubmitStyle
import random, json, re
import pandas as pd
import numpy as np
import altair as alt


st.cache_data.clear()
## Running project
##### streamlit run Home.py --theme.base dark --server.port 8502
st.session_state.data_health = False

Header.add_logo()


def printInitialReport(total_lines, total_bytes, avg_bytes, bigger_index, bigger_size, bigger_size_human, lowest_index, lowest_size, lowest_size_human):
    st.markdown("#### Métricas Gerais")
    col1, col2, col3 = st.columns(3)
    st.columns(4)
    st.markdown("#### Análise dos índices")
    col4, col5 = st.columns(2)


    with col1:
        style = f"background-color: {'#0f8713'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">Total Indices<br /> {total_lines}',unsafe_allow_html=True)

    with col2:
        style = f"background-color: {'#05ab1e'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">Tamanho Total (GB)<br /> {total_bytes}',unsafe_allow_html=True)

    with col3:
        style = f"background-color: {'#63bf7a'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">Mediana Tamanho (kB)<br /> {avg_bytes}',unsafe_allow_html=True)

    with col4:
        style = f"background-color: {'#91244a'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">Maior Index: {bigger_index}<br /> {bigger_size_human}',unsafe_allow_html=True)

    with col5:
        style = f"background-color: {'#3638b5'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">Menor Index: {lowest_index}<br /> {lowest_size_human}',unsafe_allow_html=True)


def createChart(df):
    df = df.rename(columns={'size': 'size_bytes'})
    st.write("Chart History 📈")

    c = (
        alt.Chart(df)
        .mark_bar()
        .encode(x=alt.X('index', sort=None), y="size_bytes", color="index", tooltip=["index", "size_bytes"])
    )

    st.altair_chart(c, use_container_width=True)

st.title("Análise Tamanho Snapshot 💾")
st.subheader("Espaço destinado para análisar o tamanho de um snapshot, visto que a informação vem segmentada índice a índice!")

st.markdown("Vamos pegar o consulta do Snapshot")
code = '''GET /_snapshot/<NOME_REPOSITORIO>/<NOME_SNAPSHOT>?index_details=true'''
st.code(code, language='php')

data_health = st.text_area('Cole aqui o retorno da consulta:')

# checagem de botao
if "btn_click" not in st.session_state:
    st.session_state['btn_click'] = False

BotaoSubmitStyle.botaoSubmit()

if st.button("Obter análise", key='shardSubmit', type="primary"):
    if data_health:
        try:
            data_health = json.loads(data_health)

            df = pd.DataFrame(columns=['index', 'size', 'human_size'])
            id = 0

            for snapshot in data_health['snapshots']:
                for indice in snapshot['index_details']:
                    df.loc[id] = indice, snapshot['index_details'][indice]['size_in_bytes'], snapshot['index_details'][indice]['size'] # size_in_bytes
                    id = id + 1
                    
            sorted_df = df.sort_values(by='size', ascending=False)
            total_lines = sorted_df.shape[0]

            first_row = sorted_df.iloc[:1].to_string(index=False)
            first_row = first_row.split("\n")[1].split(" ")
            while '' in first_row:
                first_row.remove('')
            bigger_index, bigger_size, bigger_size_human = first_row
            
            last_row = sorted_df.iloc[-1:].to_string(index=False)
            last_row = last_row.split("\n")[1].split(" ")
            while '' in last_row:
                last_row.remove('')
            lowest_index, lowest_size, lowest_size_human  = last_row

            total_bytes = sorted_df['size'].sum()
            total_bytes = ((total_bytes/1024)/1024)/1024
            total_bytes = "%.2f" % total_bytes

            median_bytes = sorted_df['size'].median()
            median_bytes = ((median_bytes/1024)/1024)
            median_bytes = "%.2f" % median_bytes

            st.session_state.data_health = data_health
            st.session_state.btn_click  = True
        except KeyError:
            st.warning('Valide se inseriu a consulta correta!!', icon="⚠️")
        except Exception as e:
            print(e)
            st.error('Valide se colou o arquivo corretamente!!!', icon="🚨")

    else:
        st.warning('Preencha os dados!', icon="⚠️")

if st.session_state.data_health:
        ### CONVERTENDO VALORES NUMERICOS
        data = st.session_state.data_health

        st.subheader("VISÃO GERAL")

        printInitialReport(
            total_lines, 
            total_bytes, 
            median_bytes, 
            bigger_index, 
            bigger_size,
            bigger_size_human,
            lowest_index, 
            lowest_size,
            lowest_size_human
        )
        
        st.divider()
        
        st.markdown("#### Top 10 Índices")

        top_10 = sorted_df.head(10)
        
        createChart(top_10)

        st.markdown("#### Dataset Completo dos Índices")
        st.write(sorted_df, use_container_width=True)
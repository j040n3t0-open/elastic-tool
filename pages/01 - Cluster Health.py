import streamlit as st
#from streamlit_extras.app_logo import add_logo
from components import Header, PrintInfo, Cadastro, BotaoSubmitStyle
import random, json, re
import pandas as pd
import numpy as np


st.cache_data.clear()
## Running project
##### streamlit run Home.py --theme.base dark --server.port 8502
st.session_state.data_health = False

Header.add_logo()


def printInitialReport(status_cluster,status_master,status_repository,status_disk,status_shards_capacity,status_shards_availability,status_ds_lifecycle,status_slm,status_ilm):
    cluster1 = st.columns([1])[0]
    st.columns(4)
    col1, col2, col3, col4 = st.columns(4)
    st.columns(4)
    col5, col6, col7, col8 = st.columns(4)

    with cluster1:
        if status_cluster == "green":
            style = f"background-color: {'green'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        elif status_cluster == "red":
            style = f"background-color: {'red'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        elif status_cluster == "yellow":
            style = f"background-color: {'Gold'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">CLUSTER<br /> {status_cluster.upper()}',unsafe_allow_html=True)

    with col1:
        if status_master == "green":
            style = f"background-color: {'green'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        elif status_master == "red":
            style = f"background-color: {'red'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        elif status_master == "yellow":
            style = f"background-color: {'Gold'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">MASTER<br /> {status_master.upper()}',unsafe_allow_html=True)

    with col2:
        if status_repository == "green":
            style = f"background-color: {'green'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        elif status_repository == "red":
            style = f"background-color: {'red'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        elif status_repository == "yellow":
            style = f"background-color: {'Gold'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">REPOSITORY<br /> {status_repository.upper()}',unsafe_allow_html=True)

    with col3:
        if status_disk == "green":
            style = f"background-color: {'green'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        elif status_disk == "red":
            style = f"background-color: {'red'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        elif status_disk == "yellow":
            style = f"background-color: {'Gold'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">DISK<br /> {status_disk.upper()}',unsafe_allow_html=True)

    with col4:
        if status_shards_capacity == "green":
            style = f"background-color: {'green'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        elif status_shards_capacity == "red":
            style = f"background-color: {'red'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        elif status_shards_capacity == "yellow":
            style = f"background-color: {'Gold'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">SHARDS CAP.<br /> {status_shards_capacity.upper()}',unsafe_allow_html=True)

    with col5:
        if status_shards_availability == "green":
            style = f"background-color: {'green'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        elif status_shards_availability == "red":
            style = f"background-color: {'red'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        elif status_shards_availability == "yellow":
            style = f"background-color: {'Gold'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">SHARDS AVAI.<br /> {status_shards_availability.upper()}',unsafe_allow_html=True)

    with col6:
        if status_ds_lifecycle == "green":
            style = f"background-color: {'green'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        elif status_ds_lifecycle == "red":
            style = f"background-color: {'red'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        elif status_ds_lifecycle == "yellow":
            style = f"background-color: {'Gold'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">DATA STREAM<br /> {status_ds_lifecycle.upper()}',unsafe_allow_html=True)

    with col7:
        if status_slm == "green":
            style = f"background-color: {'green'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        elif status_slm == "red":
            style = f"background-color: {'red'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        elif status_slm == "yellow":
            style = f"background-color: {'Gold'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">SLM<br /> {status_slm.upper()}',unsafe_allow_html=True)

    with col8:
        if status_ilm == "green":
            style = f"background-color: {'green'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        elif status_ilm == "red":
            style = f"background-color: {'red'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        elif status_ilm == "yellow":
            style = f"background-color: {'Gold'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">ILM<br /> {status_ilm.upper()}',unsafe_allow_html=True)

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


st.title("Análise de Saúde do Cluster 🏥")
st.subheader("Espaço destinado para análise geral dos principais serviços do Cluster!")

st.markdown("Vamos pegar informações de saúde. (_**Obs. Versão 8.7+**_)")
code = '''GET _health_report'''
st.code(code, language='php')

data_health = st.text_area('Cole aqui o retorno da consulta:')

# checagem de botao
if "btn_click" not in st.session_state:
    st.session_state['btn_click'] = False

BotaoSubmitStyle.botaoSubmit()

if st.button("Obter análise", key='shardSubmit', type="primary"):
    if data_health:
        data_health = json.loads(data_health)

        status_cluster = data_health['status']
        status_master = data_health['indicators']['master_is_stable']['status']
        status_repository = data_health['indicators']['repository_integrity']['status']
        status_disk = data_health['indicators']['disk']['status']
        status_shards_capacity = data_health['indicators']['shards_capacity']['status']
        status_shards_availability = data_health['indicators']['shards_availability']['status']
        status_ds_lifecycle = data_health['indicators']['data_stream_lifecycle']['status']
        status_slm = data_health['indicators']['slm']['status']
        status_ilm = data_health['indicators']['ilm']['status']

        st.session_state.data_health = data_health
        st.session_state.btn_click  = True

    else:
        st.warning('Preencha os dados!', icon="⚠️")

if st.session_state.data_health:
        ### CONVERTENDO VALORES NUMERICOS
        data = st.session_state.data_health

        st.subheader("VISÃO GERAL")

        st.markdown("#### Serviços Essenciais")

        printInitialReport(
            status_cluster,
            status_master,
            status_repository,
            status_disk,
            status_shards_capacity,
            status_shards_availability,
            status_ds_lifecycle,
            status_slm,
            status_ilm
        )
        
        st.divider()
        
        st.markdown("#### MASTER")

        st.write("Status: %s" % data_health['indicators']['master_is_stable']['status'])
        st.write("Descrição: %s" % data_health['indicators']['master_is_stable']['symptom'])
        st.write("Nome Node Master: %s" % data_health['indicators']['master_is_stable']['details']['current_master']['name'])
        st.write("ID Node Master: %s" % data_health['indicators']['master_is_stable']['details']['current_master']['node_id'])

        st.divider()
        
        st.markdown("#### REPOSITORIO")

        st.write("Status: %s" % data_health['indicators']['repository_integrity']['status'])
        st.write("Descrição: %s" % data_health['indicators']['repository_integrity']['symptom'])
        st.write("Qtd Repositorios: %s" % data_health['indicators']['repository_integrity']['details']['total_repositories'])

        st.divider()
        
        
        st.markdown("#### DISCO")

        st.write("Status: %s" % data_health['indicators']['disk']['status'])
        st.write("Descrição: %s" % data_health['indicators']['disk']['symptom'])
        st.write("Qtd Indices Somente Leitura: %s" % data_health['indicators']['disk']['details']['indices_with_readonly_block'])
        st.write("Nodes com disco suficiente: %s" % data_health['indicators']['disk']['details']['nodes_with_enough_disk_space'])
        st.write("Status igual Unknown: %s" % data_health['indicators']['disk']['details']['nodes_with_unknown_disk_status'])
        st.write("Nodes com Watermark alto: %s" % data_health['indicators']['disk']['details']['nodes_over_high_watermark'])
        st.write("Nodes com Watermark: %s" % data_health['indicators']['disk']['details']['nodes_over_flood_stage_watermark'])

        st.divider()
        
        st.markdown("#### CAPACIDADE DOS SHARDS")

        st.write("Status: %s" % data_health['indicators']['shards_capacity']['status'])
        st.write("Descrição: %s" % data_health['indicators']['shards_capacity']['symptom'])
        st.write("Maximo Shards Hot/Warm/Cold: %s" % data_health['indicators']['shards_capacity']['details']['data']['max_shards_in_cluster'])
        st.write("Maximo Shards Frozen: %s" % data_health['indicators']['shards_capacity']['details']['frozen']['max_shards_in_cluster'])

        st.divider()
        
        st.markdown("#### DISPONIBILIDADE DOS SHARDS")

        st.write("Status: %s" % data_health['indicators']['shards_availability']['status'])
        st.write("Descrição: %s" % data_health['indicators']['shards_availability']['symptom'])

        st.write("Primários Inicializados: %s" % data_health['indicators']['shards_availability']['details']['started_primaries'])
        st.write("Inicializando Primários: %s" % data_health['indicators']['shards_availability']['details']['initializing_primaries'])
        st.write("Reiniciando Primários: %s" % data_health['indicators']['shards_availability']['details']['restarting_primaries'])
        st.write("Primários Não Assinados: %s" % data_health['indicators']['shards_availability']['details']['unassigned_primaries'])
        st.write("Criando Primários: %s" % data_health['indicators']['shards_availability']['details']['creating_primaries'])

        st.write("Réplicas Inicializadas: %s" % data_health['indicators']['shards_availability']['details']['started_replicas'])
        st.write("Inicializando Réplicas: %s" % data_health['indicators']['shards_availability']['details']['initializing_replicas'])
        st.write("Reiniciando Réplicas: %s" % data_health['indicators']['shards_availability']['details']['restarting_replicas'])
        st.write("Réplicas Não Assinadas: %s" % data_health['indicators']['shards_availability']['details']['unassigned_replicas'])
        st.write("Criando Replicas: %s" % data_health['indicators']['shards_availability']['details']['creating_replicas'])
        
        st.divider()
        
        st.markdown("#### DATA STREAM")

        st.write("Status: %s" % data_health['indicators']['data_stream_lifecycle']['status'])
        st.write("Descrição: %s" % data_health['indicators']['data_stream_lifecycle']['symptom'])
        st.write("Indices Estagnados: %s" % data_health['indicators']['data_stream_lifecycle']['details']['stagnating_backing_indices_count'])
        st.write("Indices com Erro: %s" % data_health['indicators']['data_stream_lifecycle']['details']['total_backing_indices_in_error'])

        st.divider()
        
        st.markdown("#### SLM")

        st.write("Status: %s" % data_health['indicators']['slm']['status'])
        st.write("Descrição: %s" % data_health['indicators']['slm']['symptom'])
        st.write("Status do Serviço: %s" % data_health['indicators']['slm']['details']['slm_status'])
        st.write("Qtd de Politicas: %s" % data_health['indicators']['slm']['details']['policies'])

        if 'impacts' in data_health['indicators']['slm']:
            for impacts in data_health['indicators']['slm']['impacts']:
                st.write("Areas impactadas:")
                for area in impacts['impact_areas']:
                    st.markdown("* %s" % area)
                st.write("Impacto: %s" % impacts['description'])

        if 'diagnosis' in data_health['indicators']['slm']:
            for diagnosis in data_health['indicators']['slm']['diagnosis']:
                st.write("Causa: %s" % diagnosis['cause'])
                st.write("Solução Proposta: %s" % diagnosis['action'])


        st.divider()
        
        st.markdown("#### ILM")

        st.write("Status: %s" % data_health['indicators']['ilm']['status'])
        st.write("Descrição: %s" % data_health['indicators']['ilm']['symptom'])
        st.write("Status do Serviço: %s" % data_health['indicators']['ilm']['details']['ilm_status'])
        st.write("Qtd de Politicas: %s" % data_health['indicators']['ilm']['details']['policies'])
        st.write("Indices Estagnados: %s" % data_health['indicators']['ilm']['details']['stagnating_indices'])

        if 'impacts' in data_health['indicators']['ilm']:
            for impacts in data_health['indicators']['ilm']['impacts']:
                st.write("Areas impactadas:")
                for area in impacts['impact_areas']:
                    st.markdown("* %s" % area)
                st.write("Impacto: %s" % impacts['description'])

        if 'diagnosis' in data_health['indicators']['ilm']:
            for diagnosis in data_health['indicators']['ilm']['diagnosis']:
                st.write("Causa: %s" % diagnosis['cause'])
                st.write("Solução Proposta: %s" % diagnosis['action'])
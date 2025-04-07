import streamlit as st
#from streamlit_extras.app_logo import add_logo
from components import Header, PrintInfo, Cadastro, BotaoSubmitStyle
import random, json, re
import pandas as pd
import numpy as np
import altair as alt
from collections import Counter


st.cache_data.clear()
## Running project
##### streamlit run Home.py --theme.base dark --server.port 8502
st.session_state.data_health = False

Header.add_logo()

def extract_base_name(index_name):
    pattern = r"(?:partial-)?(?:restored-)?(?:shrink-.{4}-)?(?:\.ds-)?(.*?)-?(\d{4}\.\d{2}\.\d{2})?(?:-\d{6})?$"
    match = re.match(pattern, index_name)
    if match:
        base_name = match.group(1)
        return base_name
    return None

def generate_base_names(file_path, output_file_base, output_file_counts):
    index_names = []
    for index in file_path:
        index_names.append(index['index'])
    
    extracted_names = list(filter(None, map(extract_base_name, index_names)))
    
    # Lista sem duplicatas
    base_names = list(set(extracted_names))
    
    # Lista preservando duplicatas
    duplicated_list = extracted_names.copy()
    
    # Contagem de frequência
    count_dict = Counter(duplicated_list)
    
    # Salvar lista única em um CSV
    df_base = pd.DataFrame(base_names, columns=["Base Name"])
    df_base = df_base.sort_values(by="Base Name", ascending=True)
    df_base.to_csv(output_file_base, index=False, sep=';', encoding='utf-8')
    
    # Salvar contagem de ocorrências em um CSV
    df_counts = pd.DataFrame(list(count_dict.items()), columns=["Base Name", "Count"])
    df_counts = df_counts.sort_values(by="Count", ascending=False)
    df_counts.to_csv(output_file_counts, index=False, sep=';', encoding='utf-8')
    
    return df_counts

def createChart(df,field,subtitle):
    #df = df.rename(columns={'size': 'size_bytes'})
    df = df.head(20)
    st.write("Top 20 Aplicacoes 📈")

    c = (
        alt.Chart(df)
        .mark_bar()
        .encode(x=alt.X(field, sort=None), y=subtitle, color=field, tooltip=[field, subtitle])
    )

    st.altair_chart(c, use_container_width=True)

st.title("Análise agrupamento de indices 🔎")
st.subheader("Espaço destinado para agrupar indices com base no nome da aplicacao! Isso ajudara a verificar quantos indices a aplicacao XPTO possui.")

st.markdown("Por exemplo, se temos os seguintes indices:")
code = '''.ds-xpto-2025.03.21-000001
.ds-xpto-2025.03.27-000002
.ds-xpto-2025.03.30-000003'''
st.code(code, language='php')

st.markdown("")
st.markdown("Teremos o seguinte retorno:")
code = '''Aplicacao: XPTO / Total de Indices: 3'''
st.code(code, language='php')

st.markdown("Agora vamos pegar a lista de indices!")
code = '''GET _cat/indices?format=json&h=index'''
st.code(code, language='php')

st.markdown("💡 Haaaa, se voce quiser saber a quantidade de shards ao inves de indexes, basta usar o comando abaixo:")
code = '''GET _cat/shards?format=json&h=index'''
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

            # Exemplo de uso
            file_path = data_health  # Altere para o caminho correto do arquivo
            output_file_base = "base_names.csv"  # Caminho do arquivo de saída com nomes únicos
            output_file_counts = "base_names_counts.csv"  # Caminho do arquivo de saída com contagens
            df_counts = generate_base_names(file_path, output_file_base, output_file_counts)

            st.write("")
            st.write("")
            print(df_counts)

            text = f"Identificados {len(df_counts['Base Name'])} aplicacoes!"
            st.info(text,  icon="🔎")
            createChart(df_counts,"Base Name","Count")

            st.divider()
            st.subheader("Analise Completa")
            st.write(df_counts, use_container_width=True)

        except KeyError:
            st.warning('Valide se inseriu a consulta correta!!', icon="⚠️")
        except Exception as e:
            print(e)
            st.error('Valide se colou o arquivo corretamente!!!', icon="🚨")

    else:
        st.warning('Preencha os dados!', icon="⚠️")
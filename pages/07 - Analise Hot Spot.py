import streamlit as st
#from streamlit_extras.app_logo import add_logo
from components import Header, BotaoSubmitStyle
import random, json, re
import pandas as pd
import numpy as np
import altair as alt
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go

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

def generate_base_names(file_path, node_roles):
    for index in file_path:
        index['index'] = extract_base_name(index['index'])

    # Criar o DataFrame
    node_roles = pd.DataFrame(node_roles)
    df = pd.DataFrame(file_path)

    node_roles = node_roles.rename(columns={'name': 'node'})
    df = df.merge(node_roles, on='node', how='left')

    # Agrupar por 'node' e 'index' e contar as ocorrências
    df_agrupado = df.groupby(['index', 'node', 'node.role']).size().reset_index(name='count')
    df_ordenado = df_agrupado.sort_values(by="count", ascending=False)

    df_ordenado = df_ordenado[df_ordenado['node.role'].str.contains('h')]
    
    return df_ordenado

def createChart(df_counts):
    st.divider()
    st.subheader("Aplicacao VS Node (Top 100)")
    count_df = df_counts

    # Truncar nomes longos
    MAX_LEN = 100
    count_df['index_trunc'] = count_df['index'].apply(lambda x: x[:MAX_LEN] + '…' if len(x) > MAX_LEN else x)

    # Somar total por índice para ordenar
    count_df['total'] = count_df.groupby('index_trunc')['count'].transform('sum')
    count_df = count_df.sort_values(by='total', ascending=False)

    count_df = count_df[count_df['count'] > 1]
    #count_df = count_df.head(100)

    # Construir gráfico
    chart = (
        alt.Chart(count_df)
        .mark_bar()
        .encode(
            x=alt.X('count:Q', title='Quantidade de Shards', axis=alt.Axis(tickMinStep=1)),
            y=alt.Y('index_trunc:N', sort='-x', title='Aplicacao'),
            color=alt.Color('node:N', title='Node'),
            tooltip=['index', 'node', 'count']
        )
        .properties(
            width='container',
            height=2000,
            title='Distribuição de Shards'
        )
    )

    st.altair_chart(chart, use_container_width=True)

def createChartNode(df):

    df = df[df['count'] > 1]
    # Group by node and index to get sum per index per node
    grouped = df.groupby(['node', 'index'])['count'].sum().reset_index()

    # Split into a dict of dataframes by node
    nodes = grouped['node'].unique()
    node_dfs = {node: grouped[grouped['node'] == node].sort_values('count', ascending=False) for node in nodes}

    st.title("Stacked Horizontal Bar per Node")

    for node, data in node_dfs.items():
        st.subheader(f"Node: {node}")

        fig = go.Figure()

        for _, row in data.iterrows():
            fig.add_trace(go.Bar(
                name=row['index'],
                y=[node],
                x=[row['count']],
                orientation='h',
                hovertemplate=f"Index: {row['index']}<br>Count: {row['count']}<extra></extra>",
            ))

        fig.update_layout(
            barmode='stack',
            height=200,
            showlegend=False,
            xaxis_title='Total Count',
            yaxis=dict(showticklabels=False),
            margin=dict(l=30, r=10, t=10, b=10),
        )

        st.plotly_chart(fig, use_container_width=True)

def createPivoteTable(df):
    # Criação do DataFrame pivotado
    pivot_df = df.pivot_table(index='index', columns='node', values='count', aggfunc='sum')

    # Soma total dos counts por index
    pivot_df['total'] = df.groupby('index')['count'].sum()

    # Reset index e renomeia coluna
    pivot_df = pivot_df.reset_index()
    pivot_df.columns.name = None

    # Substituir NaN por "-"
    pivot_df = pivot_df.fillna("-")

    # Convert only numeric values (not "-") to int
    def convert_to_int(val):
        try:
            return int(val)
        except:
            return val  # keep "-" as is

    # Apply to all columns except 'index'
    for col in pivot_df.columns[1:]:
        pivot_df[col] = pivot_df[col].apply(convert_to_int)

    # Ordenar por total (convertendo antes para int, se necessário)
    pivot_df['total'] = pivot_df['total'].astype(int)
    pivot_df = pivot_df.sort_values(by='total', ascending=False)

    # Resultado final
    return pivot_df

def detect_imbalance_with_node(row):
    node_vals = {}
    for col in row.index[1:-1]:  # skip 'index' and 'total'
        val = row[col]
        if isinstance(val, int):
            node_vals[col] = val

    if len(node_vals) <= 1:
        return "-"  # Not enough data for comparison

    # Find node with the max value
    max_node = max(node_vals, key=node_vals.get)
    max_val = node_vals[max_node]

    others = [v for node, v in node_vals.items() if node != max_node]
    if not others:
        return "-"

    avg_others = sum(others) / len(others)

    if max_val > avg_others + 2:
        return f"⚠️ Hot Spot indicator on {max_node}"
    return "-"

def render_wrapped_table(df):
    styles = """
    <style>
    .dataframe-wrapper table {
        table-layout: fixed;
        width: 100%;
    }
    .dataframe-wrapper th, .dataframe-wrapper td {
        word-wrap: break-word;
        white-space: pre-wrap;
        text-align: left;
        padding: 8px;
        font-size: 14px;
    }
    </style>
    """

    html_table = df.to_html(classes='dataframe-wrapper', index=False, escape=False)
    st.markdown(styles + html_table, unsafe_allow_html=True)

def write_hot_spot_names(data_health1, node_roles1):
    # Criar o DataFrame
    node_roles1 = pd.DataFrame(node_roles1)
    df = pd.DataFrame(data_health1)

    node_roles1 = node_roles1.rename(columns={'name': 'node'})
    df = df.merge(node_roles1, on='node', how='left')

    # Agrupar por 'node' e 'index' e contar as ocorrências
    df_agrupado = df.groupby(['index', 'node', 'node.role']).size().reset_index(name='count')
    df_ordenado = df_agrupado.sort_values(by="count", ascending=False)

    df_ordenado = df_ordenado[df_ordenado['node.role'].str.contains('h')]

    return df_ordenado


st.title("Análise distruicao de aplicacoes/Node e Node/Aplicacaoes 🔎")
st.subheader("Espaço destinado para agrupar  (...)")

st.markdown("Por exemplo, se temos os seguintes indices:")
code = '''.ds-xpto-2025.03.21-000001
.ds-xpto-2025.03.27-000002
.ds-xpto-2025.03.30-000003'''
st.code(code, language='php')

st.markdown("")
st.markdown("Teremos o seguinte retorno:")
code = '''Aplicacao: XPTO / Total de Indices: 3'''
st.code(code, language='php')

st.markdown("Vamos pegar informações dos Nodes")
code = '''GET _cat/nodes?v&h=name,node.role&format=json'''
st.code(code, language='php')

node_roles = st.text_area('Cole aqui a informacao dos Nodes:')
node_roles1 = node_roles

st.markdown("Agora vamos pegar a lista de shards!")
code = '''GET _cat/shards?format=json&h=index,node'''
st.code(code, language='php')

data_health = st.text_area('Cole aqui o retorno da consulta:')
data_health1 = data_health

# checagem de botao
if "btn_click" not in st.session_state:
    st.session_state['btn_click'] = False

BotaoSubmitStyle.botaoSubmit()

if st.button("Obter análise", key='shardSubmit', type="primary"):
    if data_health:
        try:
            data_health = json.loads(data_health)
            node_roles = json.loads(node_roles)

            data_health1 = json.loads(data_health1)
            node_roles1 = json.loads(node_roles1)

            # Exemplo de uso
            file_path = data_health  # Altere para o caminho correto do arquivo
            df_counts = generate_base_names(file_path, node_roles)

            st.write("")
            st.write("")
            createChart(df_counts)

            st.write("")
            st.write("")
            createChartNode(df_counts)

            st.divider()
            st.subheader("Analise Completa Aplicacao/Node")
            df_counts = df_counts.drop(columns=["index_trunc","total"])
            st.write(df_counts, use_container_width=True)

            st.divider()
            st.subheader("Hot Spot Search - Aplicacao/Node")
            pivote_table = createPivoteTable(df_counts)
            pivote_table['hotspot_flag'] = pivote_table.apply(detect_imbalance_with_node, axis=1)
            pivote_table = pivote_table[pivote_table['hotspot_flag'].str.contains('Hot Spot')]
            #st.markdown(pivote_table.to_html(escape=False), unsafe_allow_html=True)
            st.write(pivote_table)

            st.divider()
            st.subheader("Hot Spot Index - Shard/Node")
            hotspot_index_table = write_hot_spot_names(data_health1, node_roles1)
            hotspot_index_table = createPivoteTable(hotspot_index_table)
            hotspot_index_table['hotspot_flag'] = hotspot_index_table.apply(detect_imbalance_with_node, axis=1)
            hotspot_index_table = hotspot_index_table[hotspot_index_table['hotspot_flag'].str.contains('Hot Spot')]
            #st.markdown(hotspot_index_table.to_html(escape=False), unsafe_allow_html=True)
            st.write(hotspot_index_table)

        except KeyError:
            st.warning('Valide se inseriu a consulta correta!!', icon="⚠️")
        except Exception as e:
            print(e)
            st.error('Valide se colou o arquivo corretamente!!!', icon="🚨")

    else:
        st.warning('Preencha os dados!', icon="⚠️")
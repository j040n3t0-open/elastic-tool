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

st.title("Análise tamanho de shards 🔎")
st.subheader("Espaço destinado para agrupar  (...)")

st.markdown("Vamos pegar informações dos Shards")
code = '''GET _cat/shards?format=json&h=index,store&bytes=b'''
st.code(code, language='php')

shards_size = st.text_area('Cole aqui a informacao dos Nodes:')

# checagem de botao
if "btn_click" not in st.session_state:
    st.session_state['btn_click'] = False

BotaoSubmitStyle.botaoSubmit()

if st.button("Obter análise", key='shardSubmit', type="primary"):
    if shards_size:
        try:
            data_health = json.loads(shards_size)

            df = pd.DataFrame(data_health)
            df = df.rename(columns={'store': 'store (b)'})

            null_shards = df[df["store (b)"].isna()]

            df = df[df["store (b)"].notna()]
            df = df.astype({'store (b)':'int'})

            df['store (kb)'] = df['store (b)'] / 1024
            df['store (mb)'] = df['store (kb)'] / 1024
            df['store (gb)'] = df['store (mb)'] / 1024

            df = df.sort_values(by="store (b)", ascending=False)

            # Categorize into ranges
            def store_range(b):
                kb = b / 1024
                mb = kb / 1024
                gb = mb / 1024
                if b > 0 and gb < 1:
                    return "<1 GB"
                elif 1 <= gb < 10:
                    return "1-10 GB"
                elif 10 <= gb < 30:
                    return "10-30 GB"
                elif 30 <= gb < 55:
                    return "30-55 GB"
                elif gb > 50:
                    return ">55 GB"

            df["range"] = df["store (b)"].apply(store_range)

            print(df)

            # Count by range
            counts = df["range"].value_counts().reset_index()
            counts.columns = ["Range", "Count"]

            # Plotly bar chart
            fig = px.bar(counts, x="Range", y="Count", title="Index Distribution by Store Range (GB)",
                        color="Range", color_discrete_sequence=px.colors.qualitative.Pastel)

            st.plotly_chart(fig)

            st.write(df)

            if len(null_shards["index"]) > 0:
                text = f"Identificados {len(null_shards['index'])} sem informacoes de tamanho! Valide-os."
                st.warning(text,  icon="⚠️")

                st.write(null_shards)
 

        except KeyError:
            st.warning('Valide se inseriu a consulta correta!!', icon="⚠️")
        except Exception as e:
            print(e)
            st.error('Valide se colou o arquivo corretamente!!!', icon="🚨")

    else:
        st.warning('Preencha os dados!', icon="⚠️")
import streamlit as st

def printIndexInformations(df):
    totalIndices = str(df['index'].nunique())
    totalShards = str(df['index'].size)
    totalShards50GB = str((df['store'] > 51200).sum())
    totalShards200MDocs = str((df['docs'] > 200000000).sum())


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        style = f"background-color: {'SeaGreen'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">TOTAL INDICES<br /> {totalIndices}',unsafe_allow_html=True)

    with col2:
        style = f"background-color: {'MediumSeaGreen'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">TOTAL SHARDS<br /> {totalShards}',unsafe_allow_html=True)

    with col3:
        style = f"background-color: {'orange'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">+200M DOCS<br /> {totalShards200MDocs}',unsafe_allow_html=True)

    with col4:
        style = f"background-color: {'Salmon'}; padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; line-height: 1.5; font-size: 18px; height: 80px;display: flex; justify-content: center; align-items: center;"
        hot_price_style = "font-size: 12px; margin-bottom: 0;"  # Defina o tamanho de fonte desejado
        st.markdown(f'<div id="1" style="{style}">+50GB SHARD<br /> {totalShards50GB}',unsafe_allow_html=True)

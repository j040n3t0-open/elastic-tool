# page2.py
import streamlit as st
from PIL import Image
from components import Header

## Import Structure
Header.add_logo()

image = Image.open('imagens/image.png').resize((250, 250), Image.LANCZOS)

st.title("About")
st.title("")

col1, col2= st.columns(2)
with col1:
  st.image(image, caption='Elastic Certified Professional')
with col2:
  st.header("João Neto")
  st.write("**Customer Architect at Elastic**")
  style = f"padding: 5px; border-radius: 5px; font-size: 22px; line-height: 1.35;"
  st.markdown(f'<div id="1" style="{style}"><li>GenAI, Data Analyst, Elasticsearch and Observability Certified Engineer</li><li>Elastic Community Organizer (Goiânia)</li><li>2x Gold Community Contributor</li></div>', unsafe_allow_html=True)
  st.write("📨 joao.neto@elastic.co ")
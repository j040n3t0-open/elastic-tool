# page2.py
import streamlit as st
from PIL import Image
from components import Header

## Import Structure
Header.add_logo()

image = Image.open('imagens/image.png').resize((250, 250), Image.LANCZOS)

st.title("About")

col1, image_header, col3 = st.columns(3)
name = st.columns([1])[0]
col1, col2, col3 = st.columns(3)

style = f"padding: 3px; border-radius: 3px; font-size: 15px; line-height: 1.35;"

with image_header:
  st.image(image, caption='Elastic Certified Professional')

with name:
  st.header("João Neto")
  st.markdown("###### 👔 Customer Architect at Elastic")
  st.markdown("###### 🤝 Elastic Community Organizer in Goiania")
  st.markdown("###### 📬 joao.neto@elastic.co")

with col1:
  st.markdown("**PREMIOS 🏆**")
  st.markdown(f'''<div id="1" style="{style}">
              <li>Elastic Certified Professional of the Year 2023 Runner-Up</li>
              <li>Elastic Gold Contributor 2022</li>
              <li>Elastic Gold Contributor 2021</li>
              <li>Elastic Silver Contributor 2020</li>
              <br />
              </div>''', unsafe_allow_html=True)
with col2:
  st.markdown("**CERTIFICAÇÕES 🎯**")
  st.markdown(f'''<div id="1" style="{style}">
              <li>Elastic GenAI Associate Certification</li>
              <li>Elastic Certified Observability Engineer</li>
              <li>Elastic Certified Analyst</li>
              <li>Elastic Certified Engineer</li>
              <li>AWS Cloud Practitioner</li>
              <br />
              </div>''', unsafe_allow_html=True)
with col3:
  st.markdown("**PALESTREI EM... 👨🏻‍🏫**")
  st.markdown(f'''<div id="1" style="{style}">
              <li>ElasticON</li>
              <li>Python Cerrado</li>
              <li>DevOpsDays BSB</li>
              <li>DevOpsDays Goiânia</li>
              <li>TDC</li>
              <li>FGSL</li>
              <li>FLISOL</li>
              <li>Campus Party</li>
              <li>JoinCommunity</li>
              <br />
              </div>''', unsafe_allow_html=True)

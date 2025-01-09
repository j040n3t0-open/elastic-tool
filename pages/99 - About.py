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


  style = f"padding: 3px; border-radius: 3px; font-size: 15px; line-height: 1.35;"

  st.markdown("**JOB 👔**")
  st.markdown(f'''<div id="1" style="{style}">
              <li>Customer Architect at Elastic</li>
              <li>Elastic Community Organizer in Goiania</li>
              <br />
              </div>''', unsafe_allow_html=True)

  st.markdown("**PREMIOS 🏆**")
  st.markdown(f'''<div id="1" style="{style}">
              <li>Elastic Certified Professional of the Year 2023</li>
              <li>Elastic Gold Contributor 2022</li>
              <li>Elastic Gold Contributor 2021</li>
              <li>Elastic Silver Contributor 2020</li>
              <br />
              </div>''', unsafe_allow_html=True)

  st.markdown("**CERTIFICAÇÕES 🎯**")
  st.markdown(f'''<div id="1" style="{style}">
              <li>Elastic GenAI Associate Certification</li>
              <li>Elastic Certified Observability Engineer</li>
              <li>Elastic Certified Analyst</li>
              <li>Elastic Certified Engineer</li>
              <br />
              </div>''', unsafe_allow_html=True)

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
  
  st.markdown("**CONTATO 👨‍💻**")
  st.write("📨 joao.neto@elastic.co ")
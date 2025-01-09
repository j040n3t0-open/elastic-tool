import streamlit as st
#from streamlit_extras.app_logo import add_logo
from components import Header
import random, json

## Running project
##### streamlit run Home.py --theme.base dark --server.port 8502

Header.add_logo()

st.title("Bem-vindo 👋")

st.write("""Esse projeto foi criado para acelerar ainda mais o seu trabalho com Elasticsearch usando esse plataforma inovadora, projetada para tornar sua experiência mais eficiente e produtiva.""")

st.markdown("### Recursos em Destaque:")


st.write("""**🏥 Cluster Health:** A partir da versão 8.17+ foi criado a api "_health_report", com ela conseguimos ter a visão da saúde de alguns serviços primários do funcionamento de um cluster Elasticsearch. Apenas do retorno dessa API ser bem simplificado, resolvi trazer alguns elementos visuais para deixar ainda mais simples essa análise.

**🧮 Total de Campos:** Tenha um controle completo sobre seus índices e documentos, acompanhando o número de campos em tempo real. Uma visão abrangente para melhorar sua estratégia de indexação.

**⌛ Tempo de Consulta:** Otimize suas consultas com análises detalhadas de desempenho. Saiba exatamente quanto tempo cada consulta leva e identifique oportunidades de melhoria.

**🔎 Análise de Shards:** Compreenda a distribuição dos seus shards e otimize a escalabilidade do seu cluster. Garanta que seus dados estejam distribuídos de forma eficiente.

**🔥 Análise de Hot Threads:** Nessa guia você conseguirá ver de uma maneira mais clean (tabela) as informações das Threads detalhadas por Nó, dessa forma você poderá identificar facilmente operações ofensoras no ambiente.

Com essa ferramenta foi simplificada algumas análises do Elasticsearch para que você possa focar no que realmente importa: Alcançar resultados incríveis com seus dados.

Experimente agora e eleve sua experiência com Elastic para um novo patamar!""")



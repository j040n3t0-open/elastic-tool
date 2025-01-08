import streamlit as st

def add_logo():
  st.markdown(
      """
      <style>
        [data-testid="stSidebarNav"] {
            background-image: url("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhelOlEX48HTOK5TUAsKeNtJQbUhqT45gU4Egc6IMstyeG0Q_hUVIHKZIt1yhvPfZPst-l-urmKzv0KY0HRCga4eYDXQYQcXH4eNDXYMJhK3ISCt_1eDZLQmrTbb6nKfnqRsDgzYaZU_0mz0mIfwLsSNZWBcz5YMTkNPDmeqUWjLhxrrTct4hWrv2WSkecE/w216-h216/canivete-suico.png");
            background-repeat: no-repeat;
            background-size: 40% 30%;
            padding-top: 120px;
            background-position: 20px 0px;
            align: center;
        }
        [data-testid="stSidebarNav"]::before {
            content: "Elastic Tool";
            margin-left: 20px;
            margin-top: 15px;
            font-size: 30px;
            position: relative;
            top: 10px;
        }
      </style>
      """,
      unsafe_allow_html=True,
  )
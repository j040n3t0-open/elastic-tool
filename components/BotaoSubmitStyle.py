import streamlit as st


def botaoSubmit():
    st.markdown(
        """
        <style>
        button[kind="primary"] { 
            background-color: green;
            border: 0
        }
        button[kind="primary"]:hover {
            background-color: green;
        }
        button[kind="primary"]:active {
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
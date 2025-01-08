import streamlit as st
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx
import time, random


def random_message():
    messages = ["Vamos fazer um cadastro ligeiro!",
                "Cadastra ae, pls!",
                "Deixe-me saber quem és tu!",
                "Me diga teu nome e eu saberei quem tu és..."
                ]
    size_list = len(messages)
    number = random.randint(0,size_list-1)

    return messages[number]
import streamlit as st
import sys
import os
import time

# Add the parent directory to the path so we can import the coins module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="Generate Best Cripto Wallet", page_icon="🪙", layout="centered"
)

from app import run_app

with st.container():
    st.title("Tech Challenge 2")
    st.subheader("Gerador de carteira de Criptomoedas com Algoritmo Genético")
with st.container():
    st.markdown("---")
    st.header("Instruções")
    st.subheader("Escolha os parâmetros para gerar a melhor carteira de criptomoedas.")

    sharpe_index = st.slider(
        "Selecione um valor de desejado para o índice de Sharpe (cripto 1.5, stock: 1.0, forex 0.5)",
        0.5,
        3.0,
        1.5,
    )

    risk_free_rate = st.number_input("Taxa livre de risco em %", 1.0, 100.0, 4.0)
    risk_free_rate = risk_free_rate // 100
    population_size = st.number_input("Tamanho da população inicial", 5, 50, 20)

    coins_qtd = st.number_input("Quantidade de moedas na carteira", 3, 8, 5)

    max_generations = st.number_input("Número máximo de gerações", 100, 20000, 200)
    is_debug = False

    if st.button("Gerar melhor carteira"):
        run_app(
            good_sharpe_ratio=sharpe_index,
            risk_free_rate=risk_free_rate,
            population_size=population_size,
            coins_qtd=coins_qtd,
            max_generations=max_generations,
            debug=is_debug,
        )

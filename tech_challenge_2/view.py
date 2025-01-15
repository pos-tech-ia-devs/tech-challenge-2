# import streamlit as st
# import sys
# import os
# import time

# # Add the parent directory to the path so we can import the coins module
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# st.set_page_config(
#     page_title="Generate Best Cripto Wallet", page_icon="🪙", layout="centered"
# )

# from app import run_app
# from coins import get_coins

# with st.container():
#     st.title("Tech Challenge 2")
#     st.subheader("Gerador de carteira de Criptomoedas com Algoritmo Genético")
#     st.write(
#         "O algoritmo irá gerar a melhor carteira com base no [índice de Sharpe](https://pt.wikipedia.org/wiki/%C3%8Dndice_de_Sharpe)"
#     )

# with st.container():
#     st.markdown("---")
#     st.header("Instruções")
#     st.write(
#         "Você pode configurar os parametros de entrada do algoritmo, ele irá gerar a melhor carteira de forma automática."
#     )

#     input_conditions = st.container(border=True)
#     input_conditions.header("Insira os parametros de entrada do algoritmo:")
#     risk_free_rate = input_conditions.number_input(
#         "Taxa livre de risco em %", 1.0, 100.0, 4.0
#     )
#     risk_free_rate = risk_free_rate // 100
#     population_size = input_conditions.number_input(
#         "Tamanho da população inicial", 5, 50, 20
#     )

#     coins_qtd = input_conditions.number_input(
#         "Quantidade de moedas na carteira", 3, 8, 5
#     )

#     is_debug = False

#     stop_conditions = st.container(border=True)
#     stop_conditions.header("Defina as condições de parada do algoritmo:")
#     max_generations = stop_conditions.number_input(
#         "Número máximo de gerações", 100, 20000, 200
#     )
#     sharpe_index = stop_conditions.slider(
#         "Selecione um valor de desejado para o índice de Sharpe (cripto 1.5, stock: 1.0, forex 0.5)",
#         0.1,
#         3.0,
#         1.5,
#     )

#     if st.button("Gerar melhor carteira"):
#         run_app(
#             good_sharpe_ratio=sharpe_index,
#             risk_free_rate=risk_free_rate,
#             population_size=population_size,
#             coins_qtd=coins_qtd,
#             max_generations=max_generations,
#             debug=is_debug,
#         )
import streamlit as st
import sys
import os
import time

# Adiciona o diretório pai ao path para importar o módulo coins
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="Gerador Otimizado de Carteira Cripto", page_icon="🪙", layout="centered"
)

from app import run_app
from coins import get_coins

with st.container():
    st.title("Desafio Tech 2")
    st.subheader("Monte a Melhor Carteira de Criptomoedas")
    st.write(
        "Esta aplicação utiliza um **Algoritmo Genético** para encontrar a melhor configuração de carteira de criptomoedas com base no [Índice de Sharpe](https://pt.wikipedia.org/wiki/%C3%8Dndice_de_Sharpe)."
    )

with st.container():
    st.markdown("---")
    st.header("Como Funciona")
    st.write(
        "Você pode configurar os parâmetros de entrada do algoritmo, e ele encontrará automaticamente a melhor carteira para você."
    )

    input_conditions = st.container()
    input_conditions.header("Defina os Parâmetros de Entrada do Algoritmo:")
    risk_free_rate = input_conditions.number_input(
        "Taxa Livre de Risco (%)",
        min_value=1.0,
        max_value=100.0,
        value=4.0,
        help="Insira a taxa de juros livre de risco em percentual.",
    )
    risk_free_rate = risk_free_rate // 100
    population_size = input_conditions.number_input(
        "Tamanho da População Inicial",
        min_value=5,
        max_value=50,
        value=20,
        help="Número de indivíduos na população inicial do algoritmo.",
    )

    coins_qtd = input_conditions.number_input(
        "Quantidade de Moedas na Carteira",
        min_value=3,
        max_value=8,
        value=5,
        help="Quantas criptomoedas você deseja na sua carteira.",
    )

    is_debug = False

    stop_conditions = st.container()
    stop_conditions.header("Defina as Condições de Parada do Algoritmo:")
    max_generations = stop_conditions.number_input(
        "Número Máximo de Gerações",
        min_value=100,
        max_value=20000,
        value=200,
        help="Máximo de iterações que o algoritmo executará.",
    )
    sharpe_index = stop_conditions.slider(
        "Índice de Sharpe Alvo (Cripto: 1.5, Ações: 1.0, Forex: 0.5)",
        min_value=0.1,
        max_value=3.0,
        value=1.5,
        help="Selecione o índice de Sharpe desejado para a carteira.",
    )

    if st.button("Gerar Melhor Carteira"):
        run_app(
            good_sharpe_ratio=sharpe_index,
            risk_free_rate=risk_free_rate,
            population_size=population_size,
            coins_qtd=coins_qtd,
            max_generations=max_generations,
            debug=is_debug,
        )

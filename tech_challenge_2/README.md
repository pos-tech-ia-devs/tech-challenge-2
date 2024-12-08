# Captura dos dados

Pegar dados históricos (1 a 2 anos)

- Pego de: https://br.investing.com/crypto/currencies
- Pego 22 criptos em um periodo de 2 anos (18/11/2024 ~ 18/11/2022)
- Explicação:
  - **Data**: O dia específico dessa cotação.
  - **Último**: O preço final da criptomoeda ao fim do dia.
  - **Abertura**: O preço inicial da criptomoeda no começo do dia.
  - **Máxima**: O preço mais alto alcançado pela criptomoeda durante o dia.
  - **Mínima**: O preço mais baixo registrado no dia.
  - **Vol. (Volume)**: Quantidade negociada da criptomoeda no dia (em unidades ou valor monetário).
  - **Var% (Variação Percentual)**: A variação percentual do preço em relação ao dia anterior.

---

---

## TODOS

- Ajustar a seleção :done:
  - mudar de torneio para ranking e ver se te melhora
- Ajustar o crossover
  Usar algumas das tecnicas de corte (Single-Point Crossover por exemplo)

  ```
    Carteira 1
    [btc, eth,| bnb]
    [40, 30, 30]

    Carteira 2
    [sol, btc,| pepe]
    [50, 25, 25]

    Carteira 1 Filho
    [BTC, sol, bnb]
    [25, 50, 30]

    Carteira 2 Filho
    [BTC, eth, pepe]
    [40, 25, 25]
  ```

- Ajudar mutação
  - Embaralhar os pesos
- Ajustar o erro
  ```bash
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "tech-challenge-2/tech_challenge_2/app.py", line 34, in main
        fitness = calculate_fitness(population)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "tech-challenge-2/tech_challenge_2/ag.py", line 55, in calculate_fitness
        sharpe_ratio = calculate_portfolio_sharpe(
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "tech-challenge-2/tech_challenge_2/coins.py", line 74, in calculate_portfolio_sharpe
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
                                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^
      ValueError: shapes (5,5) and (6,) not aligned: 5 (dim 1) != 6 (dim 0)
  ```
- Adicionar o Streamlit
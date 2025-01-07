import sys
import os
import random
import pandas as pd
import numpy as np

# Add the parent directory to the path so we can import the coins module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from coins import (
    get_coins,
    get_coin_return,
    calculate_portfolio_sharpe,
    calculate_covariance_matrix,
)

# Good indice to cripto is between 2% and 10%
risk_free_rate = 0.04

allowed_weights = [0.10, 0.20, 0.30, 0.40, 0.50]

def generate_exact_weights(allowed_weights, num_coins):
    while True:
        weights = [random.choice(allowed_weights) for _ in range(num_coins)]
        total = round(sum(weights), 2)
        if total == 1.0:
            return weights

def generate_population(coins_quantity, population_size=10):
    possibles_coins = get_coins()
    population = []
    unique_individuals = set()
    
    def generate_individual(possibles_coins, num_coins):
        while True:
            coins = set(random.sample(possibles_coins, num_coins))
            # allowed_weights = [0.2, 0.4, 0.5, 0.3]
            # weights = [random.choice(allowed_weights) for _ in range(num_coins)]
            # weights = [random.random() for _ in range(num_coins)]

            weights = generate_exact_weights(allowed_weights, num_coins)
            exists_zero_weight = False
            for w in weights:
                if w == 0:
                    exists_zero_weight = True
            if len(coins) == len(weights) and not exists_zero_weight:
                break

        sum_weights = sum(weights)
        normalized_weights = tuple(round(w / sum_weights, 2) for w in weights)
        normalized_coins = tuple(coins)
        return normalized_coins, normalized_weights

    while len(population) < population_size:
        coins, weights = generate_individual(possibles_coins, coins_quantity)
        individual_signature = (coins, weights)
        if individual_signature not in unique_individuals:
            unique_individuals.add(individual_signature)
            population.append(
                {"coins": list(coins), "weights": list(weights), "fitness": None}
            )

    return population


def calculate_sharpe_ratio_for_multiple_cryptos(coins, weights, risk_free_rate=0.04):
    """
    Calcula o Índice de Sharpe para uma carteira composta por múltiplas criptomoedas.

    :param paths: Lista de caminhos para os arquivos CSV de cada cripto, contendo as colunas 'Data' e 'Último'.
    :param weights: Lista de pesos para cada cripto, somando 100%.
    :param risk_free_rate: Taxa livre de risco anual.
    :return: Índice de Sharpe, Retorno Anualizado, Volatilidade Anualizada.
    """
    all_returns = []
    paths = []

    for c in coins:
        paths.append(f'quotations/{c}.csv')

    # Iterar sobre cada caminho de arquivo
    for path in paths:
        # Carregar o arquivo CSV
        data = pd.read_csv(path, delimiter=',', quotechar='\"')

        # Converter a coluna 'Último' para valores numéricos
        data['Último'] = data['Último'].str.replace('.', '').str.replace(',', '.').astype(float)

        # Converter a coluna 'Data' para o formato de data
        data['Data'] = pd.to_datetime(data['Data'], dayfirst=True)

        data = data.sort_values("Data")

        # Calcular os retornos diários
        data['Retorno'] = data['Último'].pct_change()

        # Excluir valores NA que possam resultar do cálculo de retorno
        data.dropna(inplace=True)

        all_returns.append(data[['Data', 'Retorno']])

    # Juntar todos os dados de retorno por data
    merged_data = all_returns[0]

    for i in range(1, len(all_returns)):
        merged_data = pd.merge(merged_data, all_returns[i], on='Data', suffixes=(f'_{i}', f'_{i+1}'))
    print(merged_data)
    # Calcular o retorno diário composto da carteira
    merged_data['Retorno_Carteira'] = sum(weights[i] * merged_data[f'Retorno_{i+1}'] for i in range(1,len(weights)))
    for i in range(len(weights)):
        print(f"{i}")

    # Calcular o retorno médio anualizado e desvio padrão da carteira
    retorno_medio_diario = merged_data['Retorno_Carteira'].mean()
    retorno_anualizado = (1 + retorno_medio_diario) ** 252 - 1
    volatilidade_anualizada = merged_data['Retorno_Carteira'].std() * np.sqrt(252)

    # Calcular o Índice de Sharpe
    sharpe_ratio = (retorno_anualizado - risk_free_rate) / volatilidade_anualizada

    return sharpe_ratio, retorno_anualizado, volatilidade_anualizada


def calculate_fitness(population):
    population_with_fitness = []
    for wallet in population:
        mean_returns = []

        for coin in wallet["coins"]:
            coin_data = get_coin_return(coin)
            mean_returns.append(coin_data["mean_day_return"])

        cov_matrix = calculate_covariance_matrix(wallet["coins"])
        # print(f"wallet: {wallet}")
        # print(f"cov_matrix: {cov_matrix}")
        sharpe_ratio = calculate_portfolio_sharpe(
            wallet["weights"], mean_returns, cov_matrix, risk_free_rate
        )

        # print(f"wallet: {wallet['coins']}")
        # print(f"Weights: {wallet['weights']}")
        # print(f"Sharpe Ratio: {sharpe_ratio}")
        # print("---------------------------")

        population_with_fitness.append({
            "coins": wallet["coins"],
            "weights": wallet["weights"],
            "fitness": sharpe_ratio,
        })
    return population_with_fitness


def verify_finishing_condition(population, threshold):
    for w in population:
        if w["fitness"] >= threshold:
            return True
        return False


# Two best individuals are selected to be parents
def selection_elitism(population):
    population = sorted(population, key=lambda x: x["fitness"], reverse=True)
    return population[:2]

def selection_tournament(population, tournament_size=3):
    selected = []
    for _ in range(2):  # Select two parents
        tournament = random.sample(population, tournament_size)
        winner = max(tournament, key=lambda x: x["fitness"])
        selected.append(winner)
    return selected

# Two point crossover
def crossover(parent1, parent2):
    # Ensure both parents have the same number of coins
    if len(parent1["coins"]) != len(parent2["coins"]):
        raise ValueError("Both parents must have the same number of coins.")

    num_coins = len(parent1["coins"])
    point1, point2 = sorted(random.sample(range(1, num_coins), 2))

    # Create new offspring by swapping coins and weights between the crossover points
    child1_coins = parent1["coins"][:point1] + parent2["coins"][point1:point2] + parent1["coins"][point2:]
    child1_weights = parent1["weights"][:point1] + parent2["weights"][point1:point2] + parent1["weights"][point2:]

    # Ensure each coin is unique
    unique_coins_weights = {}
    for coin, weight in zip(child1_coins, child1_weights):
        if coin not in unique_coins_weights:
            unique_coins_weights[coin] = weight

    child1_coins, child1_weights = zip(*unique_coins_weights.items())
    child1_coins, child1_weights = list(child1_coins), list(child1_weights)

    # If the number of coins is less than the original, add random coins and weights from the parents
    while len(child1_coins) < num_coins:
        additional_index = random.randint(0, num_coins - 1)
        additional_coin = parent1["coins"][additional_index]
        additional_weight = parent1["weights"][additional_index]
        if additional_coin not in child1_coins:
            child1_coins.append(additional_coin)
            child1_weights.append(additional_weight)

    # If the number of coins is more than the original, trim the list
    child1_coins = child1_coins[:num_coins]
    child1_weights = child1_weights[:num_coins]


    # Normalize weights to ensure the sum does not surpass 1
    def normalize_weights(weights):
        total_weight = sum(weights)
        return [w / total_weight for w in weights]

    child1_weights = normalize_weights(child1_weights)

    child1_weights = generate_exact_weights(allowed_weights, num_coins)

    # Create new wallet
    child1 = {
        "coins": child1_coins,
        "weights": child1_weights,
        "fitness": None,
    }

    return child1

# Codification: Mutation by Inversion
def mutate(wallet):
    total_coins = len(wallet["coins"])
    min_mutate_rate = random.randint(0, total_coins - 2)
    max_mutate_rate = random.randint(min_mutate_rate + 1, total_coins - 1)

    def apply_mutate(arr, init, end):
        if init < 0 or end >= len(arr) or init > end:
            raise ValueError("Invalid interval.")

        # Invert the interval
        arr[init : end + 1] = arr[init : end + 1][::-1]
        return arr

    wallet["coins"] = apply_mutate(wallet["coins"], min_mutate_rate, max_mutate_rate)
    wallet["weights"] = apply_mutate(wallet["weights"], min_mutate_rate, max_mutate_rate)

    # Ensure no weights are zero
    wallet["weights"] = [w if w > 0 else random.uniform(0.01, 0.1) for w in wallet["weights"]]

    # Normalize weights to ensure the sum does not surpass 1
    total_weight = sum(wallet["weights"])
    wallet["weights"] = [w / total_weight for w in wallet["weights"]]

    return wallet

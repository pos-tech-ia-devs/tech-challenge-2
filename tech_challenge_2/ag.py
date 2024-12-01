import sys
import os
import random

# Add the parent directory to the path so we can import the coins module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from coins import (
    get_coins,
    get_coin_return,
    calculate_portfolio_sharpe,
    calculate_covariance_matrix,
)

# Good indice to cripto is between 2% and 10%
risk_free_rate = 0.06
good_sharpe_ratio = 1.5


def generate_population(coins_quantity, population_size=10):
    possibles_coins = get_coins()

    def generate_individual(possibles_coins, num_coins):
        coins = random.sample(possibles_coins, num_coins)
        weights = [random.random() for _ in range(num_coins)]

        sum_weights = sum(weights)
        normalized_weights = [round(w / sum_weights, 2) for w in weights]
        return {"coins": coins, "weights": normalized_weights, "fitness": None}

    population = []
    for _ in range(population_size):
        population.append(generate_individual(possibles_coins, coins_quantity))

    return population


def calculate_fitness():
    new_wallets = generate_population(coins_quantity=6)
    for new_wallet in new_wallets:
        mean_returns = []

        for coin in new_wallet["coins"]:
            coin_data = get_coin_return(coin)
            mean_returns.append(coin_data["mean_day_return"])

        cov_matrix = calculate_covariance_matrix(new_wallet["coins"])

        sharpe_ratio = calculate_portfolio_sharpe(
            new_wallet["weights"], mean_returns, cov_matrix, risk_free_rate
        )

        print(f"new_wallet: {new_wallet['coins']}")
        print(f"Weights: {new_wallet['weights']}")
        print(f"Sharpe Ratio: {sharpe_ratio}")
        print("---------------------------")

        return {
            "coins": new_wallet["coins"],
            "weights": new_wallet["weights"],
            "fitness": sharpe_ratio,
        }


def verify_finishing_condition(population, threshold=good_sharpe_ratio):
    for individual in population:
        if individual["fitness"] >= threshold:
            return True
    return False


# Two best individuals are selected to be parents
def selection(population):
    population = sorted(population, key=lambda x: x["fitness"], reverse=True)
    return population[:2]


# Arithmetic Crossover
def crossover(parent1, parent2):

    def get_repeated_coins():
        repeated_coins = {"coins": [], "mean_weight": []}

        for index_base, coin_base in enumerate(parent1["coins"]):

            for index_compare, coin_compare in enumerate(parent2["coins"]):

                if coin_base == coin_compare:
                    # Só poderá ter duas moedas repetidas
                    mean_weights = (
                        parent1["weights"][index_base]
                        + parent2["weights"][index_compare]
                    ) / 2
                    repeated_coins["mean_weight"].append(mean_weights)
                    repeated_coins["coins"].append(coin_base)
                    break

        return repeated_coins

    repeated_coins = get_repeated_coins()
    coins = [*parent1["coins"], *parent2["coins"]]
    weights = [*parent1["weights"], *parent2["weights"]]

    new_wallet = {"coins": [], "weights": []}
    for index_base, coin_base in enumerate(coins):
        if coin_base not in repeated_coins["coins"]:
            new_wallet["coins"].append(coin_base)
            new_wallet["weights"].append(weights[index_base])

    coins = [*new_wallet["coins"], *repeated_coins["coins"]]
    weights = [*new_wallet["weights"], *repeated_coins["mean_weight"]]

    def normalized_weights(weights):
        sum_weights = sum(weights)
        return [round(w / sum_weights, 2) for w in weights]

    # Agora todos os pesos somam 1
    weights = normalized_weights(weights)

    return {
        "coins": coins,
        "weights": weights,
        "fitness": None,
    }


# Codificação Combinatória: Mutação por Inversão
def mutate(wallet):
    total_coins = len(wallet["coins"])
    min_mutate_rate = random.randint(0, total_coins - 2)
    max_mutate_rate = random.randint(min_mutate_rate + 1, total_coins - 1)

    print(f"total_coins: {total_coins}")
    print(f"min_mutate_rate: {min_mutate_rate}")
    print(f"max_mutate_rate: {max_mutate_rate}")
    print(f"---------------------------------")

    def apply_mutate(arr, init, end):
        if init < 0 or end >= len(arr) or init > end:
            raise ValueError("Intervalo inválido.")

        # Inverter o intervalo
        arr[init : end + 1] = arr[init : end + 1][::-1]
        return arr

    print(f"Original Wallet: {wallet}")
    wallet["coins"] = apply_mutate(wallet["coins"], min_mutate_rate, max_mutate_rate)
    wallet["weights"] = apply_mutate(
        wallet["weights"], min_mutate_rate, max_mutate_rate
    )

    print(f"------------------------")
    print(f"Mutated Wallet: {wallet}")
    return wallet

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


def generate_population(coins_quantity, population_size=10):
    possibles_coins = get_coins()
    population = []
    unique_individuals = set()

    def generate_individual(possibles_coins, num_coins):
        coins = tuple(random.sample(possibles_coins, num_coins))
        weights = [random.random() for _ in range(num_coins)]
        sum_weights = sum(weights)
        normalized_weights = tuple(round(w / sum_weights, 2) for w in weights)
        return coins, normalized_weights

    while len(population) < population_size:
        coins, weights = generate_individual(possibles_coins, coins_quantity)
        individual_signature = (coins, weights)
        if individual_signature not in unique_individuals:
            unique_individuals.add(individual_signature)
            population.append(
                {"coins": list(coins), "weights": list(weights), "fitness": None}
            )

    return population


def calculate_fitness(population):
    population_with_fitness = []
    for wallet in population:
        mean_returns = []

        for coin in wallet["coins"]:
            coin_data = get_coin_return(coin)
            mean_returns.append(coin_data["mean_day_return"])

        cov_matrix = calculate_covariance_matrix(wallet["coins"])
        print(f"wallet: {wallet}")
        print(f"cov_matrix: {cov_matrix}")
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


# # Arithmetic Crossover
# def crossover(parent1, parent2):
#     def get_repeated_coins():
#         repeated_coins = {"coins": [], "mean_weight": []}
#         for index_base, coin_base in enumerate(parent1["coins"]):
#             for index_compare, coin_compare in enumerate(parent2["coins"]):
#                 if coin_base == coin_compare:
#                     # can only have two repeats
#                     mean_weights = (
#                         parent1["weights"][index_base]
#                         + parent2["weights"][index_compare]
#                     ) / 2
#                     repeated_coins["mean_weight"].append(mean_weights)
#                     repeated_coins["coins"].append(coin_base)
#                     break
#
#         return repeated_coins
#
#     repeated_coins = get_repeated_coins()
#     coins = [*parent1["coins"], *parent2["coins"]]
#     weights = [*parent1["weights"], *parent2["weights"]]
#
#     new_wallet = {"coins": [], "weights": []}
#     for index_base, coin_base in enumerate(coins):
#         if coin_base not in repeated_coins["coins"]:
#             new_wallet["coins"].append(coin_base)
#             new_wallet["weights"].append(weights[index_base])
#
#     coins = [*new_wallet["coins"], *repeated_coins["coins"]]
#     weights = [*new_wallet["weights"], *repeated_coins["mean_weight"]]
#
#     def normalized_weights(weights):
#         sum_weights = sum(weights)
#         return [round(w / sum_weights, 2) for w in weights]
#
#     # Now all weights are normalized
#     weights = normalized_weights(weights)
#
#     res =  {
#         "coins": coins,
#         "weights": weights,
#         "fitness": None,
#     }
#     print(f"Crossover result: {res}")
#     return res

# Single point crossover
def crossover(parent1, parent2):
    # Ensure both parents have the same number of coins
    if len(parent1["coins"]) != len(parent2["coins"]):
        raise ValueError("Both parents must have the same number of coins.")

    num_coins = len(parent1["coins"])

    # Select a random crossover point
    crossover_point = random.randint(1, num_coins - 1)

    # Create new offspring by swapping coins and weights at the crossover point
    child1_coins = parent1["coins"][:crossover_point] + parent2["coins"][crossover_point:]
    child1_weights = parent1["weights"][:crossover_point] + parent2["weights"][crossover_point:]

    # Ensure each coin is unique
    unique_coins_weights = {}
    for coin, weight in zip(child1_coins, child1_weights):
        if coin not in unique_coins_weights:
            unique_coins_weights[coin] = weight

    child1_coins, child1_weights = zip(*unique_coins_weights.items())
    # If the number of coins is less than the original, add random coins and weights from the parents
    while len(child1_coins) < num_coins:
        additional_index = random.randint(0, num_coins - 1)
        additional_coin = parent1["coins"][additional_index]
        additional_weight = parent1["weights"][additional_index]
        if additional_coin not in child1_coins:
            child1_coins += (additional_coin,)
            child1_weights += (additional_weight,)

    # If the number of coins is more than the original, trim the list
    child1_coins = child1_coins[:num_coins]
    child1_weights = child1_weights[:num_coins]

    # Create new wallet
    child1 = {
        "coins": list(child1_coins),
        "weights": list(child1_weights),
        "fitness": None,
    }

    # Normalize weights to ensure the sum does not surpass 1
    def normalize_weights(wallet):
        total_weight = sum(wallet["weights"])
        wallet["weights"] = [w / total_weight for w in wallet["weights"]]
        return wallet

    child1 = normalize_weights(child1)
    # print(f"Crossover result: {child1}")
    return child1

# Codification: Mutation by Inversion
def mutate(wallet):
    total_coins = len(wallet["coins"])
    min_mutate_rate = random.randint(0, total_coins - 2)
    max_mutate_rate = random.randint(min_mutate_rate + 1, total_coins - 1)

    # print(f"total_coins: {total_coins}")
    # print(f"min_mutate_rate: {min_mutate_rate}")
    # print(f"max_mutate_rate: {max_mutate_rate}")
    # print(f"---------------------------------")

    def apply_mutate(arr, init, end):
        if init < 0 or end >= len(arr) or init > end:
            raise ValueError("Intervalo inválido.")

        # Invert the interval
        arr[init : end + 1] = arr[init : end + 1][::-1]
        return arr

    # print(f"Original Wallet: {wallet}")
    wallet["coins"] = apply_mutate(wallet["coins"], min_mutate_rate, max_mutate_rate)
    wallet["weights"] = apply_mutate(
        wallet["weights"], min_mutate_rate, max_mutate_rate
    )

    # print(f"------------------------")
    print(f"Mutated Wallet: {wallet}")
    return wallet

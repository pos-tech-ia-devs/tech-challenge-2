import sys
import os
import random
import pandas as pd
import numpy as np

# Add the parent directory to the path so we can import the coins module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from coins import (
    get_coins,
    get_returns,
    calculate_portfolio_sharpe,
)

allowed_weights = [0.10, 0.20, 0.30, 0.40, 0.50]


def generate_exact_weights(allowed_weights, num_coins):
    """
    Generate a list of exact weights that sum up to 1.0.

    This function randomly selects weights from the `allowed_weights` list
    and ensures their total equals 1.0.

    Args:
        allowed_weights (list): A list of allowed weight values.
        num_coins (int): Number of weights to generate.

    Returns:
        list: A list of weights summing to 1.0.
    """
    while True:
        weights = [random.choice(allowed_weights) for _ in range(num_coins)]
        total = round(sum(weights), 2)
        if total == 1.0:
            return weights


def generate_population(coins_quantity, population_size=10):
    """
    Generate an initial population of wallets.

    Each wallet contains a set of coins, their respective weights, and a fitness score.

    Args:
        coins_quantity (int): Number of coins in each wallet.
        population_size (int): Total number of wallets to generate.

    Returns:
        list: A list of dictionaries representing the population of wallets.
    """
    possibles_coins = get_coins()
    population = []
    unique_individuals = set()

    def generate_individual(possibles_coins, num_coins):
        """
        Generate a single individual wallet with coins and weights.

        Ensures coins and weights are properly normalized and unique.
        """
        while True:
            coins = set(random.sample(possibles_coins, num_coins))
            weights = generate_exact_weights(allowed_weights, num_coins)
            exists_zero_weight = any(w == 0 for w in weights)
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


def calculate_fitness(population, risk_free_rate):
    """
    Calculate the fitness (Sharpe Ratio) for each wallet in the population.

    Args:
        population (list): A list of wallets, each with coins and weights.
        risk_free_rate (float): Annualized risk-free rate as a decimal.

    Returns:
        list: The population with updated fitness values for each wallet.
    """
    population_with_fitness = []
    for wallet in population:
        coins_data = get_returns(wallet["coins"])
        mean_returns = coins_data.mean()
        sharpe_ratio = calculate_portfolio_sharpe(wallet, mean_returns, risk_free_rate)

        population_with_fitness.append(
            {
                "coins": wallet["coins"],
                "weights": wallet["weights"],
                "fitness": sharpe_ratio,
            }
        )

    return population_with_fitness


def verify_finishing_condition(population, threshold):
    """
    Verify if the finishing condition for the genetic algorithm is met.

    Args:
        population (list): The population of wallets.
        threshold (float): The fitness threshold to achieve.

    Returns:
        bool: True if any wallet meets or exceeds the threshold, otherwise False.
    """
    for w in population:
        if w["fitness"] > threshold:
            return True
    return False


def selection_elitism(population):
    """
    Select the two best individuals in the population based on fitness.

    Args:
        population (list): The population of wallets.

    Returns:
        list: The top two individuals (wallets) with the highest fitness.
    """
    population = sorted(population, key=lambda x: x["fitness"], reverse=True)
    return population[:2]


def selection_tournament(population, tournament_size=3):
    """
    Select two parents using tournament selection.

    Args:
        population (list): The population of wallets.
        tournament_size (int): Number of individuals in each tournament.

    Returns:
        list: Two selected individuals (wallets).
    """
    selected = []
    for _ in range(2):  # Select two parents
        tournament = random.sample(population, tournament_size)
        winner = max(tournament, key=lambda x: x["fitness"])
        selected.append(winner)
    return selected


def crossover(parent1, parent2):
    """
    Perform a two-point crossover to generate an offspring.

    Ensures the offspring inherits coins and weights from both parents,
    maintaining uniqueness and normalized weights.

    Args:
        parent1 (dict): The first parent wallet.
        parent2 (dict): The second parent wallet.

    Returns:
        dict: A new wallet (offspring) with combined traits from both parents.
    """
    if len(parent1["coins"]) != len(parent2["coins"]):
        raise ValueError("Both parents must have the same number of coins.")

    num_coins = len(parent1["coins"])
    point1, point2 = sorted(random.sample(range(1, num_coins), 2))

    # Create new offspring by swapping coins and weights between the crossover points
    child1_coins = (
        parent1["coins"][:point1]
        + parent2["coins"][point1:point2]
        + parent1["coins"][point2:]
    )
    child1_weights = (
        parent1["weights"][:point1]
        + parent2["weights"][point1:point2]
        + parent1["weights"][point2:]
    )

    # Ensure each coin is unique
    unique_coins_weights = {}
    for coin, weight in zip(child1_coins, child1_weights):
        if coin not in unique_coins_weights:
            unique_coins_weights[coin] = weight

    child1_coins, child1_weights = zip(*unique_coins_weights.items())
    child1_coins, child1_weights = list(child1_coins), list(child1_weights)

    while len(child1_coins) < num_coins:
        additional_index = random.randint(0, num_coins - 1)
        additional_coin = parent1["coins"][additional_index]
        additional_weight = parent1["weights"][additional_index]
        if additional_coin not in child1_coins:
            child1_coins.append(additional_coin)
            child1_weights.append(additional_weight)

    child1_coins = child1_coins[:num_coins]
    child1_weights = generate_exact_weights(allowed_weights, num_coins)

    child1 = {
        "coins": child1_coins,
        "weights": child1_weights,
        "fitness": None,
    }

    return child1


def mutate(wallet):
    """
    Apply mutation by inverting a random interval of coins and weights.

    Ensures weights are normalized and no weight is zero after mutation.

    Args:
        wallet (dict): A wallet with coins and weights.

    Returns:
        dict: A mutated wallet.
    """
    total_coins = len(wallet["coins"])
    min_mutate_rate = random.randint(0, total_coins - 2)
    max_mutate_rate = random.randint(min_mutate_rate + 1, total_coins - 1)

    def apply_mutate(arr, init, end):
        """
        Invert a specific interval in the list.
        """
        if init < 0 or end >= len(arr) or init > end:
            raise ValueError("Invalid interval.")
        arr[init : end + 1] = arr[init : end + 1][::-1]
        return arr

    wallet["coins"] = apply_mutate(wallet["coins"], min_mutate_rate, max_mutate_rate)
    wallet["weights"] = apply_mutate(
        wallet["weights"], min_mutate_rate, max_mutate_rate
    )

    wallet["weights"] = [
        w if w > 0 else random.uniform(0.01, 0.1) for w in wallet["weights"]
    ]
    total_weight = sum(wallet["weights"])
    wallet["weights"] = [w / total_weight for w in wallet["weights"]]

    return wallet

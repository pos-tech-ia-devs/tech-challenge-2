import sys
import os
import random

# Add the parent directory to the path so we can import the coins module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# To cripto the good sharpe ratio is 1.5, to stock is 1, to forex is 0.5
good_sharpe_ratio = 1.5

population_size = 10

from ag import (
    generate_population,
    calculate_fitness,
    verify_finishing_condition,
    selection,
    crossover,
    mutate,
)

wallet = []


def main():
    running = True

    while running:
        population = generate_population(
            coins_quantity=6, population_size=population_size
        )

        fitness = calculate_fitness(population)
        # print(fitness, good_sharpe_ratio)

        can_stop = verify_finishing_condition(fitness, good_sharpe_ratio)

        if can_stop:
            print(f"Best wallet: {fitness}")

            running = False
            break

        # selected = selection(fitness) ????
        # new_individual = crossover(selected)
        # mutated_individual = mutate(new_individual)

        new_population = [population[0]]
        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population[:population_size], k=2)
            child = crossover(parent1, parent2)
            child = mutate(child)
            # child2 = mutate(child2)
            new_population.extend([child])

        population = new_population
        print(population)
        print("-------------------------------------------------")

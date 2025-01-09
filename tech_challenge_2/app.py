import sys
import os
import random

# Add the parent directory to the path so we can import the coins module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# To cripto the good sharpe ratio is 1.5, to stock is 1, to forex is 0.5
good_sharpe_ratio = 1.5
# Good indice to cripto is between 2% and 10%
risk_free_rate = 0.04
population_size = 20
coins_qtd = 5
max_generations = 100
debug = True

from ag import (
    generate_population,
    calculate_fitness,
    verify_finishing_condition,
    selection_elitism,
    selection_tournament,
    crossover,
    mutate,
)


# Test fitness
# def main():
#     population = [
#         {"coins": ["Aave", "Bitcoin", "BNB"], "weights": [0.25, 0.5, 0.25]},
#     ]
#     fitness = calculate_fitness(population)
#     print(fitness)


def main():
    running = True
    has_elitism_and_tournament = True
    numGeneration = 1
    best_wallet = None

    ## generates population of ten wallets with 6 coins each
    population = generate_population(
        coins_quantity=coins_qtd, population_size=population_size
    )

    while running:
        print(f"Generation: {numGeneration}")
        print("-------------------------------------------------")
        ## calculates the fitness of each wallet
        population_with_fitness = calculate_fitness(population, risk_free_rate)

        ## check if the finishing condition is met
        can_stop = verify_finishing_condition(
            population_with_fitness, good_sharpe_ratio
        )

        ## if the finishing condition is met, print the best wallet and stop the loop
        if can_stop or numGeneration == max_generations:
            print("-------------------------------------------------")
            print("-------------------------------------------------")
            print(f"Best wallet: {best_wallet}")
            running = False
            break

        ## selection of the best wallets
        selected = []
        if has_elitism_and_tournament:
            selected = (
                selection_elitism(population_with_fitness)[:1]
                + selection_tournament(population_with_fitness)[:1]
            )
        else:
            selected = selection_elitism(population_with_fitness)

        best_wallet = selected[0]
        if debug:
            print(f"Best wallet fitness: {selected[0].get('fitness').round(2)}")
            print(f"Best wallet weight: {selected[0].get('coins')}")
            print(f"Best wallet weight: {selected[0].get('weights')}")
            print("\n")
            print(f"Actual wallet fitness: {selected[1].get('fitness').round(2)}")
            print(f"Actual wallet coins: {selected[1].get('coins')}")
            print(f"Actual wallet weights: {selected[1].get('weights')}")

        new_individual = crossover(
            random.choices(selected, k=1)[0], random.choices(selected, k=1)[0]
        )
        mutated_individual = mutate(new_individual)

        # start a new population
        new_population = [mutated_individual]
        # ensure i don't lose the best wallet
        new_population.extend(selected)

        # Generate new random individuals to fill 50% of the population
        num_random_individuals = population_size // 2
        new_random_individuals = generate_population(
            coins_quantity=coins_qtd, population_size=num_random_individuals
        )

        # Insert new random individuals one by one into new_population
        for individual in new_random_individuals:
            new_population.append(individual)

        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population[:population_size], k=2)
            child = crossover(parent1, parent2)
            child = mutate(child)

            child2 = crossover(parent1, child)
            child2 = mutate(child2)

            child3 = crossover(child, parent2)
            child3 = mutate(child3)

            new_population.extend([child])
            new_population.extend([child2])
            new_population.extend([child3])

        # overrides the population
        population.clear()
        population = new_population
        # print(population)
        numGeneration += 1
